from django.test import TestCase
from rest_framework.test import APITestCase
from parameterized import parameterized


from users.serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from rest_framework.request import Request
from workouts.models import Workout

# Create your tests here.


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
        self.email = ["valid@email.com", ("q" * 245) + "@email.com", "", "notemailformat"]
        self.password = ["password", "passsswordpasssswordpasssswordpasssswordpassssword", ""]

        # Index in pariwise table
        self.phoneIndex = 0
        self.countryIndex = 1
        self.cityIndex = 2
        self.streetIndex = 3
        self.usernameIndex = 4
        self.emailIndex = 5
        self.passwordIndex = 6

        # Pair-wise testing table, generated with this tool: https://sqamate.com/tools/pairwise
        # Input:
        # phonevalid, phonelong, phoneempty
        # contryvalid, contrylong, contryempty
        # cityvalid, citylong, cityempty
        # streetvalid, streelong, streetempty
        # usernamevalid, usernamelong, usernameempty, usernameillegalchar
        # emailvalid, emaillong, emailshort, emailIllegalformat
        # passwordvalid, passwordlong, passwordshort
        
        # Output from tool
        # phonevalid,   contryvalid,    cityvalid,  streetvalid,    usernamevalid,      emailvalid,         passwordvalid
        # phonelong,    contrylong,     citylong,   streelong,      usernamelong,       emaillong,          passwordvalid
        # phoneempty,   contryempty,    cityempty,  streetempty,    usernameempty,      emailshort,         passwordvalid
        # phoneempty,   contrylong,     cityvalid,  streetempty,    usernameillegalchar,emailIllegalformat, passwordlong
        # phonelong,    contryvalid,    cityempty,  streelong,      usernameillegalchar,emailIllegalformat, passwordshort
        # phonevalid,   contryempty,    citylong,   streetvalid,    usernameillegalchar,emailshort,         passwordshort
        # phonevalid,   contrylong,     cityempty,  streetvalid,    usernameempty,      emaillong,          passwordlong
        # phonelong,    contryempty,    cityvalid,  streelong,      usernamevalid,      emailshort,         passwordlong
        # phoneempty,   contryvalid,    citylong,   streetempty,    usernamelong,       emailvalid,         passwordlong
        # phoneempty,   contryempty,    cityvalid,  streelong,      usernamelong,       emaillong,          passwordshort
        # phonelong,    contrylong,     citylong,   streetempty,    usernamevalid,      emailvalid,         passwordshort
        # phonevalid,   contryvalid,    cityempty,  streelong,      usernameempty,      emailvalid,         passwordshort
        # phonevalid,   contryvalid,    cityempty,  streetempty,    usernamelong,       emailIllegalformat, passwordvalid
        # phonelong,    contryvalid,    citylong,   streetvalid,    usernameempty,      emailIllegalformat, passwordshort
        # phoneempty,   contryvalid,    cityempty,  streetvalid,    usernamevalid,      emaillong,          passwordshort
        # phoneempty,   contryempty,    cityvalid,  streetvalid,    usernamelong,       emailIllegalformat, passwordshort
        # phoneempty,   contryvalid,    cityvalid,  streetempty,    usernameempty,      emaillong,          passwordshort
        # phoneempty,   contryvalid,    cityvalid,  streetempty,    usernameillegalchar,emaillong,          passwordvalid
        # phoneempty,   contryvalid,    cityvalid,  streetempty,    usernamelong,       emailshort,         passwordshort
        # phoneempty,   contryempty,    cityvalid,  streetempty,    usernameillegalchar,emailvalid,         passwordshort
        # phoneempty,   contrylong,     cityvalid,  streetempty,    usernamevalid,      emailIllegalformat, passwordshort
        # phoneempty,   contrylong,     cityvalid,  streetempty,    usernamelong,       emailshort,         passwordshort
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
    
    
    @parameterized.expand([
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
        
        
        
        response = self.client.post('/api/users/', request_form)
        # print(response.status_code)
        self.assertEqual(response.status_code, self.expected_response[index])
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
