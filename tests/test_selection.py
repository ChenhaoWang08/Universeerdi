import unittest

from src.universe.body import Body, CelestialBody
from src.universe.demo_simulation import controlled_demo_to_render_bodies, create_controlled_demo_state
from src.universe.overlay_controls import OverlayControlsState, build_overlay_control_rects, handle_overlay_click
from src.universe.rendering import Camera
from src.universe.selection import (
    SelectionState,
    format_body_inspector_lines,
    get_selected_physics_body,
    handle_body_selection_click,
    select_body_at_screen_point,
)
from src.universe.solar_system_data import get_solar_system_body


class SelectionTests(unittest.TestCase):
    def test_default_selection_is_empty(self) -> None:
        state = SelectionState()
        self.assertIsNone(state.selected_body_name)

    def test_click_inside_body_selects_that_body(self) -> None:
        camera = Camera(center_x=260.0, center_y=0.0, zoom=1.0)
        bodies = controlled_demo_to_render_bodies(create_controlled_demo_state())
        runner_a = next(body for body in bodies if body.name == "DemoRunnerA")
        click = camera.world_to_screen(runner_a.position, (1280, 720))
        selected_name = select_body_at_screen_point(bodies, camera, click, (1280, 720))
        self.assertEqual(selected_name, "DemoRunnerA")

    def test_click_outside_bodies_clears_selection(self) -> None:
        camera = Camera(center_x=260.0, center_y=0.0, zoom=1.0)
        bodies = controlled_demo_to_render_bodies(create_controlled_demo_state())
        state = SelectionState(selected_body_name="DemoRunnerA")
        next_state, consumed = handle_body_selection_click(
            state,
            bodies,
            camera,
            (1200.0, 680.0),
            (1280, 720),
        )
        self.assertFalse(consumed)
        self.assertIsNone(next_state.selected_body_name)

    def test_overlapping_bodies_select_closest_center(self) -> None:
        close_data = CelestialBody(
            name="NearBody",
            category="terrestrial_planet",
            mass_kg=1.0,
            mean_radius_m=1.0,
            mean_orbital_radius_m=0.0,
            orbital_period_s=0.0,
            rotation_period_s=0.0,
            color_rgb=(255, 255, 255),
            visual_radius_px=14.0,
            source_note="test",
        )
        far_data = CelestialBody(
            name="FarBody",
            category="terrestrial_planet",
            mass_kg=1.0,
            mean_radius_m=1.0,
            mean_orbital_radius_m=0.0,
            orbital_period_s=0.0,
            rotation_period_s=0.0,
            color_rgb=(255, 255, 255),
            visual_radius_px=14.0,
            source_note="test",
        )
        close_body = Body(data=close_data, world_x=100.0, world_y=100.0)
        far_body = Body(data=far_data, world_x=106.0, world_y=100.0)
        camera = Camera(center_x=0.0, center_y=0.0, zoom=1.0)
        click = camera.world_to_screen((101.0, 100.0), (1280, 720))
        selected_name = select_body_at_screen_point(
            (far_body, close_body),
            camera,
            click,
            (1280, 720),
        )
        self.assertEqual(selected_name, "NearBody")

    def test_overlay_click_is_consumed_before_body_selection(self) -> None:
        overlay_state = OverlayControlsState()
        camera = Camera(center_x=260.0, center_y=0.0, zoom=1.0)
        bodies = controlled_demo_to_render_bodies(create_controlled_demo_state())
        selection_state = SelectionState()

        rects = build_overlay_control_rects((1280, 720))
        click = (rects.labels_rect[0] + 2, rects.labels_rect[1] + 2)
        overlay_state, overlay_consumed = handle_overlay_click(overlay_state, click, (1280, 720))
        if overlay_consumed:
            next_selection_state = selection_state
        else:
            next_selection_state, _ = handle_body_selection_click(
                selection_state, bodies, camera, click, (1280, 720)
            )

        self.assertTrue(overlay_consumed)
        self.assertEqual(next_selection_state, selection_state)

    def test_body_selection_click_is_consumed_before_camera_drag(self) -> None:
        camera = Camera(center_x=260.0, center_y=0.0, zoom=1.0)
        bodies = controlled_demo_to_render_bodies(create_controlled_demo_state())
        runner_b = next(body for body in bodies if body.name == "DemoRunnerB")
        click = camera.world_to_screen(runner_b.position, (1280, 720))
        next_state, consumed = handle_body_selection_click(
            SelectionState(), bodies, camera, click, (1280, 720)
        )
        self.assertTrue(consumed)
        self.assertEqual(next_state.selected_body_name, "DemoRunnerB")

    def test_selection_does_not_mutate_physics_state(self) -> None:
        demo_state = create_controlled_demo_state()
        before_positions = tuple(body.position_m for body in demo_state.physics_bodies)
        before_velocities = tuple(body.velocity_m_s for body in demo_state.physics_bodies)
        camera = Camera(center_x=260.0, center_y=0.0, zoom=1.0)
        render_bodies = controlled_demo_to_render_bodies(demo_state)
        _next_state, _consumed = handle_body_selection_click(
            SelectionState(), render_bodies, camera, (800.0, 360.0), (1280, 720)
        )
        self.assertEqual(before_positions, tuple(body.position_m for body in demo_state.physics_bodies))
        self.assertEqual(before_velocities, tuple(body.velocity_m_s for body in demo_state.physics_bodies))

    def test_inspector_format_includes_name_mass_position_velocity(self) -> None:
        demo_state = create_controlled_demo_state()
        body = get_selected_physics_body(demo_state.physics_bodies, "DemoRunnerA")
        lines = format_body_inspector_lines(body)
        text = "\n".join(lines)
        self.assertIn("Name: DemoRunnerA", text)
        self.assertIn("Mass:", text)
        self.assertIn("Position:", text)
        self.assertIn("Velocity:", text)
