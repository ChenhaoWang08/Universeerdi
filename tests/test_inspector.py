import unittest

from src.universe.physics import PhysicsBodyState, Vector2
from src.universe.inspector import build_inspector_lines
from src.universe.selection import get_selected_physics_body
from src.universe.solar_system_simulation import create_solar_system_simulation_state
from src.universe.demo_simulation import create_controlled_demo_state


class InspectorTests(unittest.TestCase):
    def test_inspector_data_can_be_built_for_controlled_demo_body(self) -> None:
        demo_state = create_controlled_demo_state()
        body = get_selected_physics_body(demo_state.physics_bodies, "DemoRunnerA")
        lines = build_inspector_lines(body, simulation_mode="controlled_demo")
        text = "\n".join(lines)
        self.assertIn("Name: DemoRunnerA", text)
        self.assertIn("Mode: controlled_demo", text)
        self.assertIn("Source: demo-only", text)

    def test_inspector_data_can_be_built_for_solar_system_body(self) -> None:
        solar_state = create_solar_system_simulation_state()
        body = get_selected_physics_body(solar_state.physics_bodies, "Earth")
        lines = build_inspector_lines(body, simulation_mode="solar_system")
        text = "\n".join(lines)
        self.assertIn("Name: Earth", text)
        self.assertIn("Mode: solar_system", text)
        self.assertIn("Source: local solar_system_data.py dataset", text)

    def test_solar_system_inspector_includes_required_core_fields(self) -> None:
        solar_state = create_solar_system_simulation_state()
        body = get_selected_physics_body(solar_state.physics_bodies, "Earth")
        lines = build_inspector_lines(body, simulation_mode="solar_system")
        text = "\n".join(lines)
        self.assertIn("Mass:", text)
        self.assertIn("Radius:", text)
        self.assertIn("Position:", text)
        self.assertIn("Velocity:", text)
        self.assertIn("Distance:", text)

    def test_inspector_includes_speed(self) -> None:
        solar_state = create_solar_system_simulation_state()
        body = get_selected_physics_body(solar_state.physics_bodies, "Earth")
        lines = build_inspector_lines(body, simulation_mode="solar_system")
        self.assertTrue(any(line.startswith("Speed: ") for line in lines))

    def test_missing_optional_fields_use_safe_fallback_without_crash(self) -> None:
        unknown = PhysicsBodyState(
            name="UnknownBody",
            mass_kg=1.0,
            position_m=Vector2(10.0, 20.0),
            velocity_m_s=Vector2(3.0, 4.0),
        )
        lines = build_inspector_lines(unknown, simulation_mode="solar_system")
        text = "\n".join(lines)
        self.assertIn("Radius: unknown", text)
        self.assertIn("Mean Orbit Radius: unknown", text)
        self.assertIn("Orbital Period: unknown", text)
        self.assertIn("Rotation Period: unknown", text)
        self.assertIn("Source: unknown", text)

    def test_large_values_are_formatted_readably(self) -> None:
        solar_state = create_solar_system_simulation_state()
        body = get_selected_physics_body(solar_state.physics_bodies, "Jupiter")
        lines = build_inspector_lines(body, simulation_mode="solar_system")
        self.assertTrue(any("e+" in line or "e-" in line for line in lines if ":" in line))

    def test_inspector_does_not_mutate_physics_state(self) -> None:
        solar_state = create_solar_system_simulation_state()
        before = tuple(
            (body.name, body.mass_kg, body.position_m, body.velocity_m_s)
            for body in solar_state.physics_bodies
        )
        earth = get_selected_physics_body(solar_state.physics_bodies, "Earth")
        _ = build_inspector_lines(earth, simulation_mode="solar_system")
        after = tuple(
            (body.name, body.mass_kg, body.position_m, body.velocity_m_s)
            for body in solar_state.physics_bodies
        )
        self.assertEqual(before, after)

    def test_controlled_demo_does_not_pretend_solar_metadata(self) -> None:
        demo_state = create_controlled_demo_state()
        body = get_selected_physics_body(demo_state.physics_bodies, "DemoAnchor")
        lines = build_inspector_lines(body, simulation_mode="controlled_demo")
        text = "\n".join(lines)
        self.assertIn("Radius: unknown", text)
        self.assertNotIn("Mean Orbit Radius:", text)

    def test_selection_name_based_lookup_remains_compatible(self) -> None:
        demo_state = create_controlled_demo_state()
        body = get_selected_physics_body(demo_state.physics_bodies, "DemoRunnerB")
        self.assertIsNotNone(body)
        self.assertEqual(body.name, "DemoRunnerB")
