import unittest

from server import app


class WorldCupTravelDealsApiTest(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["host_city_count"], 16)

    def test_city_detail(self):
        response = self.client.get("/cities/miami?origin=EZE&travelers=2&nights=5")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["city"]["slug"], "miami")
        self.assertIn("google_flights", data["search_links"])

    def test_deal_search(self):
        response = self.client.get("/deals/search?origin=EZE&city=los-angeles&travelers=2&nights=6")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data["results"]), 3)
        self.assertIn("deal_score", data["results"][0])

    def test_score(self):
        response = self.client.get("/score?price=900&baseline=1200&safety=official")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertGreater(data["deal_score"]["score"], 70)


if __name__ == "__main__":
    unittest.main()
