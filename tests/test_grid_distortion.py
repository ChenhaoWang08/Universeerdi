import unittest

from src.universe.body import Body
from src.universe.grid_distortion import (
    DistortionSource,
    GridDistortionState,
    GridWarpPolicy,
    build_distortion_sources_from_bodies,
    compute_influence_radius_world,
    compute_relative_mass,
    compute_visual_mass_factor,
    distort_grid_point,
    grid_distortion_status_text,
    should_render_distortion_source,
    toggle_grid_distortion,
    validate_grid_warp_policy,
)
from src.universe.solar_system_data import get_solar_system_body


class GridDistortionTests(unittest.TestCase):
    def test_default_state_is_off(self) -> None:
        state = GridDistortionState()
        self.assertFalse(state.enabled)
        self.assertEqual(state.strength, 1.0)

    def test_toggle_switches_on_and_off(self) -> None:
        state = GridDistortionState()
        self.assertTrue(toggle_grid_distortion(state).enabled)
        self.assertFalse(toggle_grid_distortion(toggle_grid_distortion(state)).enabled)

    def test_status_text_is_deterministic(self) -> None:
        self.assertEqual(grid_distortion_status_text(GridDistortionState()), "Grid warp: off")
        self.assertEqual(
            grid_distortion_status_text(GridDistortionState(enabled=True, strength=1.0)),
            "Grid warp: on x1.0",
        )

    def test_policy_validates_reference_mass(self) -> None:
        with self.assertRaises(ValueError):
            validate_grid_warp_policy(GridWarpPolicy(reference_mass_kg=0.0))

    def test_policy_rejects_invalid_strength(self) -> None:
        with self.assertRaises(ValueError):
            validate_grid_warp_policy(GridWarpPolicy(strength=-0.1))

    def test_policy_rejects_invalid_mass_exponent(self) -> None:
        with self.assertRaises(ValueError):
            validate_grid_warp_policy(GridWarpPolicy(mass_exponent=0.0))

    def test_relative_mass_is_one_for_reference_mass(self) -> None:
        policy = GridWarpPolicy(reference_mass_kg=10.0)
        self.assertEqual(compute_relative_mass(10.0, policy), 1.0)

    def test_relative_mass_is_small_for_earth_like_mass(self) -> None:
        sun = get_solar_system_body("Sun")
        earth = get_solar_system_body("Earth")
        policy = GridWarpPolicy(reference_mass_kg=sun.mass_kg)
        self.assertLess(compute_relative_mass(earth.mass_kg, policy), 1e-5)

    def test_visual_mass_factor_has_hierarchy(self) -> None:
        sun = get_solar_system_body("Sun")
        jupiter = get_solar_system_body("Jupiter")
        earth = get_solar_system_body("Earth")
        policy = GridWarpPolicy(reference_mass_kg=sun.mass_kg, min_visible_relative_mass=0.0)
        sun_factor = compute_visual_mass_factor(sun.mass_kg, policy)
        jupiter_factor = compute_visual_mass_factor(jupiter.mass_kg, policy)
        earth_factor = compute_visual_mass_factor(earth.mass_kg, policy)
        self.assertGreater(sun_factor, jupiter_factor)
        self.assertGreater(jupiter_factor, earth_factor)

    def test_overview_threshold_hides_small_bodies(self) -> None:
        sun = get_solar_system_body("Sun")
        earth = get_solar_system_body("Earth")
        policy = GridWarpPolicy(reference_mass_kg=sun.mass_kg)
        earth_relative = compute_relative_mass(earth.mass_kg, policy)
        self.assertFalse(
            should_render_distortion_source(
                relative_mass=earth_relative,
                camera_zoom=0.2,
                policy=policy,
            )
        )

    def test_influence_radius_scales_with_visual_mass(self) -> None:
        policy = GridWarpPolicy(
            base_influence_radius_world=800.0,
            min_influence_radius_world=20.0,
            max_influence_radius_world=900.0,
        )
        sun_radius = compute_influence_radius_world(1.0, policy)
        jupiter_radius = compute_influence_radius_world(0.2, policy)
        earth_radius = compute_influence_radius_world(0.01, policy)
        self.assertGreater(sun_radius, jupiter_radius)
        self.assertGreater(jupiter_radius, earth_radius)

    def test_influence_radius_is_clamped_by_max(self) -> None:
        policy = GridWarpPolicy(max_influence_radius_world=100.0)
        self.assertEqual(compute_influence_radius_world(10.0, policy), 100.0)

    def test_influence_radius_respects_min_when_visible(self) -> None:
        policy = GridWarpPolicy(min_influence_radius_world=40.0)
        self.assertEqual(compute_influence_radius_world(0.001, policy), 40.0)

    def test_no_sources_returns_original_point(self) -> None:
        point = (5.0, 6.0)
        self.assertEqual(
            distort_grid_point(point, (), policy=GridWarpPolicy(), camera_zoom=1.0),
            point,
        )

    def test_zero_strength_returns_original_point(self) -> None:
        source = DistortionSource(name="Sun", position=(0.0, 0.0), mass_kg=1.0e30)
        point = (10.0, 0.0)
        self.assertEqual(
            distort_grid_point(
                point,
                (source,),
                policy=GridWarpPolicy(strength=0.0),
                camera_zoom=1.0,
            ),
            point,
        )

    def test_point_at_source_center_is_safe(self) -> None:
        source = DistortionSource(name="Sun", position=(10.0, 10.0), mass_kg=1.0e30)
        point = (10.0, 10.0)
        self.assertEqual(
            distort_grid_point(
                point,
                (source,),
                policy=GridWarpPolicy(),
                camera_zoom=1.0,
            ),
            point,
        )

    def test_displacement_is_bounded(self) -> None:
        source = DistortionSource(name="Sun", position=(0.0, 0.0), mass_kg=1.0e35)
        point = (1.0, 0.0)
        policy = GridWarpPolicy(strength=10.0, max_displacement_world=2.0)
        distorted = distort_grid_point(point, (source,), policy=policy, camera_zoom=1.0)
        displacement = abs(distorted[0] - point[0])
        self.assertLessEqual(displacement, 2.0)

    def test_larger_mass_produces_stronger_or_equal_distortion(self) -> None:
        point = (30.0, 0.0)
        policy = GridWarpPolicy(min_visible_relative_mass=0.0)
        small = DistortionSource(name="small", position=(0.0, 0.0), mass_kg=1.0e20)
        large = DistortionSource(name="large", position=(0.0, 0.0), mass_kg=1.0e30)
        distorted_small = distort_grid_point(point, (small,), policy=policy, camera_zoom=1.0)
        distorted_large = distort_grid_point(point, (large,), policy=policy, camera_zoom=1.0)
        self.assertLessEqual(abs(point[0] - distorted_small[0]), abs(point[0] - distorted_large[0]))

    def test_farther_points_have_weaker_or_equal_distortion(self) -> None:
        source = DistortionSource(name="Sun", position=(0.0, 0.0), mass_kg=1.0e30)
        policy = GridWarpPolicy(min_visible_relative_mass=0.0)
        near_point = (10.0, 0.0)
        far_point = (70.0, 0.0)
        near_distorted = distort_grid_point(near_point, (source,), policy=policy, camera_zoom=1.0)
        far_distorted = distort_grid_point(far_point, (source,), policy=policy, camera_zoom=1.0)
        self.assertGreaterEqual(abs(near_point[0] - near_distorted[0]), abs(far_point[0] - far_distorted[0]))

    def test_sun_multiplier_increases_sun_visual_factor(self) -> None:
        sun = get_solar_system_body("Sun")
        policy = GridWarpPolicy(reference_mass_kg=sun.mass_kg)
        baseline = compute_visual_mass_factor(sun.mass_kg, policy)
        boosted = compute_visual_mass_factor(sun.mass_kg * 100.0, policy)
        self.assertGreater(boosted, baseline)

    def test_earth_visual_factor_is_independent_from_sun_multiplier(self) -> None:
        sun = get_solar_system_body("Sun")
        earth = get_solar_system_body("Earth")
        policy = GridWarpPolicy(reference_mass_kg=sun.mass_kg)
        earth_factor_a = compute_visual_mass_factor(earth.mass_kg, policy)
        earth_factor_b = compute_visual_mass_factor(earth.mass_kg, policy)
        self.assertEqual(earth_factor_a, earth_factor_b)

    def test_build_sources_uses_body_position_and_mass(self) -> None:
        earth = Body(data=get_solar_system_body("Earth"), world_x=12.5, world_y=-8.0)
        sources = build_distortion_sources_from_bodies((earth,))
        self.assertEqual(len(sources), 1)
        self.assertEqual(sources[0].position, (12.5, -8.0))
        self.assertEqual(sources[0].mass_kg, earth.data.mass_kg)

    def test_effective_mass_override_is_applied_without_mutating_body_data(self) -> None:
        sun = Body(data=get_solar_system_body("Sun"), world_x=0.0, world_y=0.0)
        baseline_mass = sun.data.mass_kg
        sources = build_distortion_sources_from_bodies(
            (sun,),
            effective_masses_by_name={"Sun": baseline_mass * 5.0},
        )
        self.assertEqual(sources[0].mass_kg, baseline_mass * 5.0)
        self.assertEqual(sun.data.mass_kg, baseline_mass)
