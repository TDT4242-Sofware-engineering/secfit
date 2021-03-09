from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status
from rest_framework.request import Request
from django.test import TestCase
from users.serializers import UserSerializer
from django.contrib.auth import get_user_model
from workouts.models import Workout

# Create your tests here.
# Unit tests

class UserSerializerTestCase(TestCase):
    def setUp(self):
        pass

    def tests_serialize_user_ok(self):
        
        coach = get_user_model().objects.create(
            username="coach", 
            email="email@email.no", 
            phone_number="91919191", 
            country="Norway", 
            city="Trondheim", 
            street_address="Prinsen gate"
        )

        ahtlete = get_user_model().objects.create(
            username="athlete", 
            email="email@email.no", 
            phone_number="91919191", 
            country="Norway", 
            city="Trondheim", 
            street_address="Prinsen gate"
        )

        user = get_user_model().objects.create(
            username="username1", 
            email="email@email.no", 
            phone_number="91919191", 
            country="Norway", 
            city="Trondheim", 
            street_address="Prinsen gate",
            coach=coach
        )
        user.athletes.set([ahtlete])
        user.set_password("password")

        

        workout = Workout.objects.create(
            name="workout",
            owner=user,
            date="2021-03-11T13:37:00Z",
            notes="workoutnote",
            visibility="PU"
        )


        factory = APIRequestFactory()
        request = factory.get('/')

        context = {'request': Request(request)}
        user_serializer = UserSerializer(user, context=context)

        expected = \
            {'url': 'http://testserver/api/users/3/', 
            'id': 3, 
            'email': 'email@email.no', 
            'username': 'username1', 
            'athletes': ['http://testserver/api/users/2/'],
            'phone_number': '91919191', 
            'country': 'Norway', 
            'city': 'Trondheim', 
            'street_address': 
            'Prinsen gate', 
            'coach': 'http://testserver/api/users/1/', 
            'workouts': ['http://testserver/api/workouts/1/'], 
            'coach_files': [], 
            'athlete_files': []}

        self.assertEqual(expected, user_serializer.data)

    # The password field is read only, which results in validating "None"
    # There is no validator enabled, which means that the ValidationError cannot be raised
    def tests_validate_password_ok(self):

        user = get_user_model().objects.create(
            username="username1", 
            email="email@email.no", 
            phone_number="91919191", 
            country="Norway", 
            city="Trondheim", 
            street_address="Prinsen gate",
        )
        user.set_password("thebestpassword")


        factory = APIRequestFactory()
        request = factory.get('/')

        context = {'request': Request(request)}
        user_serializer = UserSerializer(user, context=context)
        self.assertEqual(user_serializer.validate_password(None), None)


# Boundary tests
class UsernameTestCase(APITestCase):

    def test_username_too_short(self):
        tooShortUsername = ""
        user = {"username": tooShortUsername, "email": "valid@email.com", "password": "validPassword", "password1": "validPassword"}
        response = self.client.post('/api/users/', user,  format="json")
        self.assertEqual(str(response.data["username"][0]), "This field may not be blank.")
    
    def test_username_too_long(self):
        tooLongUsername = "x" * 151
        user = {"username": tooLongUsername, "email": "valid@email.com", "password": "validPassword", "password1": "validPassword"}
        response = self.client.post("/api/users/", user, format="json")
        self.assertEqual(str(response.data["username"][0]), "Ensure this field has no more than 150 characters.")

    def test_username_upper_limit(self):
        longUsername = "x" * 150
        user = {"username": longUsername, "email": "valid@email.com", "password": "validPassword", "password1": "validPassword"}
        response = self.client.post("/api/users/", user, format="json")
        self.assertIsNone(response.data.get("username"))

    def test_username_lower_limit(self):
        shortUsername = "x"
        user = {"username": shortUsername, "email": "valid@email.com", "password": "validPassword", "password1": "validPassword"}
        response = self.client.post("/api/users/", user, format="json")
        self.assertIsNone(response.data.get("username"))

    def test_username_valid(self):
        validUsername = "userName"
        user = {"username": validUsername, "email": "valid@email.com", "password": "validPassword", "password1": "validPassword"}
        response = self.client.post("/api/users/", user, format="json")
        self.assertIsNone(response.data.get("username"))

    def test_username_invalid(self):
        invalidUsername = "userName!!"
        user = {"username": invalidUsername, "email": "valid@email.com", "password": "validPassword", "password1": "validPassword"}
        response = self.client.post("/api/users/", user, format="json")
        self.assertEqual(str(response.data["username"][0]), "Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.")
        

