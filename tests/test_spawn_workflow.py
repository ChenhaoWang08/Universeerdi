import unittest

from src.universe.spawn_workflow import (
    SETTINGS_VALID_NOTE,
    SPAWN_MENU_OFFSET_X,
    SPAWN_MENU_WIDTH,
    SPAWN_SETTINGS_FIELD_ROW_HEIGHT,
    SPAWN_SETTINGS_FIELD_START_TOP,
    SPAWN_SETTINGS_FIELD_TEXT_PADDING_X,
    SpawnSettingsState,
    build_spawn_templates,
    click_spawn_menu_item,
    clamp_spawn_menu_scroll,
    close_spawn_settings_panel,
    compute_density_kg_m3,
    compute_volume_m3,
    create_spawn_draft,
    focus_spawn_settings_field_at_point,
    get_spawn_text_input,
    handle_spawn_settings_click,
    handle_spawn_settings_keydown,
    is_point_in_spawn_menu,
    open_spawn_menu,
    open_spawn_settings_panel,
    parse_color_rgb_text,
    spawn_menu_item_index_at_point,
    spawn_menu_max_scroll,
    spawn_menu_rect,
    spawn_menu_row_top_for_index,
    spawn_menu_scroll,
    spawn_settings_editable_field_ids,
    spawn_settings_field_rect,
    spawn_settings_panel_rect,
    spawn_settings_set_button_rect,
    spawn_text_input_text,
    update_spawn_menu_hover,
    validate_spawn_settings,
)


class SpawnWorkflowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.templates = build_spawn_templates()

    def _open_settings_panel(self) -> SpawnSettingsState:
        menu_state = open_spawn_menu((200.0, 120.0), (1280, 720), len(self.templates))
        click_point = (menu_state.menu_left + 12, menu_state.menu_top + 12)
        _next_menu, settings_state, consumed = click_spawn_menu_item(
            menu_state,
            click_point,
            self.templates,
            (1280, 720),
        )
        self.assertTrue(consumed)
        return settings_state

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
        settings_state = self._open_settings_panel()
        self.assertFalse(hasattr(settings_state, "preview"))

    def test_clicking_item_does_not_spawn_body(self) -> None:
        settings_state = self._open_settings_panel()
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

    def test_focusing_field_does_not_clear_existing_text(self) -> None:
        panel = self._open_settings_panel()
        name_before = spawn_text_input_text(panel, "name")
        field_rect = spawn_settings_field_rect(panel, "name")
        point = (field_rect[0] + 2, field_rect[1] + 2)
        focused_panel, consumed = focus_spawn_settings_field_at_point(panel, point)
        self.assertTrue(consumed)
        self.assertEqual(spawn_text_input_text(focused_panel, "name"), name_before)

    def test_cursor_index_is_clamped(self) -> None:
        panel = self._open_settings_panel()
        field_rect = spawn_settings_field_rect(panel, "name")
        point = (field_rect[0] + 2000, field_rect[1] + 4)
        focused_panel, _ = focus_spawn_settings_field_at_point(panel, point)
        text = spawn_text_input_text(focused_panel, "name")
        text_input = get_spawn_text_input(focused_panel, "name")
        self.assertEqual(text_input.cursor_index, len(text))

    def test_clicking_x_position_sets_cursor(self) -> None:
        panel = self._open_settings_panel()
        field_rect = spawn_settings_field_rect(panel, "name")
        point = (field_rect[0] + SPAWN_SETTINGS_FIELD_TEXT_PADDING_X + 18, field_rect[1] + 4)
        focused_panel, _ = focus_spawn_settings_field_at_point(panel, point)
        text_input = get_spawn_text_input(focused_panel, "name")
        self.assertGreaterEqual(text_input.cursor_index, 1)

    def test_typing_inserts_text_at_cursor(self) -> None:
        panel = self._open_settings_panel()
        field_rect = spawn_settings_field_rect(panel, "name")
        focused_panel, _ = focus_spawn_settings_field_at_point(panel, (field_rect[0] + 2, field_rect[1] + 2))
        next_panel, consumed = handle_spawn_settings_keydown(
            focused_panel,
            key="",
            text="Z",
            command_or_control=False,
            shift=False,
        )
        self.assertTrue(consumed)
        self.assertTrue(spawn_text_input_text(next_panel, "name").startswith("Z"))

    def test_typing_replaces_selected_text(self) -> None:
        panel = self._open_settings_panel()
        field_rect = spawn_settings_field_rect(panel, "name")
        focused_panel, _ = focus_spawn_settings_field_at_point(panel, (field_rect[0] + 2, field_rect[1] + 2))
        selected_panel, _ = handle_spawn_settings_keydown(
            focused_panel,
            key="a",
            text="",
            command_or_control=True,
            shift=False,
        )
        replaced_panel, _ = handle_spawn_settings_keydown(
            selected_panel,
            key="",
            text="X",
            command_or_control=False,
            shift=False,
        )
        self.assertEqual(spawn_text_input_text(replaced_panel, "name"), "X")

    def test_backspace_deletes_previous_character(self) -> None:
        panel = self._open_settings_panel()
        field_rect = spawn_settings_field_rect(panel, "name")
        focused_panel, _ = focus_spawn_settings_field_at_point(panel, (field_rect[0] + 200, field_rect[1] + 2))
        before = spawn_text_input_text(focused_panel, "name")
        next_panel, _ = handle_spawn_settings_keydown(
            focused_panel,
            key="backspace",
            text="",
            command_or_control=False,
            shift=False,
        )
        self.assertEqual(len(spawn_text_input_text(next_panel, "name")), max(0, len(before) - 1))

    def test_backspace_deletes_selection(self) -> None:
        panel = self._open_settings_panel()
        field_rect = spawn_settings_field_rect(panel, "name")
        focused_panel, _ = focus_spawn_settings_field_at_point(panel, (field_rect[0] + 2, field_rect[1] + 2))
        selected_panel, _ = handle_spawn_settings_keydown(
            focused_panel,
            key="a",
            text="",
            command_or_control=True,
            shift=False,
        )
        next_panel, _ = handle_spawn_settings_keydown(
            selected_panel,
            key="backspace",
            text="",
            command_or_control=False,
            shift=False,
        )
        self.assertEqual(spawn_text_input_text(next_panel, "name"), "")

    def test_delete_deletes_next_character(self) -> None:
        panel = self._open_settings_panel()
        field_rect = spawn_settings_field_rect(panel, "name")
        focused_panel, _ = focus_spawn_settings_field_at_point(panel, (field_rect[0] + 2, field_rect[1] + 2))
        before = spawn_text_input_text(focused_panel, "name")
        next_panel, _ = handle_spawn_settings_keydown(
            focused_panel,
            key="delete",
            text="",
            command_or_control=False,
            shift=False,
        )
        self.assertEqual(len(spawn_text_input_text(next_panel, "name")), max(0, len(before) - 1))

    def test_delete_deletes_selection(self) -> None:
        panel = self._open_settings_panel()
        field_rect = spawn_settings_field_rect(panel, "name")
        focused_panel, _ = focus_spawn_settings_field_at_point(panel, (field_rect[0] + 2, field_rect[1] + 2))
        selected_panel, _ = handle_spawn_settings_keydown(
            focused_panel,
            key="a",
            text="",
            command_or_control=True,
            shift=False,
        )
        next_panel, _ = handle_spawn_settings_keydown(
            selected_panel,
            key="delete",
            text="",
            command_or_control=False,
            shift=False,
        )
        self.assertEqual(spawn_text_input_text(next_panel, "name"), "")

    def test_left_and_right_arrow_move_cursor(self) -> None:
        panel = self._open_settings_panel()
        field_rect = spawn_settings_field_rect(panel, "name")
        focused_panel, _ = focus_spawn_settings_field_at_point(panel, (field_rect[0] + 200, field_rect[1] + 2))
        left_panel, _ = handle_spawn_settings_keydown(
            focused_panel,
            key="left",
            text="",
            command_or_control=False,
            shift=False,
        )
        right_panel, _ = handle_spawn_settings_keydown(
            left_panel,
            key="right",
            text="",
            command_or_control=False,
            shift=False,
        )
        self.assertEqual(
            get_spawn_text_input(right_panel, "name").cursor_index,
            get_spawn_text_input(focused_panel, "name").cursor_index,
        )

    def test_ctrl_or_cmd_a_selects_all(self) -> None:
        panel = self._open_settings_panel()
        field_rect = spawn_settings_field_rect(panel, "name")
        focused_panel, _ = focus_spawn_settings_field_at_point(panel, (field_rect[0] + 2, field_rect[1] + 2))
        selected_panel, consumed = handle_spawn_settings_keydown(
            focused_panel,
            key="a",
            text="",
            command_or_control=True,
            shift=False,
        )
        self.assertTrue(consumed)
        text_input = get_spawn_text_input(selected_panel, "name")
        self.assertEqual(text_input.selection_anchor, 0)
        self.assertEqual(text_input.selection_focus, len(text_input.text))

    def test_escape_clears_focus_before_panel_close(self) -> None:
        panel = self._open_settings_panel()
        field_rect = spawn_settings_field_rect(panel, "name")
        focused_panel, _ = focus_spawn_settings_field_at_point(panel, (field_rect[0] + 2, field_rect[1] + 2))
        next_panel, consumed = handle_spawn_settings_keydown(
            focused_panel,
            key="escape",
            text="",
            command_or_control=False,
            shift=False,
        )
        self.assertTrue(consumed)
        self.assertTrue(next_panel.is_open)
        self.assertIsNone(next_panel.focused_field_id)

    def test_text_input_updates_name_without_changing_template(self) -> None:
        panel = self._open_settings_panel()
        original_template = next(template for template in self.templates if template.display_name == "Sun")
        field_rect = spawn_settings_field_rect(panel, "name")
        focused_panel, _ = focus_spawn_settings_field_at_point(panel, (field_rect[0] + 2, field_rect[1] + 2))
        next_panel, _ = handle_spawn_settings_keydown(
            focused_panel,
            key="",
            text="Q",
            command_or_control=False,
            shift=False,
        )
        self.assertTrue(spawn_text_input_text(next_panel, "name").startswith("Q"))
        self.assertEqual(original_template.display_name, "Sun")

    def test_typing_m_is_consumed_by_field_logic(self) -> None:
        panel = self._open_settings_panel()
        field_rect = spawn_settings_field_rect(panel, "name")
        focused_panel, _ = focus_spawn_settings_field_at_point(panel, (field_rect[0] + 2, field_rect[1] + 2))
        _next_panel, consumed = handle_spawn_settings_keydown(
            focused_panel,
            key="",
            text="M",
            command_or_control=False,
            shift=False,
        )
        self.assertTrue(consumed)

    def test_valid_mass_radius_velocity_and_rgb_parse(self) -> None:
        self.assertEqual(parse_color_rgb_text("111,163,245"), (111, 163, 245))
        self.assertEqual(parse_color_rgb_text("20, 20, 24"), (20, 20, 24))

    def test_invalid_mass_is_rejected(self) -> None:
        panel = self._open_settings_panel()
        panel = self._set_field_text(panel, "mass_kg", "abc")
        validated = validate_spawn_settings(panel)
        self.assertIsNotNone(next((e for e in validated.validation_errors if e.field_id == "mass_kg"), None))

    def test_invalid_radius_is_rejected(self) -> None:
        panel = self._open_settings_panel()
        panel = self._set_field_text(panel, "radius_m", "")
        validated = validate_spawn_settings(panel)
        self.assertIsNotNone(next((e for e in validated.validation_errors if e.field_id == "radius_m"), None))

    def test_negative_velocity_is_allowed(self) -> None:
        panel = self._open_settings_panel()
        panel = self._set_field_text(panel, "velocity_x_m_s", "-123.4")
        panel = self._set_field_text(panel, "velocity_y_m_s", "-1e3")
        validated = validate_spawn_settings(panel)
        self.assertFalse(any(e.field_id == "velocity_x_m_s" for e in validated.validation_errors))
        self.assertFalse(any(e.field_id == "velocity_y_m_s" for e in validated.validation_errors))

    def test_invalid_rgb_is_rejected(self) -> None:
        self.assertIsNone(parse_color_rgb_text("300,20,24"))
        self.assertIsNone(parse_color_rgb_text("abc"))
        self.assertIsNone(parse_color_rgb_text("20,20,24,1"))

    def test_volume_and_density_read_only_not_focusable(self) -> None:
        panel = self._open_settings_panel()
        row_y = (
            panel.panel_top
            + SPAWN_SETTINGS_FIELD_START_TOP
            + (len(spawn_settings_editable_field_ids()) * SPAWN_SETTINGS_FIELD_ROW_HEIGHT)
            + 12
        )
        point = (panel.panel_left + 20, row_y)
        next_panel, consumed = handle_spawn_settings_click(panel, point)
        self.assertTrue(consumed)
        self.assertIsNone(next_panel.focused_field_id)

    def test_set_with_valid_fields_shows_valid_note_and_no_preview_spawn(self) -> None:
        panel = self._open_settings_panel()
        panel = self._set_field_text(panel, "name", "EarthX")
        panel = self._set_field_text(panel, "mass_kg", "5.97217e24")
        panel = self._set_field_text(panel, "radius_m", "6.3710084e6")
        panel = self._set_field_text(panel, "velocity_x_m_s", "-12.0")
        panel = self._set_field_text(panel, "velocity_y_m_s", "33.0")
        panel = self._set_field_text(panel, "color_rgb", "111,163,245")
        validated = validate_spawn_settings(panel)
        self.assertEqual(validated.note_text, SETTINGS_VALID_NOTE)
        self.assertTrue(validated.is_open)
        self.assertFalse(hasattr(validated, "preview"))
        self.assertFalse(hasattr(validated, "spawn_action"))

    def test_set_with_invalid_fields_shows_errors_and_no_preview_spawn(self) -> None:
        panel = self._open_settings_panel()
        panel = self._set_field_text(panel, "mass_kg", "")
        validated = validate_spawn_settings(panel)
        self.assertTrue(validated.validation_errors)
        self.assertTrue(validated.is_open)
        self.assertFalse(hasattr(validated, "preview"))
        self.assertFalse(hasattr(validated, "spawn_action"))

    def test_cancel_closes_settings_panel(self) -> None:
        panel = self._open_settings_panel()
        left, top, _width, height = spawn_settings_panel_rect(panel)
        cancel_point = (left + 300, top + height - 36)
        next_panel, consumed = handle_spawn_settings_click(panel, cancel_point)
        self.assertTrue(consumed)
        self.assertFalse(next_panel.is_open)

    def test_set_button_click_runs_validation_and_keeps_panel_open(self) -> None:
        panel = self._open_settings_panel()
        panel = self._set_field_text(panel, "name", "ValidName")
        set_rect = spawn_settings_set_button_rect(panel)
        next_panel, consumed = handle_spawn_settings_click(panel, (set_rect[0] + 3, set_rect[1] + 3))
        self.assertTrue(consumed)
        self.assertTrue(next_panel.is_open)

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

    def _set_field_text(self, panel: SpawnSettingsState, field_id: str, value: str) -> SpawnSettingsState:
        field_rect = spawn_settings_field_rect(panel, field_id)
        focus_point = (field_rect[0] + 2, field_rect[1] + 2)
        focused_panel, _ = focus_spawn_settings_field_at_point(panel, focus_point)
        selected_panel, _ = handle_spawn_settings_keydown(
            focused_panel,
            key="a",
            text="",
            command_or_control=True,
            shift=False,
        )
        next_panel = selected_panel
        if value == "":
            next_panel, _ = handle_spawn_settings_keydown(
                next_panel,
                key="backspace",
                text="",
                command_or_control=False,
                shift=False,
            )
            return next_panel
        for character in value:
            next_panel, _ = handle_spawn_settings_keydown(
                next_panel,
                key="",
                text=character,
                command_or_control=False,
                shift=False,
            )
        return next_panel


if __name__ == "__main__":
    unittest.main()
