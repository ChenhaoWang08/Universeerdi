import unittest

from src.universe.rendering import (
    MAX_GRID_PIXELS,
    MIN_GRID_PIXELS,
    Camera,
    build_grid_segments,
    choose_grid_world_spacing,
)


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
