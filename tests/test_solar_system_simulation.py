import math
import unittest
from unittest.mock import patch

from src.universe.demo_simulation import create_controlled_demo_state
from src.universe.physics import step_bodies
from src.universe.solar_system_data import SOLAR_SYSTEM_BODIES
from src.universe.solar_system_simulation import (
    build_solar_system_body_states,
    create_solar_system_simulation_state,
    solar_system_to_render_bodies,
    step_solar_system_simulation_state,
)


class SolarSystemSimulationTests(unittest.TestCase):
    def test_solar_system_mode_can_be_constructed(self) -> None:
        state = create_solar_system_simulation_state()
        self.assertGreaterEqual(len(state.physics_bodies), 9)

    def test_sun_is_at_origin(self) -> None:
        state = create_solar_system_simulation_state()
        sun = next(body for body in state.physics_bodies if body.name == "Sun")
        self.assertAlmostEqual(sun.position_m.x, 0.0)
        self.assertAlmostEqual(sun.position_m.y, 0.0)

    def test_at_least_eight_planets_exist(self) -> None:
        state = create_solar_system_simulation_state()
        planet_count = sum(1 for body in state.physics_bodies if body.name != "Sun")
        self.assertGreaterEqual(planet_count, 8)

    def test_all_states_have_required_fields(self) -> None:
        state = create_solar_system_simulation_state()
        for body in state.physics_bodies:
            self.assertTrue(body.name)
            self.assertGreater(body.mass_kg, 0.0)
            self.assertTrue(math.isfinite(body.position_m.x))
            self.assertTrue(math.isfinite(body.position_m.y))
            self.assertTrue(math.isfinite(body.velocity_m_s.x))
            self.assertTrue(math.isfinite(body.velocity_m_s.y))

    def test_planet_positions_are_nonzero_meter_scale(self) -> None:
        state = create_solar_system_simulation_state()
        for body in state.physics_bodies:
            if body.name == "Sun":
                continue
            self.assertGreater(body.position_m.x, 1e9)
            self.assertAlmostEqual(body.position_m.y, 0.0)

    def test_planet_velocities_are_finite(self) -> None:
        state = create_solar_system_simulation_state()
        for body in state.physics_bodies:
            if body.name == "Sun":
                continue
            self.assertTrue(math.isfinite(body.velocity_m_s.y))
            self.assertGreater(body.velocity_m_s.y, 0.0)

    def test_builder_does_not_mutate_dataset(self) -> None:
        before = tuple(
            (
                body.name,
                body.mass_kg,
                body.mean_orbital_radius_m,
                body.orbital_period_s,
                body.rotation_period_s,
            )
            for body in SOLAR_SYSTEM_BODIES
        )
        _ = build_solar_system_body_states()
        after = tuple(
            (
                body.name,
                body.mass_kg,
                body.mean_orbital_radius_m,
                body.orbital_period_s,
                body.rotation_period_s,
            )
            for body in SOLAR_SYSTEM_BODIES
        )
        self.assertEqual(before, after)

    def test_step_bodies_can_advance_states(self) -> None:
        state = create_solar_system_simulation_state()
        stepped = step_solar_system_simulation_state(state, dt_seconds=60.0)
        self.assertEqual(len(stepped.physics_bodies), len(state.physics_bodies))
        earth_before = next(body for body in state.physics_bodies if body.name == "Earth")
        earth_after = next(body for body in stepped.physics_bodies if body.name == "Earth")
        self.assertNotEqual(earth_before.position_m, earth_after.position_m)

    def test_step_uses_physics_foundation_step(self) -> None:
        state = create_solar_system_simulation_state()
        with patch(
            "src.universe.solar_system_simulation.step_bodies",
            wraps=step_bodies,
        ) as patched_step:
            _ = step_solar_system_simulation_state(state, dt_seconds=30.0)
        patched_step.assert_called_once()

    def test_render_body_conversion_exists_for_solar_system_states(self) -> None:
        state = create_solar_system_simulation_state()
        render_bodies = solar_system_to_render_bodies(state)
        self.assertEqual(len(render_bodies), len(state.physics_bodies))

    def test_controlled_demo_mode_still_constructs(self) -> None:
        demo_state = create_controlled_demo_state()
        self.assertEqual(len(demo_state.physics_bodies), 3)
