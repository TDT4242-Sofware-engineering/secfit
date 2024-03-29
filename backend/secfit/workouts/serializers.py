"""Serializers for the workouts application
"""
from rest_framework import serializers
from rest_framework.serializers import HyperlinkedRelatedField
from workouts.models import Workout, Exercise, ExerciseInstance, WorkoutFile, WorkoutInvitation, ExerciseFile
from django.contrib.auth import get_user_model


class ExerciseInstanceSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for an ExerciseInstance. Hyperlinks are used for relationships by default.

    Serialized fields: url, id, exercise, sets, number, workout

    Attributes:
        workout:    The associated workout for this instance, represented by a hyperlink
    """

    workout = HyperlinkedRelatedField(
        queryset=Workout.objects.all(), view_name="workout-detail", required=False
    )

    class Meta:
        model = ExerciseInstance
        fields = ["url", "id", "exercise", "sets", "number", "workout"]


class WorkoutFileSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for a WorkoutFile. Hyperlinks are used for relationships by default.

    Serialized fields: url, id, owner, file, workout

    Attributes:
        owner:      The owner (User) of the WorkoutFile, represented by a username. ReadOnly
        workout:    The associate workout for this WorkoutFile, represented by a hyperlink
    """

    owner = serializers.ReadOnlyField(source="owner.username")
    workout = HyperlinkedRelatedField(
        queryset=Workout.objects.all(), view_name="workout-detail", required=False
    )

    class Meta:
        model = WorkoutFile
        fields = ["url", "id", "owner", "file", "workout"]

    def create(self, validated_data):
        return WorkoutFile.objects.create(**validated_data)


class WorkoutInvitationSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for a WorkoutInvitation. Hyperlinks are used for relationships by default.

    Serialized fields: url, id, owner, participant, workout

    Attributes:
        owner:      The owner (User) of the Workout invitation, represented by a username. ReadOnly
        workout:    The associate workout for this Workout invitation, represented by a hyperlink
        participant: The participant (User)
    """

    owner = serializers.ReadOnlyField(source="owner.username")
    workout = HyperlinkedRelatedField(
        queryset=Workout.objects.all(), view_name="workout-detail", required=False
    )
    participant = serializers.SlugRelatedField(
        many=False,
        slug_field='username',
        queryset=get_user_model().objects.all()
     )

    class Meta:
        model = WorkoutInvitation
        fields = ["url", "id", "owner", "participant", "workout"]

    def create(self, validated_data):
        return WorkoutInvitation.objects.create(**validated_data)


class WorkoutSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for a Workout. Hyperlinks are used for relationships by default.

    This serializer specifies nested serialization since a workout consists of WorkoutFiles
    and ExerciseInstances.

    Serialized fields: url, id, name, date, notes, owner, owner_username, visiblity,
                       exercise_instances, files

    Attributes:
        owner_username:     Username of the owning User
        exercise_instance:  Serializer for ExericseInstances
        files:              Serializer for WorkoutFiles
        participants:       The participants (Users)
    """

    owner_username = serializers.SerializerMethodField()
    exercise_instances = ExerciseInstanceSerializer(many=True, required=True)
    files = WorkoutFileSerializer(many=True, required=False)
    participants = serializers.SlugRelatedField(
        many=True,
        slug_field='username',
        queryset=get_user_model().objects.all()
    )

    class Meta:
        model = Workout
        fields = [
            "url",
            "id",
            "name",
            "date",
            "notes",
            "owner",
            "owner_username",
            "visibility",
            "exercise_instances",
            "files",
            "participants"
        ]
        extra_kwargs = {"owner": {"read_only": True}}

    def create(self, validated_data):
        """Custom logic for creating ExerciseInstances, WorkoutFiles, and a Workout.

        This is needed to iterate over the files and exercise instances, since this serializer is
        nested.

        Args:
            validated_data: Validated files and exercise_instances

        Returns:
            Workout: A newly created Workout
        """
        exercise_instances_data = validated_data.pop("exercise_instances")
        files_data = []
        if "files" in validated_data:
            files_data = validated_data.pop("files")

        name = validated_data["name"]
        date = validated_data["date"]
        notes = validated_data["notes"]
        owner = validated_data["owner"]
        visibility = validated_data["visibility"]
        results = validated_data["participants"]

        workout = Workout.objects.create(name=name, date=date, notes=notes, owner=owner, visibility=visibility)

        usernames = set(result.get_username() for result in results)
        users = get_user_model().objects.filter(username__in=usernames).values_list('id', flat=True)
        workout.participants.set(users)
        workout.save()

        for exercise_instance_data in exercise_instances_data:
            ExerciseInstance.objects.create(workout=workout, **exercise_instance_data)
        for file_data in files_data:
            WorkoutFile.objects.create(
                workout=workout, owner=workout.owner, file=file_data.get("file")
            )

        return workout

    def update(self, instance, validated_data):
        """Custom logic for updating a Workout with its ExerciseInstances and Workouts.

        This is needed because each object in both exercise_instances and files must be iterated
        over and handled individually.

        Args:
            instance (Workout): Current Workout object
            validated_data: Contains data for validated fields

        Returns:
            Workout: Updated Workout instance
        """
        exercise_instances_data = validated_data.pop("exercise_instances")
        exercise_instances = instance.exercise_instances

        instance.name = validated_data.get("name", instance.name)
        instance.notes = validated_data.get("notes", instance.notes)
        instance.visibility = validated_data.get("visibility", instance.visibility)
        instance.date = validated_data.get("date", instance.date)
        results = validated_data.get("participants", instance.participants)
        usernames = set(result.get_username() for result in results)
        users = get_user_model().objects.filter(username__in=usernames).values_list('id', flat=True)
        instance.participants.set(users)
        instance.save()

        self.handleExercises(instance, exercise_instances, exercise_instances_data)

        self.handleWorkoutFiles(instance,validated_data)

        return instance
    
    def handleExercises(self, instance, exercise_instances, exercise_instances_data):
        # This updates existing exercise instances without adding or deleting object.
        # zip() will yield n 2-tuples, where n is
        # min(len(exercise_instance), len(exercise_instance_data))
        for exercise_instance, exercise_instance_data in zip(
            exercise_instances.all(), exercise_instances_data
        ):
            exercise_instance.exercise = exercise_instance_data.get(
                "exercise", exercise_instance.exercise
            )
            exercise_instance.number = exercise_instance_data.get(
                "number", exercise_instance.number
            )
            exercise_instance.sets = exercise_instance_data.get(
                "sets", exercise_instance.sets
            )
            exercise_instance.save()

        # If new exercise instances have been added to the workout, then create them
        if len(exercise_instances_data) > len(exercise_instances.all()):
            for i in range(len(exercise_instances.all()), len(exercise_instances_data)):
                exercise_instance_data = exercise_instances_data[i]
                ExerciseInstance.objects.create(
                    workout=instance, **exercise_instance_data
                )
        # Else if exercise instances have been removed from the workout, then delete them
        elif len(exercise_instances_data) < len(exercise_instances.all()):
            for i in range(len(exercise_instances_data), len(exercise_instances.all())):
                exercise_instances.all()[i].delete()

    def handleWorkoutFiles(self, instance, validated_data):
        if "files" in validated_data:
            files_data = validated_data.pop("files")
            files = instance.files

            for file, file_data in zip(files.all(), files_data):
                file.file = file_data.get("file", file.file)

            # If new files have been added, creating new WorkoutFiles
            if len(files_data) > len(files.all()):
                for i in range(len(files.all()), len(files_data)):
                    WorkoutFile.objects.create(
                        workout=instance,
                        owner=instance.owner,
                        file=files_data[i].get("file"),
                    )
            # Else if files have been removed, delete WorkoutFiles
            elif len(files_data) < len(files.all()):
                for i in range(len(files_data), len(files.all())):
                    files.all()[i].delete()


    def get_owner_username(self, obj):
        """Returns the owning user's username

        Args:
            obj (Workout): Current Workout

        Returns:
            str: Username of owner
        """
        return obj.owner.username

class ExerciseFileSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for a ExerciseFile. Hyperlinks are used for relationships by default.

    Serialized fields: url, id, owner, file, Exercise

    Attributes:
        owner:      The owner (User) of the ExerciseFile, represented by a username. ReadOnly
        Exercise:    The associate Exercise for this ExerciseFile, represented by a hyperlink
    """

    owner = serializers.ReadOnlyField(source="owner.username")
    exercise = HyperlinkedRelatedField(
        queryset=Exercise.objects.all(), view_name="exercise-detail", required=False
    )

    class Meta:
        model = ExerciseFile
        fields = ["url", "id", "owner", "file", "exercise"]

    def create(self, validated_data):
        return ExerciseFile.objects.create(**validated_data)

class ExerciseSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for an Exercise. Hyperlinks are used for relationships by default.

    Serialized fields: url, id, name, description, unit, instances

    Attributes:
        instances:  Associated exercise instances with this Exercise type. Hyperlinks.
    """
    owner_username = serializers.SerializerMethodField()
    files = ExerciseFileSerializer(many=True, required=False)

    class Meta:
        model = Exercise
        fields = ["url", "id", "owner", "owner_username", "name", "description", "unit", "files"]
        extra_kwargs = {"owner": {"read_only": True}}
    
    def get_owner_username(self, obj):
        return obj.owner.username
    
    def create(self, validated_data):
        files_data = []

        if "files" in validated_data:
            files_data = validated_data.pop("files")

        exercise = Exercise.objects.create(**validated_data)

        for file_data in files_data:
            ExerciseFile.objects.create(
                exercise=exercise, owner=exercise.owner, file=file_data.get("file")
            )
        return exercise

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.unit = validated_data.get("unit", instance.unit)
        instance.save()
        
        if "files" in validated_data:
            files_data = validated_data.pop("files")
            for file_data in files_data:
                ExerciseFile.objects.create(
                    exercise=instance, owner=instance.owner, file=file_data.get("file")
                )

        return instance


