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
        token_dealer = os.environ.get('TOKEN_DEALER','eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ikh6MzRpZzNDMjB2TDdvR09tc1RoNiJ9.eyJpc3MiOiJodHRwczovL3BodWNuZ3V5ZW4udXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDY0YjcyMThjM2RkNGZhNTQ1Nzk4YWNiYiIsImF1ZCI6InBodWMiLCJpYXQiOjE2OTAwMDI0MTEsImV4cCI6MTY5MDA4ODgxMSwiYXpwIjoiSjgwNFR1bWd0RVBKOVNyME1ZNm9wV0l1M1NtZ1JPTTkiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDp2ZWhpY2xlcyIsInBhdGNoOnZlaGljbGVzIiwicG9zdDp2ZWhpY2xlcyJdfQ.W3OIJ1vbTxJl4gphi4EMcl-ex8mXhqs6-0TjyD9k7bXrd5yQNoCPDs8tkUAmw7wKcXfVL5peVSlp3RWEWJDD7qvR9z_RcAvqZMRiFgeydYyjFrHEu6g0C9NW6l8TMg3URtVz3Oi1rXlJbsfmiLM5ZhzSMXeugjxtwZPojGCjb_ZHfAr42yHs7ZsJuDvErcJAejzIZLX0qPM_9YDbU1WgN5xdfVbLcor73HM9VfSUuvhttQCHQpHvwkQyDVVvghawU7Er2xydfmDSx5s24DefzCcKLK5etrguTNnZEnNmE6FX3Lx42-XikwrD5Ay4SLlu6bpIgC71C2Qcckqh4A_JbA')
        token_dealer_manager = os.environ.get('TOKEN_DEALER_MANAGER', 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ikh6MzRpZzNDMjB2TDdvR09tc1RoNiJ9.eyJpc3MiOiJodHRwczovL3BodWNuZ3V5ZW4udXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDY0YjczMmMxZmE2NGU3ZjIwZTYxMTZmMyIsImF1ZCI6InBodWMiLCJpYXQiOjE2OTAwMDI4MjUsImV4cCI6MTY5MDA4OTIyNSwiYXpwIjoiSjgwNFR1bWd0RVBKOVNyME1ZNm9wV0l1M1NtZ1JPTTkiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTp2ZWhpY2xlcyIsImdldDp2ZWhpY2xlcyIsInBhdGNoOnZlaGljbGVzIiwicG9zdDp2ZWhpY2xlcyJdfQ.UXp0DnG1y3yG8e9mIfpv4u3EzgSwx9J6niAA5yQqeNSnS9Pa0k9vinZUen6KuY09ACzbCn5wfjK883HwBh2tUMtwwKaYDtq-NYXiBJ454HwsjALIAQ4fIBd_fNrLfzRSo7jmhlH--wWRZJQfhdrAhCQY6MVCtUkY26I-EuamyLTSDdEbzGbwMKs7eTjY4L0IxZjeHoR6ylMAj_Z8xS8AUzrL2vFUAisen__8H_aiD9KPCMHdH2q7_0HSmwqZt5Hv7JXcOleryBgvunoq4xl_Tu3SNJJttm-1oP8TrkDGXSzMXxUXcK9YaYL3SE2H4ZrwKD8dKf4lM8nwqIoZH5M-NA')
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