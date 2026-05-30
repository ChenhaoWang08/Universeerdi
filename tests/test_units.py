import unittest

from src.universe.units import AU_M, DAY_S, KM_M, YEAR_S, au_to_m, days_to_s, km_to_m, years_to_s


class UnitTests(unittest.TestCase):
    def test_unit_constants_match_expected_si_values(self) -> None:
        self.assertEqual(KM_M, 1000.0)
        self.assertEqual(DAY_S, 86400.0)
        self.assertEqual(YEAR_S, 365.25 * DAY_S)
        self.assertEqual(AU_M, 149_597_870_700.0)

    def test_unit_helpers_convert_to_si(self) -> None:
        self.assertEqual(km_to_m(2.5), 2500.0)
        self.assertEqual(days_to_s(2.0), 172800.0)
        self.assertEqual(years_to_s(1.0), YEAR_S)
        self.assertEqual(au_to_m(1.0), AU_M)
