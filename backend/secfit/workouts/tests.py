from rest_framework.test import APITestCase, force_authenticate, APIClient, APIRequestFactory
from rest_framework import status
from rest_framework.authtoken.models import Token
from datetime import datetime
from users.models import User
from workouts.models import ExerciseInstance, Exercise, Workout, ExerciseFile
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
from comments.models import Comment
from django.contrib.auth import get_user_model
from .models import Exercise, ExerciseInstance, Workout, WorkoutFile, WorkoutInvitation
"""
Tests for the workouts application.
"""
from django.test import TestCase
from unittest.mock import MagicMock, Mock

# Unit tests

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
    
    def test_IsOwnerOfWorkout_no_missing_workout(self):
        request = APIRequestFactory().get('/')
        request.method = 'POST'
        request.user = self.requestuser

        permission_check = IsOwnerOfWorkout()
        permission = permission_check.has_permission(request, None)

        self.assertFalse(permission)
    
    def test_IsOwnerOfWorkout_Not_post_method(self):
        request = APIRequestFactory().get('/')
        request.method = 'GET'

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

    def test_IsOwnerOfWorkout_object_yes(self):
        request = APIRequestFactory().get('/')
        request.user = self.requestuser

        workoutfile = WorkoutFile.objects.create(
            owner=self.requestuser,
            workout=self.workout
        )

        permission_check = IsOwnerOfWorkout()
        permission = permission_check.has_object_permission(request, None, workoutfile)

        self.assertTrue(permission)
    
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
    
    def test_IsOwnerOfExercise_missing_exercise(self):
        request = APIRequestFactory().get('/')
        request.method = 'POST'
        request.user = self.requestuser

        permission_check = IsOwnerOfExercise()
        permission = permission_check.has_permission(request, None)

        self.assertFalse(permission)
    
    def test_IsOwnerOfExercise_Not_post_method(self):
        request = APIRequestFactory().get('/')
        request.method = 'GET'
        request.user = self.requestuser

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
    
    def test_IsOwnerOfExercise_object_yes(self):
        request = APIRequestFactory().get('/')
        request.user = self.requestuser

        exercise = Exercise.objects.create(
            name="exname",
            owner=self.requestuser,
            description="desc",
            unit="m"
        )
        exercise.save()

        exercisefile = ExerciseFile.objects.create(
            owner=self.requestuser,
            exercise=exercise
        )

        permission_check = IsOwnerOfExercise()
        permission = permission_check.has_object_permission(request, None, exercisefile)

        self.assertTrue(permission)

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
    
    def test_IsInvitedToWorkout_Not_put_method(self):
        request = APIRequestFactory().get('/')
        request.method = 'PATCH'

        permission_check = IsInvitedToWorkout()
        permission = permission_check.has_object_permission(request, None, None)

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


# Boundary tests
class NameTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="tester", email="test@test.no")
        self.user.set_password("password")
        self.user.save()

        self.accessToken = None

        self.client.login(username="tester", password="password")
        response = self.client.post('/api/token/', {"username": "tester", "password": "password"},  format="json")
        self.accessToken = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.accessToken)
        
        
    def test_name_too_short(self):
        date = datetime.utcnow()
        tooShortName= ""
        workout = {"name": tooShortName, "date": date, "notes": "validNotes", "visibility": "PU", "exercise_instances": [], "files": [], "participants": []}
        response = self.client.post('/api/workouts/', workout,  format="json")
        self.assertEqual(str(response.data["name"][0]), "This field may not be blank.")
    
    def test_name_too_long(self):
        date = datetime.utcnow()
        tooLongName= "x" * 101
        workout = {"name": tooLongName, "date": date, "notes": "validNotes", "visibility": "PU", "exercise_instances": [], "files": [], "participants": []}
        response = self.client.post("/api/workouts/", workout, format="json")
        self.assertEqual(str(response.data["name"][0]), "Ensure this field has no more than 100 characters.")

    def test_name_upper_limit(self):
        date = datetime.utcnow()
        longName= "x" * 100
        workout = {"name": longName, "date": date, "notes": "validNotes", "visibility": "PU", "exercise_instances": [], "files": [], "participants": []}
        response = self.client.post("/api/workouts/", workout, format="json")
        self.assertEqual(response.data.get("name"), longName)

    def test_name_lower_limit(self):
        date = datetime.utcnow()
        shortName= "x"
        workout = {"name": shortName, "date": date, "notes": "validNotes", "visibility": "PU", "exercise_instances": [], "files": [], "participants": []}
        response = self.client.post("/api/workouts/", workout, format="json")
        self.assertEqual(response.data.get("name"), shortName)

    def test_name_valid(self):
        date = datetime.utcnow()
        validName= "name"
        workout = {"name": validName, "date": date, "notes": "validNotes", "visibility": "PU", "exercise_instances": [], "files": [], "participants": []}
        response = self.client.post("/api/workouts/", workout, format="json")
        self.assertEqual(response.data.get("name"), validName)

class DateTimeCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="tester", email="test@test.no")
        self.user.set_password("password")
        self.user.save()

        self.accessToken = None

        self.client.login(username="tester", password="password")
        response = self.client.post('/api/token/', {"username": "tester", "password": "password"},  format="json")
        self.accessToken = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.accessToken)

    def test_date_upper_limit(self):
        date = datetime.max
        workout = {"name": "validName", "date": date, "notes": "validNotes", "visibility": "PU", "exercise_instances": [], "files": [], "participants": []}
        response = self.client.post("/api/workouts/", workout, format="json")
        self.assertEqual(str(response.data.get("date"))[:-1], date.isoformat())


    def test_date_lower_limit(self):
        date = datetime.min
        workout = {"name": "validName", "date": date, "notes": "validNotes", "visibility": "PU", "exercise_instances": [], "files": [], "participants": []}
        response = self.client.post("/api/workouts/", workout, format="json")
        self.assertEqual(str(response.data.get("date"))[:-1], date.isoformat())


    def test_date_valid(self):
        date = datetime.utcnow()
        workout = {"name": "validName", "date": date, "notes": "validNotes", "visibility": "PU", "exercise_instances": [], "files": [], "participants": []}
        response = self.client.post("/api/workouts/", workout, format="json")
        self.assertEqual(str(response.data.get("date"))[:-1], date.isoformat())

    def test_date_invalid(self):
        time = "22.10.93"
        invalidName= "name!!..,m.,\+w0\+932\+3+49\+2904|+94!!\#m.,m.,m.,m.,m.,"
        workout = {"name": invalidName, "date": time, "notes": "validNotes", "visibility": "PU", "exercise_instances": [], "files": [], "participants": []}
        response = self.client.post("/api/workouts/", workout, format="json")
        self.assertEqual(str(response.data["date"][0]), "Datetime has wrong format. Use one of these formats instead: YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].")


class VisibilityTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="tester", email="test@test.no")
        self.user.set_password("password")
        self.user.save()

        self.accessToken = None

        self.client.login(username="tester", password="password")
        response = self.client.post('/api/token/', {"username": "tester", "password": "password"},  format="json")
        self.accessToken = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.accessToken)
        
        
    def test_visibility_too_short(self):
        date = datetime.utcnow()
        tooShortVisibility = "P"
        workout = {"name": "validName", "date": date, "notes": "validNotes", "visibility": tooShortVisibility, "exercise_instances": [], "files": [], "participants": []}
        response = self.client.post('/api/workouts/', workout,  format="json")
        self.assertEqual(str(response.data["visibility"][0]), "\"P\"" + " is not a valid choice.")
    
    def test_visibility_too_long(self):
        date = datetime.utcnow()
        tooLongVisibility = "PUT"
        workout = {"name": "validName", "date": date, "notes": "validNotes", "visibility": tooLongVisibility, "exercise_instances": [], "files": [], "participants": []}
        response = self.client.post("/api/workouts/", workout, format="json")
        self.assertEqual(str(response.data["visibility"][0]), "\"PUT\"" + " is not a valid choice.")

    def test_visibility_valid(self):
        date = datetime.utcnow()
        validVisibility = "PU"
        workout = {"name": "validName", "date": date, "notes": "validNotes", "visibility": validVisibility, "exercise_instances": [], "files": [], "participants": []}
        response = self.client.post("/api/workouts/", workout, format="json")
        self.assertEqual(response.data.get("visibility"), validVisibility)

    def test_visibility_invalid(self):
        date = datetime.utcnow()
        invalidVisibility = "!@!#"
        workout = {"name": "validName", "date": date, "notes": "validNotes", "visibility": invalidVisibility, "exercise_instances": [], "files": [], "participants": []}
        response = self.client.post("/api/workouts/", workout, format="json")
        self.assertEqual(str(response.data["visibility"][0]), "\"!@!#\"" + " is not a valid choice.")


class NotesTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="tester", email="test@test.no")
        self.user.set_password("password")
        self.user.save()

        self.accessToken = None

        self.client.login(username="tester", password="password")
        response = self.client.post('/api/token/', {"username": "tester", "password": "password"},  format="json")
        self.accessToken = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.accessToken)
        
        
    def test_notes_too_short(self):
        date = datetime.utcnow()
        tooShortNote= ""
        workout = {"name": "validName", "date": date, "notes": tooShortNote, "visibility": "PU", "exercise_instances": [], "files": [], "participants": []}
        response = self.client.post('/api/workouts/', workout,  format="json")
        self.assertEqual(str(response.data["notes"][0]), "This field may not be blank.")
    
    def test_notes_upper_limit(self):
        date = datetime.utcnow()
        longNote= "x" * 1000000
        workout = {"name": "validName", "date": date, "notes":longNote, "visibility": "PU", "exercise_instances": [], "files": [], "participants": []}
        response = self.client.post("/api/workouts/", workout, format="json")
        self.assertEqual(response.data.get("notes"), longNote)

    def test_notes_lower_limit(self):
        date = datetime.utcnow()
        shortNote= "x"
        workout = {"name": "validName", "date": date, "notes": shortNote, "visibility": "PU", "exercise_instances": [], "files": [], "participants": []}
        response = self.client.post("/api/workouts/", workout, format="json")
        self.assertEqual(response.data.get("notes"), shortNote)

    def test_notes_valid(self):
        date = datetime.utcnow()
        validNote= "validNote"
        workout = {"name": "validName", "date": date, "notes": validNote, "visibility": "PU", "exercise_instances": [], "files": [], "participants": []}
        response = self.client.post("/api/workouts/", workout, format="json")
        self.assertEqual(response.data.get("notes"), validNote)


class ExerciseTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="tester", email="test@test.no")
        self.user.set_password("password")
        self.user.save()

        self.accessToken = None

        self.client.login(username="tester", password="password")
        response = self.client.post('/api/token/', {"username": "tester", "password": "password"},  format="json")
        self.accessToken = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.accessToken)
        
        self.date = datetime.utcnow()
        self.pushups = Exercise.objects.create(name="Push-ups", unit="number", owner=self.user)
       
        
        
    def test_too_short(self):
        
        exercise = {"exercise":"", "workout":"api/workouts/1", "sets":"", "number":""}
        workout = {"name": "validName", "date": self.date, "notes": "validNote", "visibility": "PU", "exercise_instances": [exercise], "files": [], "participants": []}
        response = self.client.post('/api/workouts/', workout,  format="json")
        feedback =response.data["exercise_instances"][0]
        
        self.assertEqual(str(feedback["exercise"][0]), "This field may not be null.")
        self.assertEqual(str(feedback["sets"][0]), "A valid integer is required.")
        self.assertEqual(str(feedback["number"][0]), "A valid integer is required.")

    
    def test_too_long(self):
        toobigNum = "2"*1001
        exercise = {"exercise":"http://testserver/api/exercises/1/", "workout": "validWorkout", "sets": toobigNum, "number": toobigNum}
        workout = {"name": "validName", "date": self.date, "notes": "validNote", "visibility": "PU", "exercise_instances": [exercise], "files": [], "participants": []}
        
        response = self.client.post("/api/workouts/", workout, format="json")
        
        feedback=response.data["exercise_instances"][0]
        self.assertEqual(str(feedback["sets"][0]), "String value too large.")
        self.assertEqual(str(feedback["number"][0]), "String value too large.")

    def test_upper_limit(self):
        longNum= "2" * 1000
        exercise = {"exercise":"http://testserver/api/exercises/1/", "workout": "validWorkout", "sets": longNum, "number": longNum}
        workout = {"name": "validName", "date": self.date, "notes": "validNote", "visibility": "PU", "exercise_instances": [exercise], "files": [], "participants": []}
        response = self.client.post("/api/workouts/", workout, format="json")
        
        feedback=response.data["exercise_instances"][0]
        self.assertIsNone(feedback.get("sets"))
        self.assertIsNone(feedback.get("number"))

    def test_lower_limit(self):
        shortNum= "2"
        exercise = {"exercise":"http://testserver/api/exercises/1/", "workout": "validWorkout", "sets": shortNum, "number": shortNum}
        workout = {"name": "validName", "date": self.date, "notes": "validNote", "visibility": "PU", "exercise_instances": [exercise], "files": [], "participants": []}
        response = self.client.post("/api/workouts/", workout, format="json")

        feedback=response.data["exercise_instances"][0]
        self.assertIsNone(feedback.get("sets"))
        self.assertIsNone(feedback.get("number"))

    def test_valid(self):

        validNum = "15"
        exercise = {"exercise":"http://testserver/api/exercises/1/", "workout": "validWorkout", "sets": validNum, "number": validNum}
        workout = {"name": "validName", "date": self.date, "notes": "validNote", "visibility": "PU", "exercise_instances": [exercise], "files": [], "participants": []}
        response = self.client.post("/api/workouts/", workout, format="json")

        feedback=response.data["exercise_instances"][0]
        self.assertIsNone(feedback.get("exercise"))
        self.assertIsNone(feedback.get("sets"))
        self.assertIsNone(feedback.get("number"))


    def test_not_valid(self):

        invalidNum = "notValid"
        exercise = {"exercise":"notValid", "workout": "workout", "sets": invalidNum, "number": invalidNum}
        workout = {"name": "validName", "date": self.date, "notes": "validNote", "visibility": "PU", "exercise_instances": [exercise], "files": [], "participants": []}
        response = self.client.post("/api/workouts/", workout, format="json")

        feedback=response.data["exercise_instances"][0]
        self.assertEqual(str(feedback["exercise"][0]), "Invalid hyperlink - No URL match.")
        self.assertEqual(str(feedback["sets"][0]), "A valid integer is required.")
        self.assertEqual(str(feedback["number"][0]), "A valid integer is required.")