class EmailTestCase(APITestCase):

    def test_email_too_short(self):
        tooShortEmail = "x@x.x"
        user = {"username": "validUsername", "email": tooShortEmail, "password": "validPassword", "password1": "validPassword"}
        response = self.client.post('/api/users/', user,  format="json")
        self.assertEqual(str(response.data["email"][0]), "Enter a valid email address.")
    
    def test_email_too_long(self):
        tooLongEmail = ("x" * 250)+"@x.xx"
        user = {"username": "validUsername", "email": tooLongEmail, "password": "validPassword", "password1": "validPassword"}
        response = self.client.post("/api/users/", user, format="json")
        self.assertEqual(str(response.data["email"][0]), "Ensure this field has no more than 254 characters.")

    def test_email_upper_limit(self):
        longEmail = ("x" * 249)+"@x.xx"
        user = {"username": "validUsername", "email": longEmail, "password": "validPassword", "password1": "validPassword"}
        response = self.client.post("/api/users/", user, format="json")
        self.assertIsNone(response.data.get("email"))

    def test_email_lower_limit(self):
        shortEmail = "x@x.xx"
        user = {"username": "validUsername", "email": shortEmail, "password": "validPassword", "password1": "validPassword"}
        response = self.client.post("/api/users/", user, format="json")
        self.assertIsNone(response.data.get("email"))

    def test_email_valid(self):
        validEmail = "valid@email.com"
        user = {"username": "validUsername", "email": validEmail, "password": "validPassword", "password1": "validPassword"}
        response = self.client.post("/api/users/", user, format="json")
        self.assertIsNone(response.data.get("email"))

    def test_email_invalid(self):
        invalidEmail = "..@xx.xx"
        user = {"username": "validUsername", "email": invalidEmail, "password": "validPassword", "password1": "validPassword"}
        response = self.client.post("/api/users/", user, format="json")
        self.assertEqual(str(response.data["email"][0]), "Enter a valid email address.")



class PhoneNumberTestCase(APITestCase):
    
    def test_phone_too_long(self):
        tooLongPhone = "x" * 51
        user = {"username": "validUsername", "email": "valid@email.com", "password": "validPassword", "password1": "validPassword", "phone_number": tooLongPhone}
        response = self.client.post("/api/users/", user, format="json")
        self.assertEqual(str(response.data["phone_number"][0]), "Ensure this field has no more than 50 characters.")

    def test_phone_upper_limit(self):
        longPhone = "x" * 50
        user = {"username": "validUsername", "email": "valid@email.com", "password": "validPassword", "password1": "validPassword", "phone_number": longPhone}
        response = self.client.post("/api/users/", user, format="json")
        self.assertIsNone(response.data.get("phone_number"))

    def test_phone_lower_limit(self):
        shortPhone = ""
        user = {"username": "validUsername", "email": "valid@email.com", "password": "validPassword", "password1": "validPassword", "phone_number": shortPhone}
        response = self.client.post("/api/users/", user, format="json")
        self.assertIsNone(response.data.get("phone_number"))

    def test_phone_valid(self):
        validPhone = "12436487"
        user = {"username": "validUsername", "email": "valid@email.com", "password": "validPassword", "password1": "validPassword", "phone_number": validPhone}
        response = self.client.post("/api/users/", user, format="json")
        self.assertIsNone(response.data.get("phone_number"))


