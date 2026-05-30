import unittest

from src.universe.simulation import create_placeholder_bodies


class SimulationSetupTests(unittest.TestCase):
    def test_placeholder_bodies_include_sun_and_eight_planets(self) -> None:
        bodies = create_placeholder_bodies()
        self.assertEqual(
            [body.name for body in bodies],
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

    def test_placeholder_layout_keeps_render_positions_separate_from_physical_orbits(self) -> None:
        earth = next(body for body in create_placeholder_bodies() if body.name == "Earth")
        self.assertLess(abs(earth.world_x), 10_000.0)
        self.assertGreater(earth.data.mean_orbital_radius_m, 100_000_000_000.0)
