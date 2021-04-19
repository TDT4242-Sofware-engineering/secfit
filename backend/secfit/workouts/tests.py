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

## Global constants
TOKEN_PATH = "/api/token/"
AUTH_PREFIX = "Bearer "
WORKOUTS_PATH = "/api/workouts/"
WORKOUTS_ORDERING_PATH = "/api/workouts/?ordering=-date"
COMMENTS_PATH = "/api/comments/"
WORKOUT_FILES_PATH = "/api/workout-files/"
### Dummy data
DUMMY_EMAIL = "email@email.no"
DUMMY_STREET = "Prinsen gate"
DUMMY_DATE = "2021-03-11T13:37:00Z"

class WorkoutPermissionsTestCase(TestCase):
    def setUp(self):
        self.requestuser = get_user_model().objects.create(
            username="requestuser", 
            email=DUMMY_EMAIL, 
            phone_number="91919191", 
            country="Norway", 
            city="Trondheim", 
            street_address=DUMMY_STREET
        )
        self.requestuser.save()
        self.workout = Workout.objects.create(
            name="workout",
            owner=self.requestuser,
            date=DUMMY_DATE,
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
            email=DUMMY_EMAIL, 
            phone_number="91919191", 
            country="Norway", 
            city="Trondheim", 
            street_address=DUMMY_STREET
        )

        workout = Workout.objects.create(
            name="workout",
            owner=user,
            date=DUMMY_DATE,
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
            date=DUMMY_DATE,
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
            email=DUMMY_EMAIL, 
            phone_number="91919191", 
            country="Norway", 
            city="Trondheim", 
            street_address=DUMMY_STREET
        )
        user.save()

        workout = Workout.objects.create(
            name="workout",
            owner=user,
            date=DUMMY_DATE,
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
            email=DUMMY_EMAIL, 
            phone_number="91919191", 
            country="Norway", 
            city="Trondheim", 
            street_address=DUMMY_STREET
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
            email=DUMMY_EMAIL, 
            phone_number="91919191", 
            country="Norway", 
            city="Trondheim", 
            street_address=DUMMY_STREET
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
            email=DUMMY_EMAIL, 
            phone_number="91919191", 
            country="Norway", 
            city="Trondheim", 
            street_address=DUMMY_STREET
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
            email=DUMMY_EMAIL, 
            phone_number="91919191", 
            country="Norway", 
            city="Trondheim", 
            street_address=DUMMY_STREET
        )
        workout = Workout.objects.create(
            name="workout",
            owner=user,
            date=DUMMY_DATE,
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
            date=DUMMY_DATE,
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
            date=DUMMY_DATE,
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
            email=DUMMY_EMAIL, 
            phone_number="91919191", 
            country="Norway", 
            city="Trondheim", 
            street_address=DUMMY_STREET
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
            email=DUMMY_EMAIL, 
            phone_number="91919191", 
            country="Norway", 
            city="Trondheim", 
            street_address=DUMMY_STREET
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
            email=DUMMY_EMAIL, 
            phone_number="91919191", 
            country="Norway", 
            city="Trondheim", 
            street_address=DUMMY_STREET
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
            email=DUMMY_EMAIL, 
            phone_number="91919191", 
            country="Norway", 
            city="Trondheim", 
            street_address=DUMMY_STREET
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
            email=DUMMY_EMAIL, 
            phone_number="91919191", 
            country="Norway", 
            city="Trondheim", 
            street_address=DUMMY_STREET
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
            email=DUMMY_EMAIL, 
            phone_number="91919191", 
            country="Norway", 
            city="Trondheim", 
            street_address=DUMMY_STREET
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
            date=DUMMY_DATE,
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
            date=DUMMY_DATE,
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
        self.user = User.objects.create(username="tester", email=DUMMY_EMAIL)
        self.user.set_password("password")
        self.user.save()

        self.accessToken = None

        self.client.login(username="tester", password="password")
        response = self.client.post(TOKEN_PATH, {"username": "tester", "password": "password"},  format="json")
        self.accessToken = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=AUTH_PREFIX + self.accessToken)
        
        
    def test_name_too_short(self):
        date = datetime.utcnow()
        too_short_name= ""
        workout = {"name": too_short_name, "date": date, "notes": "validNotes", "visibility": "PU", "exercise_instances": [], "files": [], "participants": []}
        response = self.client.post(WORKOUTS_PATH, workout,  format="json")
        self.assertEqual(str(response.data["name"][0]), "This field may not be blank.")
    
    def test_name_too_long(self):
        date = datetime.utcnow()
        too_long_name= "x" * 101
        workout = {"name": too_long_name, "date": date, "notes": "validNotes", "visibility": "PU", "exercise_instances": [], "files": [], "participants": []}
        response = self.client.post(WORKOUTS_PATH, workout, format="json")
        self.assertEqual(str(response.data["name"][0]), "Ensure this field has no more than 100 characters.")

    def test_name_upper_limit(self):
        date = datetime.utcnow()
        long_name= "x" * 100
        workout = {"name": long_name, "date": date, "notes": "validNotes", "visibility": "PU", "exercise_instances": [], "files": [], "participants": []}
        response = self.client.post(WORKOUTS_PATH, workout, format="json")
        self.assertEqual(response.data.get("name"), long_name)

    def test_name_lower_limit(self):
        date = datetime.utcnow()
        short_name= "x"
        workout = {"name": short_name, "date": date, "notes": "validNotes", "visibility": "PU", "exercise_instances": [], "files": [], "participants": []}
        response = self.client.post(WORKOUTS_PATH, workout, format="json")
        self.assertEqual(response.data.get("name"), short_name)

    def test_name_valid(self):
        date = datetime.utcnow()
        valid_name= "name"
        workout = {"name": valid_name, "date": date, "notes": "validNotes", "visibility": "PU", "exercise_instances": [], "files": [], "participants": []}
        response = self.client.post(WORKOUTS_PATH, workout, format="json")
        self.assertEqual(response.data.get("name"), valid_name)

class DateTimeCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="tester", email=DUMMY_EMAIL)
        self.user.set_password("password")
        self.user.save()

        self.accessToken = None

        self.client.login(username="tester", password="password")
        response = self.client.post(TOKEN_PATH, {"username": "tester", "password": "password"},  format="json")
        self.accessToken = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=AUTH_PREFIX + self.accessToken)

    def test_date_upper_limit(self):
        date = datetime.max
        workout = {"name": "validName", "date": date, "notes": "validNotes", "visibility": "PU", "exercise_instances": [], "files": [], "participants": []}
        response = self.client.post(WORKOUTS_PATH, workout, format="json")
        self.assertEqual(str(response.data.get("date"))[:-1], date.isoformat())


    def test_date_lower_limit(self):
        date = datetime.min
        workout = {"name": "validName", "date": date, "notes": "validNotes", "visibility": "PU", "exercise_instances": [], "files": [], "participants": []}
        response = self.client.post(WORKOUTS_PATH, workout, format="json")
        self.assertEqual(str(response.data.get("date"))[:-1], date.isoformat())


    def test_date_valid(self):
        date = datetime.utcnow()
        workout = {"name": "validName", "date": date, "notes": "validNotes", "visibility": "PU", "exercise_instances": [], "files": [], "participants": []}
        response = self.client.post(WORKOUTS_PATH, workout, format="json")
        self.assertEqual(str(response.data.get("date"))[:-1], date.isoformat())

    def test_date_invalid(self):
        time = "22.10.93"
        invalid_name= "name!!..,m.,\+w0\+932\+3+49\+2904|+94!!\#m.,m.,m.,m.,m.,"
        workout = {"name": invalid_name, "date": time, "notes": "validNotes", "visibility": "PU", "exercise_instances": [], "files": [], "participants": []}
        response = self.client.post(WORKOUTS_PATH, workout, format="json")
        self.assertEqual(str(response.data["date"][0]), "Datetime has wrong format. Use one of these formats instead: YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].")


class VisibilityTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="tester", email=DUMMY_EMAIL)
        self.user.set_password("password")
        self.user.save()

        self.accessToken = None

        self.client.login(username="tester", password="password")
        response = self.client.post(TOKEN_PATH, {"username": "tester", "password": "password"},  format="json")
        self.accessToken = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=AUTH_PREFIX + self.accessToken)
        
        
    def test_visibility_too_short(self):
        date = datetime.utcnow()
        too_short_visibility = "P"
        workout = {"name": "validName", "date": date, "notes": "validNotes", "visibility": too_short_visibility, "exercise_instances": [], "files": [], "participants": []}
        response = self.client.post(WORKOUTS_PATH, workout,  format="json")
        self.assertEqual(str(response.data["visibility"][0]), "\"P\"" + " is not a valid choice.")
    
    def test_visibility_too_long(self):
        date = datetime.utcnow()
        too_long_visibility = "PUT"
        workout = {"name": "validName", "date": date, "notes": "validNotes", "visibility": too_long_visibility, "exercise_instances": [], "files": [], "participants": []}
        response = self.client.post(WORKOUTS_PATH, workout, format="json")
        self.assertEqual(str(response.data["visibility"][0]), "\"PUT\"" + " is not a valid choice.")

    def test_visibility_valid(self):
        date = datetime.utcnow()
        valid_visibility = "PU"
        workout = {"name": "validName", "date": date, "notes": "validNotes", "visibility": valid_visibility, "exercise_instances": [], "files": [], "participants": []}
        response = self.client.post(WORKOUTS_PATH, workout, format="json")
        self.assertEqual(response.data.get("visibility"), valid_visibility)

    def test_visibility_invalid(self):
        date = datetime.utcnow()
        invalid_visibility = "!@!#"
        workout = {"name": "validName", "date": date, "notes": "validNotes", "visibility": invalid_visibility, "exercise_instances": [], "files": [], "participants": []}
        response = self.client.post(WORKOUTS_PATH, workout, format="json")
        self.assertEqual(str(response.data["visibility"][0]), "\"!@!#\"" + " is not a valid choice.")


class NotesTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="tester", email=DUMMY_EMAIL)
        self.user.set_password("password")
        self.user.save()

        self.accessToken = None

        self.client.login(username="tester", password="password")
        response = self.client.post(TOKEN_PATH, {"username": "tester", "password": "password"},  format="json")
        self.accessToken = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=AUTH_PREFIX + self.accessToken)
        
        
    def test_notes_too_short(self):
        date = datetime.utcnow()
        too_short_note= ""
        workout = {"name": "validName", "date": date, "notes": too_short_note, "visibility": "PU", "exercise_instances": [], "files": [], "participants": []}
        response = self.client.post(WORKOUTS_PATH, workout,  format="json")
        self.assertEqual(str(response.data["notes"][0]), "This field may not be blank.")
    
    def test_notes_upper_limit(self):
        date = datetime.utcnow()
        long_note= "x" * 1000000
        workout = {"name": "validName", "date": date, "notes":long_note, "visibility": "PU", "exercise_instances": [], "files": [], "participants": []}
        response = self.client.post(WORKOUTS_PATH, workout, format="json")
        self.assertEqual(response.data.get("notes"), long_note)

    def test_notes_lower_limit(self):
        date = datetime.utcnow()
        short_note= "x"
        workout = {"name": "validName", "date": date, "notes": short_note, "visibility": "PU", "exercise_instances": [], "files": [], "participants": []}
        response = self.client.post(WORKOUTS_PATH, workout, format="json")
        self.assertEqual(response.data.get("notes"), short_note)

    def test_notes_valid(self):
        date = datetime.utcnow()
        valid_note= "validNote"
        workout = {"name": "validName", "date": date, "notes": valid_note, "visibility": "PU", "exercise_instances": [], "files": [], "participants": []}
        response = self.client.post(WORKOUTS_PATH, workout, format="json")
        self.assertEqual(response.data.get("notes"), valid_note)


