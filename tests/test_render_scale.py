import unittest

from src.universe.body import Body, CelestialBody
from src.universe.physics import PhysicsBodyState, Vector2
from src.universe.render_scale import (
    RenderScalePolicy,
    map_physical_position_to_world,
    map_physical_radius_to_visible_px,
)
from src.universe.rendering import Camera
from src.universe.selection import select_body_at_screen_point
from src.universe.solar_system_simulation import create_solar_system_simulation_state, solar_system_to_render_bodies


class RenderScalePolicyTests(unittest.TestCase):
    def test_render_scale_policy_has_safe_defaults(self) -> None:
        policy = RenderScalePolicy(
            meters_per_world_unit=1_000.0,
            min_body_radius_px=4.0,
            max_body_radius_px=24.0,
            body_radius_scale=0.001,
        )
        self.assertGreater(policy.meters_per_world_unit, 0.0)
        self.assertGreater(policy.min_body_radius_px, 0.0)
        self.assertGreaterEqual(policy.max_body_radius_px, policy.min_body_radius_px)
        self.assertGreater(policy.body_radius_scale, 0.0)

    def test_physical_position_maps_deterministically(self) -> None:
        policy = RenderScalePolicy(
            meters_per_world_unit=100.0,
            min_body_radius_px=4.0,
            max_body_radius_px=20.0,
            body_radius_scale=0.01,
        )
        self.assertEqual(map_physical_position_to_world((250.0, -100.0), policy), (2.5, -1.0))

    def test_physical_radius_maps_to_visible_radius(self) -> None:
        policy = RenderScalePolicy(
            meters_per_world_unit=1000.0,
            min_body_radius_px=3.0,
            max_body_radius_px=30.0,
            body_radius_scale=0.001,
        )
        self.assertAlmostEqual(
            map_physical_radius_to_visible_px(8_000.0, policy),
            8.0,
        )

    def test_small_radius_clamps_to_minimum_visible_radius(self) -> None:
        policy = RenderScalePolicy(
            meters_per_world_unit=1000.0,
            min_body_radius_px=5.0,
            max_body_radius_px=30.0,
            body_radius_scale=0.001,
        )
        self.assertAlmostEqual(map_physical_radius_to_visible_px(1.0, policy), 5.0)

    def test_large_radius_clamps_to_maximum_visible_radius(self) -> None:
        policy = RenderScalePolicy(
            meters_per_world_unit=1000.0,
            min_body_radius_px=5.0,
            max_body_radius_px=30.0,
            body_radius_scale=0.001,
        )
        self.assertAlmostEqual(map_physical_radius_to_visible_px(1_000_000.0, policy), 30.0)

    def test_missing_radius_uses_fallback_safely(self) -> None:
        policy = RenderScalePolicy(
            meters_per_world_unit=1000.0,
            min_body_radius_px=5.0,
            max_body_radius_px=30.0,
            body_radius_scale=0.001,
            fallback_body_radius_px=7.0,
        )
        self.assertAlmostEqual(map_physical_radius_to_visible_px(None, policy), 7.0)

    def test_mapping_does_not_mutate_physics_body_state(self) -> None:
        body = PhysicsBodyState(
            name="T",
            mass_kg=1.0,
            position_m=Vector2(10.0, -20.0),
            velocity_m_s=Vector2(3.0, 4.0),
        )
        before = (body.position_m, body.velocity_m_s, body.mass_kg)
        policy = RenderScalePolicy(
            meters_per_world_unit=1000.0,
            min_body_radius_px=3.0,
            max_body_radius_px=20.0,
            body_radius_scale=0.001,
        )
        _ = map_physical_position_to_world((body.position_m.x, body.position_m.y), policy)
        _ = map_physical_radius_to_visible_px(1_000.0, policy)
        after = (body.position_m, body.velocity_m_s, body.mass_kg)
        self.assertEqual(before, after)

    def test_solar_system_body_can_be_mapped_without_crashing(self) -> None:
        state = create_solar_system_simulation_state()
        render_bodies = solar_system_to_render_bodies(state)
        self.assertEqual(len(render_bodies), len(state.physics_bodies))
        self.assertTrue(all(body.render_radius_px is not None for body in render_bodies))

    def test_selection_hit_testing_can_use_rendered_radius(self) -> None:
        policy = RenderScalePolicy(
            meters_per_world_unit=1.0,
            min_body_radius_px=4.0,
            max_body_radius_px=25.0,
            body_radius_scale=0.001,
        )
        data = CelestialBody(
            name="Scaled",
            category="terrestrial_planet",
            mass_kg=1.0,
            mean_radius_m=40_000.0,
            mean_orbital_radius_m=0.0,
            orbital_period_s=0.0,
            rotation_period_s=0.0,
            color_rgb=(255, 255, 255),
            visual_radius_px=1.0,
            source_note="test",
        )
        scaled_radius = map_physical_radius_to_visible_px(data.mean_radius_m, policy)
        body = Body(
            data=data,
            world_x=0.0,
            world_y=0.0,
            render_radius_px=scaled_radius,
        )
        camera = Camera(center_x=0.0, center_y=0.0, zoom=1.0)
        center = camera.world_to_screen(body.position, (1280, 720))
        click = (center[0] + (scaled_radius - 1.0), center[1])
        selected_name = select_body_at_screen_point((body,), camera, click, (1280, 720))
        self.assertEqual(selected_name, "Scaled")
