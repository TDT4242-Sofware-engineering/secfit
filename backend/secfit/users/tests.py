from django.test import TestCase
from rest_framework.test import APITestCase
from parameterized import parameterized



# Create your tests here.


class RegisterTestCase(APITestCase):
    def setUp(self):
        # Initializing test data
        # Indexes used to choose the different values in the variables
        self.valid = 0
        self.long = 1
        self.empty = 2

        # Variable values: valid, long, empty
        self.phone = ["12341234", "123456789112345678911234567891123456789112345678911", ""]
        self.country = ["Norway", "NorwayyyyyNorwayyyyyNorwayyyyyNorwayyyyyNorwayyyyyQ", ""]
        self.city = ["Trondheim", "TrondheimeTrondheimeTrondheimeTrondheimeTrondheimeQ", ""]
        self.street = ["Street", "StreeeeeetStreeeeeetStreeeeeetStreeeeeetStreeeeeetQ", ""]
        self.username = ["username", "uuusernameuuusernameuuusernameuuusernameuuusernameq", ""]
        self.email = ["valid@email.com", "validvalidvalidvalidvalidvalidvalidvalidq@email.com", ""]
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
        # usernamevalid, usernamelong, usernameempty
        # emailvalid, emaillong, emailshort
        # passwordvalid, passwordlong, passwordshort
        
        # Output from tool
        # phonevalid, contryvalid, cityvalid, streetvalid, usernamevalid, emailvalid, passwordvalid
        # phonelong, contrylong, citylong, streelong, usernamelong, emaillong, passwordvalid
        # phoneempty, contryempty, cityempty, streetempty, usernameempty, emailshort, passwordvalid
        # phoneempty, contrylong, cityvalid, streetempty, usernamelong, emailvalid, passwordlong
        # phonelong, contryvalid, cityempty, streelong, usernamevalid, emailshort, passwordlong
        
        # phonevalid, contryempty, citylong, streetvalid, usernameempty, emaillong, passwordlong
        # phonevalid, contrylong, cityempty, streetvalid, usernamelong, emailshort, passwordshort
        # phonelong, contryempty, cityvalid, streelong, usernameempty, emailvalid, passwordshort
        # phoneempty, contryvalid, citylong, streetempty, usernamevalid, emaillong, passwordshort
        # phoneempty, contryvalid, citylong, streelong, usernameempty, emailvalid, passwordshort
        # phonelong, contryempty, cityvalid, streetvalid, usernamelong, emailshort, passwordshort
        # phonevalid, contrylong, cityempty, streelong, usernameempty, emailvalid, passwordshort
        # phonevalid, contrylong, cityempty, streetempty, usernamevalid, emaillong, passwordshort
        # phonelong, contryempty, cityvalid, streetempty, usernamevalid, emaillong, passwordshort
        # phoneempty, contryvalid, citylong, streetvalid, usernamelong, emailshort, passwordshort
        self.pairwistable = [
            [self.phone[self.valid], self.country[self.valid], self.city[self.valid], self.street[self.valid], self.username[self.valid], self.email[self.valid], self.password[self.valid]],
            [self.phone[self.long], self.country[self.long], self.city[self.long], self.street[self.long], self.username[self.long], self.email[self.long], self.password[self.valid]],
            [self.phone[self.empty], self.country[self.empty], self.city[self.empty], self.street[self.empty], self.username[self.empty], self.email[self.empty], self.password[self.valid]],
            [self.phone[self.empty], self.country[self.long], self.city[self.valid], self.street[self.empty], self.username[self.long], self.email[self.valid], self.password[self.long]],
            [self.phone[self.long], self.country[self.valid], self.city[self.empty], self.street[self.long], self.username[self.valid], self.email[self.empty], self.password[self.long]],
        ]
        self.expected_response = [ 201, 400, 400, 400, 400]
    
    
    @parameterized.expand([
        (0, ),
        (1, ),
        (2, ),
        (3, ),
        (4, ),
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
