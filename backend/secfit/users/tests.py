from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status
from rest_framework.request import Request
from django.test import TestCase
from rest_framework.test import APITestCase
from parameterized import parameterized


from users.serializers import UserSerializer
from django.contrib.auth import get_user_model
from workouts.models import Workout

# Global constants
USERS_PATH = "/api/users/"

# Dummy data
DUMMY_EMAIL = "valid@email.com"
DUMMY_STREET = "Prinsen gate"


# Pair-wise testing
class RegisterTestCase(APITestCase):
    def setUp(self):
        # Initializing test data
        # Indexes used to choose the different values in the variables
        self.valid = 0
        self.long = 1
        self.empty = 2
        self.illegal = 3

        # Variable values: valid, long, empty
        self.phone = ["12341234", "123456789112345678911234567891123456789112345678911", ""]
        self.country = ["Norway", "NorwayyyyyNorwayyyyyNorwayyyyyNorwayyyyyNorwayyyyyQ", ""]
        self.city = ["Trondheim", "TrondheimeTrondheimeTrondheimeTrondheimeTrondheimeQ", ""]
        self.street = ["Street", "StreeeeeetStreeeeeetStreeeeeetStreeeeeetStreeeeeetQ", ""]
        self.username = ["username", "x" * 151, "", "illegal!"]
        self.email = [DUMMY_EMAIL, ("q" * 245) + "@email.com", "", "notemailformat"]
        self.password = ["password", "passsswordpasssswordpasssswordpasssswordpassssword", ""]

        # Index in pariwise table
        self.phoneIndex = 0
        self.countryIndex = 1
        self.cityIndex = 2
        self.streetIndex = 3
        self.usernameIndex = 4
        self.emailIndex = 5
        self.passwordIndex = 6

        # Initializing the scenarios that will be tested
        self.pairwistable = [
            [self.phone[self.valid],    self.country[self.valid],   self.city[self.valid],  self.street[self.valid],    self.username[self.valid],  self.email[self.valid],  self.password[self.valid]],
            [self.phone[self.long],     self.country[self.long],    self.city[self.long],   self.street[self.long],     self.username[self.long],   self.email[self.long],   self.password[self.valid]],
            [self.phone[self.empty],    self.country[self.empty],   self.city[self.empty],  self.street[self.empty],    self.username[self.empty],  self.email[self.empty],  self.password[self.valid]],
            [self.phone[self.empty],    self.country[self.long],    self.city[self.valid],  self.street[self.empty],    self.username[self.illegal],self.email[self.illegal],self.password[self.long]],
            [self.phone[self.long],     self.country[self.valid],   self.city[self.empty],  self.street[self.long],     self.username[self.illegal],self.email[self.illegal],self.password[self.empty]],
            [self.phone[self.valid],    self.country[self.empty],   self.city[self.long],   self.street[self.valid],    self.username[self.illegal],self.email[self.empty],  self.password[self.empty]],
            [self.phone[self.valid],    self.country[self.long],    self.city[self.empty],  self.street[self.valid],    self.username[self.empty],  self.email[self.long],   self.password[self.long]],
            [self.phone[self.long],     self.country[self.empty],   self.city[self.valid],  self.street[self.long],     self.username[self.valid],  self.email[self.empty],  self.password[self.long]],
            [self.phone[self.empty],    self.country[self.valid],   self.city[self.long],   self.street[self.empty],    self.username[self.long],   self.email[self.valid],  self.password[self.long]],
            [self.phone[self.empty],    self.country[self.empty],   self.city[self.valid],  self.street[self.long],     self.username[self.long],   self.email[self.long],   self.password[self.empty]],
            [self.phone[self.long],     self.country[self.long],    self.city[self.long],   self.street[self.empty],    self.username[self.valid],  self.email[self.valid],  self.password[self.empty]],
            [self.phone[self.valid],    self.country[self.valid],   self.city[self.empty],  self.street[self.long],     self.username[self.empty],  self.email[self.valid],  self.password[self.empty]],
            [self.phone[self.valid],    self.country[self.valid],   self.city[self.empty],  self.street[self.empty],    self.username[self.long],   self.email[self.illegal],self.password[self.valid]],
            [self.phone[self.long],     self.country[self.valid],   self.city[self.long],   self.street[self.valid],    self.username[self.empty],  self.email[self.illegal],self.password[self.empty]],
            [self.phone[self.empty],    self.country[self.valid],   self.city[self.empty],  self.street[self.valid],    self.username[self.valid],  self.email[self.long],   self.password[self.empty]],
            [self.phone[self.empty],    self.country[self.empty],   self.city[self.valid],  self.street[self.valid],    self.username[self.long],   self.email[self.illegal],self.password[self.empty]],
            [self.phone[self.empty],    self.country[self.valid],   self.city[self.valid],  self.street[self.empty],    self.username[self.empty],  self.email[self.long],   self.password[self.empty]],
            [self.phone[self.empty],    self.country[self.valid],   self.city[self.valid],  self.street[self.empty],    self.username[self.illegal],self.email[self.long],   self.password[self.valid]],
            [self.phone[self.empty],    self.country[self.valid],   self.city[self.valid],  self.street[self.empty],    self.username[self.long],   self.email[self.empty],  self.password[self.empty]],
            [self.phone[self.empty],    self.country[self.empty],   self.city[self.valid],  self.street[self.empty],    self.username[self.illegal],self.email[self.valid],  self.password[self.empty]],
            [self.phone[self.empty],    self.country[self.long],    self.city[self.valid],  self.street[self.empty],    self.username[self.valid],  self.email[self.illegal],self.password[self.empty]],
            [self.phone[self.empty],    self.country[self.long],    self.city[self.valid],  self.street[self.empty],    self.username[self.long],   self.email[self.empty],  self.password[self.empty]],
        ]
        
        self.expected_response = [ 201, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400]
    
    
    @parameterized.expand([ # The test runs one time for each tuple
        (0, ),(1, ),(2, ),(3, ),(4, ),(5, ),(6, ),(7, ),(8, ),(9, ),(10, ),(11, ),(12, ),(13, ),(14, ),(15, ),(16, ),(17, ),(18, ),(19, ),(20, ),(21, ),
    ])
    def test_case(self, index):
        request_form = {"username":         self.pairwistable[index][self.usernameIndex], 
                        "email":            self.pairwistable[index][self.emailIndex], 
                        "password":         self.pairwistable[index][self.passwordIndex], 
                        "password1":        self.pairwistable[index][self.passwordIndex],
                        "phone_number":     self.pairwistable[index][self.phoneIndex],
                        "country":          self.pairwistable[index][self.countryIndex],
                        "city":             self.pairwistable[index][self.cityIndex],
                        "street_address":   self.pairwistable[index][self.streetIndex]
                    }
        
        
        
        response = self.client.post(USERS_PATH, request_form)
        self.assertEqual(response.status_code, self.expected_response[index])