class FR5TestCase(APITestCase):
    def setUp(self):
        self.coach = User.objects.create(username="coach", email="test@test.no")
        self.coach.set_password("password")
        self.coach.save()
        
        self.athlete = User.objects.create(username="athlete", email="test@test.no", coach=self.coach)
        self.athlete.set_password("password")
        self.athlete.save()

        self.outsider = User.objects.create(username="outsider", email="test@test.no")
        self.outsider.set_password("password")
        self.outsider.save()

        # Setting ut data to query as different roles
        ex = Exercise.objects.create(
            name="ex1",
            owner=self.athlete,
            description="ex desc",
            unit="m"
        )
        ex.save()

        w_pr = Workout.objects.create(
            name="workout_PR",
            owner=self.athlete,
            date="2021-03-11T13:37:00Z",
            notes="workoutnote",
            visibility="PR"
        )
        w_pr.save()

        ExerciseInstance.objects.create(
            workout=w_pr,
            exercise=ex,
            sets=2,
            number=3
        ).save()

        Comment.objects.create(
            owner=self.athlete,
            workout=w_pr,
            content="comment_PR"
        ).save()
        
        WorkoutFile.objects.create(
            owner=self.athlete,
            workout=w_pr
        ).save()

        w_co = Workout.objects.create(
            name="workout_CO",
            owner=self.athlete,
            date="2021-03-12T13:37:00Z",
            notes="workoutnote",
            visibility="CO"
        )
        w_co.save()

        ExerciseInstance.objects.create(
            workout=w_co,
            exercise=ex,
            sets=2,
            number=3
        ).save()

        Comment.objects.create(
            owner=self.athlete,
            workout=w_co,
            content="comment_CO"
        ).save()
        WorkoutFile.objects.create(
            owner=self.athlete,
            workout=w_co
        ).save()

        w_pu = Workout.objects.create(
            name="workout_PU",
            owner=self.athlete,
            date="2021-03-13T13:37:00Z",
            notes="workoutnote",
            visibility="PU"
        )
        w_pu.save()

        ExerciseInstance.objects.create(
            workout=w_pu,
            exercise=ex,
            sets=2,
            number=3
        ).save()

        Comment.objects.create(
            owner=self.athlete,
            workout=w_pu,
            content="comment_PU"
        ).save()
        WorkoutFile.objects.create(
            owner=self.athlete,
            workout=w_pu
        ).save()
       
        
        
    def test_get_workouts_athlete(self):
        # Login as athlete
        self.client.login(username="athlete", password="password")
        response = self.client.post('/api/token/', {"username": "athlete", "password": "password"},  format="json")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + response.data["access"])

        # Workouts
        response = self.client.get('/api/workouts/?ordering=-date')
        self.assertEqual(response.data.get("count"), 3)
        self.assertEqual(response.data["results"][0]["name"], "workout_PU")
        self.assertEqual(response.data["results"][1]["name"], "workout_CO")
        self.assertEqual(response.data["results"][2]["name"], "workout_PR")
        # Exercise instances
        self.assertEqual(len(response.data["results"][0]["exercise_instances"]), 1)
        self.assertEqual(len(response.data["results"][1]["exercise_instances"]), 1)
        self.assertEqual(len(response.data["results"][2]["exercise_instances"]), 1)

        # Comments
        response = self.client.get('/api/comments/')
        self.assertEqual(response.data.get("count"), 3)
        self.assertEqual(response.data["results"][0]["content"], "comment_PU")
        self.assertEqual(response.data["results"][1]["content"], "comment_CO")
        self.assertEqual(response.data["results"][2]["content"], "comment_PR")

        # Workout files
        response = self.client.get('/api/workout-files/')
        self.assertEqual(response.data.get("count"), 3)

    def test_get_workouts_coach(self):
        # Login as coach
        self.client.login(username="coach", password="password")
        response = self.client.post('/api/token/', {"username": "coach", "password": "password"},  format="json")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + response.data["access"])

        # Workouts
        response = self.client.get('/api/workouts/?ordering=-date')
        self.assertEqual(response.data.get("count"), 2)
        self.assertEqual(response.data["results"][0]["name"], "workout_PU")
        self.assertEqual(response.data["results"][1]["name"], "workout_CO")
        # Exercise instances
        self.assertEqual(len(response.data["results"][0]["exercise_instances"]), 1)
        self.assertEqual(len(response.data["results"][1]["exercise_instances"]), 1)
        
        # Comments
        response = self.client.get('/api/comments/')
        self.assertEqual(response.data.get("count"), 2)
        self.assertEqual(response.data["results"][0]["content"], "comment_PU")
        self.assertEqual(response.data["results"][1]["content"], "comment_CO")

        # Workoutfiles
        response = self.client.get('/api/workout-files/')
        self.assertEqual(response.data.get("count"), 2)

    def test_get_workouts_outsider(self):
        # Login as outsider
        self.client.login(username="outsider", password="password")
        response = self.client.post('/api/token/', {"username": "outsider", "password": "password"},  format="json")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + response.data["access"])      
        
        # Workouts
        response = self.client.get('/api/workouts/?ordering=-date')
        self.assertEqual(response.data.get("count"), 1)
        self.assertEqual(response.data["results"][0]["name"], "workout_PU")
        # Exercise instances
        self.assertEqual(len(response.data["results"][0]["exercise_instances"]), 1)

        # Comments
        response = self.client.get('/api/comments/')
        self.assertEqual(response.data.get("count"), 1)
        self.assertEqual(response.data["results"][0]["content"], "comment_PU")

        # Workout files
        response = self.client.get('/api/workout-files/')
        self.assertEqual(response.data.get("count"), 1)
