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

    def test_policy_validates_local_zoom_threshold(self) -> None:
        with self.assertRaises(ValueError):
            validate_grid_warp_policy(GridWarpPolicy(local_zoom_threshold=0.0))

    def test_policy_validates_local_influence_radius_px(self) -> None:
        with self.assertRaises(ValueError):
            validate_grid_warp_policy(GridWarpPolicy(local_influence_radius_px=0.0))

    def test_policy_validates_local_max_displacement_px(self) -> None:
        with self.assertRaises(ValueError):
            validate_grid_warp_policy(GridWarpPolicy(local_max_displacement_px=-1.0))

    def test_classify_returns_global_for_sun_like_mass(self) -> None:
        policy = GridWarpPolicy()
        kind = classify_warp_source(relative_mass=1.0, camera_zoom=0.2, policy=policy)
        self.assertEqual(kind, "global")

    def test_classify_returns_hidden_for_earth_like_mass_at_overview(self) -> None:
        sun = get_solar_system_body("Sun")
        earth = get_solar_system_body("Earth")
        policy = GridWarpPolicy(reference_mass_kg=sun.mass_kg)
        relative = compute_relative_mass(earth.mass_kg, policy)
        kind = classify_warp_source(relative_mass=relative, camera_zoom=0.2, policy=policy)
        self.assertEqual(kind, "hidden")

    def test_classify_returns_local_for_earth_like_mass_at_close_zoom(self) -> None:
        sun = get_solar_system_body("Sun")
        earth = get_solar_system_body("Earth")
        policy = GridWarpPolicy(reference_mass_kg=sun.mass_kg)
        relative = compute_relative_mass(earth.mass_kg, policy)
        kind = classify_warp_source(relative_mass=relative, camera_zoom=2.5, policy=policy)
        self.assertEqual(kind, "local")

    def test_local_influence_radius_converts_px_to_world(self) -> None:
        policy = GridWarpPolicy(local_influence_radius_px=90.0)
        self.assertAlmostEqual(compute_local_influence_radius_world(3.0, policy), 30.0)

    def test_local_max_displacement_converts_px_to_world(self) -> None:
        policy = GridWarpPolicy(local_max_displacement_px=12.0)
        self.assertAlmostEqual(compute_local_max_displacement_world(3.0, policy), 4.0)

    def test_local_warp_displacement_is_bounded_by_local_cap(self) -> None:
        sun = get_solar_system_body("Sun")
        earth = get_solar_system_body("Earth")
        policy = GridWarpPolicy(reference_mass_kg=sun.mass_kg, local_max_displacement_px=12.0)
        source = DistortionSource(name="Earth", position=(0.0, 0.0), mass_kg=earth.mass_kg)
        point = (0.5, 0.0)
        zoom = 3.0
        distorted = distort_grid_point(point, (source,), policy=policy, camera_zoom=zoom)
        displacement = abs(distorted[0] - point[0])
        self.assertLessEqual(displacement, compute_local_max_displacement_world(zoom, policy))

    def test_local_warp_is_disabled_below_zoom_threshold(self) -> None:
        sun = get_solar_system_body("Sun")
        earth = get_solar_system_body("Earth")
        policy = GridWarpPolicy(reference_mass_kg=sun.mass_kg, local_zoom_threshold=2.0)
        source = DistortionSource(name="Earth", position=(0.0, 0.0), mass_kg=earth.mass_kg)
        point = (20.0, 0.0)
        distorted = distort_grid_point(point, (source,), policy=policy, camera_zoom=1.0)
        self.assertEqual(distorted, point)

    def test_global_warp_uses_world_space_influence_radius(self) -> None:
        policy = GridWarpPolicy(base_influence_radius_world=800.0)
        radius = compute_influence_radius_world(0.5, policy)
        self.assertAlmostEqual(radius, 400.0)

    def test_visual_factor_hierarchy_sun_jupiter_earth_global(self) -> None:
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

    def test_overview_terrestrial_warp_is_suppressed(self) -> None:
        sun = get_solar_system_body("Sun")
        mars = get_solar_system_body("Mars")
        policy = GridWarpPolicy(reference_mass_kg=sun.mass_kg)
        relative = compute_relative_mass(mars.mass_kg, policy)
        self.assertFalse(
            should_render_distortion_source(relative_mass=relative, camera_zoom=0.2, policy=policy)
        )

    def test_local_warp_non_zero_for_earth_like_mass_at_close_zoom(self) -> None:
        sun = get_solar_system_body("Sun")
        earth = get_solar_system_body("Earth")
        policy = GridWarpPolicy(reference_mass_kg=sun.mass_kg)
        source = DistortionSource(name="Earth", position=(0.0, 0.0), mass_kg=earth.mass_kg)
        point = (20.0, 0.0)
        distorted = distort_grid_point(point, (source,), policy=policy, camera_zoom=3.0)
        self.assertNotEqual(distorted, point)

    def test_local_warp_radius_is_limited_vs_global_sun_radius(self) -> None:
        policy = GridWarpPolicy()
        local_radius = compute_local_influence_radius_world(3.0, policy)
        global_radius = compute_influence_radius_world(1.0, policy)
        self.assertLess(local_radius, global_radius)

    def test_sun_multiplier_increases_sun_warp(self) -> None:
        sun = get_solar_system_body("Sun")
        policy = GridWarpPolicy(reference_mass_kg=sun.mass_kg)
        point = (100.0, 0.0)
        base_source = DistortionSource(name="Sun", position=(0.0, 0.0), mass_kg=sun.mass_kg)
        strong_source = DistortionSource(name="Sun", position=(0.0, 0.0), mass_kg=sun.mass_kg * 100.0)
        base = distort_grid_point(point, (base_source,), policy=policy, camera_zoom=1.0)
        strong = distort_grid_point(point, (strong_source,), policy=policy, camera_zoom=1.0)
        self.assertLessEqual(abs(point[0] - base[0]), abs(point[0] - strong[0]))

    def test_sun_multiplier_does_not_increase_non_sun_warp(self) -> None:
        sun = get_solar_system_body("Sun")
        earth = get_solar_system_body("Earth")
        policy = GridWarpPolicy(reference_mass_kg=sun.mass_kg)
        point = (20.0, 0.0)
        earth_source = DistortionSource(name="Earth", position=(0.0, 0.0), mass_kg=earth.mass_kg)
        first = distort_grid_point(point, (earth_source,), policy=policy, camera_zoom=3.0)
        second = distort_grid_point(point, (earth_source,), policy=policy, camera_zoom=3.0)
        self.assertEqual(first, second)

    def test_point_at_source_center_is_safe(self) -> None:
        source = DistortionSource(name="Sun", position=(10.0, 10.0), mass_kg=1.0e30)
        point = (10.0, 10.0)
        self.assertEqual(distort_grid_point(point, (source,), policy=GridWarpPolicy(), camera_zoom=1.0), point)

    def test_no_sources_returns_original_point(self) -> None:
        point = (5.0, 6.0)
        self.assertEqual(distort_grid_point(point, (), policy=GridWarpPolicy(), camera_zoom=1.0), point)

    def test_strength_zero_returns_original_point(self) -> None:
        source = DistortionSource(name="Sun", position=(0.0, 0.0), mass_kg=1.0e30)
        point = (10.0, 0.0)
        self.assertEqual(
            distort_grid_point(point, (source,), policy=GridWarpPolicy(strength=0.0), camera_zoom=1.0),
            point,
        )

    def test_build_sources_uses_body_position_and_mass(self) -> None:
        earth = Body(data=get_solar_system_body("Earth"), world_x=12.5, world_y=-8.0)
        sources = build_distortion_sources_from_bodies((earth,))
        self.assertEqual(len(sources), 1)
        self.assertEqual(sources[0].position, (12.5, -8.0))
        self.assertEqual(sources[0].mass_kg, earth.data.mass_kg)
