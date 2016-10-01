import unittest
from decimal import Decimal

from fbacalculator import fbacalculator as fba


class FBACalculatorTests(unittest.TestCase):
    """ Test the FBA Calulator functions to make sure they return the expected responses """

    def test_get_30_day(self):
        """ Make sure the correct amount is returned from get_30_day """
        # Test standard sized
        self.assertEqual(fba.get_30_day("Standard", 2), Decimal('1.1050'))
        # Test oversized
        self.assertEqual(fba.get_30_day("Oversize", 30), Decimal("12.9750"))

    def test_get_standard_or_oversize(self):
        """ Make sure the correct size is returned """
        self.assertEqual("Standard", fba.get_standard_or_oversize(1, 1, 1, 1))
        # Test weight > 20
        self.assertEqual("Oversize", fba.get_standard_or_oversize(1, 1, 1, 21))
        # Test max > 18
        self.assertEqual("Oversize", fba.get_standard_or_oversize(19, 1, 1, 1))
        self.assertEqual("Oversize", fba.get_standard_or_oversize(1, 19, 1, 1))
        self.assertEqual("Oversize", fba.get_standard_or_oversize(1, 1, 19, 1))

        # Test min > 8
        self.assertEqual("Oversize", fba.get_standard_or_oversize(9, 10, 10, 1))
        self.assertEqual("Oversize", fba.get_standard_or_oversize(10, 9, 10, 1))
        self.assertEqual("Oversize", fba.get_standard_or_oversize(10, 10, 9, 1))

        # Test median > 14
        self.assertEqual("Oversize", fba.get_standard_or_oversize(1, 15, 19, 1))

    def test_get_dimensional_weight(self):
        """ Make sure get_dimensional_weight returns the expected response """
        self.assertEqual(fba.get_dimensional_weight(20, 20, 20), Decimal("48.19"))

    def test_get_girth_and_length(self):
        """ Make sure get_girth_and_length returns the expected response """
        self.assertEqual(fba.get_girth_and_length(10, 15, 20), Decimal("70.0"))

    def test_get_cubic_foot(self):
        """ Make sure get_cubic_foot returns the expected response """
        self.assertEqual(fba.get_cubic_foot(9, 25, 6), Decimal("0.78125"))

    def test_get_weight_handling(self):
        """ Make sure get_weight_handling returns the expected response """
        # Test SML_STND
        self.assertEqual(fba.get_weight_handling("SML_STND", 0.5), Decimal("0.5"))

        # Test LRG_STND
        self.assertEqual(fba.get_weight_handling("LRG_STND", 0.5), Decimal("0.96"))
        self.assertEqual(fba.get_weight_handling("LRG_STND", 1.5, True), Decimal("1.95"))
        self.assertEqual(fba.get_weight_handling("LRG_STND", 2.5, True), Decimal("2.34"))
        self.assertEqual(fba.get_weight_handling("LRG_STND", 1.5), Decimal("1.95"))
        self.assertEqual(fba.get_weight_handling("LRG_STND", 2.5), Decimal("2.34"))

        # Test SPL_OVER
        self.assertEqual(fba.get_weight_handling("SPL_OVER", 80), Decimal("124.58"))
        self.assertEqual(fba.get_weight_handling("SPL_OVER", 100), Decimal("133.78"))

        # Test LRG_OVER
        self.assertEqual(fba.get_weight_handling("LRG_OVER", 80), Decimal("63.98"))
        self.assertEqual(fba.get_weight_handling("LRG_OVER", 150), Decimal("111.98"))

        # Test MED_OVER
        self.assertEqual(fba.get_weight_handling("MED_OVER", 1.5), Decimal("2.73"))
        self.assertEqual(fba.get_weight_handling("MED_OVER", 2.5), Decimal("3.12"))

        # Test Standard
        self.assertEqual(fba.get_weight_handling("Standard", 1.5), Decimal("2.06"))
        self.assertEqual(fba.get_weight_handling("Standard", 2.5), Decimal("2.45"))

    def test_calculate_fees(self):
        """ Make sure calculate_fees returns the expected response """
        self.assertEqual(
            fba.calculate_fees(5.6, 4.9, 0.4, 0.25, is_media=True), Decimal("2.91")
        )

        self.assertEqual(
            fba.calculate_fees(32, 9, 6, 5.05, is_pro=False),
            Decimal("11.48")
        )


if __name__ == "__main__":
    unittest.main()
