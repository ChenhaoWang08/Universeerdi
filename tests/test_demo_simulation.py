import unittest
from unittest.mock import patch

from src.universe.demo_simulation import (
    DEMO_BODY_DATA_BY_NAME,
    controlled_demo_to_render_bodies,
    create_controlled_demo_state,
    step_controlled_demo_state,
)
from src.universe.physics import step_bodies


class ControlledDemoSimulationTests(unittest.TestCase):
    def test_demo_initial_states_exist(self) -> None:
        state = create_controlled_demo_state()
        self.assertEqual(len(state.physics_bodies), 3)
        self.assertTrue(all(body.mass_kg > 0.0 for body in state.physics_bodies))

    def test_demo_render_bodies_use_demo_data(self) -> None:
        state = create_controlled_demo_state()
        render_bodies = controlled_demo_to_render_bodies(state)
        self.assertEqual(len(render_bodies), len(state.physics_bodies))
        self.assertTrue(all(body.name in DEMO_BODY_DATA_BY_NAME for body in render_bodies))
        self.assertTrue(all("Not real solar-system data" in body.data.source_note for body in render_bodies))

    def test_demo_step_changes_positions(self) -> None:
        state = create_controlled_demo_state()
        stepped = step_controlled_demo_state(state, dt_seconds=0.5)
        self.assertTrue(
            any(
                before.position_m != after.position_m
                for before, after in zip(state.physics_bodies, stepped.physics_bodies)
            )
        )

    def test_demo_step_does_not_mutate_input(self) -> None:
        state = create_controlled_demo_state()
        before_positions = tuple(body.position_m for body in state.physics_bodies)
        _ = step_controlled_demo_state(state, dt_seconds=0.5)
        self.assertEqual(before_positions, tuple(body.position_m for body in state.physics_bodies))

    def test_demo_step_uses_physics_foundation_step(self) -> None:
        state = create_controlled_demo_state()
        with patch(
            "src.universe.demo_simulation.step_bodies",
            wraps=step_bodies,
        ) as patched_step:
            _ = step_controlled_demo_state(state, dt_seconds=0.5)
        patched_step.assert_called_once()

