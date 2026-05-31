import math
import unittest

from src.universe.relativity import (
    SPEED_OF_LIGHT_M_S,
    lorentz_factor,
    lorentz_factor_from_velocity,
)


class RelativityTests(unittest.TestCase):
    def test_lorentz_factor_at_zero_speed_is_one(self) -> None:
        self.assertEqual(lorentz_factor(0.0), 1.0)

    def test_lorentz_factor_for_planetary_speed_is_close_to_one(self) -> None:
        gamma = lorentz_factor(30_000.0)
        self.assertGreaterEqual(gamma, 1.0)
        self.assertLess(gamma, 1.00000001)

    def test_lorentz_factor_increases_with_speed(self) -> None:
        low = lorentz_factor(1_000.0)
        high = lorentz_factor(100_000.0)
        self.assertGreater(high, low)

    def test_lorentz_factor_near_speed_of_light_is_greater_than_one(self) -> None:
        gamma = lorentz_factor(0.99 * SPEED_OF_LIGHT_M_S)
        self.assertGreater(gamma, 1.0)

    def test_lorentz_factor_returns_inf_for_speed_at_or_above_c(self) -> None:
        self.assertEqual(lorentz_factor(SPEED_OF_LIGHT_M_S), math.inf)
        self.assertEqual(lorentz_factor(SPEED_OF_LIGHT_M_S * 1.01), math.inf)

    def test_lorentz_factor_rejects_negative_speed(self) -> None:
        with self.assertRaises(ValueError):
            lorentz_factor(-1.0)

    def test_lorentz_factor_from_velocity_uses_vector_speed(self) -> None:
        gamma_from_velocity = lorentz_factor_from_velocity(3.0, 4.0)
        gamma_from_speed = lorentz_factor(5.0)
        self.assertAlmostEqual(gamma_from_velocity, gamma_from_speed)
