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