class AddressTestCase(APITestCase):

    def test_address_too_long(self):
        tooLongAddress = "x" * 51
        user = {"username": "validUsername", "email": "valid@email.com", "password": "validPassword", "password1": "validPassword", "street_address": tooLongAddress}
        response = self.client.post("/api/users/", user, format="json")
        self.assertEqual(str(response.data["street_address"][0]), "Ensure this field has no more than 50 characters.")

    def test_address_upper_limit(self):
        longAddress = "x" * 50
        user = {"username": "validUsername", "email": "valid@email.com", "password": "validPassword", "password1": "validPassword", "street_address": longAddress}
        response = self.client.post("/api/users/", user, format="json")
        self.assertIsNone(response.data.get("street_address"))

    def test_address_lower_limit(self):
        shortAddress = ""
        user = {"username": "validUsername", "email": "valid@email.com", "password": "validPassword", "password1": "validPassword", "street_address": shortAddress}
        response = self.client.post("/api/users/", user, format="json")
        self.assertIsNone(response.data.get("street_address"))

    def test_address_valid(self):
        validAddress = "Munkegata 34"
        user = {"username": "validUsername", "email": "valid@email.com", "password": "validPassword", "password1": "validPassword", "street_address": validAddress}
        response = self.client.post("/api/users/", user, format="json")
        self.assertIsNone(response.data.get("street_address"))




class CountryTestCase(APITestCase):

    
    def test_country_too_long(self):
        tooLongCountry = "x" * 51
        user = {"username": "validUsername", "email": "valid@email.com", "password": "validPassword", "password1": "validPassword", "country": tooLongCountry}
        response = self.client.post("/api/users/", user, format="json")
        self.assertEqual(str(response.data["country"][0]), "Ensure this field has no more than 50 characters.")

    def test_country_upper_limit(self):
        longCountry = "x" * 50
        user = {"username": "validUsername", "email": "valid@email.com", "password": "validPassword", "password1": "validPassword", "country": longCountry}
        response = self.client.post("/api/users/", user, format="json")
        self.assertIsNone(response.data.get("country"))

    def test_country_lower_limit(self):
        shortCountry = ""
        user = {"username": "validUsername", "email": "valid@email.com", "password": "validPassword", "password1": "validPassword", "country": shortCountry}
        response = self.client.post("/api/users/", user, format="json")
        self.assertIsNone(response.data.get("country"))

    def test_country_valid(self):
        validCountry = "Munkegata 34"
        user = {"username": "validUsername", "email": "valid@email.com", "password": "validPassword", "password1": "validPassword", "country": validCountry}
        response = self.client.post("/api/users/", user, format="json")
        self.assertIsNone(response.data.get("country"))


class CityTestCase(APITestCase):

    
    def test_city_too_long(self):
        tooLongCity = "x" * 51
        user = {"username": "validUsername", "email": "valid@email.com", "password": "validPassword", "password1": "validPassword", "city": tooLongCity}
        response = self.client.post("/api/users/", user, format="json")
        self.assertEqual(str(response.data["city"][0]), "Ensure this field has no more than 50 characters.")

    def test_city_upper_limit(self):
        longCity = "x" * 50
        user = {"username": "validUsername", "email": "valid@email.com", "password": "validPassword", "password1": "validPassword", "city": longCity}
        response = self.client.post("/api/users/", user, format="json")
        self.assertIsNone(response.data.get("city"))

    def test_city_lower_limit(self):
        shortCity = ""
        user = {"username": "validUsername", "email": "valid@email.com", "password": "validPassword", "password1": "validPassword", "city": shortCity}
        response = self.client.post("/api/users/", user, format="json")
        self.assertIsNone(response.data.get("city"))

    def test_city_valid(self):
        validCity = "Oslo"
        user = {"username": "validUsername", "email": "valid@email.com", "password": "validPassword", "password1": "validPassword", "city": validCity}
        response = self.client.post("/api/users/", user, format="json")
        self.assertIsNone(response.data.get("city"))