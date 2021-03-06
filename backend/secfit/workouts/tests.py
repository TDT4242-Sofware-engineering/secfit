from rest_framework.test import APITestCase, force_authenticate, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from datetime import datetime
from users.models import User
from workouts.models import ExerciseInstance, Exercise, Workout


# Create your tests here.
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
        workout = {"name": tooShortName, "date": date, "notes": "validNotes", "visibility": "PU", "exercise_instances": [], "files": []}
        response = self.client.post('/api/workouts/', workout,  format="json")
        self.assertEqual(str(response.data["name"][0]), "This field may not be blank.")
    
    def test_name_too_long(self):
        date = datetime.utcnow()
        tooLongName= "x" * 101
        workout = {"name": tooLongName, "date": date, "notes": "validNotes", "visibility": "PU", "exercise_instances": [], "files": []}
        response = self.client.post("/api/workouts/", workout, format="json")
        self.assertEqual(str(response.data["name"][0]), "Ensure this field has no more than 100 characters.")

    def test_name_upper_limit(self):
        date = datetime.utcnow()
        longName= "x" * 100
        workout = {"name": longName, "date": date, "notes": "validNotes", "visibility": "PU", "exercise_instances": [], "files": []}
        response = self.client.post("/api/workouts/", workout, format="json")
        self.assertEqual(response.data.get("name"), longName)

    def test_name_lower_limit(self):
        date = datetime.utcnow()
        shortName= "x"
        workout = {"name": shortName, "date": date, "notes": "validNotes", "visibility": "PU", "exercise_instances": [], "files": []}
        response = self.client.post("/api/workouts/", workout, format="json")
        self.assertEqual(response.data.get("name"), shortName)

    def test_name_valid(self):
        date = datetime.utcnow()
        validName= "name"
        workout = {"name": validName, "date": date, "notes": "validNotes", "visibility": "PU", "exercise_instances": [], "files": []}
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
        workout = {"name": "validName", "date": date, "notes": "validNotes", "visibility": "PU", "exercise_instances": [], "files": []}
        response = self.client.post("/api/workouts/", workout, format="json")
        self.assertEqual(str(response.data.get("date"))[:-1], date.isoformat())


    def test_date_lower_limit(self):
        date = datetime.min
        workout = {"name": "validName", "date": date, "notes": "validNotes", "visibility": "PU", "exercise_instances": [], "files": []}
        response = self.client.post("/api/workouts/", workout, format="json")
        self.assertEqual(str(response.data.get("date"))[:-1], date.isoformat())


    def test_date_valid(self):
        date = datetime.utcnow()
        workout = {"name": "validName", "date": date, "notes": "validNotes", "visibility": "PU", "exercise_instances": [], "files": []}
        response = self.client.post("/api/workouts/", workout, format="json")
        self.assertEqual(str(response.data.get("date"))[:-1], date.isoformat())

    def test_date_invalid(self):
        time = "22.10.93"
        invalidName= "name!!..,m.,\+w0\+932\+3+49\+2904|+94!!\#m.,m.,m.,m.,m.,"
        workout = {"name": invalidName, "date": time, "notes": "validNotes", "visibility": "PU", "exercise_instances": [], "files": []}
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
        workout = {"name": "validName", "date": date, "notes": "validNotes", "visibility": tooShortVisibility, "exercise_instances": [], "files": []}
        response = self.client.post('/api/workouts/', workout,  format="json")
        self.assertEqual(str(response.data["visibility"][0]), "\"P\"" + " is not a valid choice.")
    
    def test_visibility_too_long(self):
        date = datetime.utcnow()
        tooLongVisibility = "PUT"
        workout = {"name": "validName", "date": date, "notes": "validNotes", "visibility": tooLongVisibility, "exercise_instances": [], "files": []}
        response = self.client.post("/api/workouts/", workout, format="json")
        self.assertEqual(str(response.data["visibility"][0]), "\"PUT\"" + " is not a valid choice.")

    def test_visibility_valid(self):
        date = datetime.utcnow()
        validVisibility = "PU"
        workout = {"name": "validName", "date": date, "notes": "validNotes", "visibility": validVisibility, "exercise_instances": [], "files": []}
        response = self.client.post("/api/workouts/", workout, format="json")
        self.assertEqual(response.data.get("visibility"), validVisibility)

    def test_visibility_invalid(self):
        date = datetime.utcnow()
        invalidVisibility = "!@!#"
        workout = {"name": "validName", "date": date, "notes": "validNotes", "visibility": invalidVisibility, "exercise_instances": [], "files": []}
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
        workout = {"name": "validName", "date": date, "notes": tooShortNote, "visibility": "PU", "exercise_instances": [], "files": []}
        response = self.client.post('/api/workouts/', workout,  format="json")
        self.assertEqual(str(response.data["notes"][0]), "This field may not be blank.")
    
    def test_notes_upper_limit(self):
        date = datetime.utcnow()
        longNote= "x" * 1000000
        workout = {"name": "validName", "date": date, "notes":longNote, "visibility": "PU", "exercise_instances": [], "files": []}
        response = self.client.post("/api/workouts/", workout, format="json")
        self.assertEqual(response.data.get("notes"), longNote)

    def test_notes_lower_limit(self):
        date = datetime.utcnow()
        shortNote= "x"
        workout = {"name": "validName", "date": date, "notes": shortNote, "visibility": "PU", "exercise_instances": [], "files": []}
        response = self.client.post("/api/workouts/", workout, format="json")
        self.assertEqual(response.data.get("notes"), shortNote)

    def test_notes_valid(self):
        date = datetime.utcnow()
        validNote= "validNote"
        workout = {"name": "validName", "date": date, "notes": validNote, "visibility": "PU", "exercise_instances": [], "files": []}
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
        self.pushups = Exercise.objects.create(name="Push-ups", unit="number")
       
        
        
    def test_too_short(self):
        
        exercise = {"exercise":"", "workout":"api/workouts/1", "sets":"", "number":""}
        workout = {"name": "validName", "date": self.date, "notes": "validNote", "visibility": "PU", "exercise_instances": [exercise], "files": []}
        response = self.client.post('/api/workouts/', workout,  format="json")
        feedback =response.data["exercise_instances"][0]
        
        self.assertEqual(str(feedback["exercise"][0]), "This field may not be null.")
        self.assertEqual(str(feedback["sets"][0]), "A valid integer is required.")
        self.assertEqual(str(feedback["number"][0]), "A valid integer is required.")

    
    def test_too_long(self):
        toobigNum = "2"*1001
        exercise = {"exercise":"http://testserver/api/exercises/1/", "workout": "validWorkout", "sets": toobigNum, "number": toobigNum}
        workout = {"name": "validName", "date": self.date, "notes": "validNote", "visibility": "PU", "exercise_instances": [exercise], "files": []}
        
        response = self.client.post("/api/workouts/", workout, format="json")
        
        feedback=response.data["exercise_instances"][0]
        self.assertEqual(str(feedback["sets"][0]), "String value too large.")
        self.assertEqual(str(feedback["number"][0]), "String value too large.")

    def test_upper_limit(self):
        longNum= "2" * 1000
        exercise = {"exercise":"http://testserver/api/exercises/1/", "workout": "validWorkout", "sets": longNum, "number": longNum}
        workout = {"name": "validName", "date": self.date, "notes": "validNote", "visibility": "PU", "exercise_instances": [exercise], "files": []}
        response = self.client.post("/api/workouts/", workout, format="json")
        
        feedback=response.data["exercise_instances"][0]
        self.assertIsNone(feedback.get("sets"))
        self.assertIsNone(feedback.get("number"))

    def test_lower_limit(self):
        shortNum= "2"
        exercise = {"exercise":"http://testserver/api/exercises/1/", "workout": "validWorkout", "sets": shortNum, "number": shortNum}
        workout = {"name": "validName", "date": self.date, "notes": "validNote", "visibility": "PU", "exercise_instances": [exercise], "files": []}
        response = self.client.post("/api/workouts/", workout, format="json")

        feedback=response.data["exercise_instances"][0]
        self.assertIsNone(feedback.get("sets"))
        self.assertIsNone(feedback.get("number"))

    def test_valid(self):

        validNum = "15"
        exercise = {"exercise":"http://testserver/api/exercises/1/", "workout": "validWorkout", "sets": validNum, "number": validNum}
        workout = {"name": "validName", "date": self.date, "notes": "validNote", "visibility": "PU", "exercise_instances": [exercise], "files": []}
        response = self.client.post("/api/workouts/", workout, format="json")

        feedback=response.data["exercise_instances"][0]
        self.assertIsNone(feedback.get("exercise"))
        self.assertIsNone(feedback.get("sets"))
        self.assertIsNone(feedback.get("number"))


    def test_not_valid(self):

        invalidNum = "notValid"
        exercise = {"exercise":"notValid", "workout": "workout", "sets": invalidNum, "number": invalidNum}
        workout = {"name": "validName", "date": self.date, "notes": "validNote", "visibility": "PU", "exercise_instances": [exercise], "files": []}
        response = self.client.post("/api/workouts/", workout, format="json")

        feedback=response.data["exercise_instances"][0]
        self.assertEqual(str(feedback["exercise"][0]), "Invalid hyperlink - No URL match.")
        self.assertEqual(str(feedback["sets"][0]), "A valid integer is required.")
        self.assertEqual(str(feedback["number"][0]), "A valid integer is required.")