from __future__ import annotations

from dataclasses import dataclass, replace
from math import pi
from typing import Optional, Sequence, Tuple

from .solar_system_data import get_solar_system_bodies

Color = Tuple[int, int, int]
Point = Tuple[float, float]
Rect = Tuple[int, int, int, int]
Size = Tuple[int, int]

SPAWN_MENU_WIDTH = 220
SPAWN_MENU_HEIGHT = 280
SPAWN_MENU_ROW_HEIGHT = 30
SPAWN_MENU_OFFSET_X = 12

SPAWN_SETTINGS_PANEL_WIDTH = 360
SPAWN_SETTINGS_PANEL_HEIGHT = 360
SPAWN_SETTINGS_PANEL_OFFSET_X = 12
SPAWN_SETTINGS_BUTTON_WIDTH = 88
SPAWN_SETTINGS_BUTTON_HEIGHT = 32
SPAWN_SETTINGS_BUTTON_GAP = 12

SPAWN_SETTINGS_TITLE_TOP = 12
SPAWN_SETTINGS_FIELD_START_TOP = 46
SPAWN_SETTINGS_FIELD_ROW_HEIGHT = 34
SPAWN_SETTINGS_FIELD_LABEL_WIDTH = 84
SPAWN_SETTINGS_FIELD_HEIGHT = 26
SPAWN_SETTINGS_FIELD_TEXT_PADDING_X = 6
SPAWN_SETTINGS_FIELD_APPROX_CHAR_WIDTH = 9
SPAWN_SETTINGS_FIELD_BOX_LEFT_PADDING = 12
SPAWN_SETTINGS_FIELD_BOX_RIGHT_PADDING = 12

SETTINGS_PENDING_NOTE = "Preview/spawn will be added in a later PR"
SETTINGS_VALID_NOTE = "Draft valid. Preview/spawn will be added in a later PR."
SETTINGS_INVALID_NOTE = "Please fix invalid fields before proceeding."

EDITABLE_FIELD_IDS = (
    "name",
    "mass_kg",
    "radius_m",
    "velocity_x_m_s",
    "velocity_y_m_s",
    "color_rgb",
)

EDITABLE_FIELD_LABELS = {
    "name": "Name",
    "mass_kg": "Mass kg",
    "radius_m": "Radius m",
    "velocity_x_m_s": "Velocity X",
    "velocity_y_m_s": "Velocity Y",
    "color_rgb": "Color RGB",
}


@dataclass(frozen=True)
class SpawnTemplate:
    template_id: str
    display_name: str
    category: str
    mass_kg: float
    radius_m: float
    color_rgb: Color
    default_velocity_x_m_s: float = 0.0
    default_velocity_y_m_s: float = 0.0
    source_label: str = ""
    is_black_hole_placeholder: bool = False


@dataclass(frozen=True)
class SpawnDraft:
    template_id: str
    custom_name: str
    category: str
    mass_kg: float
    radius_m: float
    velocity_x_m_s: float
    velocity_y_m_s: float
    color_rgb: Color
    is_black_hole_placeholder: bool = False


@dataclass(frozen=True)
class SpawnMenuState:
    is_open: bool = False
    menu_left: int = 0
    menu_top: int = 0
    scroll_offset: int = 0
    hovered_template_id: Optional[str] = None


@dataclass(frozen=True)
class TextInputState:
    field_id: str
    text: str
    cursor_index: int = 0
    selection_anchor: Optional[int] = None
    selection_focus: Optional[int] = None


@dataclass(frozen=True)
class FieldValidationError:
    field_id: str
    message: str


@dataclass(frozen=True)
class SpawnSettingsState:
    is_open: bool = False
    panel_left: int = 0
    panel_top: int = 0
    selected_template_id: Optional[str] = None
    draft: Optional[SpawnDraft] = None
    note_text: Optional[str] = None
    text_inputs: Tuple[TextInputState, ...] = ()
    focused_field_id: Optional[str] = None
    validation_errors: Tuple[FieldValidationError, ...] = ()


