import unittest
from datetime import date
from app.models import Quote, Order


class ModelsTestCase(unittest.TestCase):
    def test_quote_model(self):
        q = Quote(symbol="ibm", price=123.45, timestamp=date.today())
        self.assertEqual(q.symbol, "ibm")
        self.assertEqual(q.price, 123.45)

    def test_order_model_validation(self):
        with self.assertRaises(ValueError):
            # negative quantity should fail
            Order(id=1, symbol="NFLX", quantity=-1, side="buy", price=100)


if __name__ == "__main__":
    unittest.main()
