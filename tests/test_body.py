import unittest

from src.universe.body import Body, CelestialBody


class BodyTests(unittest.TestCase):
    def test_render_body_position_and_visual_fields_are_separate(self) -> None:
        data = CelestialBody(
            name="Earth",
            category="terrestrial_planet",
            mass_kg=5.97217e24,
            mean_radius_m=6.3710084e6,
            mean_orbital_radius_m=1.4959826115e11,
            orbital_period_s=3.1558149102e7,
            rotation_period_s=86164.1,
            color_rgb=(1, 2, 3),
            visual_radius_px=10.0,
            source_note="test",
        )
        body = Body(data=data, world_x=12.5, world_y=-8.0)
        self.assertEqual(body.position, (12.5, -8.0))
        self.assertEqual(body.name, "Earth")
        self.assertEqual(body.color, (1, 2, 3))
        self.assertEqual(body.draw_radius, 10.0)
        self.assertNotEqual(body.data.mean_radius_m, body.draw_radius)
