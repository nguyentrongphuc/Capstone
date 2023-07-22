import os
import unittest
import json
import main

from database.models import db_drop_and_create_all, setup_db, VehicleMake, VehicleModel
class CapstoneTestCase(unittest.TestCase):
    """This class represents the trivia test case"""


    def setUp(self):
        self.app = main.create_app(test_config='config.test')
        self.client = self.app.test_client
        token_dealer = os.environ.get('TOKEN_DEALER','eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ikh6MzRpZzNDMjB2TDdvR09tc1RoNiJ9.eyJpc3MiOiJodHRwczovL3BodWNuZ3V5ZW4udXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDY0YjcyMThjM2RkNGZhNTQ1Nzk4YWNiYiIsImF1ZCI6InBodWMiLCJpYXQiOjE2ODk5NzE3NTksImV4cCI6MTY5MDA1ODE1OSwiYXpwIjoiSjgwNFR1bWd0RVBKOVNyME1ZNm9wV0l1M1NtZ1JPTTkiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDp2ZWhpY2xlcyIsInBhdGNoOnZlaGljbGVzIiwicG9zdDp2ZWhpY2xlcyJdfQ.UHjrQld6PCB_V0yuGyE5x1-RTZRa1PIOmRcs5S5-8fxiHa6WwirqxWxwmHtyX3EdBwcJMQG8auZJCyrvbLLqvcb2zvxF_GSaKr18hRdEPPDXSzy0WCuJjPM7cFqI657RjDlvYm0gDdrKetPUgsLXwQq4IQd8iKe6ja-jhSaVxHdpGsy7LPqrVApPh-6WBiocVkOwj5Kb5t6kAkE_F7lZoBe2Xj8qUNMBQQO72j5yeKiBoXAWY79StL_s-mKlx68Malt9_Fx4AsW-dHRczcTLm2yFZEezxFsQYi7NrkNGkoMBK9TdAZUdSjjhGxAobm7tKMbOGulsrGaDq_KobjC2nA')
        token_dealer_manager = os.environ.get('TOKEN_DEALER_MANAGER', 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ikh6MzRpZzNDMjB2TDdvR09tc1RoNiJ9.eyJpc3MiOiJodHRwczovL3BodWNuZ3V5ZW4udXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDY0YjczMmMxZmE2NGU3ZjIwZTYxMTZmMyIsImF1ZCI6InBodWMiLCJpYXQiOjE2ODk5NzE4NDksImV4cCI6MTY5MDA1ODI0OSwiYXpwIjoiSjgwNFR1bWd0RVBKOVNyME1ZNm9wV0l1M1NtZ1JPTTkiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTp2ZWhpY2xlcyIsImdldDp2ZWhpY2xlcyIsInBhdGNoOnZlaGljbGVzIiwicG9zdDp2ZWhpY2xlcyJdfQ.piONGFPrNQDiXjaF2huDqgOVmQDAav-2xSX5MWXqSEOrNzKH_J55L64hWqTT2U0A3YORtVGsJ3bIMtCNsSYw3k_R06ycjuF078_gm0KRHrn4E_7SG3aZuZr-rS06y70Tssq6TMHwv8s8iKr79m4XrAx8hKMScZz1slzqRZRQK5sqUVD9OZRKXKNc2IiSSrGMlPE7AAJGw-iSMOrtrXkjWq-gNW4CYMRkUWnTTahUz9mWdW69zXUB_2RWMAiXIQzsZ9yy-qMLvDpnPeUEOZFYBJ-HPI01W_OKmycox_WOWsLf6D5iCVvYK5VVt41EkB4ZHKxGeV9r--5AF-W4T9Fl_g')
        self.headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token_dealer_manager}
        self.dealer_headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token_dealer}

    def tearDown(self) -> None:
        db_drop_and_create_all()
        return super().tearDown()

    def test_401_get_makes_unauthorization(self):
        res = self.client().get('/makes')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 401)

    def test_get_makes_authorization(self):
        res = self.client().get('/makes', headers=self.headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["makes"][0]["name"], 'Acura')

    def test_401_get_models_unauthorization(self):
        res = self.client().get('/models')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 401)

    def test_get_models_authorization(self):
        res = self.client().get('/models', headers=self.headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["models"][0]["name"], 'Integra')
        self.assertEqual(data["models"][0]["makeName"], 'Acura')

    def test_search_makes_authorization(self):
        res = self.client().post('/makes/search',
                                headers=self.headers,
                                json={"make_name": "Al"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["makes"][0]["name"], 'Alfa Romeo')

    def test_update_makes_authorization(self):
        res = self.client().patch('/makes/1',
                                headers=self.headers,
                                json={"name": "Acura 2023"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["makes"][0]["name"], 'Acura 2023')

    def test_create_makes_authorization(self):
        res = self.client().post('/makes',
                                headers=self.headers,
                                json={"name": "Honda"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["makes"][2]["name"], 'Honda')

    def test_create_models_authorization(self):
        res = self.client().post('/makes',
                                headers=self.headers,
                                json={"name": "Honda"})
        res = self.client().post('/models/3',
                                headers=self.headers,
                                json={"name": "new Hoda model 2026"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["makes"][2]["models"][0]['name'], 'new Hoda model 2026')
    
    def test_delete_makes_authorization(self):
        res = self.client().post('/makes',
                                headers=self.headers,
                                json={"name": "Honda"})
        res = self.client().delete('/makes/3',
                                headers=self.headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
    
    def test_delete_makes_unauthorization(self):
        res = self.client().post('/makes',
                                headers=self.dealer_headers,
                                json={"name": "Honda"})
        res = self.client().delete('/makes/3',
                                headers=self.dealer_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 403)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()