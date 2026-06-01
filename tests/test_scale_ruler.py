import unittest

from src.universe.scale_ruler import build_scale_ruler, format_distance_label
from src.universe.units import AU_M


class ScaleRulerTests(unittest.TestCase):
    def test_distance_label_formats_meters(self) -> None:
        self.assertEqual(format_distance_label(999.0), "999 m")

    def test_distance_label_formats_km(self) -> None:
        self.assertEqual(format_distance_label(1_000.0), "1 km")
        self.assertEqual(format_distance_label(1_000_000.0), "1,000 km")

    def test_distance_label_formats_au(self) -> None:
        self.assertEqual(format_distance_label(AU_M), "1 AU")

    def test_build_scale_ruler_rejects_non_positive_zoom(self) -> None:
        with self.assertRaises(ValueError):
            build_scale_ruler(camera_zoom=0.0, meters_per_world_unit=1.0)

    def test_build_scale_ruler_rejects_non_positive_meters_per_world_unit(self) -> None:
        with self.assertRaises(ValueError):
            build_scale_ruler(camera_zoom=1.0, meters_per_world_unit=0.0)

    def test_ruler_distance_follows_formula(self) -> None:
        ruler = build_scale_ruler(
            camera_zoom=2.0,
            meters_per_world_unit=1_000_000_000.0,
            target_pixel_length=120,
        )
        expected = (120 / 2.0) * 1_000_000_000.0
        self.assertAlmostEqual(ruler.distance_m, expected)
        self.assertEqual(ruler.pixel_length, 120)

    def test_ruler_label_is_deterministic(self) -> None:
        first = build_scale_ruler(
            camera_zoom=0.5,
            meters_per_world_unit=250_000_000.0,
            target_pixel_length=120,
        )
        second = build_scale_ruler(
            camera_zoom=0.5,
            meters_per_world_unit=250_000_000.0,
            target_pixel_length=120,
        )
        self.assertEqual(first, second)
