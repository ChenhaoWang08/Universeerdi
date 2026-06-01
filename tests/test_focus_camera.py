import unittest

from src.universe.camera_views import CameraViewState, apply_camera_view_preset
from src.universe.demo_simulation import create_controlled_demo_state, controlled_demo_to_render_bodies
from src.universe.focus_camera import (
    FocusCameraState,
    apply_focus_to_camera,
    clear_focus,
    focus_status_text,
    sync_focus_with_render_bodies,
    toggle_focus_from_selection,
)
from src.universe.rendering import Camera


class FocusCameraTests(unittest.TestCase):
    def test_default_focus_is_none(self) -> None:
        state = FocusCameraState()
        self.assertIsNone(state.focused_body_name)
        self.assertEqual(focus_status_text(state), "Focus: none")

    def test_toggle_focus_from_selected_body_sets_focus(self) -> None:
        state = FocusCameraState()
        next_state = toggle_focus_from_selection(state, "Earth")
        self.assertEqual(next_state.focused_body_name, "Earth")

    def test_toggle_focus_again_clears_focus(self) -> None:
        state = FocusCameraState(focused_body_name="Earth")
        next_state = toggle_focus_from_selection(state, "Earth")
        self.assertIsNone(next_state.focused_body_name)

    def test_toggle_focus_without_selection_clears_focus(self) -> None:
        state = FocusCameraState(focused_body_name="Earth")
        next_state = toggle_focus_from_selection(state, None)
        self.assertIsNone(next_state.focused_body_name)

    def test_focus_is_cleared_when_body_disappears(self) -> None:
        demo_state = create_controlled_demo_state()
        bodies = controlled_demo_to_render_bodies(demo_state)
        state = FocusCameraState(focused_body_name="DemoRunnerA")
        self.assertEqual(sync_focus_with_render_bodies(state, bodies).focused_body_name, "DemoRunnerA")
        filtered = tuple(body for body in bodies if body.name != "DemoRunnerA")
        self.assertIsNone(sync_focus_with_render_bodies(state, filtered).focused_body_name)

    def test_apply_focus_to_camera_tracks_body_position(self) -> None:
        demo_state = create_controlled_demo_state()
        bodies = controlled_demo_to_render_bodies(demo_state)
        camera = Camera(center_x=0.0, center_y=0.0, zoom=1.0)
        apply_camera_view_preset(camera, CameraViewState(preset="normal"))
        state = FocusCameraState(focused_body_name="DemoRunnerB")
        applied = apply_focus_to_camera(camera, state, bodies)
        target = next(body for body in bodies if body.name == "DemoRunnerB")
        self.assertTrue(applied)
        self.assertAlmostEqual(camera.center_x, target.world_x)
        self.assertAlmostEqual(camera.center_y, target.world_y)

    def test_apply_focus_returns_false_for_missing_target(self) -> None:
        demo_state = create_controlled_demo_state()
        bodies = controlled_demo_to_render_bodies(demo_state)
        camera = Camera(center_x=0.0, center_y=0.0, zoom=1.0)
        applied = apply_focus_to_camera(camera, FocusCameraState("Missing"), bodies)
        self.assertFalse(applied)

    def test_clear_focus_is_deterministic(self) -> None:
        state = FocusCameraState(focused_body_name="Earth")
        self.assertEqual(clear_focus(state), FocusCameraState())
