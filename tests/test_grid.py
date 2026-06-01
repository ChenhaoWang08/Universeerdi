import unittest

from src.universe.body import Body
from src.universe.rendering import (
    MAX_GRID_PIXELS,
    MIN_GRID_PIXELS,
    LABEL_OFFSET_PX,
    Camera,
    body_label_anchor,
    build_grid_segments,
    build_grid_world_segments,
    choose_grid_world_spacing,
    update_trail_history,
)
from src.universe.solar_system_data import get_solar_system_body


class GridTests(unittest.TestCase):
    def test_spacing_stays_within_target_bounds_for_common_zooms(self) -> None:
        for zoom in (0.25, 0.5, 1.0, 2.5, 4.0):
            spacing = choose_grid_world_spacing(zoom)
            pixel_spacing = spacing * zoom
            self.assertGreaterEqual(pixel_spacing, MIN_GRID_PIXELS)
            self.assertLessEqual(pixel_spacing, MAX_GRID_PIXELS)

    def test_grid_build_produces_minor_and_major_lines(self) -> None:
        camera = Camera(center_x=120.0, center_y=-40.0, zoom=1.0)
        minor, major, spacing = build_grid_segments(camera, (1280, 720))
        self.assertGreater(spacing, 0.0)
        self.assertGreater(len(minor), 0)
        self.assertGreater(len(major), 0)

    def test_grid_density_remains_bounded(self) -> None:
        camera = Camera(zoom=0.2)
        minor, major, _ = build_grid_segments(camera, (1600, 900))
        self.assertLess(len(minor) + len(major), 80)

    def test_screen_grid_segments_match_world_grid_projection(self) -> None:
        camera = Camera(center_x=50.0, center_y=-25.0, zoom=1.2)
        viewport = (1280, 720)
        minor_screen, major_screen, _ = build_grid_segments(camera, viewport)
        minor_world, major_world, _ = build_grid_world_segments(camera, viewport)
        self.assertEqual(len(minor_screen), len(minor_world))
        self.assertEqual(len(major_screen), len(major_world))

    def test_trail_history_appends_and_caps_points(self) -> None:
        earth = get_solar_system_body("Earth")
        history = {}
        history = update_trail_history(history, (Body(data=earth, world_x=1.0, world_y=2.0),), max_points=2)
        history = update_trail_history(history, (Body(data=earth, world_x=3.0, world_y=4.0),), max_points=2)
        history = update_trail_history(history, (Body(data=earth, world_x=5.0, world_y=6.0),), max_points=2)
        self.assertEqual(history["Earth"], ((3.0, 4.0), (5.0, 6.0)))

    def test_trail_history_keeps_only_visible_bodies(self) -> None:
        earth = get_solar_system_body("Earth")
        mars = get_solar_system_body("Mars")
        history = update_trail_history(
            {},
            (
                Body(data=earth, world_x=1.0, world_y=1.0),
                Body(data=mars, world_x=2.0, world_y=2.0),
            ),
        )
        history = update_trail_history(history, (Body(data=earth, world_x=3.0, world_y=3.0),))
        self.assertIn("Earth", history)
        self.assertNotIn("Mars", history)

    def test_body_label_anchor_offsets_by_radius_and_padding(self) -> None:
        center = (100.0, 80.0)
        radius = 12.0
        anchor = body_label_anchor(center, radius)
        self.assertEqual(anchor[0], center[0] + radius + LABEL_OFFSET_PX)
        self.assertEqual(anchor[1], center[1] - radius - LABEL_OFFSET_PX)

    def test_trail_history_rejects_non_positive_max_points(self) -> None:
        with self.assertRaises(ValueError):
            update_trail_history({}, (), max_points=0)
