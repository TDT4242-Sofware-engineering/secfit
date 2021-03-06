from rest_framework.test import APITestCase, force_authenticate, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from datetime import datetime
from users.models import User
from workouts.models import ExerciseInstance, Exercise



# from workouts import views

# view = views.WorkoutDetail.as_view()


# admin ={"username": "admin", "email": "email@valid.com"}


#     self.user = User.objects.create_user(username="tester", email="user1@test.com", password="password1", is_staff=True)

    # def test_x(self):
    #     self.client.force_authenticate(self.user)

    #     url = reverse('customuser-detail', args=(self.user.id,))
    #     data = {'first_name': 'test', 'last_name': 'user'}
    #     response = self.client.put(url, data, format='json')

    #     self.assertEqual(response.status_code, status.HTTP_200_OK)



        # user = get_user_model().objects.get(username="tester")
        # us = get_user_model().objects.filter(username="tester")
        # print(client.force_authenticate(user=user))
        # user = User.objects.get(username="tester") 

        # print(us.values())
   
        # client = APIClient(enforce_csrf_checks=True)

# print(self.accessToken)
        
        # u = User.objects.get(username="tester")
        # self.client.force_authenticate(user)


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
    
    # def test_notes_too_long(self):
    #     date = datetime.utcnow()
    #     tooLongNote= "x" * 100000
    #     workout = {"name": "validName", "date": date, "notes": tooLongNote, "visibility": "PU", "exercise_instances": [], "files": []}
    #     response = self.client.post("/api/workouts/", workout, format="json")
    #     print(response.data)
    #     self.assertEqual(str(response.data["notes"]), "Ensure this field has no more than 100 characters.")

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


class TypeTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="tester", email="test@test.no")
        self.user.set_password("password")
        self.user.save()

        self.accessToken = None

        self.client.login(username="tester", password="password")
        response = self.client.post('/api/token/', {"username": "tester", "password": "password"},  format="json")
        self.accessToken = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.accessToken)
        
        pushups = Exercise.objects.create(name="Push-ups")
        situps = Exercise.objects.create(name="Sit-ups")
        ExerciseInstance.objects.create(pushups)
        ExerciseInstance.objects.create(situps)

        self.exercises = ExerciseInstance.objects.all()
        print(self.exercises)
        
        
    def test_type_too_short(self):
        date = datetime.utcnow()
        tooShortNote= ""
        workout = {"name": "validName", "date": date, "notes": tooShortNote, "visibility": "PU", "exercise_instances": [], "files": []}
        response = self.client.post('/api/workouts/', workout,  format="json")
        self.assertEqual(str(response.data["notes"][0]), "This field may not be blank.")
    
    # def test_type_too_long(self):
    #     date = datetime.utcnow()
    #     tooLongNote= "x" * 100000
    #     workout = {"name": "validName", "date": date, "notes": tooLongNote, "visibility": "PU", "exercise_instances": [], "files": []}
    #     response = self.client.post("/api/workouts/", workout, format="json")
    #     print(response.data)
    #     self.assertEqual(str(response.data["notes"]), "Ensure this field has no more than 100 characters.")

    def test_type_upper_limit(self):
        date = datetime.utcnow()
        longNote= "x" * 1000000
        workout = {"name": "validName", "date": date, "notes":longNote, "visibility": "PU", "exercise_instances": [], "files": []}
        response = self.client.post("/api/workouts/", workout, format="json")
        self.assertEqual(response.data.get("notes"), longNote)

    def test_type_lower_limit(self):
        date = datetime.utcnow()
        shortNote= "x"
        workout = {"name": "validName", "date": date, "notes": shortNote, "visibility": "PU", "exercise_instances": [], "files": []}
        response = self.client.post("/api/workouts/", workout, format="json")
        self.assertEqual(response.data.get("notes"), shortNote)

    def test_type_valid(self):
        date = datetime.utcnow()
        validNote= "validNote"
        workout = {"name": "validName", "date": date, "notes": validNote, "visibility": "PU", "exercise_instances": [], "files": []}
        response = self.client.post("/api/workouts/", workout, format="json")
        self.assertEqual(response.data.get("notes"), validNote)