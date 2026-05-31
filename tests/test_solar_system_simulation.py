import math
import unittest
from unittest.mock import patch

from src.universe.demo_simulation import create_controlled_demo_state
from src.universe.physics import Vector2, step_bodies
from src.universe.render_scale_presets import render_scale_policy_for_preset
from src.universe.solar_system_data import SOLAR_SYSTEM_BODIES
from src.universe.solar_system_simulation import (
    BASELINE_SOLAR_MASS_KG,
    SUN_ABSORPTION_RADIUS_M,
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

    def test_substeps_one_preserves_default_step_behavior(self) -> None:
        state = create_solar_system_simulation_state()
        baseline = step_solar_system_simulation_state(state, dt_seconds=30.0)
        explicit = step_solar_system_simulation_state(
            state,
            dt_seconds=30.0,
            physics_substeps=1,
        )
        self.assertEqual(baseline, explicit)

    def test_step_rejects_invalid_physics_substeps(self) -> None:
        state = create_solar_system_simulation_state()
        with self.assertRaises(ValueError):
            step_solar_system_simulation_state(state, dt_seconds=1.0, physics_substeps=0)

    def test_substeps_split_total_dt_into_multiple_physics_steps(self) -> None:
        state = create_solar_system_simulation_state()
        with patch(
            "src.universe.solar_system_simulation.step_bodies",
            wraps=step_bodies,
        ) as patched_step:
            _ = step_solar_system_simulation_state(
                state,
                dt_seconds=30.0,
                physics_substeps=4,
            )
        self.assertEqual(patched_step.call_count, 4)

    def test_solar_mass_multiplier_changes_runtime_gravity_without_mutating_source_mass(self) -> None:
        state = create_solar_system_simulation_state()
        nominal = step_solar_system_simulation_state(state, dt_seconds=1.0, solar_mass_multiplier=1.0)
        boosted = step_solar_system_simulation_state(state, dt_seconds=1.0, solar_mass_multiplier=20.0)

        earth_nominal = next(body for body in nominal.physics_bodies if body.name == "Earth")
        earth_boosted = next(body for body in boosted.physics_bodies if body.name == "Earth")
        self.assertLess(earth_boosted.velocity_m_s.x, earth_nominal.velocity_m_s.x)

        sun_boosted = next(body for body in boosted.physics_bodies if body.name == "Sun")
        self.assertEqual(sun_boosted.mass_kg, BASELINE_SOLAR_MASS_KG)

    def test_step_rejects_non_positive_solar_mass_multiplier(self) -> None:
        state = create_solar_system_simulation_state()
        with self.assertRaises(ValueError):
            step_solar_system_simulation_state(state, dt_seconds=1.0, solar_mass_multiplier=0.0)

    def test_absorption_removes_non_sun_bodies_inside_solar_radius(self) -> None:
        state = create_solar_system_simulation_state()
        custom_bodies = []
        for body in state.physics_bodies:
            if body.name == "Mercury":
                custom_bodies.append(
                    type(body)(
                        name=body.name,
                        mass_kg=body.mass_kg,
                        position_m=Vector2(SUN_ABSORPTION_RADIUS_M * 0.5, 0.0),
                        velocity_m_s=body.velocity_m_s,
                    )
                )
            else:
                custom_bodies.append(body)
        custom_state = type(state)(physics_bodies=tuple(custom_bodies))
        stepped = step_solar_system_simulation_state(custom_state, dt_seconds=1.0, absorb_into_sun=True)
        names = {body.name for body in stepped.physics_bodies}
        self.assertIn("Sun", names)
        self.assertNotIn("Mercury", names)

    def test_absorption_toggle_can_be_disabled(self) -> None:
        state = create_solar_system_simulation_state()
        custom_bodies = []
        for body in state.physics_bodies:
            if body.name == "Mercury":
                custom_bodies.append(
                    type(body)(
                        name=body.name,
                        mass_kg=body.mass_kg,
                        position_m=Vector2(SUN_ABSORPTION_RADIUS_M * 0.5, 0.0),
                        velocity_m_s=body.velocity_m_s,
                    )
                )
            else:
                custom_bodies.append(body)
        custom_state = type(state)(physics_bodies=tuple(custom_bodies))
        stepped = step_solar_system_simulation_state(custom_state, dt_seconds=1.0, absorb_into_sun=False)
        names = {body.name for body in stepped.physics_bodies}
        self.assertIn("Mercury", names)

    def test_absorption_is_applied_after_each_substep(self) -> None:
        state = create_solar_system_simulation_state()
        with patch(
            "src.universe.solar_system_simulation._apply_solar_absorption",
            wraps=lambda bodies: bodies,
        ) as patched_absorb:
            _ = step_solar_system_simulation_state(
                state,
                dt_seconds=1.0,
                absorb_into_sun=True,
                physics_substeps=8,
            )
        self.assertEqual(patched_absorb.call_count, 8)

    def test_body_entering_solar_radius_in_early_substep_is_removed(self) -> None:
        state = create_solar_system_simulation_state()
        sun = next(body for body in state.physics_bodies if body.name == "Sun")
        mercury = next(body for body in state.physics_bodies if body.name == "Mercury")
        outside = type(mercury)(
            name=mercury.name,
            mass_kg=mercury.mass_kg,
            position_m=Vector2(SUN_ABSORPTION_RADIUS_M * 2.0, 0.0),
            velocity_m_s=mercury.velocity_m_s,
        )
        inside = type(mercury)(
            name=mercury.name,
            mass_kg=mercury.mass_kg,
            position_m=Vector2(SUN_ABSORPTION_RADIUS_M * 0.25, 0.0),
            velocity_m_s=mercury.velocity_m_s,
        )
        custom_state = type(state)(physics_bodies=(sun, outside))

        call_index = {"value": 0}

        def fake_step_bodies(bodies, dt_seconds, epsilon_m=1e-3):  # noqa: ANN001
            _ = dt_seconds
            _ = epsilon_m
            call_index["value"] += 1
            if call_index["value"] == 1:
                return (sun, inside)
            return tuple(bodies)

        with patch(
            "src.universe.solar_system_simulation.step_bodies",
            side_effect=fake_step_bodies,
        ):
            stepped = step_solar_system_simulation_state(
                custom_state,
                dt_seconds=10.0,
                absorb_into_sun=True,
                physics_substeps=2,
            )

        names = {body.name for body in stepped.physics_bodies}
        self.assertIn("Sun", names)
        self.assertNotIn("Mercury", names)

    def test_render_body_conversion_exists_for_solar_system_states(self) -> None:
        state = create_solar_system_simulation_state()
        render_bodies = solar_system_to_render_bodies(state)
        self.assertEqual(len(render_bodies), len(state.physics_bodies))

    def test_render_body_conversion_accepts_runtime_render_scale_policy(self) -> None:
        state = create_solar_system_simulation_state()
        readable = solar_system_to_render_bodies(
            state,
            policy=render_scale_policy_for_preset("readable"),
        )
        realistic = solar_system_to_render_bodies(
            state,
            policy=render_scale_policy_for_preset("realistic"),
        )
        self.assertEqual(len(readable), len(realistic))
        earth_readable = next(body for body in readable if body.name == "Earth")
        earth_realistic = next(body for body in realistic if body.name == "Earth")
        self.assertNotEqual(earth_readable.draw_radius, earth_realistic.draw_radius)

    def test_controlled_demo_mode_still_constructs(self) -> None:
        demo_state = create_controlled_demo_state()
        self.assertEqual(len(demo_state.physics_bodies), 3)
