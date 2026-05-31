import unittest

from src.universe.demo_simulation import create_controlled_demo_state
from src.universe.render_scale import RenderScalePolicy
from src.universe.render_scale_presets import (
    RenderScalePresetState,
    cycle_render_scale_preset,
    render_scale_policy_for_preset,
    render_scale_preset_status_text,
)
from src.universe.solar_system_simulation import (
    create_solar_system_simulation_state,
    solar_system_to_render_bodies,
)


class RenderScalePresetStateTests(unittest.TestCase):
    def test_default_preset_is_readable(self) -> None:
        state = RenderScalePresetState()
        self.assertEqual(state.preset, "readable")

    def test_preset_cycle_order_is_deterministic(self) -> None:
        state = RenderScalePresetState(preset="readable")
        state = cycle_render_scale_preset(state)
        self.assertEqual(state.preset, "realistic")
        state = cycle_render_scale_preset(state)
        self.assertEqual(state.preset, "overview")
        state = cycle_render_scale_preset(state)
        self.assertEqual(state.preset, "readable")

    def test_each_preset_resolves_to_valid_policy(self) -> None:
        for preset in ("readable", "realistic", "overview"):
            policy = render_scale_policy_for_preset(preset)
            self.assertIsInstance(policy, RenderScalePolicy)
            self.assertGreater(policy.meters_per_world_unit, 0.0)
            self.assertGreater(policy.min_body_radius_px, 0.0)
            self.assertGreaterEqual(policy.max_body_radius_px, policy.min_body_radius_px)
            self.assertGreater(policy.body_radius_scale, 0.0)

    def test_realistic_radius_scale_matches_distance_scale(self) -> None:
        policy = render_scale_policy_for_preset("realistic")
        self.assertAlmostEqual(
            policy.body_radius_scale,
            1.0 / policy.meters_per_world_unit,
        )

    def test_scale_status_text_is_deterministic(self) -> None:
        state = RenderScalePresetState(preset="overview")
        self.assertEqual(render_scale_preset_status_text(state), "Scale: overview")

    def test_preset_switching_does_not_mutate_physics_state(self) -> None:
        solar_state = create_solar_system_simulation_state()
        before_positions = tuple(body.position_m for body in solar_state.physics_bodies)
        before_velocities = tuple(body.velocity_m_s for body in solar_state.physics_bodies)
        _ = solar_system_to_render_bodies(
            solar_state,
            policy=render_scale_policy_for_preset("readable"),
        )
        _ = solar_system_to_render_bodies(
            solar_state,
            policy=render_scale_policy_for_preset("realistic"),
        )
        _ = solar_system_to_render_bodies(
            solar_state,
            policy=render_scale_policy_for_preset("overview"),
        )
        self.assertEqual(before_positions, tuple(body.position_m for body in solar_state.physics_bodies))
        self.assertEqual(before_velocities, tuple(body.velocity_m_s for body in solar_state.physics_bodies))

    def test_preset_helpers_do_not_mutate_demo_state(self) -> None:
        demo_state = create_controlled_demo_state()
        before_positions = tuple(body.position_m for body in demo_state.physics_bodies)
        state = RenderScalePresetState()
        state = cycle_render_scale_preset(state)
        state = cycle_render_scale_preset(state)
        state = cycle_render_scale_preset(state)
        self.assertEqual(state.preset, "readable")
        self.assertEqual(before_positions, tuple(body.position_m for body in demo_state.physics_bodies))
