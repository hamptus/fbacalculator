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
        self.assertEqual(fba.get_weight_handling("LRG_STND", 0.5), Decimal("0.63"))
        self.assertEqual(fba.get_weight_handling("LRG_STND", 1.5, True), Decimal("0.88"))
        self.assertEqual(fba.get_weight_handling("LRG_STND", 2.5, True), Decimal("1.29"))
        self.assertEqual(fba.get_weight_handling("LRG_STND", 1.5), Decimal("1.59"))
        self.assertEqual(fba.get_weight_handling("LRG_STND", 2.5), Decimal("1.98"))

        # Test SPL_OVER
        self.assertEqual(fba.get_weight_handling("SPL_OVER", 80), Decimal("124.58"))
        self.assertEqual(fba.get_weight_handling("SPL_OVER", 100), Decimal("133.78"))

        # Test LRG_OVER
        self.assertEqual(fba.get_weight_handling("LRG_OVER", 80), Decimal("63.09"))
        self.assertEqual(fba.get_weight_handling("LRG_OVER", 150), Decimal("118.29"))

        # Test MED_OVER
        self.assertEqual(fba.get_weight_handling("MED_OVER", 1.5), Decimal("2.23"))
        self.assertEqual(fba.get_weight_handling("MED_OVER", 2.5), Decimal("2.62"))

        # Test Standard
        self.assertEqual(fba.get_weight_handling("Standard", 1.5), Decimal("1.59"))
        self.assertEqual(fba.get_weight_handling("Standard", 2.5), Decimal("1.98"))

    def test_calculate_fees(self):
        """ Make sure calculate_fees returns the expected response """
        self.assertEqual(
            fba.calculate_fees(7.5, 5.2, 1, 0.45, is_media=True), Decimal("1.68")
        )

        self.assertEqual(
            fba.calculate_fees(32.8, 16.5, 7.8, 23.55),
            Decimal("16.45")
        )


if __name__ == "__main__":
    unittest.main()