def build_spawn_templates() -> Tuple[SpawnTemplate, ...]:
    templates = [
        SpawnTemplate(
            template_id=body.name.lower(),
            display_name=body.name,
            category=body.category,
            mass_kg=body.mass_kg,
            radius_m=body.mean_radius_m,
            color_rgb=body.color_rgb,
            source_label="solar_system_data",
        )
        for body in get_solar_system_bodies()
    ]
    templates.append(
        SpawnTemplate(
            template_id="black_hole_placeholder",
            display_name="Black Hole placeholder",
            category="black_hole_placeholder",
            mass_kg=1.989e31,
            radius_m=7.0e6,
            color_rgb=(20, 20, 24),
            source_label="local placeholder, not a physical black hole simulation",
            is_black_hole_placeholder=True,
        )
    )
    return tuple(templates)


def create_spawn_draft(template: SpawnTemplate) -> SpawnDraft:
    return SpawnDraft(
        template_id=template.template_id,
        custom_name=template.display_name,
        category=template.category,
        mass_kg=template.mass_kg,
        radius_m=template.radius_m,
        velocity_x_m_s=template.default_velocity_x_m_s,
        velocity_y_m_s=template.default_velocity_y_m_s,
        color_rgb=template.color_rgb,
        is_black_hole_placeholder=template.is_black_hole_placeholder,
    )


def _create_text_inputs_from_draft(draft: SpawnDraft) -> Tuple[TextInputState, ...]:
    return (
        TextInputState(field_id="name", text=draft.custom_name, cursor_index=len(draft.custom_name)),
        TextInputState(field_id="mass_kg", text=f"{draft.mass_kg:.6e}", cursor_index=0),
        TextInputState(field_id="radius_m", text=f"{draft.radius_m:.6e}", cursor_index=0),
        TextInputState(field_id="velocity_x_m_s", text=f"{draft.velocity_x_m_s:.3f}", cursor_index=0),
        TextInputState(field_id="velocity_y_m_s", text=f"{draft.velocity_y_m_s:.3f}", cursor_index=0),
        TextInputState(
            field_id="color_rgb",
            text=f"{draft.color_rgb[0]},{draft.color_rgb[1]},{draft.color_rgb[2]}",
            cursor_index=0,
        ),
    )


def find_template_by_id(
    templates: Sequence[SpawnTemplate],
    template_id: str,
) -> Optional[SpawnTemplate]:
    for template in templates:
        if template.template_id == template_id:
            return template
    return None


