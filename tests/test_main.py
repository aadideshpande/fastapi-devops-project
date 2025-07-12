import unittest
from fastapi.testclient import TestClient
from app.main import app, PORTFOLIO, ORDERS

client = TestClient(app)


class MainTestCase(unittest.TestCase):
    def setUp(self):
        PORTFOLIO.clear()
        ORDERS.clear()

    def test_health(self):
        r = client.get("/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), {"status": "ok"})

    def test_get_quote(self):
        r = client.get("/quote/GOOG")
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(data["symbol"], "GOOG")
        self.assertGreaterEqual(data["price"], 10)

    def test_place_order_buy(self):
        order = {"id": 1, "symbol": "MSFT",
                 "quantity": 5, "side": "buy", "price": 100.0}
        r = client.post("/orders/", json=order)
        self.assertEqual(r.status_code, 200)
        res = r.json()
        self.assertEqual(res["status"], "accepted")
        self.assertEqual(res["order"], order)

    def test_place_order_invalid(self):
        bad = {"id": 2, "symbol": "TSLA",
               "quantity": 0, "side": "buy", "price": -5}
        r = client.post("/orders/", json=bad)
        self.assertEqual(r.status_code, 422)

    def test_portfolio_updates(self):
        buy1 = {"id": 3, "symbol": "AAPL",
                "quantity": 2, "side": "buy", "price": 50.0}
        buy2 = {"id": 4, "symbol": "AAPL",
                "quantity": 3, "side": "buy", "price": 70.0}
        client.post("/orders/", json=buy1)
        client.post("/orders/", json=buy2)

        r = client.get("/portfolio/")
        self.assertEqual(r.status_code, 200)
        pf = r.json()
        self.assertEqual(len(pf), 1)
        self.assertEqual(pf[0]["symbol"], "AAPL")
        # avg_price = (2*50 + 3*70) / 5 = 62.0
        self.assertAlmostEqual(pf[0]["avg_price"], 62.0, places=6)


if __name__ == "__main__":
    unittest.main()
