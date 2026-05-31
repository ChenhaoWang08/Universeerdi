import unittest

from src.universe.camera_views import (
    CameraViewState,
    apply_camera_view_preset,
    camera_view_settings_for_preset,
    camera_view_status_text,
    cycle_camera_view_preset,
)
from src.universe.demo_simulation import create_controlled_demo_state
from src.universe.rendering import Camera


class CameraViewPresetTests(unittest.TestCase):
    def test_default_camera_view_is_normal(self) -> None:
        state = CameraViewState()
        self.assertEqual(state.preset, "normal")

    def test_camera_view_cycle_order_is_deterministic(self) -> None:
        state = CameraViewState(preset="normal")
        state = cycle_camera_view_preset(state)
        self.assertEqual(state.preset, "overview")
        state = cycle_camera_view_preset(state)
        self.assertEqual(state.preset, "close")
        state = cycle_camera_view_preset(state)
        self.assertEqual(state.preset, "normal")

    def test_each_preset_has_valid_settings(self) -> None:
        for preset in ("normal", "overview", "close"):
            settings = camera_view_settings_for_preset(preset)
            self.assertGreater(settings.zoom, 0.0)
            self.assertGreater(settings.min_zoom, 0.0)
            self.assertGreaterEqual(settings.max_zoom, settings.min_zoom)
            self.assertGreater(settings.zoom_step, 1.0)

    def test_apply_normal_preset_updates_camera_settings(self) -> None:
        camera = Camera(center_x=0.0, center_y=0.0, zoom=3.0)
        apply_camera_view_preset(camera, CameraViewState(preset="normal"))
        self.assertAlmostEqual(camera.zoom, 1.0)
        self.assertAlmostEqual(camera.min_zoom, 0.02)
        self.assertAlmostEqual(camera.max_zoom, 40.0)
        self.assertAlmostEqual(camera.zoom_step, 1.15)

    def test_apply_overview_preset_is_wider_than_normal(self) -> None:
        camera = Camera(center_x=0.0, center_y=0.0, zoom=1.0)
        apply_camera_view_preset(camera, CameraViewState(preset="overview"))
        self.assertLessEqual(camera.zoom, 0.25)
        self.assertLessEqual(camera.min_zoom, 0.02)

    def test_apply_close_preset_allows_higher_max_zoom(self) -> None:
        camera = Camera(center_x=0.0, center_y=0.0, zoom=1.0)
        apply_camera_view_preset(camera, CameraViewState(preset="close"))
        self.assertGreaterEqual(camera.max_zoom, 100.0)

    def test_resetting_camera_to_same_preset_is_deterministic(self) -> None:
        camera = Camera(center_x=999.0, center_y=-999.0, zoom=9.0)
        state = CameraViewState(preset="overview")
        apply_camera_view_preset(camera, state)
        first = (camera.center_x, camera.center_y, camera.zoom, camera.min_zoom, camera.max_zoom, camera.zoom_step)
        camera.center_x += 100.0
        camera.zoom = 5.0
        apply_camera_view_preset(camera, state)
        second = (camera.center_x, camera.center_y, camera.zoom, camera.min_zoom, camera.max_zoom, camera.zoom_step)
        self.assertEqual(first, second)

    def test_status_text_is_deterministic(self) -> None:
        self.assertEqual(camera_view_status_text(CameraViewState(preset="close")), "View: close")

    def test_camera_view_helpers_do_not_mutate_physics_state(self) -> None:
        demo_state = create_controlled_demo_state()
        before_positions = tuple(body.position_m for body in demo_state.physics_bodies)
        state = CameraViewState()
        _ = cycle_camera_view_preset(state)
        _ = camera_view_settings_for_preset("overview")
        self.assertEqual(before_positions, tuple(body.position_m for body in demo_state.physics_bodies))
