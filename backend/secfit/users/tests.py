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
        self.phone_index = 0
        self.country_index = 1
        self.city_index = 2
        self.street_index = 3
        self.username_index = 4
        self.email_index = 5
        self.password_index = 6

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
        request_form = {"username":         self.pairwistable[index][self.username_index], 
                        "email":            self.pairwistable[index][self.email_index], 
                        "password":         self.pairwistable[index][self.password_index], 
                        "password1":        self.pairwistable[index][self.password_index],
                        "phone_number":     self.pairwistable[index][self.phone_index],
                        "country":          self.pairwistable[index][self.country_index],
                        "city":             self.pairwistable[index][self.city_index],
                        "street_address":   self.pairwistable[index][self.street_index]
                    }
        
        
        
        response = self.client.post(USERS_PATH, request_form)
        self.assertEqual(response.status_code, self.expected_response[index])


class UserSerializerTestCase(TestCase):

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

        

        Workout.objects.create(
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
        too_short_username = ""
        user = {"username": too_short_username, "email": DUMMY_EMAIL, "password": "validPassword", "password1": "validPassword"}
        response = self.client.post(USERS_PATH, user,  format="json")
        self.assertEqual(str(response.data["username"][0]), "This field may not be blank.")
    
    def test_username_too_long(self):
        too_long_username = "x" * 151
        user = {"username": too_long_username, "email": DUMMY_EMAIL, "password": "validPassword", "password1": "validPassword"}
        response = self.client.post(USERS_PATH, user, format="json")
        self.assertEqual(str(response.data["username"][0]), "Ensure this field has no more than 150 characters.")

    def test_username_upper_limit(self):
        long_username = "x" * 150
        user = {"username": long_username, "email": DUMMY_EMAIL, "password": "validPassword", "password1": "validPassword"}
        response = self.client.post(USERS_PATH, user, format="json")
        self.assertIsNone(response.data.get("username"))

    def test_username_lower_limit(self):
        short_username = "x"
        user = {"username": short_username, "email": DUMMY_EMAIL, "password": "validPassword", "password1": "validPassword"}
        response = self.client.post(USERS_PATH, user, format="json")
        self.assertIsNone(response.data.get("username"))

    def test_username_valid(self):
        valid_username = "userName"
        user = {"username": valid_username, "email": DUMMY_EMAIL, "password": "validPassword", "password1": "validPassword"}
        response = self.client.post(USERS_PATH, user, format="json")
        self.assertIsNone(response.data.get("username"))

    def test_username_invalid(self):
        invalid_username = "userName!!"
        user = {"username": invalid_username, "email": DUMMY_EMAIL, "password": "validPassword", "password1": "validPassword"}
        response = self.client.post(USERS_PATH, user, format="json")
        self.assertEqual(str(response.data["username"][0]), "Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.")
        

class EmailTestCase(APITestCase):

    def test_email_too_short(self):
        too_short_email = "x@x.x"
        user = {"username": "validUsername", "email": too_short_email, "password": "validPassword", "password1": "validPassword"}
        response = self.client.post(USERS_PATH, user,  format="json")
        self.assertEqual(str(response.data["email"][0]), "Enter a valid email address.")
    
    def test_email_too_long(self):
        too_long_email = ("x" * 250)+"@x.xx"
        user = {"username": "validUsername", "email": too_long_email, "password": "validPassword", "password1": "validPassword"}
        response = self.client.post(USERS_PATH, user, format="json")
        self.assertEqual(str(response.data["email"][0]), "Ensure this field has no more than 254 characters.")

    def test_email_upper_limit(self):
        long_email = ("x" * 249)+"@x.xx"
        user = {"username": "validUsername", "email": long_email, "password": "validPassword", "password1": "validPassword"}
        response = self.client.post(USERS_PATH, user, format="json")
        self.assertIsNone(response.data.get("email"))

    def test_email_lower_limit(self):
        short_email = "x@x.xx"
        user = {"username": "validUsername", "email": short_email, "password": "validPassword", "password1": "validPassword"}
        response = self.client.post(USERS_PATH, user, format="json")
        self.assertIsNone(response.data.get("email"))

    def test_email_valid(self):
        valid_email = "valid@email.com"
        user = {"username": "validUsername", "email": valid_email, "password": "validPassword", "password1": "validPassword"}
        response = self.client.post(USERS_PATH, user, format="json")
        self.assertIsNone(response.data.get("email"))

    def test_email_invalid(self):
        invalid_email = "..@xx.xx"
        user = {"username": "validUsername", "email": invalid_email, "password": "validPassword", "password1": "validPassword"}
        response = self.client.post(USERS_PATH, user, format="json")
        self.assertEqual(str(response.data["email"][0]), "Enter a valid email address.")



class PhoneNumberTestCase(APITestCase):
    
    def test_phone_too_long(self):
        too_long_phone = "x" * 51
        user = {"username": "validUsername", "email": DUMMY_EMAIL, "password": "validPassword", "password1": "validPassword", "phone_number": too_long_phone}
        response = self.client.post(USERS_PATH, user, format="json")
        self.assertEqual(str(response.data["phone_number"][0]), "Ensure this field has no more than 50 characters.")

    def test_phone_upper_limit(self):
        long_phone = "x" * 50
        user = {"username": "validUsername", "email": DUMMY_EMAIL, "password": "validPassword", "password1": "validPassword", "phone_number": long_phone}
        response = self.client.post(USERS_PATH, user, format="json")
        self.assertIsNone(response.data.get("phone_number"))

    def test_phone_lower_limit(self):
        short_phone = ""
        user = {"username": "validUsername", "email": DUMMY_EMAIL, "password": "validPassword", "password1": "validPassword", "phone_number": short_phone}
        response = self.client.post(USERS_PATH, user, format="json")
        self.assertIsNone(response.data.get("phone_number"))

    def test_phone_valid(self):
        valid_phone = "12436487"
        user = {"username": "validUsername", "email": DUMMY_EMAIL, "password": "validPassword", "password1": "validPassword", "phone_number": valid_phone}
        response = self.client.post(USERS_PATH, user, format="json")
        self.assertIsNone(response.data.get("phone_number"))


class AddressTestCase(APITestCase):

    def test_address_too_long(self):
        too_long_address = "x" * 51
        user = {"username": "validUsername", "email": DUMMY_EMAIL, "password": "validPassword", "password1": "validPassword", "street_address": too_long_address}
        response = self.client.post(USERS_PATH, user, format="json")
        self.assertEqual(str(response.data["street_address"][0]), "Ensure this field has no more than 50 characters.")

    def test_address_upper_limit(self):
        long_address = "x" * 50
        user = {"username": "validUsername", "email": DUMMY_EMAIL, "password": "validPassword", "password1": "validPassword", "street_address": long_address}
        response = self.client.post(USERS_PATH, user, format="json")
        self.assertIsNone(response.data.get("street_address"))

    def test_address_lower_limit(self):
        short_address = ""
        user = {"username": "validUsername", "email": DUMMY_EMAIL, "password": "validPassword", "password1": "validPassword", "street_address": short_address}
        response = self.client.post(USERS_PATH, user, format="json")
        self.assertIsNone(response.data.get("street_address"))

    def test_address_valid(self):
        valid_address = "Munkegata 34"
        user = {"username": "validUsername", "email": DUMMY_EMAIL, "password": "validPassword", "password1": "validPassword", "street_address": valid_address}
        response = self.client.post(USERS_PATH, user, format="json")
        self.assertIsNone(response.data.get("street_address"))




class CountryTestCase(APITestCase):

    
    def test_country_too_long(self):
        too_long_country = "x" * 51
        user = {"username": "validUsername", "email": DUMMY_EMAIL, "password": "validPassword", "password1": "validPassword", "country": too_long_country}
        response = self.client.post(USERS_PATH, user, format="json")
        self.assertEqual(str(response.data["country"][0]), "Ensure this field has no more than 50 characters.")

    def test_country_upper_limit(self):
        long_country = "x" * 50
        user = {"username": "validUsername", "email": DUMMY_EMAIL, "password": "validPassword", "password1": "validPassword", "country": long_country}
        response = self.client.post(USERS_PATH, user, format="json")
        self.assertIsNone(response.data.get("country"))

    def test_country_lower_limit(self):
        short_country = ""
        user = {"username": "validUsername", "email": DUMMY_EMAIL, "password": "validPassword", "password1": "validPassword", "country": short_country}
        response = self.client.post(USERS_PATH, user, format="json")
        self.assertIsNone(response.data.get("country"))

    def test_country_valid(self):
        valid_country = "Munkegata 34"
        user = {"username": "validUsername", "email": DUMMY_EMAIL, "password": "validPassword", "password1": "validPassword", "country": valid_country}
        response = self.client.post(USERS_PATH, user, format="json")
        self.assertIsNone(response.data.get("country"))


class CityTestCase(APITestCase):

    
    def test_city_too_long(self):
        too_long_city = "x" * 51
        user = {"username": "validUsername", "email": DUMMY_EMAIL, "password": "validPassword", "password1": "validPassword", "city": too_long_city}
        response = self.client.post(USERS_PATH, user, format="json")
        self.assertEqual(str(response.data["city"][0]), "Ensure this field has no more than 50 characters.")

    def test_city_upper_limit(self):
        long_city = "x" * 50
        user = {"username": "validUsername", "email": DUMMY_EMAIL, "password": "validPassword", "password1": "validPassword", "city": long_city}
        response = self.client.post(USERS_PATH, user, format="json")
        self.assertIsNone(response.data.get("city"))

    def test_city_lower_limit(self):
        short_city = ""
        user = {"username": "validUsername", "email": DUMMY_EMAIL, "password": "validPassword", "password1": "validPassword", "city": short_city}
        response = self.client.post(USERS_PATH, user, format="json")
        self.assertIsNone(response.data.get("city"))

    def test_city_valid(self):
        valid_city = "Oslo"
        user = {"username": "validUsername", "email": DUMMY_EMAIL, "password": "validPassword", "password1": "validPassword", "city": valid_city}
        response = self.client.post(USERS_PATH, user, format="json")
        self.assertIsNone(response.data.get("city"))
