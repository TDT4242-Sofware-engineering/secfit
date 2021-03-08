from types import SimpleNamespace
from workouts.permissions import (
    IsOwner,
    IsCoachAndVisibleToCoach,
    IsOwnerOfWorkout,
    IsCoachOfWorkoutAndVisibleToCoach,
    IsReadOnly,
    IsPublic,
    IsWorkoutPublic,
    IsOwnerOrParticipantOfWorkoutInvitation,
    IsInvitedToWorkout,
    IsParticipantToWorkout,
    IsOwnerOfExercise,
)
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from .models import Exercise, ExerciseInstance, Workout, WorkoutFile, WorkoutInvitation
"""
Tests for the workouts application.
"""
from django.test import TestCase
from unittest.mock import MagicMock

# Create your tests here.

class WorkoutPermissionsTestCase(TestCase):
    def setUp(self):
        self.requestuser = get_user_model().objects.create(
            username="requestuser", 
            email="email@email.no", 
            phone_number="91919191", 
            country="Norway", 
            city="Trondheim", 
            street_address="Prinsen gate"
        )
        self.requestuser.save()
        self.workout = Workout.objects.create(
            name="workout",
            owner=self.requestuser,
            date="2021-03-11T13:37:00Z",
            notes="workoutnote",
            visibility="PU"
        )
        self.workout.save()

    def test_IsOwner_yes(self):
        request = APIRequestFactory().get('/')
        request.user = self.requestuser

        workout = self.workout
        workout.user = request.user

        permission_check = IsOwner()
        permission = permission_check.has_object_permission(request, None, workout)

        self.assertTrue(permission)
    
    def test_IsOwner_no(self):
        request = APIRequestFactory().get('/')
        request.user = self.requestuser

        user = get_user_model().objects.create(
            username="username2", 
            email="email@email.no", 
            phone_number="91919191", 
            country="Norway", 
            city="Trondheim", 
            street_address="Prinsen gate"
        )

        workout = Workout.objects.create(
            name="workout",
            owner=user,
            date="2021-03-11T13:37:00Z",
            notes="workoutnote",
            visibility="PU"
        )

        permission_check = IsOwner()
        permission = permission_check.has_object_permission(request, None, workout)

        self.assertFalse(permission)


    def test_IsOwnerOfWorkout_yes(self):
        request = APIRequestFactory().get('/')
        request.method = 'POST'
        request.user = self.requestuser

        request.data = {
            "workout": "http://localhost:8000/wokrkouts/1/"
        }

        Workout.objects.create(
            name="workout",
            owner=self.requestuser,
            date="2021-03-11T13:37:00Z",
            notes="workoutnote",
            visibility="PU"
        ).save()


        permission_check = IsOwnerOfWorkout()
        permission = permission_check.has_permission(request, None)

        self.assertTrue(permission)

    def test_IsOwnerOfWorkout_no(self):
        request = APIRequestFactory().get('/')
        request.method = 'POST'
        request.user = self.requestuser

        request.data = {
            "workout": "http://localhost:8000/wokrkouts/2/"
        }

        user = get_user_model().objects.create(
            username="username2", 
            email="email@email.no", 
            phone_number="91919191", 
            country="Norway", 
            city="Trondheim", 
            street_address="Prinsen gate"
        )
        user.save()

        workout = Workout.objects.create(
            name="workout",
            owner=user,
            date="2021-03-11T13:37:00Z",
            notes="workoutnote",
            visibility="PU"
        )
        workout.save()

        permission_check = IsOwnerOfWorkout()
        permission = permission_check.has_permission(request, None)

        self.assertEqual(workout.owner, user)
        self.assertFalse(permission)
    
    def test_IsOwnerOfExercise_yes(self):
        request = APIRequestFactory().get('/')
        request.method = 'POST'
        request.user = self.requestuser

        request.data = {
            "exercise": "http://localhost:8000/exercise/1/"
        }

        Exercise.objects.create(
            name="Ex1",
            owner=self.requestuser,
            description="desc",
            unit="m"

        ).save()


        permission_check = IsOwnerOfExercise()
        permission = permission_check.has_permission(request, None)

        self.assertTrue(permission)

    def test_IsOwnerOfExercise_no(self):
        request = APIRequestFactory().get('/')
        request.method = 'POST'
        request.user = self.requestuser

        request.data = {
            "exercise": "http://localhost:8000/exercise/1/"
        }

        user = get_user_model().objects.create(
            username="username2", 
            email="email@email.no", 
            phone_number="91919191", 
            country="Norway", 
            city="Trondheim", 
            street_address="Prinsen gate"
        )
        user.save()

        Exercise.objects.create(
            name="Ex1",
            owner=user,
            description="desc",
            unit="m"

        ).save()


        permission_check = IsOwnerOfExercise()
        permission = permission_check.has_permission(request, None)

        self.assertFalse(permission)

    def test_IsCoachAndVisibleToCoach_yes(self):
        request = APIRequestFactory().get('/')
        request.user = get_user_model().objects.create(
            username="coach", 
            email="email@email.no", 
            phone_number="91919191", 
            country="Norway", 
            city="Trondheim", 
            street_address="Prinsen gate"
        )
        self.requestuser.coach = request.user
        workout = self.workout

        permission_check = IsCoachAndVisibleToCoach()
        permission = permission_check.has_object_permission(request, None, workout)

        self.assertTrue(permission)

    def test_IsCoachAndVisibleToCoach_no(self):
        request = APIRequestFactory().get('/')
        request.user = get_user_model().objects.create(
            username="coach", 
            email="email@email.no", 
            phone_number="91919191", 
            country="Norway", 
            city="Trondheim", 
            street_address="Prinsen gate"
        )
        self.requestuser.coach = self.requestuser
        workout = self.workout

        permission_check = IsCoachAndVisibleToCoach()
        permission = permission_check.has_object_permission(request, None, workout)

        self.assertFalse(permission)
    
    def test_IsCoachOfWorkoutAndVisibleToCoach_yes(self):
        request = APIRequestFactory().get('/')
        request.user = self.requestuser
        self.requestuser.coach = request.user

        workoutfile = WorkoutFile.objects.create(
            owner=self.requestuser,
            workout=self.workout
        )

        permission_check = IsCoachOfWorkoutAndVisibleToCoach()
        permission = permission_check.has_object_permission(request, None, workoutfile)

        self.assertTrue(permission)

    def test_IsCoachOfWorkoutAndVisibleToCoach_no(self):
        request = APIRequestFactory().get('/')
        request.user = self.requestuser
        self.requestuser.coach = request.user

        user = get_user_model().objects.create(
            username="otheruser", 
            email="email@email.no", 
            phone_number="91919191", 
            country="Norway", 
            city="Trondheim", 
            street_address="Prinsen gate"
        )
        workout = Workout.objects.create(
            name="workout",
            owner=user,
            date="2021-03-11T13:37:00Z",
            notes="workoutnote",
            visibility="PU"
        )
        workoutfile = WorkoutFile.objects.create(
            owner=user,
            workout=workout
        )

        permission_check = IsCoachOfWorkoutAndVisibleToCoach()
        permission = permission_check.has_object_permission(request, None, workoutfile)

        self.assertFalse(permission)
    
    def test_IsPublic_yes(self):
        request = APIRequestFactory().get('/')

        permission_check = IsPublic()
        permission = permission_check.has_object_permission(request, None, self.workout)

        self.assertTrue(permission)
    
    def test_IsPublic_no(self):
        request = APIRequestFactory().get('/')

        workout = Workout.objects.create(
            name="workout",
            owner=self.requestuser,
            date="2021-03-11T13:37:00Z",
            notes="workoutnote",
            visibility="PR"
        )

        permission_check = IsPublic()
        permission = permission_check.has_object_permission(request, None, workout)

        self.assertFalse(permission)
    
    def test_IsWorkoutPublic_yes(self):
        request = APIRequestFactory().get('/')
        request.user = self.requestuser
        self.requestuser.coach = request.user

        workoutfile = WorkoutFile.objects.create(
            owner=self.requestuser,
            workout=self.workout
        )

        permission_check = IsWorkoutPublic()
        permission = permission_check.has_object_permission(request, None, workoutfile)

        self.assertTrue(permission)
    
    def test_IsWorkoutPublic_no(self):
        request = APIRequestFactory().get('/')
        request.user = self.requestuser
        self.requestuser.coach = request.user

        workout = Workout.objects.create(
            name="workout",
            owner=self.requestuser,
            date="2021-03-11T13:37:00Z",
            notes="workoutnote",
            visibility="PR"
        )

        workoutfile = WorkoutFile.objects.create(
            owner=self.requestuser,
            workout=workout
        )

        permission_check = IsWorkoutPublic()
        permission = permission_check.has_object_permission(request, None, workoutfile)

        self.assertFalse(permission)
    
    def test_IsReadOnly_yes(self):
        request = APIRequestFactory().get('/')
        request.method = 'GET'

        permission_check = IsReadOnly()
        permission = permission_check.has_object_permission(request, None, None)

        self.assertTrue(permission)
    
    def test_IsReadOnly_no(self):
        request = APIRequestFactory().get('/')
        request.method = 'POST'

        permission_check = IsReadOnly()
        permission = permission_check.has_object_permission(request, None, None)

        self.assertFalse(permission)
    
    def test_IsOwnerOrParticipantOfWorkoutInvitation_owner_yes(self):
        request = APIRequestFactory().get('/')
        request.method = 'DELETE'
        request.user = self.requestuser

        participant = get_user_model().objects.create(
            username="participant", 
            email="email@email.no", 
            phone_number="91919191", 
            country="Norway", 
            city="Trondheim", 
            street_address="Prinsen gate"
        )

        WorkoutInvitation.objects.create(
            owner=self.requestuser,
            workout=self.workout,
            participant=participant
        ).save()

        view = MagicMock()
        view.kwargs = {'pk': 1}

        permission_check = IsOwnerOrParticipantOfWorkoutInvitation()
        permission = permission_check.has_object_permission(request, view, None)

        self.assertTrue(permission)
    
    def test_IsOwnerOrParticipantOfWorkoutInvitation_owner_no(self):
        request = APIRequestFactory().get('/')
        request.method = 'DELETE'
        request.user = self.requestuser

        participant = get_user_model().objects.create(
            username="participant", 
            email="email@email.no", 
            phone_number="91919191", 
            country="Norway", 
            city="Trondheim", 
            street_address="Prinsen gate"
        )

        WorkoutInvitation.objects.create(
            owner=participant,
            workout=self.workout,
            participant=participant
        ).save()

        view = MagicMock()
        view.kwargs = {'pk': 1}

        permission_check = IsOwnerOrParticipantOfWorkoutInvitation()
        permission = permission_check.has_object_permission(request, view, None)

        self.assertFalse(permission)

    def test_IsOwnerOrParticipantOfWorkoutInvitation_participant_yes(self):
        participant = get_user_model().objects.create(
            username="participant", 
            email="email@email.no", 
            phone_number="91919191", 
            country="Norway", 
            city="Trondheim", 
            street_address="Prinsen gate"
        )
        request = APIRequestFactory().get('/')
        request.method = 'DELETE'
        request.user = participant


        WorkoutInvitation.objects.create(
            owner=self.requestuser,
            workout=self.workout,
            participant=participant
        ).save()

        view = MagicMock()
        view.kwargs = {'pk': 1}

        permission_check = IsOwnerOrParticipantOfWorkoutInvitation()
        permission = permission_check.has_object_permission(request, view, None)

        self.assertTrue(permission)

    def test_IsOwnerOrParticipantOfWorkoutInvitation_participant_no(self):
        participant = get_user_model().objects.create(
            username="participant", 
            email="email@email.no", 
            phone_number="91919191", 
            country="Norway", 
            city="Trondheim", 
            street_address="Prinsen gate"
        )
        request = APIRequestFactory().get('/')
        request.method = 'DELETE'
        request.user = participant


        WorkoutInvitation.objects.create(
            owner=self.requestuser,
            workout=self.workout,
            participant=self.requestuser
        ).save()

        view = MagicMock()
        view.kwargs = {'pk': 1}

        permission_check = IsOwnerOrParticipantOfWorkoutInvitation()
        permission = permission_check.has_object_permission(request, view, None)

        self.assertFalse(permission)
    
    def test_IsInvitedToWorkout__yes(self):
        participant = get_user_model().objects.create(
            username="participant", 
            email="email@email.no", 
            phone_number="91919191", 
            country="Norway", 
            city="Trondheim", 
            street_address="Prinsen gate"
        )
        request = APIRequestFactory().get('/')
        request.method = 'PUT'
        request.user = participant


        WorkoutInvitation.objects.create(
            owner=self.requestuser,
            workout=self.workout,
            participant=participant
        ).save()

        view = MagicMock()
        view.kwargs = {'pk': 1}

        permission_check = IsInvitedToWorkout()
        permission = permission_check.has_object_permission(request, view, None)

        self.assertTrue(permission)

    def test_IsInvitedToWorkout__no(self):
        participant = get_user_model().objects.create(
            username="participant", 
            email="email@email.no", 
            phone_number="91919191", 
            country="Norway", 
            city="Trondheim", 
            street_address="Prinsen gate"
        )
        request = APIRequestFactory().get('/')
        request.method = 'PUT'
        request.user = participant


        WorkoutInvitation.objects.create(
            owner=self.requestuser,
            workout=self.workout,
            participant=self.requestuser
        ).save()

        view = MagicMock()
        view.kwargs = {'pk': 1}

        permission_check = IsInvitedToWorkout()
        permission = permission_check.has_object_permission(request, view, None)

        self.assertFalse(permission)
    
    def test_IsInvitedToWorkout__no_Invitation_found(self):
        request = APIRequestFactory().get('/')
        request.method = 'PUT'
        request.user = self.requestuser

        view = MagicMock()
        view.kwargs = {'pk': 1}

        permission_check = IsInvitedToWorkout()
        permission = permission_check.has_object_permission(request, view, None)

        self.assertFalse(permission)

    def test_IsParticipantToWorkout__yes(self):
        request = APIRequestFactory().get('/')
        request.method = 'GET'
        request.user = self.requestuser

        workout = Workout.objects.create(
            name="workout_participants",
            owner=self.requestuser,
            date="2021-03-11T13:37:00Z",
            notes="workoutnote",
            visibility="PR"
        )
        workout.participants.set([self.requestuser])
        workout.save()        

        view = MagicMock()
        view.kwargs = {'pk': 2}

        permission_check = IsParticipantToWorkout()
        permission = permission_check.has_object_permission(request, view, None)

        self.assertTrue(permission)
    
    def test_IsParticipantToWorkout__no(self):
        request = APIRequestFactory().get('/')
        request.method = 'GET'
        request.user = self.requestuser

        workout = Workout.objects.create(
            name="workout_participants",
            owner=self.requestuser,
            date="2021-03-11T13:37:00Z",
            notes="workoutnote",
            visibility="PR"
        )
        workout.save()        

        view = MagicMock()
        view.kwargs = {'pk': 2}

        permission_check = IsParticipantToWorkout()
        permission = permission_check.has_object_permission(request, view, None)

        self.assertFalse(permission)
