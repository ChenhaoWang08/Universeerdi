import unittest

from src.universe.body import Body
from src.universe.grid_distortion import (
    DistortionSource,
    GridDistortionState,
    build_distortion_sources_from_bodies,
    distort_grid_point,
    grid_distortion_status_text,
    toggle_grid_distortion,
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

    def test_invalid_strength_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            distort_grid_point((1.0, 2.0), (), strength=-0.1, influence_radius_world=10.0, max_displacement_world=1.0)

    def test_invalid_influence_radius_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            distort_grid_point((1.0, 2.0), (), strength=1.0, influence_radius_world=0.0, max_displacement_world=1.0)

    def test_invalid_max_displacement_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            distort_grid_point((1.0, 2.0), (), strength=1.0, influence_radius_world=10.0, max_displacement_world=-1.0)

    def test_no_sources_returns_original_point(self) -> None:
        point = (5.0, 6.0)
        self.assertEqual(
            distort_grid_point(point, (), strength=1.0, influence_radius_world=50.0, max_displacement_world=5.0),
            point,
        )

    def test_zero_strength_returns_original_point(self) -> None:
        source = DistortionSource(name="Sun", position=(0.0, 0.0), mass_kg=1.0e30)
        point = (10.0, 0.0)
        self.assertEqual(
            distort_grid_point(point, (source,), strength=0.0, influence_radius_world=50.0, max_displacement_world=5.0),
            point,
        )

    def test_point_at_source_center_is_safe(self) -> None:
        source = DistortionSource(name="Sun", position=(10.0, 10.0), mass_kg=1.0e30)
        point = (10.0, 10.0)
        self.assertEqual(
            distort_grid_point(point, (source,), strength=1.0, influence_radius_world=50.0, max_displacement_world=5.0),
            point,
        )

    def test_displacement_is_bounded(self) -> None:
        source = DistortionSource(name="Sun", position=(0.0, 0.0), mass_kg=1.0e35)
        point = (1.0, 0.0)
        distorted = distort_grid_point(
            point,
            (source,),
            strength=10.0,
            influence_radius_world=100.0,
            max_displacement_world=2.0,
        )
        displacement = abs(distorted[0] - point[0])
        self.assertLessEqual(displacement, 2.0)

    def test_larger_mass_produces_stronger_or_equal_distortion(self) -> None:
        point = (30.0, 0.0)
        small = DistortionSource(name="small", position=(0.0, 0.0), mass_kg=1.0e20)
        large = DistortionSource(name="large", position=(0.0, 0.0), mass_kg=1.0e30)
        distorted_small = distort_grid_point(
            point,
            (small,),
            strength=1.0,
            influence_radius_world=100.0,
            max_displacement_world=10.0,
        )
        distorted_large = distort_grid_point(
            point,
            (large,),
            strength=1.0,
            influence_radius_world=100.0,
            max_displacement_world=10.0,
        )
        self.assertLessEqual(abs(point[0] - distorted_small[0]), abs(point[0] - distorted_large[0]))

    def test_farther_points_have_weaker_or_equal_distortion(self) -> None:
        source = DistortionSource(name="Sun", position=(0.0, 0.0), mass_kg=1.0e30)
        near_point = (10.0, 0.0)
        far_point = (70.0, 0.0)
        near_distorted = distort_grid_point(
            near_point,
            (source,),
            strength=1.0,
            influence_radius_world=100.0,
            max_displacement_world=10.0,
        )
        far_distorted = distort_grid_point(
            far_point,
            (source,),
            strength=1.0,
            influence_radius_world=100.0,
            max_displacement_world=10.0,
        )
        self.assertGreaterEqual(abs(near_point[0] - near_distorted[0]), abs(far_point[0] - far_distorted[0]))

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