class ExerciseTestCase(APITestCase):

    def setUp(self):
        self.EXERCISE_URL = "http://testserver/api/exercises/1/"

        self.user = User.objects.create(username="tester", email=DUMMY_EMAIL)
        self.user.set_password("password")
        self.user.save()

        self.accessToken = None

        self.client.login(username="tester", password="password")
        response = self.client.post(TOKEN_PATH, {"username": "tester", "password": "password"},  format="json")
        self.accessToken = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=AUTH_PREFIX + self.accessToken)
        
        self.date = datetime.utcnow()
        self.pushups = Exercise.objects.create(name="Push-ups", unit="number", owner=self.user)
       
        
        
    def test_too_short(self):
        
        exercise = {"exercise":"", "workout":"api/workouts/1", "sets":"", "number":""}
        workout = {"name": "validName", "date": self.date, "notes": "validNote", "visibility": "PU", "exercise_instances": [exercise], "files": [], "participants": []}
        response = self.client.post(WORKOUTS_PATH, workout,  format="json")
        feedback =response.data["exercise_instances"][0]
        
        self.assertEqual(str(feedback["exercise"][0]), "This field may not be null.")
        self.assertEqual(str(feedback["sets"][0]), "A valid integer is required.")
        self.assertEqual(str(feedback["number"][0]), "A valid integer is required.")

    
    def test_too_long(self):
        too_big_num = "2"*1001
        exercise = {"exercise":self.EXERCISE_URL, "workout": "validWorkout", "sets": too_big_num, "number": too_big_num}
        workout = {"name": "validName", "date": self.date, "notes": "validNote", "visibility": "PU", "exercise_instances": [exercise], "files": [], "participants": []}
        
        response = self.client.post(WORKOUTS_PATH, workout, format="json")
        
        feedback=response.data["exercise_instances"][0]
        self.assertEqual(str(feedback["sets"][0]), "String value too large.")
        self.assertEqual(str(feedback["number"][0]), "String value too large.")

    def test_upper_limit(self):
        long_num= "2" * 1000
        exercise = {"exercise":self.EXERCISE_URL, "workout": "validWorkout", "sets": long_num, "number": long_num}
        workout = {"name": "validName", "date": self.date, "notes": "validNote", "visibility": "PU", "exercise_instances": [exercise], "files": [], "participants": []}
        response = self.client.post(WORKOUTS_PATH, workout, format="json")
        
        feedback=response.data["exercise_instances"][0]
        self.assertIsNone(feedback.get("sets"))
        self.assertIsNone(feedback.get("number"))

    def test_lower_limit(self):
        short_num= "2"
        exercise = {"exercise":self.EXERCISE_URL, "workout": "validWorkout", "sets": short_num, "number": short_num}
        workout = {"name": "validName", "date": self.date, "notes": "validNote", "visibility": "PU", "exercise_instances": [exercise], "files": [], "participants": []}
        response = self.client.post(WORKOUTS_PATH, workout, format="json")

        feedback=response.data["exercise_instances"][0]
        self.assertIsNone(feedback.get("sets"))
        self.assertIsNone(feedback.get("number"))

    def test_valid(self):

        valid_num = "15"
        exercise = {"exercise":self.EXERCISE_URL, "workout": "validWorkout", "sets": valid_num, "number": valid_num}
        workout = {"name": "validName", "date": self.date, "notes": "validNote", "visibility": "PU", "exercise_instances": [exercise], "files": [], "participants": []}
        response = self.client.post(WORKOUTS_PATH, workout, format="json")

        feedback=response.data["exercise_instances"][0]
        self.assertIsNone(feedback.get("exercise"))
        self.assertIsNone(feedback.get("sets"))
        self.assertIsNone(feedback.get("number"))


    def test_not_valid(self):

        invalid_num = "notValid"
        exercise = {"exercise":"notValid", "workout": "workout", "sets": invalid_num, "number": invalid_num}
        workout = {"name": "validName", "date": self.date, "notes": "validNote", "visibility": "PU", "exercise_instances": [exercise], "files": [], "participants": []}
        response = self.client.post(WORKOUTS_PATH, workout, format="json")

        feedback=response.data["exercise_instances"][0]
        self.assertEqual(str(feedback["exercise"][0]), "Invalid hyperlink - No URL match.")
        self.assertEqual(str(feedback["sets"][0]), "A valid integer is required.")
        self.assertEqual(str(feedback["number"][0]), "A valid integer is required.")


