import unittest
import json
import main

from database.models import db_drop_and_create_all, setup_db, VehicleMake, VehicleModel

class CapstoneTestCase(unittest.TestCase):
    """This class represents the trivia test case"""
    def setUp(self):
        self.app = main.create_app(test_config='config.test')
        self.client = self.app.test_client
        self.headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ikh6MzRpZzNDMjB2TDdvR09tc1RoNiJ9.eyJpc3MiOiJodHRwczovL3BodWNuZ3V5ZW4udXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDY0YjczMmMxZmE2NGU3ZjIwZTYxMTZmMyIsImF1ZCI6InBodWMiLCJpYXQiOjE2ODk3Nzk5NTAsImV4cCI6MTY4OTg2NjM1MCwiYXpwIjoiSjgwNFR1bWd0RVBKOVNyME1ZNm9wV0l1M1NtZ1JPTTkiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTp2ZWhpY2xlcyIsImdldDp2ZWhpY2xlcyIsInBhdGNoOnZlaGljbGVzIiwicG9zdDp2ZWhpY2xlcyJdfQ.nq9_xyN7JzFCF6AEkNIQf7g2vhPg17jgmZLqRkUpc3gFKzpaPoh7gN3QX825FG5iV1j4Ahx76besr6R5oJBikhAu5rkQQfBnY3bnvPQFtJcU1xc8Q4nq-JJ2MNxAQjmXW-cvLipSwNrZUyEki0xeuVJxmdJyJ-aIEMCvnSv6cEB898Dv3vmIkELeI3vZUtsYjucdhRT2vsD-Rz-B_dKgagtWT60vBy5pRvaeThGW_JqgTUE-HRHUBocsvqY8cckhqhtD1j6OiDP6TUpF50Mg1Rsc19Un93Y8g09nN1Sg4rdVW8n-jGXMkasxGDxCekWKA-EdTHtCvSEW_a4baFFJNA'}
        self.dealer_headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ikh6MzRpZzNDMjB2TDdvR09tc1RoNiJ9.eyJpc3MiOiJodHRwczovL3BodWNuZ3V5ZW4udXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDY0YjcyMThjM2RkNGZhNTQ1Nzk4YWNiYiIsImF1ZCI6InBodWMiLCJpYXQiOjE2ODk4MTQ5NTIsImV4cCI6MTY4OTkwMTM1MiwiYXpwIjoiSjgwNFR1bWd0RVBKOVNyME1ZNm9wV0l1M1NtZ1JPTTkiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDp2ZWhpY2xlcyIsInBhdGNoOnZlaGljbGVzIiwicG9zdDp2ZWhpY2xlcyJdfQ.pfKj8PSuvReRre3jxRVkaeF3ILIqThl_HDRM5aRoa3OC7fY6ESqyZAUn5S_FmJYUYtytln5mWjZOvN827lFnVjuMg9gudLPhEhpwU9iqAZWYoM22_GadN25NZF0T42GC6wt7_UmiQCaaisBnRNbyG6K_YsVUyS1zLM16-keGkZA2F3e0Nxe-odY6FqIUkIb6A7fxjjaUqAauqUn8xylBLrb9D4MDiDXg14ibSp3i2aRJ9HKiog7yrTX8zSZxSwtdDK_6N0axPhvx_9mP2tAAh5b_9SUeRZFipgl2_i3p7IY3G7QSm2iaAlQ4E9Dy4L73yuAuUkCB3Jc76qGBmgC5_Q'}

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