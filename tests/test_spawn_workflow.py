import unittest

from src.universe.spawn_workflow import (
    SETTINGS_PENDING_NOTE,
    SPAWN_MENU_OFFSET_X,
    SPAWN_MENU_WIDTH,
    SpawnMenuState,
    SpawnSettingsState,
    build_spawn_templates,
    click_spawn_menu_item,
    clamp_spawn_menu_scroll,
    close_spawn_settings_panel,
    compute_density_kg_m3,
    compute_volume_m3,
    create_spawn_draft,
    handle_spawn_settings_click,
    is_point_in_spawn_menu,
    open_spawn_menu,
    open_spawn_settings_panel,
    spawn_menu_item_index_at_point,
    spawn_menu_max_scroll,
    spawn_menu_rect,
    spawn_menu_row_top_for_index,
    spawn_menu_scroll,
    spawn_settings_panel_rect,
    spawn_settings_set_button_rect,
    update_spawn_menu_hover,
)


class SpawnWorkflowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.templates = build_spawn_templates()

    def test_template_list_contains_sun_and_planets(self) -> None:
        names = {template.display_name for template in self.templates}
        for expected in (
            "Sun",
            "Mercury",
            "Venus",
            "Earth",
            "Mars",
            "Jupiter",
            "Saturn",
            "Uranus",
            "Neptune",
        ):
            self.assertIn(expected, names)

    def test_template_list_contains_black_hole_placeholder(self) -> None:
        names = {template.display_name for template in self.templates}
        self.assertIn("Black Hole placeholder", names)

    def test_black_hole_placeholder_flag_is_true(self) -> None:
        placeholder = next(
            template for template in self.templates if template.template_id == "black_hole_placeholder"
        )
        self.assertTrue(placeholder.is_black_hole_placeholder)

    def test_create_draft_from_earth_copies_fields(self) -> None:
        earth = next(template for template in self.templates if template.display_name == "Earth")
        draft = create_spawn_draft(earth)
        self.assertEqual(draft.mass_kg, earth.mass_kg)
        self.assertEqual(draft.radius_m, earth.radius_m)
        self.assertEqual(draft.color_rgb, earth.color_rgb)

    def test_create_draft_does_not_mutate_template(self) -> None:
        earth = next(template for template in self.templates if template.display_name == "Earth")
        _draft = create_spawn_draft(earth)
        self.assertEqual(earth.display_name, "Earth")
        self.assertFalse(earth.is_black_hole_placeholder)

    def test_volume_positive_for_positive_radius(self) -> None:
        self.assertGreater(compute_volume_m3(10.0), 0.0)

    def test_density_positive_for_positive_mass_and_radius(self) -> None:
        self.assertGreater(compute_density_kg_m3(10.0, 2.0), 0.0)

    def test_open_menu_places_to_right_of_mouse_by_default(self) -> None:
        state = open_spawn_menu((100.0, 120.0), (1280, 720), len(self.templates))
        self.assertEqual(state.menu_left, 100 + SPAWN_MENU_OFFSET_X)
        self.assertEqual(state.menu_top, 120)

    def test_menu_placement_clamps_inside_viewport(self) -> None:
        state = open_spawn_menu((1270.0, 710.0), (1280, 720), len(self.templates))
        left, top, width, height = spawn_menu_rect(state)
        self.assertGreaterEqual(left, 12)
        self.assertGreaterEqual(top, 12)
        self.assertLessEqual(left + width, 1280)
        self.assertLessEqual(top + height, 720)

    def test_hover_detection_returns_template_id_for_visible_row(self) -> None:
        state = open_spawn_menu((200.0, 120.0), (1280, 720), len(self.templates))
        hover_point = (state.menu_left + 20, state.menu_top + 10)
        updated = update_spawn_menu_hover(state, hover_point, self.templates)
        self.assertEqual(updated.hovered_template_id, self.templates[0].template_id)

    def test_hover_outside_rows_returns_none(self) -> None:
        state = open_spawn_menu((200.0, 120.0), (1280, 720), len(self.templates))
        updated = update_spawn_menu_hover(state, (10.0, 10.0), self.templates)
        self.assertIsNone(updated.hovered_template_id)

    def test_menu_scroll_clamps_to_valid_range(self) -> None:
        state = open_spawn_menu((200.0, 120.0), (1280, 720), len(self.templates))
        max_scroll = spawn_menu_max_scroll(len(self.templates))
        self.assertEqual(clamp_spawn_menu_scroll(-20, len(self.templates)), 0)
        self.assertEqual(clamp_spawn_menu_scroll(999, len(self.templates)), max_scroll)
        scrolled = spawn_menu_scroll(state, -999, len(self.templates))
        self.assertEqual(scrolled.scroll_offset, max_scroll)

    def test_clicking_item_closes_menu_and_opens_settings(self) -> None:
        menu_state = open_spawn_menu((200.0, 120.0), (1280, 720), len(self.templates))
        click_point = (menu_state.menu_left + 12, menu_state.menu_top + 12)
        next_menu, settings_state, consumed = click_spawn_menu_item(
            menu_state,
            click_point,
            self.templates,
            (1280, 720),
        )
        self.assertTrue(consumed)
        self.assertFalse(next_menu.is_open)
        self.assertTrue(settings_state.is_open)

    def test_clicking_item_does_not_create_preview_state(self) -> None:
        menu_state = open_spawn_menu((200.0, 120.0), (1280, 720), len(self.templates))
        click_point = (menu_state.menu_left + 12, menu_state.menu_top + 12)
        _next_menu, settings_state, consumed = click_spawn_menu_item(
            menu_state,
            click_point,
            self.templates,
            (1280, 720),
        )
        self.assertTrue(consumed)
        self.assertFalse(hasattr(settings_state, "preview"))

    def test_clicking_item_does_not_spawn_body(self) -> None:
        menu_state = open_spawn_menu((200.0, 120.0), (1280, 720), len(self.templates))
        click_point = (menu_state.menu_left + 12, menu_state.menu_top + 12)
        _next_menu, settings_state, consumed = click_spawn_menu_item(
            menu_state,
            click_point,
            self.templates,
            (1280, 720),
        )
        self.assertTrue(consumed)
        self.assertIsNotNone(settings_state.draft)

    def test_settings_panel_placement_clamps_inside_viewport(self) -> None:
        menu_state = open_spawn_menu((1260.0, 700.0), (1280, 720), len(self.templates))
        panel = open_spawn_settings_panel(
            menu_state=menu_state,
            selected_template=self.templates[0],
            viewport_size=(1280, 720),
            preferred_top=700,
        )
        left, top, width, height = spawn_settings_panel_rect(panel)
        self.assertLessEqual(left + width, 1280)
        self.assertLessEqual(top + height, 720)

    def test_cancel_closes_settings_panel(self) -> None:
        menu_state = open_spawn_menu((200.0, 120.0), (1280, 720), len(self.templates))
        panel = open_spawn_settings_panel(
            menu_state=menu_state,
            selected_template=self.templates[0],
            viewport_size=(1280, 720),
            preferred_top=menu_state.menu_top,
        )
        left, top, _width, height = spawn_settings_panel_rect(panel)
        cancel_point = (left + 300, top + height - 36)
        next_panel, consumed = handle_spawn_settings_click(panel, cancel_point)
        self.assertTrue(consumed)
        self.assertFalse(next_panel.is_open)

    def test_set_does_not_preview_or_spawn(self) -> None:
        menu_state = open_spawn_menu((200.0, 120.0), (1280, 720), len(self.templates))
        panel = open_spawn_settings_panel(
            menu_state=menu_state,
            selected_template=self.templates[0],
            viewport_size=(1280, 720),
            preferred_top=menu_state.menu_top,
        )
        set_rect = spawn_settings_set_button_rect(panel)
        set_point = (set_rect[0] + 4, set_rect[1] + 4)
        next_panel, consumed = handle_spawn_settings_click(panel, set_point)
        self.assertTrue(consumed)
        self.assertTrue(next_panel.is_open)
        self.assertEqual(next_panel.note_text, SETTINGS_PENDING_NOTE)
        self.assertFalse(hasattr(next_panel, "preview"))

    def test_menu_row_index_helper(self) -> None:
        menu_state = open_spawn_menu((200.0, 120.0), (1280, 720), len(self.templates))
        point = (menu_state.menu_left + 5, menu_state.menu_top + 5)
        index = spawn_menu_item_index_at_point(menu_state, point, len(self.templates))
        self.assertEqual(index, 0)

    def test_menu_row_top_helper(self) -> None:
        menu_state = open_spawn_menu((200.0, 120.0), (1280, 720), len(self.templates))
        top = spawn_menu_row_top_for_index(menu_state, menu_state.scroll_offset)
        self.assertEqual(top, menu_state.menu_top)

    def test_mouse_wheel_over_menu_consumption_condition_helper(self) -> None:
        menu_state = open_spawn_menu((200.0, 120.0), (1280, 720), len(self.templates))
        inside = (menu_state.menu_left + 2, menu_state.menu_top + 2)
        outside = (20, 20)
        self.assertTrue(is_point_in_spawn_menu(menu_state, inside))
        self.assertFalse(is_point_in_spawn_menu(menu_state, outside))

    def test_close_spawn_settings_panel_resets_state(self) -> None:
        self.assertFalse(close_spawn_settings_panel().is_open)


if __name__ == "__main__":
    unittest.main()
