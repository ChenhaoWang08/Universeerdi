import unittest

from src.universe.rendering import Camera


class CameraTests(unittest.TestCase):
    def test_pan_uses_screen_delta_and_zoom(self) -> None:
        camera = Camera(center_x=0.0, center_y=0.0, zoom=2.0)
        camera.pan_by_screen_delta(20.0, -10.0)
        self.assertAlmostEqual(camera.center_x, -10.0)
        self.assertAlmostEqual(camera.center_y, 5.0)

    def test_scroll_down_zooms_in_while_preserving_anchor_world_point(self) -> None:
        camera = Camera(center_x=100.0, center_y=-50.0, zoom=1.0)
        viewport_size = (800, 600)
        anchor = (620.0, 420.0)

        world_before = camera.screen_to_world(anchor, viewport_size)
        camera.zoom_by_scroll(-2, anchor, viewport_size)
        world_after = camera.screen_to_world(anchor, viewport_size)

        self.assertGreater(camera.zoom, 1.0)
        self.assertAlmostEqual(world_before[0], world_after[0], places=6)
        self.assertAlmostEqual(world_before[1], world_after[1], places=6)

    def test_scroll_up_zooms_out(self) -> None:
        camera = Camera(zoom=1.5)
        camera.zoom_by_scroll(1, (400.0, 300.0), (800, 600))
        self.assertLess(camera.zoom, 1.5)

    def test_zoom_step_is_camera_configurable(self) -> None:
        slow = Camera(zoom=1.0, zoom_step=1.05)
        fast = Camera(zoom=1.0, zoom_step=1.3)
        anchor = (400.0, 300.0)
        viewport = (800, 600)
        slow.zoom_by_scroll(-1, anchor, viewport)
        fast.zoom_by_scroll(-1, anchor, viewport)
        self.assertGreater(fast.zoom, slow.zoom)

    def test_invalid_zoom_step_is_rejected(self) -> None:
        camera = Camera(zoom=1.0, zoom_step=1.0)
        with self.assertRaises(ValueError):
            camera.zoom_by_scroll(-1, (400.0, 300.0), (800, 600))

    def test_invalid_min_zoom_is_rejected(self) -> None:
        camera = Camera(zoom=1.0, min_zoom=0.0)
        with self.assertRaises(ValueError):
            camera.zoom_by_scroll(-1, (400.0, 300.0), (800, 600))

    def test_invalid_max_zoom_is_rejected(self) -> None:
        camera = Camera(zoom=1.0, min_zoom=2.0, max_zoom=1.0)
        with self.assertRaises(ValueError):
            camera.zoom_by_scroll(-1, (400.0, 300.0), (800, 600))