class FR5TestCase(APITestCase):
    def setUp(self):
        self.coach = User.objects.create(username="coach", email=DUMMY_EMAIL)
        self.coach.set_password("password")
        self.coach.save()
        
        self.athlete = User.objects.create(username="athlete", email=DUMMY_EMAIL, coach=self.coach)
        self.athlete.set_password("password")
        self.athlete.save()

        self.outsider = User.objects.create(username="outsider", email=DUMMY_EMAIL)
        self.outsider.set_password("password")
        self.outsider.save()

        # Setting ut data to query as different roles
        exercise1 = Exercise.objects.create(
            name="ex1",
            owner=self.athlete,
            description="ex desc",
            unit="m"
        )
        exercise1.save()

        workout_private = Workout.objects.create(
            name="workout_PR",
            owner=self.athlete,
            date=DUMMY_DATE,
            notes="workoutnote",
            visibility="PR"
        )
        workout_private.save()

        ExerciseInstance.objects.create(
            workout=workout_private,
            exercise=exercise1,
            sets=2,
            number=3
        ).save()

        Comment.objects.create(
            owner=self.athlete,
            workout=workout_private,
            content="comment_PR"
        ).save()
        
        WorkoutFile.objects.create(
            owner=self.athlete,
            workout=workout_private
        ).save()

        workout_coach = Workout.objects.create(
            name="workout_CO",
            owner=self.athlete,
            date="2021-03-12T13:37:00Z",
            notes="workoutnote",
            visibility="CO"
        )
        workout_coach.save()

        ExerciseInstance.objects.create(
            workout=workout_coach,
            exercise=exercise1,
            sets=2,
            number=3
        ).save()

        Comment.objects.create(
            owner=self.athlete,
            workout=workout_coach,
            content="comment_CO"
        ).save()
        WorkoutFile.objects.create(
            owner=self.athlete,
            workout=workout_coach
        ).save()

        workout_public = Workout.objects.create(
            name="workout_PU",
            owner=self.athlete,
            date="2021-03-13T13:37:00Z",
            notes="workoutnote",
            visibility="PU"
        )
        workout_public.save()

        ExerciseInstance.objects.create(
            workout=workout_public,
            exercise=exercise1,
            sets=2,
            number=3
        ).save()

        Comment.objects.create(
            owner=self.athlete,
            workout=workout_public,
            content="comment_PU"
        ).save()
        WorkoutFile.objects.create(
            owner=self.athlete,
            workout=workout_public
        ).save()
       
        
        
    def test_get_workouts_athlete(self):
        # Login as athlete
        self.client.login(username="athlete", password="password")
        response = self.client.post(TOKEN_PATH, {"username": "athlete", "password": "password"},  format="json")
        self.client.credentials(HTTP_AUTHORIZATION=AUTH_PREFIX + response.data["access"])

        # Workouts
        response = self.client.get(WORKOUTS_ORDERING_PATH)
        self.assertEqual(response.data.get("count"), 3)
        self.assertEqual(response.data["results"][0]["name"], "workout_PU")
        self.assertEqual(response.data["results"][1]["name"], "workout_CO")
        self.assertEqual(response.data["results"][2]["name"], "workout_PR")
        # Exercise instances
        self.assertEqual(len(response.data["results"][0]["exercise_instances"]), 1)
        self.assertEqual(len(response.data["results"][1]["exercise_instances"]), 1)
        self.assertEqual(len(response.data["results"][2]["exercise_instances"]), 1)

        # Comments
        response = self.client.get(COMMENTS_PATH)
        self.assertEqual(response.data.get("count"), 3)
        self.assertEqual(response.data["results"][0]["content"], "comment_PU")
        self.assertEqual(response.data["results"][1]["content"], "comment_CO")
        self.assertEqual(response.data["results"][2]["content"], "comment_PR")

        # Workout files
        response = self.client.get(WORKOUT_FILES_PATH)
        self.assertEqual(response.data.get("count"), 3)

    def test_get_workouts_coach(self):
        # Login as coach
        self.client.login(username="coach", password="password")
        response = self.client.post('/api/token/', {"username": "coach", "password": "password"},  format="json")
        self.client.credentials(HTTP_AUTHORIZATION=AUTH_PREFIX + response.data["access"])

        # Workouts
        response = self.client.get(WORKOUTS_ORDERING_PATH)
        self.assertEqual(response.data.get("count"), 2)
        self.assertEqual(response.data["results"][0]["name"], "workout_PU")
        self.assertEqual(response.data["results"][1]["name"], "workout_CO")
        # Exercise instances
        self.assertEqual(len(response.data["results"][0]["exercise_instances"]), 1)
        self.assertEqual(len(response.data["results"][1]["exercise_instances"]), 1)
        
        # Comments
        response = self.client.get(COMMENTS_PATH)
        self.assertEqual(response.data.get("count"), 2)
        self.assertEqual(response.data["results"][0]["content"], "comment_PU")
        self.assertEqual(response.data["results"][1]["content"], "comment_CO")

        # Workoutfiles
        response = self.client.get(WORKOUT_FILES_PATH)
        self.assertEqual(response.data.get("count"), 2)

    def test_get_workouts_outsider(self):
        # Login as outsider
        self.client.login(username="outsider", password="password")
        response = self.client.post('/api/token/', {"username": "outsider", "password": "password"},  format="json")
        self.client.credentials(HTTP_AUTHORIZATION=AUTH_PREFIX + response.data["access"])      
        
        # Workouts
        response = self.client.get(WORKOUTS_ORDERING_PATH)
        self.assertEqual(response.data.get("count"), 1)
        self.assertEqual(response.data["results"][0]["name"], "workout_PU")
        # Exercise instances
        self.assertEqual(len(response.data["results"][0]["exercise_instances"]), 1)

        # Comments
        response = self.client.get(COMMENTS_PATH)
        self.assertEqual(response.data.get("count"), 1)
        self.assertEqual(response.data["results"][0]["content"], "comment_PU")

        # Workout files
        response = self.client.get(WORKOUT_FILES_PATH)
        self.assertEqual(response.data.get("count"), 1)

