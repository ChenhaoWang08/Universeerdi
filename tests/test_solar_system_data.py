import unittest

from src.universe.solar_system_data import SOLAR_SYSTEM_BODIES, SOLAR_SYSTEM_BODY_MAP


class SolarSystemDataTests(unittest.TestCase):
    def test_required_bodies_exist(self) -> None:
        self.assertEqual(
            [body.name for body in SOLAR_SYSTEM_BODIES],
            [
                "Sun",
                "Mercury",
                "Venus",
                "Earth",
                "Mars",
                "Jupiter",
                "Saturn",
                "Uranus",
                "Neptune",
            ],
        )

    def test_dataset_body_names_are_unique(self) -> None:
        names = [body.name for body in SOLAR_SYSTEM_BODIES]
        self.assertEqual(len(names), len(set(names)))

    def test_categories_cover_star_and_planet_types(self) -> None:
        expected = {
            "Sun": "star",
            "Mercury": "terrestrial_planet",
            "Venus": "terrestrial_planet",
            "Earth": "terrestrial_planet",
            "Mars": "terrestrial_planet",
            "Jupiter": "gas_giant",
            "Saturn": "gas_giant",
            "Uranus": "ice_giant",
            "Neptune": "ice_giant",
        }
        self.assertEqual(
            {body.name: body.category for body in SOLAR_SYSTEM_BODIES},
            expected,
        )

    def test_planets_have_positive_core_physical_values(self) -> None:
        for name in (
            "Mercury",
            "Venus",
            "Earth",
            "Mars",
            "Jupiter",
            "Saturn",
            "Uranus",
            "Neptune",
        ):
            body = SOLAR_SYSTEM_BODY_MAP[name]
            self.assertGreater(body.mass_kg, 0.0)
            self.assertGreater(body.mean_radius_m, 0.0)
            self.assertGreater(body.mean_orbital_radius_m, 0.0)
            self.assertGreater(body.orbital_period_s, 0.0)

    def test_sun_orbit_convention_is_documented_in_data(self) -> None:
        sun = SOLAR_SYSTEM_BODY_MAP["Sun"]
        self.assertGreater(sun.mass_kg, 0.0)
        self.assertGreater(sun.mean_radius_m, 0.0)
        self.assertEqual(sun.mean_orbital_radius_m, 0.0)
        self.assertEqual(sun.orbital_period_s, 0.0)

    def test_visual_radius_is_positive_for_all_renderable_bodies(self) -> None:
        for body in SOLAR_SYSTEM_BODIES:
            self.assertGreater(body.visual_radius_px, 0.0)

    def test_physical_radius_and_visual_radius_are_separate_fields(self) -> None:
        earth = SOLAR_SYSTEM_BODY_MAP["Earth"]
        self.assertGreater(earth.mean_radius_m, 1_000_000.0)
        self.assertLess(earth.visual_radius_px, 100.0)
        self.assertNotEqual(earth.mean_radius_m, earth.visual_radius_px)

    def test_source_notes_exist(self) -> None:
        for body in SOLAR_SYSTEM_BODIES:
            self.assertTrue(body.source_note)
