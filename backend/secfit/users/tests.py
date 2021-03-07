from django.test import TestCase
from users.serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from rest_framework.request import Request
from workouts.models import Workout

# Create your tests here.


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