def spawn_menu_visible_row_count() -> int:
    return max(1, SPAWN_MENU_HEIGHT // SPAWN_MENU_ROW_HEIGHT)


def spawn_menu_max_scroll(template_count: int) -> int:
    return max(0, template_count - spawn_menu_visible_row_count())


def clamp_spawn_menu_scroll(scroll_offset: int, template_count: int) -> int:
    return max(0, min(spawn_menu_max_scroll(template_count), scroll_offset))


def open_spawn_menu(mouse_position: Point, viewport_size: Size, template_count: int) -> SpawnMenuState:
    mouse_x, mouse_y = int(mouse_position[0]), int(mouse_position[1])
    menu_left = mouse_x + SPAWN_MENU_OFFSET_X
    menu_top = mouse_y

    if menu_left + SPAWN_MENU_WIDTH > viewport_size[0]:
        menu_left = mouse_x - SPAWN_MENU_WIDTH - SPAWN_MENU_OFFSET_X
    if menu_top + SPAWN_MENU_HEIGHT > viewport_size[1]:
        menu_top = viewport_size[1] - SPAWN_MENU_HEIGHT - 12

    menu_left = max(12, menu_left)
    menu_top = max(12, menu_top)

    return SpawnMenuState(
        is_open=True,
        menu_left=menu_left,
        menu_top=menu_top,
        scroll_offset=clamp_spawn_menu_scroll(0, template_count),
        hovered_template_id=None,
    )


def close_spawn_menu() -> SpawnMenuState:
    return SpawnMenuState()


def spawn_menu_rect(state: SpawnMenuState) -> Rect:
    return (state.menu_left, state.menu_top, SPAWN_MENU_WIDTH, SPAWN_MENU_HEIGHT)


def is_point_in_rect(point: Point, rect: Rect) -> bool:
    x, y = point
    left, top, width, height = rect
    return left <= x <= (left + width) and top <= y <= (top + height)


def is_point_in_spawn_menu(state: SpawnMenuState, point: Point) -> bool:
    return state.is_open and is_point_in_rect(point, spawn_menu_rect(state))


def spawn_menu_scroll(state: SpawnMenuState, wheel_y: int, template_count: int) -> SpawnMenuState:
    if not state.is_open or wheel_y == 0:
        return state
    next_offset = clamp_spawn_menu_scroll(state.scroll_offset - wheel_y, template_count)
    return replace(state, scroll_offset=next_offset)


def spawn_menu_item_index_at_point(
    state: SpawnMenuState,
    point: Point,
    template_count: int,
) -> Optional[int]:
    if not is_point_in_spawn_menu(state, point):
        return None

    local_y = int(point[1]) - state.menu_top
    visible_row = local_y // SPAWN_MENU_ROW_HEIGHT
    if visible_row < 0 or visible_row >= spawn_menu_visible_row_count():
        return None

    absolute_index = state.scroll_offset + visible_row
    if absolute_index < 0 or absolute_index >= template_count:
        return None
    return absolute_index


def spawn_menu_row_top_for_index(state: SpawnMenuState, index: int) -> int:
    return state.menu_top + ((index - state.scroll_offset) * SPAWN_MENU_ROW_HEIGHT)


def update_spawn_menu_hover(
    state: SpawnMenuState,
    point: Point,
    templates: Sequence[SpawnTemplate],
) -> SpawnMenuState:
    if not state.is_open:
        return state

    index = spawn_menu_item_index_at_point(state, point, len(templates))
    hovered_template_id = templates[index].template_id if index is not None else None
    if hovered_template_id == state.hovered_template_id:
        return state
    return replace(state, hovered_template_id=hovered_template_id)


def click_spawn_menu_item(
    state: SpawnMenuState,
    point: Point,
    templates: Sequence[SpawnTemplate],
    viewport_size: Size,
) -> Tuple[SpawnMenuState, SpawnSettingsState, bool]:
    if not state.is_open:
        return state, SpawnSettingsState(), False

    index = spawn_menu_item_index_at_point(state, point, len(templates))
    if index is None:
        return state, SpawnSettingsState(), False

    template = templates[index]
    row_top = spawn_menu_row_top_for_index(state, index)
    settings_state = open_spawn_settings_panel(
        menu_state=state,
        selected_template=template,
        viewport_size=viewport_size,
        preferred_top=row_top,
    )
    return close_spawn_menu(), settings_state, True


def open_spawn_settings_panel(
    *,
    menu_state: SpawnMenuState,
    selected_template: SpawnTemplate,
    viewport_size: Size,
    preferred_top: int,
) -> SpawnSettingsState:
    menu_left, _menu_top, menu_width, _menu_height = spawn_menu_rect(menu_state)
    panel_left = menu_left + menu_width + SPAWN_SETTINGS_PANEL_OFFSET_X
    panel_top = preferred_top

    if panel_left + SPAWN_SETTINGS_PANEL_WIDTH > viewport_size[0]:
        panel_left = menu_left - SPAWN_SETTINGS_PANEL_WIDTH - SPAWN_SETTINGS_PANEL_OFFSET_X
    if panel_top + SPAWN_SETTINGS_PANEL_HEIGHT > viewport_size[1]:
        panel_top = viewport_size[1] - SPAWN_SETTINGS_PANEL_HEIGHT - 12

    panel_left = max(12, panel_left)
    panel_top = max(12, panel_top)
    draft = create_spawn_draft(selected_template)

    return SpawnSettingsState(
        is_open=True,
        panel_left=panel_left,
        panel_top=panel_top,
        selected_template_id=selected_template.template_id,
        draft=draft,
        note_text=None,
        text_inputs=_create_text_inputs_from_draft(draft),
        focused_field_id=None,
        validation_errors=(),
    )


def close_spawn_settings_panel() -> SpawnSettingsState:
    return SpawnSettingsState()


def spawn_settings_panel_rect(state: SpawnSettingsState) -> Rect:
    return (
        state.panel_left,
        state.panel_top,
        SPAWN_SETTINGS_PANEL_WIDTH,
        SPAWN_SETTINGS_PANEL_HEIGHT,
    )


def is_point_in_spawn_settings_panel(state: SpawnSettingsState, point: Point) -> bool:
    return state.is_open and is_point_in_rect(point, spawn_settings_panel_rect(state))


def spawn_settings_set_button_rect(state: SpawnSettingsState) -> Rect:
    left, top, width, height = spawn_settings_panel_rect(state)
    button_top = top + height - 52
    set_left = left + width - ((SPAWN_SETTINGS_BUTTON_WIDTH * 2) + SPAWN_SETTINGS_BUTTON_GAP + 16)
    return (set_left, button_top, SPAWN_SETTINGS_BUTTON_WIDTH, SPAWN_SETTINGS_BUTTON_HEIGHT)


def spawn_settings_cancel_button_rect(state: SpawnSettingsState) -> Rect:
    set_left, button_top, _button_width, _button_height = spawn_settings_set_button_rect(state)
    cancel_left = set_left + SPAWN_SETTINGS_BUTTON_WIDTH + SPAWN_SETTINGS_BUTTON_GAP
    return (cancel_left, button_top, SPAWN_SETTINGS_BUTTON_WIDTH, SPAWN_SETTINGS_BUTTON_HEIGHT)


def spawn_settings_field_rect(state: SpawnSettingsState, field_id: str) -> Rect:
    editable_index = EDITABLE_FIELD_IDS.index(field_id)
    left = state.panel_left + SPAWN_SETTINGS_FIELD_BOX_LEFT_PADDING + SPAWN_SETTINGS_FIELD_LABEL_WIDTH
    top = state.panel_top + SPAWN_SETTINGS_FIELD_START_TOP + (editable_index * SPAWN_SETTINGS_FIELD_ROW_HEIGHT)
    width = (
        SPAWN_SETTINGS_PANEL_WIDTH
        - SPAWN_SETTINGS_FIELD_LABEL_WIDTH
        - SPAWN_SETTINGS_FIELD_BOX_LEFT_PADDING
        - SPAWN_SETTINGS_FIELD_BOX_RIGHT_PADDING
    )
    return (left, top, width, SPAWN_SETTINGS_FIELD_HEIGHT)


def spawn_settings_editable_field_ids() -> Tuple[str, ...]:
    return EDITABLE_FIELD_IDS


def _clamp_cursor_index(text: str, cursor_index: int) -> int:
    return max(0, min(len(text), cursor_index))


def _normalize_selection(input_state: TextInputState) -> Optional[Tuple[int, int]]:
    if input_state.selection_anchor is None or input_state.selection_focus is None:
        return None
    start = _clamp_cursor_index(input_state.text, input_state.selection_anchor)
    end = _clamp_cursor_index(input_state.text, input_state.selection_focus)
    if start == end:
        return None
    return (min(start, end), max(start, end))


def _clear_selection(input_state: TextInputState) -> TextInputState:
    return replace(input_state, selection_anchor=None, selection_focus=None)


def get_spawn_text_input(state: SpawnSettingsState, field_id: str) -> Optional[TextInputState]:
    for text_input in state.text_inputs:
        if text_input.field_id == field_id:
            return text_input
    return None


def _replace_spawn_text_input(state: SpawnSettingsState, updated: TextInputState) -> SpawnSettingsState:
    inputs = []
    for text_input in state.text_inputs:
        if text_input.field_id == updated.field_id:
            inputs.append(updated)
        else:
            inputs.append(text_input)
    return replace(state, text_inputs=tuple(inputs))


def spawn_text_input_text(state: SpawnSettingsState, field_id: str) -> str:
    text_input = get_spawn_text_input(state, field_id)
    return text_input.text if text_input is not None else ""


def _cursor_index_from_point(text: str, point_x: float, rect_left: int) -> int:
    content_x = point_x - rect_left - SPAWN_SETTINGS_FIELD_TEXT_PADDING_X
    approx = int(round(content_x / SPAWN_SETTINGS_FIELD_APPROX_CHAR_WIDTH))
    return _clamp_cursor_index(text, approx)


def focus_spawn_settings_field_at_point(
    state: SpawnSettingsState,
    point: Point,
) -> Tuple[SpawnSettingsState, bool]:
    if not state.is_open:
        return state, False

    for field_id in EDITABLE_FIELD_IDS:
        field_rect = spawn_settings_field_rect(state, field_id)
        if not is_point_in_rect(point, field_rect):
            continue

        text_input = get_spawn_text_input(state, field_id)
        if text_input is None:
            return state, False
        next_cursor = _cursor_index_from_point(text_input.text, point[0], field_rect[0])
        focused_input = replace(
            text_input,
            cursor_index=next_cursor,
            selection_anchor=None,
            selection_focus=None,
        )
        next_state = _replace_spawn_text_input(state, focused_input)
        return replace(next_state, focused_field_id=field_id), True

    return state, False


def clear_spawn_settings_focus(state: SpawnSettingsState) -> SpawnSettingsState:
    if state.focused_field_id is None:
        return state
    focused_input = get_spawn_text_input(state, state.focused_field_id)
    next_state = state
    if focused_input is not None:
        next_state = _replace_spawn_text_input(next_state, _clear_selection(focused_input))
    return replace(next_state, focused_field_id=None)


def _replace_selection_or_insert(input_state: TextInputState, inserted_text: str) -> TextInputState:
    selection = _normalize_selection(input_state)
    if selection is None:
        cursor = _clamp_cursor_index(input_state.text, input_state.cursor_index)
        next_text = input_state.text[:cursor] + inserted_text + input_state.text[cursor:]
        next_cursor = cursor + len(inserted_text)
    else:
        start, end = selection
        next_text = input_state.text[:start] + inserted_text + input_state.text[end:]
        next_cursor = start + len(inserted_text)

    return TextInputState(
        field_id=input_state.field_id,
        text=next_text,
        cursor_index=next_cursor,
        selection_anchor=None,
        selection_focus=None,
    )


def _delete_backward(input_state: TextInputState) -> TextInputState:
    selection = _normalize_selection(input_state)
    if selection is not None:
        start, end = selection
        next_text = input_state.text[:start] + input_state.text[end:]
        return TextInputState(
            field_id=input_state.field_id,
            text=next_text,
            cursor_index=start,
            selection_anchor=None,
            selection_focus=None,
        )

    cursor = _clamp_cursor_index(input_state.text, input_state.cursor_index)
    if cursor == 0:
        return _clear_selection(input_state)

    next_text = input_state.text[: cursor - 1] + input_state.text[cursor:]
    return TextInputState(
        field_id=input_state.field_id,
        text=next_text,
        cursor_index=cursor - 1,
        selection_anchor=None,
        selection_focus=None,
    )


def _delete_forward(input_state: TextInputState) -> TextInputState:
    selection = _normalize_selection(input_state)
    if selection is not None:
        start, end = selection
        next_text = input_state.text[:start] + input_state.text[end:]
        return TextInputState(
            field_id=input_state.field_id,
            text=next_text,
            cursor_index=start,
            selection_anchor=None,
            selection_focus=None,
        )

    cursor = _clamp_cursor_index(input_state.text, input_state.cursor_index)
    if cursor >= len(input_state.text):
        return _clear_selection(input_state)

    next_text = input_state.text[:cursor] + input_state.text[cursor + 1 :]
    return TextInputState(
        field_id=input_state.field_id,
        text=next_text,
        cursor_index=cursor,
        selection_anchor=None,
        selection_focus=None,
    )


def _move_cursor(input_state: TextInputState, direction: int, shift: bool) -> TextInputState:
    base_cursor = _clamp_cursor_index(input_state.text, input_state.cursor_index)
    if not shift:
        selection = _normalize_selection(input_state)
        if selection is not None:
            boundary = selection[0] if direction < 0 else selection[1]
            return replace(
                input_state,
                cursor_index=boundary,
                selection_anchor=None,
                selection_focus=None,
            )

    next_cursor = _clamp_cursor_index(input_state.text, base_cursor + direction)
    if not shift:
        return replace(
            input_state,
            cursor_index=next_cursor,
            selection_anchor=None,
            selection_focus=None,
        )

    anchor = input_state.selection_anchor
    if anchor is None:
        anchor = base_cursor
    return replace(
        input_state,
        cursor_index=next_cursor,
        selection_anchor=anchor,
        selection_focus=next_cursor,
    )


def _select_all(input_state: TextInputState) -> TextInputState:
    return replace(
        input_state,
        cursor_index=len(input_state.text),
        selection_anchor=0,
        selection_focus=len(input_state.text),
    )


def handle_spawn_settings_keydown(
    state: SpawnSettingsState,
    *,
    key: str,
    text: str,
    command_or_control: bool,
    shift: bool,
) -> Tuple[SpawnSettingsState, bool]:
    if not state.is_open:
        return state, False
    if state.focused_field_id is None:
        return state, False

    focused_input = get_spawn_text_input(state, state.focused_field_id)
    if focused_input is None:
        return state, False

    updated_input = focused_input
    consumed = True

    if command_or_control and key == "a":
        updated_input = _select_all(focused_input)
    elif key == "left":
        updated_input = _move_cursor(focused_input, -1, shift)
    elif key == "right":
        updated_input = _move_cursor(focused_input, 1, shift)
    elif key == "backspace":
        updated_input = _delete_backward(focused_input)
    elif key == "delete":
        updated_input = _delete_forward(focused_input)
    elif key == "escape":
        return clear_spawn_settings_focus(state), True
    elif len(text) == 1 and text.isprintable() and text not in ("\r", "\n", "\t"):
        updated_input = _replace_selection_or_insert(focused_input, text)
    else:
        consumed = False

    if not consumed:
        return state, False

    next_state = _replace_spawn_text_input(state, updated_input)
    return replace(next_state, note_text=None, validation_errors=()), True


def _parse_float_text(text: str) -> Optional[float]:
    stripped = text.strip()
    if not stripped:
        return None
    try:
        return float(stripped)
    except ValueError:
        return None


def parse_color_rgb_text(text: str) -> Optional[Color]:
    parts = [part.strip() for part in text.split(",")]
    if len(parts) != 3:
        return None
    values = []
    for part in parts:
        if not part:
            return None
        try:
            value = int(part)
        except ValueError:
            return None
        if value < 0 or value > 255:
            return None
        values.append(value)
    return (values[0], values[1], values[2])


def validate_spawn_settings(state: SpawnSettingsState) -> SpawnSettingsState:
    if not state.is_open or state.draft is None:
        return state

    name_text = spawn_text_input_text(state, "name")
    mass_text = spawn_text_input_text(state, "mass_kg")
    radius_text = spawn_text_input_text(state, "radius_m")
    velocity_x_text = spawn_text_input_text(state, "velocity_x_m_s")
    velocity_y_text = spawn_text_input_text(state, "velocity_y_m_s")
    color_text = spawn_text_input_text(state, "color_rgb")

    errors: list[FieldValidationError] = []

    mass_value = _parse_float_text(mass_text)
    radius_value = _parse_float_text(radius_text)
    velocity_x_value = _parse_float_text(velocity_x_text)
    velocity_y_value = _parse_float_text(velocity_y_text)
    color_value = parse_color_rgb_text(color_text)

    if not name_text.strip():
        errors.append(FieldValidationError(field_id="name", message="Name cannot be empty."))
    if mass_value is None or mass_value <= 0.0:
        errors.append(FieldValidationError(field_id="mass_kg", message="Mass must be a positive number."))
    if radius_value is None or radius_value <= 0.0:
        errors.append(FieldValidationError(field_id="radius_m", message="Radius must be a positive number."))
    if velocity_x_value is None:
        errors.append(
            FieldValidationError(field_id="velocity_x_m_s", message="Velocity X must be a number.")
        )
    if velocity_y_value is None:
        errors.append(
            FieldValidationError(field_id="velocity_y_m_s", message="Velocity Y must be a number.")
        )
    if color_value is None:
        errors.append(
            FieldValidationError(
                field_id="color_rgb",
                message="Color RGB must be three integers between 0 and 255.",
            )
        )

    if errors:
        return replace(
            state,
            note_text=SETTINGS_INVALID_NOTE,
            validation_errors=tuple(errors),
        )

    assert mass_value is not None
    assert radius_value is not None
    assert velocity_x_value is not None
    assert velocity_y_value is not None
    assert color_value is not None

    next_draft = replace(
        state.draft,
        custom_name=name_text.strip(),
        mass_kg=mass_value,
        radius_m=radius_value,
        velocity_x_m_s=velocity_x_value,
        velocity_y_m_s=velocity_y_value,
        color_rgb=color_value,
    )

    return replace(
        state,
        draft=next_draft,
        note_text=SETTINGS_VALID_NOTE,
        validation_errors=(),
    )


def spawn_settings_error_for_field(
    state: SpawnSettingsState,
    field_id: str,
) -> Optional[str]:
    for error in state.validation_errors:
        if error.field_id == field_id:
            return error.message
    return None


def handle_spawn_settings_click(
    state: SpawnSettingsState,
    point: Point,
) -> Tuple[SpawnSettingsState, bool]:
    if not state.is_open:
        return state, False

    if is_point_in_rect(point, spawn_settings_cancel_button_rect(state)):
        return close_spawn_settings_panel(), True
    if is_point_in_rect(point, spawn_settings_set_button_rect(state)):
        return validate_spawn_settings(state), True

    focused_state, focused = focus_spawn_settings_field_at_point(state, point)
    if focused:
        return replace(focused_state, note_text=None, validation_errors=()), True
    if is_point_in_spawn_settings_panel(state, point):
        return clear_spawn_settings_focus(state), True
    return state, False


def compute_volume_m3(radius_m: float) -> float:
    if radius_m <= 0.0:
        return 0.0
    return (4.0 / 3.0) * pi * (radius_m**3)


def compute_density_kg_m3(mass_kg: float, radius_m: float) -> float:
    volume = compute_volume_m3(radius_m)
    if volume <= 0.0:
        return 0.0
    return mass_kg / volume


def _parsed_mass_radius_from_text(state: SpawnSettingsState) -> Tuple[Optional[float], Optional[float]]:
    return (
        _parse_float_text(spawn_text_input_text(state, "mass_kg")),
        _parse_float_text(spawn_text_input_text(state, "radius_m")),
    )


def spawn_settings_display_lines(state: SpawnSettingsState) -> Tuple[str, ...]:
    if not state.is_open or state.draft is None:
        return ()

    mass_from_text, radius_from_text = _parsed_mass_radius_from_text(state)
    if mass_from_text is None or radius_from_text is None or mass_from_text <= 0.0 or radius_from_text <= 0.0:
        volume_text = "--"
        density_text = "--"
    else:
        volume = compute_volume_m3(radius_from_text)
        density = compute_density_kg_m3(mass_from_text, radius_from_text)
        volume_text = f"{volume:.6e}"
        density_text = f"{density:.6e}"

    lines = [
        f"Configure {state.draft.custom_name}",
        f"Volume m3: {volume_text}",
        f"Density kg/m3: {density_text}",
    ]

    if state.note_text:
        lines.append(state.note_text)

    return tuple(lines)
