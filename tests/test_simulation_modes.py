import unittest

from src.universe.demo_simulation import create_controlled_demo_state
from src.universe.simulation_modes import (
    SimulationModeState,
    simulation_mode_status_text,
    toggle_simulation_mode,
)
from src.universe.solar_system_simulation import create_solar_system_simulation_state


class SimulationModeStateTests(unittest.TestCase):
    def test_default_mode_is_controlled_demo(self) -> None:
        state = SimulationModeState()
        self.assertEqual(state.mode, "controlled_demo")

    def test_toggling_from_controlled_demo_goes_to_solar_system(self) -> None:
        state = SimulationModeState(mode="controlled_demo")
        next_state = toggle_simulation_mode(state)
        self.assertEqual(next_state.mode, "solar_system")

    def test_toggling_from_solar_system_goes_to_controlled_demo(self) -> None:
        state = SimulationModeState(mode="solar_system")
        next_state = toggle_simulation_mode(state)
        self.assertEqual(next_state.mode, "controlled_demo")

    def test_mode_status_text_is_deterministic(self) -> None:
        self.assertEqual(
            simulation_mode_status_text(SimulationModeState(mode="controlled_demo")),
            "Mode: controlled_demo",
        )
        self.assertEqual(
            simulation_mode_status_text(SimulationModeState(mode="solar_system")),
            "Mode: solar_system",
        )

    def test_mode_toggle_does_not_mutate_source_simulation_builders(self) -> None:
        demo_before = tuple(body.position_m for body in create_controlled_demo_state().physics_bodies)
        solar_before = tuple(
            body.position_m for body in create_solar_system_simulation_state().physics_bodies
        )

        state = SimulationModeState()
        _ = toggle_simulation_mode(state)
        _ = toggle_simulation_mode(SimulationModeState(mode="solar_system"))

        demo_after = tuple(body.position_m for body in create_controlled_demo_state().physics_bodies)
        solar_after = tuple(
            body.position_m for body in create_solar_system_simulation_state().physics_bodies
        )
        self.assertEqual(demo_before, demo_after)
        self.assertEqual(solar_before, solar_after)
