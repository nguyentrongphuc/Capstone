import unittest
import json
import main as app

from database.models import db_drop_and_create_all, setup_db, VehicleMake, VehicleModel

class CapstoneTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        self.app = app.create_app()
        self.client = self.app.test_client
        self.headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ikh6MzRpZzNDMjB2TDdvR09tc1RoNiJ9.eyJpc3MiOiJodHRwczovL3BodWNuZ3V5ZW4udXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDY0YjczMmMxZmE2NGU3ZjIwZTYxMTZmMyIsImF1ZCI6InBodWMiLCJpYXQiOjE2ODk3Mjc3NTMsImV4cCI6MTY4OTgxNDE1MywiYXpwIjoiSjgwNFR1bWd0RVBKOVNyME1ZNm9wV0l1M1NtZ1JPTTkiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTp2ZWhpY2xlcyIsImdldDp2ZWhpY2xlcyIsInBhdGNoOnZlaGljbGVzIiwicG9zdDp2ZWhpY2xlcyJdfQ.OtUkaCIA2gAoY6gx-Pyzgwn4JBTE6y_9zJeL9mkJxKy4qWwOXlwqeHBJpSiPUhZQ0UTuGHBNsdlsga2jfbTxiOFC1prwxF-TUdF32_EGP589Xi5EAjbqLBuLtk1jY5TqMdDfnFFpa6v3RLPirhM8NWYdDqZcXKvOMkIwEIOfFtT4R85k2WTp2NqDlKC0NwVwjSA-DzOW_GIpBsrE4OQAvnGXrg-ZqfO2vsGFGiXGqPWUY72tEcSz4xn90_a5oTnUz9px_WeTFGHR8mmxxwoTHQSuqcjxVdQSUdbMoO-WP717vHRMXYe09LhTBBDvhKTnUWwzTlFuSJE0giH02WUw0g'}
        self.dealer_headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ikh6MzRpZzNDMjB2TDdvR09tc1RoNiJ9.eyJpc3MiOiJodHRwczovL3BodWNuZ3V5ZW4udXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDY0YjcyMThjM2RkNGZhNTQ1Nzk4YWNiYiIsImF1ZCI6InBodWMiLCJpYXQiOjE2ODk3MzQ5NDMsImV4cCI6MTY4OTgyMTM0MywiYXpwIjoiSjgwNFR1bWd0RVBKOVNyME1ZNm9wV0l1M1NtZ1JPTTkiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDp2ZWhpY2xlcyIsInBhdGNoOnZlaGljbGVzIiwicG9zdDp2ZWhpY2xlcyJdfQ.TKerPdA9G0jUBEXNzTHGLuNbO8jxtSqdGK2NBev-oacKz54sd4hlxHs980WlNux9Khbh6BQTCn_MVrabc9SE9T9YySqB5eR4A026DE2heIHhVoifKqmFgU15trI1H0dqoy-LRXxhjO79VlQSQvYkKUn6DmLn7PrTkBdLQ2G2bkPUGuL65pwThlRBodDqF3FusP9MJAiCM4zHl9CMnsc-MVBpDzV-rEN2uQHHLbJsrbiy6cTmD71HWLruc8oHKSMf2HtU3Wz0cGeEg2C-pKRvSPSHYy-urCkLIsLQ73NA8D7e6nyMi2pdzrL94suqWy_BRZ44Fkxv6hPDgSNZPEcDxA'}


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