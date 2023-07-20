import unittest
import json
import main

from database.models import db_drop_and_create_all, setup_db, VehicleMake, VehicleModel

class CapstoneTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        self.app = main.create_app(test_config='config.test')
        self.client = self.app.test_client
        self.headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ikh6MzRpZzNDMjB2TDdvR09tc1RoNiJ9.eyJpc3MiOiJodHRwczovL3BodWNuZ3V5ZW4udXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDY0YjczMmMxZmE2NGU3ZjIwZTYxMTZmMyIsImF1ZCI6InBodWMiLCJpYXQiOjE2ODk4NzI4ODEsImV4cCI6MTY4OTk1OTI4MSwiYXpwIjoiSjgwNFR1bWd0RVBKOVNyME1ZNm9wV0l1M1NtZ1JPTTkiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTp2ZWhpY2xlcyIsImdldDp2ZWhpY2xlcyIsInBhdGNoOnZlaGljbGVzIiwicG9zdDp2ZWhpY2xlcyJdfQ.ADjf7aa-qk93NPJYV_zkHutuhLfCcdsW3PYkIFx0304iwDoS7cBT3QzKwCHoAVm-hnipIcuLHM3KO2Q4EGFsKsEdsxpsJxdHBibYrWoX8dpxPgh4oKpMxGMDkhqBbkt_dOqxBvfkdxdAHiYWKHe9-zhY3CV8qGKFgW7ZA8XOnKIXKD3zQqgC371iAe2y5W9VaL_BGas5GyuiCdLLwSE8Xxah0hHLSAEHiaFWES-b9_8sVZdYtvanrkJoaRhw1LuhiE6lsBO2G30DWlh9PhvOxoeUVmLUGmLfclftdres9rbn-0MSHuTaPObevL57CUK4CKoU5Qzcrm2tVL8GxFVZxg'}
        self.dealer_headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ikh6MzRpZzNDMjB2TDdvR09tc1RoNiJ9.eyJpc3MiOiJodHRwczovL3BodWNuZ3V5ZW4udXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDY0YjcyMThjM2RkNGZhNTQ1Nzk4YWNiYiIsImF1ZCI6InBodWMiLCJpYXQiOjE2ODk4NzI3NTksImV4cCI6MTY4OTk1OTE1OSwiYXpwIjoiSjgwNFR1bWd0RVBKOVNyME1ZNm9wV0l1M1NtZ1JPTTkiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDp2ZWhpY2xlcyIsInBhdGNoOnZlaGljbGVzIiwicG9zdDp2ZWhpY2xlcyJdfQ.SHkIqRqMOcEtJ8cUzFIrVsTsLZ8GxT5DaIO661PzGsP1PjfjpAd1dWEsARApyQWglzBoRrhN7TA64lI_XNHP5wdfl2er45Bk6vO6AKWJ4OEbs-jU_I7KC3IwZNsTgaUnEH3Esz1V4qoaRg2MAqfwo3XoZlL0AmMW6NEJYFUB-9Qi8mECm8f-u6sPC8nGdIGShC3JHu-Y_xTUumtmDXkHErHMUzoqUDyc8-dkbob_lg53QupDStia9kANOvpEzvoq9sMC_BGFOBKrKM5zCtyHxqJ1BT_CM5oDNAnOBaXafA6tdJFnZo7Eu6BVKtNTo4WJTBn7UbYL7IFu1b_x8I2m_w'}

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