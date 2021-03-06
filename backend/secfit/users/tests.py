from rest_framework.test import APITestCase
from rest_framework import status

# Create your tests here.
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