class WorkoutSerializerUpdateTestCase(APITestCase):
    def setUp(self):       
        self.athlete = User.objects.create(username="athlete", email=DUMMY_EMAIL)
        self.athlete.set_password("password")
        self.athlete.save()

        # Setting ut data to query as different roles
        exercise1 = Exercise.objects.create(
            name="ex1",
            owner=self.athlete,
            description="ex desc",
            unit="m"
        )
        exercise1.save()

        workout_private = Workout.objects.create(
            name="workout_PR",
            owner=self.athlete,
            date=DUMMY_DATE,
            notes="workoutnote",
            visibility="PR"
        )
        workout_private.save()

        ExerciseInstance.objects.create(
            workout=workout_private,
            exercise=exercise1,
            sets=1,
            number=2
        ).save()

        ExerciseInstance.objects.create(
            workout=workout_private,
            exercise=exercise1,
            sets=2,
            number=3
        ).save()
        
        WorkoutFile.objects.create(
            owner=self.athlete,
            workout=workout_private
        ).save()
    
    def test_add_exercise(self):
        self.client.login(username="athlete", password="password")
        response = self.client.post('/api/token/', {"username": "athlete", "password": "password"},  format="json")
        self.client.credentials(HTTP_AUTHORIZATION=AUTH_PREFIX + response.data["access"])

        data = {
            'name': "name from put",
            'date': "2021-04-11T11:18:00.000Z",
            'notes': "notes from put",
            'visibility': 'PR',
            'participants': '[]',
            'exercise_instances': '[\
                {"exercise":"https://secfit.vassbo.as/api/exercises/1/","number":"3","sets":"4"}, \
                {"exercise":"https://secfit.vassbo.as/api/exercises/1/","number":"4","sets":"5"},\
                {"exercise":"https://secfit.vassbo.as/api/exercises/1/","number":"5","sets":"6"}\
                ]',
            'files': []
        }
        response = self.client.put(WORKOUTS_PATH + "1/", data,  format="multipart")
        
        exepected = {
            "url":"http://testserver/api/workouts/1/",
            "id":1,
            "name":"name from put",
            "date":"2021-04-11T11:18:00Z",
            "notes":"notes from put",
            "owner":"http://testserver/api/users/1/",
            "owner_username":"athlete",
            "visibility":"PR",
            "exercise_instances":[
                {"url":"http://testserver/api/exercise-instances/1/","id":1,"exercise":"http://testserver/api/exercises/1/","sets":4,"number":3,"workout":"http://testserver/api/workouts/1/"},
                {"url":"http://testserver/api/exercise-instances/2/","id":2,"exercise":"http://testserver/api/exercises/1/","sets":5,"number":4,"workout":"http://testserver/api/workouts/1/"},
                {"url":"http://testserver/api/exercise-instances/3/","id":3,"exercise":"http://testserver/api/exercises/1/","sets":6,"number":5,"workout":"http://testserver/api/workouts/1/"}],
            "files":[],
            "participants":[]
        }
            
        self.assertEqual(response.json(), exepected)
    
    def test_remove_exercise(self):
        self.client.login(username="athlete", password="password")
        response = self.client.post('/api/token/', {"username": "athlete", "password": "password"},  format="json")
        self.client.credentials(HTTP_AUTHORIZATION=AUTH_PREFIX + response.data["access"])

        data = {
            'name': "name from put",
            'date': "2021-04-11T11:18:00.000Z",
            'notes': "notes from put",
            'visibility': 'PR',
            'participants': '[]',
            'exercise_instances': '[\
                {"exercise":"https://secfit.vassbo.as/api/exercises/1/","number":"3","sets":"4"}\
                ]',
            'files': []
        }
        response = self.client.put(WORKOUTS_PATH + "1/", data,  format="multipart")
        
        exepected = {
            "url":"http://testserver/api/workouts/1/",
            "id":1,
            "name":"name from put",
            "date":"2021-04-11T11:18:00Z",
            "notes":"notes from put",
            "owner":"http://testserver/api/users/1/",
            "owner_username":"athlete",
            "visibility":"PR",
            "exercise_instances":[
                {"url":"http://testserver/api/exercise-instances/1/","id":1,"exercise":"http://testserver/api/exercises/1/","sets":4,"number":3,"workout":"http://testserver/api/workouts/1/"}],
            "files":[],
            "participants":[]
        }
            
        self.assertEqual(response.json(), exepected)

