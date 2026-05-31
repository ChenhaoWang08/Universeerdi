import unittest

from src.universe.demo_simulation import create_controlled_demo_state
from src.universe.solar_mass_experiment import (
    SolarMassExperimentState,
    decrease_solar_mass_multiplier,
    increase_solar_mass_multiplier,
    reset_solar_mass_multiplier,
    solar_mass_experiment_status_text,
)


class SolarMassExperimentTests(unittest.TestCase):
    def test_default_multiplier_is_one(self) -> None:
        state = SolarMassExperimentState()
        self.assertEqual(state.solar_mass_multiplier, 1.0)

    def test_increase_multiplier_is_bounded_by_max(self) -> None:
        state = SolarMassExperimentState(solar_mass_multiplier=50.0)
        next_state = increase_solar_mass_multiplier(state)
        self.assertEqual(next_state.solar_mass_multiplier, 50.0)

    def test_decrease_multiplier_is_bounded_by_min(self) -> None:
        state = SolarMassExperimentState(solar_mass_multiplier=1.0)
        next_state = decrease_solar_mass_multiplier(state)
        self.assertEqual(next_state.solar_mass_multiplier, 1.0)

    def test_reset_multiplier_returns_to_one(self) -> None:
        state = SolarMassExperimentState(solar_mass_multiplier=7.0)
        next_state = reset_solar_mass_multiplier(state)
        self.assertEqual(next_state.solar_mass_multiplier, 1.0)

    def test_status_text_is_deterministic(self) -> None:
        state = SolarMassExperimentState(solar_mass_multiplier=3.0)
        text = solar_mass_experiment_status_text(state, active_body_count=9)
        self.assertEqual(text, "Sun Gravity: x3.0 | Absorb: ON | Bodies: 9")

    def test_state_helpers_do_not_mutate_physics_state(self) -> None:
        demo_state = create_controlled_demo_state()
        before_positions = tuple(body.position_m for body in demo_state.physics_bodies)
        state = SolarMassExperimentState()
        _ = increase_solar_mass_multiplier(state)
        _ = decrease_solar_mass_multiplier(state)
        _ = reset_solar_mass_multiplier(state)
        self.assertEqual(before_positions, tuple(body.position_m for body in demo_state.physics_bodies))