class UserSerializerTestCase(TestCase):
    def setUp(self):
        pass

    def tests_serialize_user_ok(self):
        
        coach = get_user_model().objects.create(
            username="coach", 
            email=DUMMY_EMAIL, 
            phone_number="91919191", 
            country="Norway", 
            city="Trondheim", 
            street_address=DUMMY_STREET
        )

        ahtlete = get_user_model().objects.create(
            username="athlete", 
            email=DUMMY_EMAIL, 
            phone_number="91919191", 
            country="Norway", 
            city="Trondheim", 
            street_address=DUMMY_STREET
        )

        user = get_user_model().objects.create(
            username="username1", 
            email=DUMMY_EMAIL, 
            phone_number="91919191", 
            country="Norway", 
            city="Trondheim", 
            street_address=DUMMY_STREET,
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
            'email': DUMMY_EMAIL, 
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
            email=DUMMY_EMAIL, 
            phone_number="91919191", 
            country="Norway", 
            city="Trondheim", 
            street_address=DUMMY_STREET,
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
        user = {"username": tooShortUsername, "email": DUMMY_EMAIL, "password": "validPassword", "password1": "validPassword"}
        response = self.client.post(USERS_PATH, user,  format="json")
        self.assertEqual(str(response.data["username"][0]), "This field may not be blank.")
    
    def test_username_too_long(self):
        tooLongUsername = "x" * 151
        user = {"username": tooLongUsername, "email": DUMMY_EMAIL, "password": "validPassword", "password1": "validPassword"}
        response = self.client.post(USERS_PATH, user, format="json")
        self.assertEqual(str(response.data["username"][0]), "Ensure this field has no more than 150 characters.")

    def test_username_upper_limit(self):
        longUsername = "x" * 150
        user = {"username": longUsername, "email": DUMMY_EMAIL, "password": "validPassword", "password1": "validPassword"}
        response = self.client.post(USERS_PATH, user, format="json")
        self.assertIsNone(response.data.get("username"))

    def test_username_lower_limit(self):
        shortUsername = "x"
        user = {"username": shortUsername, "email": DUMMY_EMAIL, "password": "validPassword", "password1": "validPassword"}
        response = self.client.post(USERS_PATH, user, format="json")
        self.assertIsNone(response.data.get("username"))

    def test_username_valid(self):
        validUsername = "userName"
        user = {"username": validUsername, "email": DUMMY_EMAIL, "password": "validPassword", "password1": "validPassword"}
        response = self.client.post(USERS_PATH, user, format="json")
        self.assertIsNone(response.data.get("username"))

    def test_username_invalid(self):
        invalidUsername = "userName!!"
        user = {"username": invalidUsername, "email": DUMMY_EMAIL, "password": "validPassword", "password1": "validPassword"}
        response = self.client.post(USERS_PATH, user, format="json")
        self.assertEqual(str(response.data["username"][0]), "Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.")
        

class EmailTestCase(APITestCase):

    def test_email_too_short(self):
        tooShortEmail = "x@x.x"
        user = {"username": "validUsername", "email": tooShortEmail, "password": "validPassword", "password1": "validPassword"}
        response = self.client.post(USERS_PATH, user,  format="json")
        self.assertEqual(str(response.data["email"][0]), "Enter a valid email address.")
    
    def test_email_too_long(self):
        tooLongEmail = ("x" * 250)+"@x.xx"
        user = {"username": "validUsername", "email": tooLongEmail, "password": "validPassword", "password1": "validPassword"}
        response = self.client.post(USERS_PATH, user, format="json")
        self.assertEqual(str(response.data["email"][0]), "Ensure this field has no more than 254 characters.")

    def test_email_upper_limit(self):
        longEmail = ("x" * 249)+"@x.xx"
        user = {"username": "validUsername", "email": longEmail, "password": "validPassword", "password1": "validPassword"}
        response = self.client.post(USERS_PATH, user, format="json")
        self.assertIsNone(response.data.get("email"))

    def test_email_lower_limit(self):
        shortEmail = "x@x.xx"
        user = {"username": "validUsername", "email": shortEmail, "password": "validPassword", "password1": "validPassword"}
        response = self.client.post(USERS_PATH, user, format="json")
        self.assertIsNone(response.data.get("email"))

    def test_email_valid(self):
        validEmail = "valid@email.com"
        user = {"username": "validUsername", "email": validEmail, "password": "validPassword", "password1": "validPassword"}
        response = self.client.post(USERS_PATH, user, format="json")
        self.assertIsNone(response.data.get("email"))

    def test_email_invalid(self):
        invalidEmail = "..@xx.xx"
        user = {"username": "validUsername", "email": invalidEmail, "password": "validPassword", "password1": "validPassword"}
        response = self.client.post(USERS_PATH, user, format="json")
        self.assertEqual(str(response.data["email"][0]), "Enter a valid email address.")



class PhoneNumberTestCase(APITestCase):
    
    def test_phone_too_long(self):
        tooLongPhone = "x" * 51
        user = {"username": "validUsername", "email": DUMMY_EMAIL, "password": "validPassword", "password1": "validPassword", "phone_number": tooLongPhone}
        response = self.client.post(USERS_PATH, user, format="json")
        self.assertEqual(str(response.data["phone_number"][0]), "Ensure this field has no more than 50 characters.")

    def test_phone_upper_limit(self):
        longPhone = "x" * 50
        user = {"username": "validUsername", "email": DUMMY_EMAIL, "password": "validPassword", "password1": "validPassword", "phone_number": longPhone}
        response = self.client.post(USERS_PATH, user, format="json")
        self.assertIsNone(response.data.get("phone_number"))

    def test_phone_lower_limit(self):
        shortPhone = ""
        user = {"username": "validUsername", "email": DUMMY_EMAIL, "password": "validPassword", "password1": "validPassword", "phone_number": shortPhone}
        response = self.client.post(USERS_PATH, user, format="json")
        self.assertIsNone(response.data.get("phone_number"))

    def test_phone_valid(self):
        validPhone = "12436487"
        user = {"username": "validUsername", "email": DUMMY_EMAIL, "password": "validPassword", "password1": "validPassword", "phone_number": validPhone}
        response = self.client.post(USERS_PATH, user, format="json")
        self.assertIsNone(response.data.get("phone_number"))


class AddressTestCase(APITestCase):

    def test_address_too_long(self):
        tooLongAddress = "x" * 51
        user = {"username": "validUsername", "email": DUMMY_EMAIL, "password": "validPassword", "password1": "validPassword", "street_address": tooLongAddress}
        response = self.client.post(USERS_PATH, user, format="json")
        self.assertEqual(str(response.data["street_address"][0]), "Ensure this field has no more than 50 characters.")

    def test_address_upper_limit(self):
        longAddress = "x" * 50
        user = {"username": "validUsername", "email": DUMMY_EMAIL, "password": "validPassword", "password1": "validPassword", "street_address": longAddress}
        response = self.client.post(USERS_PATH, user, format="json")
        self.assertIsNone(response.data.get("street_address"))

    def test_address_lower_limit(self):
        shortAddress = ""
        user = {"username": "validUsername", "email": DUMMY_EMAIL, "password": "validPassword", "password1": "validPassword", "street_address": shortAddress}
        response = self.client.post(USERS_PATH, user, format="json")
        self.assertIsNone(response.data.get("street_address"))

    def test_address_valid(self):
        validAddress = "Munkegata 34"
        user = {"username": "validUsername", "email": DUMMY_EMAIL, "password": "validPassword", "password1": "validPassword", "street_address": validAddress}
        response = self.client.post(USERS_PATH, user, format="json")
        self.assertIsNone(response.data.get("street_address"))




class CountryTestCase(APITestCase):

    
    def test_country_too_long(self):
        tooLongCountry = "x" * 51
        user = {"username": "validUsername", "email": DUMMY_EMAIL, "password": "validPassword", "password1": "validPassword", "country": tooLongCountry}
        response = self.client.post(USERS_PATH, user, format="json")
        self.assertEqual(str(response.data["country"][0]), "Ensure this field has no more than 50 characters.")

    def test_country_upper_limit(self):
        longCountry = "x" * 50
        user = {"username": "validUsername", "email": DUMMY_EMAIL, "password": "validPassword", "password1": "validPassword", "country": longCountry}
        response = self.client.post(USERS_PATH, user, format="json")
        self.assertIsNone(response.data.get("country"))

    def test_country_lower_limit(self):
        shortCountry = ""
        user = {"username": "validUsername", "email": DUMMY_EMAIL, "password": "validPassword", "password1": "validPassword", "country": shortCountry}
        response = self.client.post(USERS_PATH, user, format="json")
        self.assertIsNone(response.data.get("country"))

    def test_country_valid(self):
        validCountry = "Munkegata 34"
        user = {"username": "validUsername", "email": DUMMY_EMAIL, "password": "validPassword", "password1": "validPassword", "country": validCountry}
        response = self.client.post(USERS_PATH, user, format="json")
        self.assertIsNone(response.data.get("country"))


class CityTestCase(APITestCase):

    
    def test_city_too_long(self):
        tooLongCity = "x" * 51
        user = {"username": "validUsername", "email": DUMMY_EMAIL, "password": "validPassword", "password1": "validPassword", "city": tooLongCity}
        response = self.client.post(USERS_PATH, user, format="json")
        self.assertEqual(str(response.data["city"][0]), "Ensure this field has no more than 50 characters.")

    def test_city_upper_limit(self):
        longCity = "x" * 50
        user = {"username": "validUsername", "email": DUMMY_EMAIL, "password": "validPassword", "password1": "validPassword", "city": longCity}
        response = self.client.post(USERS_PATH, user, format="json")
        self.assertIsNone(response.data.get("city"))

    def test_city_lower_limit(self):
        shortCity = ""
        user = {"username": "validUsername", "email": DUMMY_EMAIL, "password": "validPassword", "password1": "validPassword", "city": shortCity}
        response = self.client.post(USERS_PATH, user, format="json")
        self.assertIsNone(response.data.get("city"))

    def test_city_valid(self):
        validCity = "Oslo"
        user = {"username": "validUsername", "email": DUMMY_EMAIL, "password": "validPassword", "password1": "validPassword", "city": validCity}
        response = self.client.post(USERS_PATH, user, format="json")
        self.assertIsNone(response.data.get("city"))
