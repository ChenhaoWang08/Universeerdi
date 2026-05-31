import unittest

from src.universe.demo_simulation import create_controlled_demo_state
from src.universe.physics_substeps import (
    PhysicsSubstepState,
    SUBSTEP_VALUES,
    decrease_physics_substeps,
    increase_physics_substeps,
    physics_substeps_status_text,
)


class PhysicsSubstepsTests(unittest.TestCase):
    def test_default_substeps_is_one(self) -> None:
        self.assertEqual(PhysicsSubstepState().substeps, 1)

    def test_increase_substeps_advances_to_next_value(self) -> None:
        state = PhysicsSubstepState()
        state = increase_physics_substeps(state)
        self.assertEqual(state.substeps, 2)

    def test_decrease_substeps_moves_back_safely(self) -> None:
        state = PhysicsSubstepState(index=2)
        state = decrease_physics_substeps(state)
        self.assertEqual(state.substeps, 2)

    def test_substeps_clamp_at_bounds(self) -> None:
        state = PhysicsSubstepState(index=len(SUBSTEP_VALUES) - 1)
        self.assertEqual(increase_physics_substeps(state).substeps, SUBSTEP_VALUES[-1])
        state = PhysicsSubstepState(index=0)
        self.assertEqual(decrease_physics_substeps(state).substeps, SUBSTEP_VALUES[0])

    def test_substeps_status_text_is_deterministic(self) -> None:
        state = PhysicsSubstepState(index=3)
        self.assertEqual(physics_substeps_status_text(state), "Substeps: 8")

    def test_helpers_do_not_mutate_physics_state(self) -> None:
        demo_state = create_controlled_demo_state()
        before_positions = tuple(body.position_m for body in demo_state.physics_bodies)

        state = PhysicsSubstepState()
        _ = increase_physics_substeps(state)
        _ = decrease_physics_substeps(state)

        self.assertEqual(before_positions, tuple(body.position_m for body in demo_state.physics_bodies))
