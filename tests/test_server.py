import os
import unittest

from server import app


class WorldCupTravelDealsApiTest(unittest.TestCase):
    def setUp(self):
        os.environ["REQUIRE_PAID_GATEWAY"] = "false"
        self.client = app.test_client()

    def tearDown(self):
        os.environ.pop("REQUIRE_PAID_GATEWAY", None)
        os.environ.pop("PAID_GATEWAY_SECRET", None)
        os.environ.pop("PAID_GATEWAY_SECRETS", None)
        os.environ.pop("PAID_GATEWAY_SECRET_HASHES", None)
        os.environ.pop("TELEGRAM_WEBHOOK_SECRET", None)
        os.environ.pop("META_VERIFY_TOKEN", None)

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
        expected_total = (
            data["baseline"]["flight_per_person"] * 2
            + data["baseline"]["hotel_per_room_night"] * 5
            + data["baseline"]["local_daily_per_person"] * 5 * 2
        )
        self.assertEqual(data["baseline"]["estimated_total"], expected_total)

    def test_deal_search(self):
        response = self.client.get("/deals/search?origin=EZE&city=los-angeles&travelers=2&nights=6")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data["results"]), 3)
        self.assertIn("deal_score", data["results"][0])
        self.assertFalse(data["results"][0]["is_live_offer"])
        self.assertFalse(data["inventory_disclosure"]["contains_live_fares"])

    def test_score(self):
        response = self.client.get("/score?price=900&baseline=1200&safety=official")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertGreater(data["deal_score"]["score"], 70)

    def test_invalid_dates_and_numbers_return_400(self):
        self.assertEqual(
            self.client.get("/deals/search?start=2026-06-20&end=2026-06-19").status_code,
            400,
        )
        self.assertEqual(self.client.get("/score?price=nan&baseline=1200").status_code, 400)
        self.assertEqual(self.client.get("/score?price=900&baseline=1200&safety=unsafe").status_code, 400)

    def test_paid_gateway_fails_closed_by_default(self):
        os.environ.pop("REQUIRE_PAID_GATEWAY", None)
        os.environ.pop("PAID_GATEWAY_SECRET", None)
        os.environ["PAID_GATEWAY_SECRET_HASHES"] = ""
        self.assertEqual(self.client.get("/health").status_code, 200)
        self.assertEqual(self.client.get("/cities").status_code, 503)

    def test_paid_gateway_blocks_product_data_but_keeps_health_public(self):
        os.environ["REQUIRE_PAID_GATEWAY"] = "true"
        os.environ["PAID_GATEWAY_SECRETS"] = "rapidapi-secret,other-market-secret"
        os.environ["PAID_GATEWAY_SECRET_HASHES"] = (
            "4e598f5daafc2fda61641ddbb5956deb23fde6616366dc9dd5a7c9f47da4d787"
        )

        self.assertEqual(self.client.get("/health").status_code, 200)
        self.assertEqual(self.client.get("/cities").status_code, 402)
        self.assertEqual(
            self.client.get("/cities", headers={"X-API-Gateway-Secret": "other-market-secret"}).status_code,
            200,
        )
        self.assertEqual(
            self.client.get("/cities", headers={"X-API-Gateway-Secret": "hashed-secret"}).status_code,
            200,
        )

    def test_omnireply_health_and_openapi_are_public(self):
        os.environ["REQUIRE_PAID_GATEWAY"] = "true"

        health = self.client.get("/omni/health")
        self.assertEqual(health.status_code, 200)
        self.assertEqual(health.get_json()["api"], "OmniReplyAIAPI")
        self.assertIn("whatsapp", health.get_json()["channels"])

        schema = self.client.get("/omni/openapi.json")
        self.assertEqual(schema.status_code, 200)
        self.assertEqual(schema.get_json()["info"]["title"], "OmniReplyAIAPI")

    def test_omnireply_paid_gateway_blocks_and_accepts_secret(self):
        os.environ["REQUIRE_PAID_GATEWAY"] = "true"
        os.environ["PAID_GATEWAY_SECRETS"] = "rapidapi-secret"
        os.environ["PAID_GATEWAY_SECRET_HASHES"] = ""

        blocked = self.client.post("/omni/reply", json={"message": "hello"})
        self.assertEqual(blocked.status_code, 402)

        allowed = self.client.post(
            "/omni/reply",
            headers={"X-OmniReplyAI-Secret": "rapidapi-secret"},
            json={"message": "hello", "business": {"business_name": "Demo Shop"}},
        )
        self.assertEqual(allowed.status_code, 200)
        self.assertIn("Demo Shop", allowed.get_json()["reply"])

    def test_omnireply_generates_spanish_pricing_reply(self):
        response = self.client.post(
            "/omni/reply",
            json={
                "channel": "whatsapp",
                "message": "Hola, cuanto cuesta el servicio?",
                "business": {
                    "business_name": "Clinica Norte",
                    "pricing_note": "Los planes empiezan en USD 19 por mes.",
                },
            },
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["locale"], "es")
        self.assertEqual(data["intent"], "pricing")
        self.assertIn("USD 19", data["reply"])
        self.assertFalse(data["escalation_required"])

    def test_omnireply_complaint_escalates(self):
        response = self.client.post(
            "/omni/reply",
            json={"message": "Estoy muy molesto, parece una estafa y quiero hablar con un humano"},
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["sentiment"], "negative")
        self.assertTrue(data["escalation_required"])
        self.assertEqual(data["recommended_action"], "human_handoff")

    def test_omnireply_batch_and_webhook_normalizers(self):
        batch = self.client.post(
            "/omni/batch/reply",
            json={
                "business": {"business_name": "Demo"},
                "messages": [
                    {"message": "hello", "channel": "webchat"},
                    {"message": "Necesito agendar un turno", "channel": "telegram"},
                ],
            },
        )
        self.assertEqual(batch.status_code, 200)
        self.assertEqual(batch.get_json()["count"], 2)
        self.assertEqual(batch.get_json()["results"][1]["intent"], "appointment")

        os.environ["TELEGRAM_WEBHOOK_SECRET"] = "telegram-secret"
        telegram = self.client.post(
            "/omni/webhooks/telegram/demo?telegram_inline_method=true",
            headers={"X-Telegram-Bot-Api-Secret-Token": "telegram-secret"},
            json={
                "update_id": 123,
                "message": {
                    "message_id": 44,
                    "text": "Hello, what are your hours?",
                    "from": {"id": 5, "language_code": "en", "username": "buyer"},
                    "chat": {"id": 99},
                },
            },
        )
        self.assertEqual(telegram.status_code, 200)
        self.assertEqual(telegram.get_json()["telegram_method"]["method"], "sendMessage")

        os.environ["META_VERIFY_TOKEN"] = "meta-secret"
        verify = self.client.get(
            "/omni/webhooks/meta/demo?hub.mode=subscribe&hub.verify_token=meta-secret&hub.challenge=abc123"
        )
        self.assertEqual(verify.status_code, 200)
        self.assertEqual(verify.text, "abc123")


if __name__ == "__main__":
    unittest.main()
