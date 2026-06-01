import unittest

from src.universe.body import Body
from src.universe.grid_distortion import (
    DistortionSource,
    GridDistortionState,
    GridWarpPolicy,
    build_distortion_sources_from_bodies,
    classify_warp_source,
    compute_influence_radius_world,
    compute_local_influence_radius_world,
    compute_local_max_displacement_world,
    compute_local_zoom_fade,
    compute_relative_mass,
    compute_smooth_falloff,
    compute_visual_mass_factor,
    distort_grid_point,
    grid_distortion_status_text,
    smoothstep,
    smoothstep_between,
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

    def test_smoothstep_clamps_and_endpoints(self) -> None:
        self.assertEqual(smoothstep(-0.1), 0.0)
        self.assertEqual(smoothstep(0.0), 0.0)
        self.assertEqual(smoothstep(1.0), 1.0)
        self.assertEqual(smoothstep(1.4), 1.0)

    def test_smoothstep_is_monotonic(self) -> None:
        samples = [smoothstep(value) for value in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0)]
        self.assertEqual(samples, sorted(samples))

    def test_smoothstep_between_clamps_and_rejects_invalid_bounds(self) -> None:
        self.assertEqual(smoothstep_between(1.0, 3.0, 0.5), 0.0)
        self.assertEqual(smoothstep_between(1.0, 3.0, 3.5), 1.0)
        with self.assertRaises(ValueError):
            smoothstep_between(2.0, 2.0, 2.0)

    def test_policy_validates_local_and_smoothing_fields(self) -> None:
        with self.assertRaises(ValueError):
            validate_grid_warp_policy(GridWarpPolicy(local_zoom_fade_start=0.0))
        with self.assertRaises(ValueError):
            validate_grid_warp_policy(GridWarpPolicy(local_zoom_fade_full=1.0, local_zoom_fade_start=1.0))
        with self.assertRaises(ValueError):
            validate_grid_warp_policy(GridWarpPolicy(soft_core_px=-1.0))
        with self.assertRaises(ValueError):
            validate_grid_warp_policy(GridWarpPolicy(max_sources_per_point=0))

    def test_local_zoom_fade_progression(self) -> None:
        policy = GridWarpPolicy(local_zoom_fade_start=1.2, local_zoom_fade_full=2.4)
        self.assertEqual(compute_local_zoom_fade(1.0, policy), 0.0)
        self.assertEqual(compute_local_zoom_fade(3.0, policy), 1.0)
        mid = compute_local_zoom_fade(1.8, policy)
        self.assertGreater(mid, 0.0)
        self.assertLess(mid, 1.0)

    def test_classify_source_global_local_hidden(self) -> None:
        policy = GridWarpPolicy()
        self.assertEqual(classify_warp_source(relative_mass=1.0, camera_zoom=0.2, policy=policy), "global")
        self.assertEqual(classify_warp_source(relative_mass=1e-8, camera_zoom=3.0, policy=policy), "hidden")
        self.assertEqual(
            classify_warp_source(relative_mass=3e-6, camera_zoom=2.0, policy=policy),
            "local",
        )

    def test_px_to_world_conversions(self) -> None:
        policy = GridWarpPolicy(local_influence_radius_px=220.0, local_max_displacement_px=34.0)
        self.assertAlmostEqual(compute_local_influence_radius_world(2.0, policy), 110.0)
        self.assertAlmostEqual(compute_local_max_displacement_world(2.0, policy), 17.0)

    def test_no_sources_returns_original_point(self) -> None:
        point = (5.0, 6.0)
        self.assertEqual(
            distort_grid_point(point, (), policy=GridWarpPolicy(), camera_zoom=1.0),
            point,
        )

    def test_strength_zero_returns_original_point(self) -> None:
        source = DistortionSource(name="Sun", position=(0.0, 0.0), mass_kg=1.0e30)
        point = (10.0, 0.0)
        self.assertEqual(
            distort_grid_point(point, (source,), policy=GridWarpPolicy(strength=0.0), camera_zoom=1.0),
            point,
        )

    def test_point_at_source_center_is_safe(self) -> None:
        source = DistortionSource(name="Sun", position=(10.0, 10.0), mass_kg=1.0e30)
        point = (10.0, 10.0)
        self.assertEqual(
            distort_grid_point(point, (source,), policy=GridWarpPolicy(), camera_zoom=1.0),
            point,
        )

    def test_smooth_falloff_decreases_with_distance(self) -> None:
        policy = GridWarpPolicy()
        near = compute_smooth_falloff(10.0, 100.0, policy)
        mid = compute_smooth_falloff(40.0, 100.0, policy)
        far = compute_smooth_falloff(90.0, 100.0, policy)
        self.assertGreater(near, mid)
        self.assertGreater(mid, far)

    def test_outside_influence_radius_has_zero_falloff(self) -> None:
        policy = GridWarpPolicy()
        self.assertEqual(compute_smooth_falloff(100.0, 100.0, policy), 0.0)

    def test_top_k_source_limit_uses_strongest_influences(self) -> None:
        point = (60.0, 0.0)
        policy = GridWarpPolicy(min_visible_relative_mass=0.0, max_sources_per_point=1)
        strong = DistortionSource(name="A", position=(0.0, 0.0), mass_kg=1.0e32)
        weak_1 = DistortionSource(name="B", position=(0.0, 10.0), mass_kg=1.0e23)
        weak_2 = DistortionSource(name="C", position=(0.0, -10.0), mass_kg=1.0e23)
        combined = distort_grid_point(point, (strong, weak_1, weak_2), policy=policy, camera_zoom=1.0)
        strong_only = distort_grid_point(point, (strong,), policy=policy, camera_zoom=1.0)
        self.assertAlmostEqual(combined[0], strong_only[0], places=6)
        self.assertAlmostEqual(combined[1], strong_only[1], places=6)

    def test_displacement_is_bounded(self) -> None:
        source = DistortionSource(name="Sun", position=(0.0, 0.0), mass_kg=1.0e35)
        point = (1.0, 0.0)
        policy = GridWarpPolicy(strength=10.0, max_displacement_world=2.0)
        distorted = distort_grid_point(point, (source,), policy=policy, camera_zoom=1.0)
        displacement = abs(distorted[0] - point[0])
        self.assertLessEqual(displacement, 2.0)

    def test_visual_factor_hierarchy_global_sun_jupiter_earth(self) -> None:
        sun = get_solar_system_body("Sun")
        jupiter = get_solar_system_body("Jupiter")
        earth = get_solar_system_body("Earth")
        policy = GridWarpPolicy(reference_mass_kg=sun.mass_kg, min_visible_relative_mass=0.0)
        self.assertGreater(
            compute_visual_mass_factor(sun.mass_kg, policy),
            compute_visual_mass_factor(jupiter.mass_kg, policy),
        )
        self.assertGreater(
            compute_visual_mass_factor(jupiter.mass_kg, policy),
            compute_visual_mass_factor(earth.mass_kg, policy),
        )

    def test_overview_terrestrial_warp_remains_suppressed(self) -> None:
        sun = get_solar_system_body("Sun")
        earth = get_solar_system_body("Earth")
        policy = GridWarpPolicy(reference_mass_kg=sun.mass_kg)
        earth_relative = compute_relative_mass(earth.mass_kg, policy)
        self.assertEqual(
            classify_warp_source(relative_mass=earth_relative, camera_zoom=0.2, policy=policy),
            "hidden",
        )

    def test_zoomed_in_earth_local_warp_non_zero(self) -> None:
        sun = get_solar_system_body("Sun")
        earth = get_solar_system_body("Earth")
        policy = GridWarpPolicy(reference_mass_kg=sun.mass_kg)
        source = DistortionSource(name="Earth", position=(0.0, 0.0), mass_kg=earth.mass_kg)
        point = (20.0, 0.0)
        distorted = distort_grid_point(point, (source,), policy=policy, camera_zoom=3.0)
        self.assertNotEqual(distorted, point)

    def test_local_radius_is_limited_vs_global_sun_radius(self) -> None:
        policy = GridWarpPolicy()
        local_radius = compute_local_influence_radius_world(3.0, policy)
        global_radius = compute_influence_radius_world(1.0, policy)
        self.assertLess(local_radius, global_radius)

    def test_sun_multiplier_strengthens_sun_only(self) -> None:
        sun = get_solar_system_body("Sun")
        earth = get_solar_system_body("Earth")
        policy = GridWarpPolicy(reference_mass_kg=sun.mass_kg)

        point_sun = (100.0, 0.0)
        base_sun = DistortionSource(name="Sun", position=(0.0, 0.0), mass_kg=sun.mass_kg)
        boosted_sun = DistortionSource(name="Sun", position=(0.0, 0.0), mass_kg=sun.mass_kg * 100.0)
        base_result = distort_grid_point(point_sun, (base_sun,), policy=policy, camera_zoom=1.0)
        boosted_result = distort_grid_point(point_sun, (boosted_sun,), policy=policy, camera_zoom=1.0)
        self.assertLessEqual(abs(point_sun[0] - base_result[0]), abs(point_sun[0] - boosted_result[0]))

        point_earth = (20.0, 0.0)
        earth_source = DistortionSource(name="Earth", position=(0.0, 0.0), mass_kg=earth.mass_kg)
        first = distort_grid_point(point_earth, (earth_source,), policy=policy, camera_zoom=3.0)
        second = distort_grid_point(point_earth, (earth_source,), policy=policy, camera_zoom=3.0)
        self.assertEqual(first, second)

    def test_build_sources_uses_body_position_and_mass(self) -> None:
        earth = Body(data=get_solar_system_body("Earth"), world_x=12.5, world_y=-8.0)
        sources = build_distortion_sources_from_bodies((earth,))
        self.assertEqual(len(sources), 1)
        self.assertEqual(sources[0].position, (12.5, -8.0))
        self.assertEqual(sources[0].mass_kg, earth.data.mass_kg)
