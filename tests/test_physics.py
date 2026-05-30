import unittest

from src.universe.physics import step_placeholder_bodies
from src.universe.simulation import create_placeholder_bodies


class PhysicsPlaceholderTests(unittest.TestCase):
    def test_placeholder_step_returns_bodies_unchanged(self) -> None:
        bodies = create_placeholder_bodies()[:2]
        stepped = step_placeholder_bodies(bodies, 0.016)
        self.assertEqual(stepped, tuple(bodies))
