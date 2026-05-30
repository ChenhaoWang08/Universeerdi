import unittest

from src.universe.physics import (
    Vector2,
    PhysicsBodyState,
    acceleration_from_source,
    compute_net_accelerations,
    step_bodies,
    step_placeholder_bodies,
    update_position,
    update_velocity,
)
from src.universe.units import NEWTON_G_M3_KG_S2
from src.universe.simulation import create_placeholder_bodies


def make_body(
    name: str,
    mass_kg: float,
    position: tuple[float, float],
    velocity: tuple[float, float] = (0.0, 0.0),
) -> PhysicsBodyState:
    return PhysicsBodyState(
        name=name,
        mass_kg=mass_kg,
        position_m=Vector2(*position),
        velocity_m_s=Vector2(*velocity),
    )


class PhysicsFoundationTests(unittest.TestCase):
    def test_pairwise_acceleration_points_toward_positive_x(self) -> None:
        target = make_body("target", 1.0, (0.0, 0.0))
        source = make_body("source", 10.0, (10.0, 0.0))
        acceleration = acceleration_from_source(target, source)
        self.assertGreater(acceleration.x, 0.0)
        self.assertAlmostEqual(acceleration.y, 0.0)

    def test_pairwise_acceleration_magnitude_matches_newtonian_formula(self) -> None:
        target = make_body("target", 1.0, (0.0, 0.0))
        source = make_body("source", 50.0, (10.0, 0.0))
        acceleration = acceleration_from_source(target, source)
        expected = (NEWTON_G_M3_KG_S2 * source.mass_kg) / (10.0**2)
        self.assertAlmostEqual(acceleration.magnitude(), expected)

    def test_pairwise_acceleration_points_toward_negative_x(self) -> None:
        target = make_body("target", 1.0, (0.0, 0.0))
        source = make_body("source", 10.0, (-10.0, 0.0))
        acceleration = acceleration_from_source(target, source)
        self.assertLess(acceleration.x, 0.0)
        self.assertAlmostEqual(acceleration.y, 0.0)

    def test_self_interaction_is_ignored(self) -> None:
        body = make_body("same", 10.0, (1.0, 2.0))
        acceleration = acceleration_from_source(body, body)
        self.assertEqual(acceleration, Vector2(0.0, 0.0))

    def test_zero_distance_is_safe(self) -> None:
        target = make_body("target", 1.0, (0.0, 0.0))
        source = make_body("source", 10.0, (0.0, 0.0))
        acceleration = acceleration_from_source(target, source)
        self.assertEqual(acceleration, Vector2(0.0, 0.0))

    def test_symmetric_sources_cancel_net_acceleration(self) -> None:
        center = make_body("center", 1.0, (0.0, 0.0))
        left = make_body("left", 100.0, (-10.0, 0.0))
        right = make_body("right", 100.0, (10.0, 0.0))
        center_acceleration = compute_net_accelerations((center, left, right))[0]
        self.assertAlmostEqual(center_acceleration.x, 0.0)
        self.assertAlmostEqual(center_acceleration.y, 0.0)

    def test_velocity_update_uses_acceleration_and_dt(self) -> None:
        velocity = Vector2(1.0, -2.0)
        acceleration = Vector2(0.5, 1.5)
        updated = update_velocity(velocity, acceleration, 4.0)
        self.assertEqual(updated, Vector2(3.0, 4.0))

    def test_position_update_uses_velocity_and_dt(self) -> None:
        position = Vector2(2.0, -1.0)
        velocity = Vector2(3.0, 0.5)
        updated = update_position(position, velocity, 2.0)
        self.assertEqual(updated, Vector2(8.0, 0.0))

    def test_step_uses_semi_implicit_euler(self) -> None:
        target = make_body("target", 10.0, (0.0, 0.0), (0.0, 0.0))
        source = make_body("source", 100.0, (10.0, 0.0), (0.0, 0.0))
        stepped_target = step_bodies((target, source), dt_seconds=2.0)[0]
        expected_acceleration = (NEWTON_G_M3_KG_S2 * 100.0) / (10.0**2)
        self.assertAlmostEqual(stepped_target.velocity_m_s.x, expected_acceleration * 2.0)
        self.assertAlmostEqual(stepped_target.position_m.x, expected_acceleration * 4.0)

    def test_step_returns_new_state_without_mutating_inputs(self) -> None:
        original = make_body("target", 1.0, (0.0, 0.0))
        source = make_body("source", 1.0, (10.0, 0.0))
        stepped = step_bodies((original, source), dt_seconds=1.0)
        self.assertIsNot(stepped[0], original)
        self.assertEqual(original.position_m, Vector2(0.0, 0.0))
        self.assertEqual(original.velocity_m_s, Vector2(0.0, 0.0))

    def test_step_rejects_non_positive_dt(self) -> None:
        body = make_body("target", 1.0, (0.0, 0.0))
        with self.assertRaises(ValueError):
            step_bodies((body,), dt_seconds=0.0)


class PhysicsCompatibilityTests(unittest.TestCase):
    def test_placeholder_step_returns_bodies_unchanged(self) -> None:
        bodies = create_placeholder_bodies()[:2]
        stepped = step_placeholder_bodies(bodies, 0.016)
        self.assertEqual(stepped, tuple(bodies))
