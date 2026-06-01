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

SETTINGS_PENDING_NOTE = "Preview/spawn will be added in a later PR"


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
class SpawnSettingsState:
    is_open: bool = False
    panel_left: int = 0
    panel_top: int = 0
    selected_template_id: Optional[str] = None
    draft: Optional[SpawnDraft] = None
    note_text: Optional[str] = None


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
    menu_left, menu_top, menu_width, _menu_height = spawn_menu_rect(menu_state)
    panel_left = menu_left + menu_width + SPAWN_SETTINGS_PANEL_OFFSET_X
    panel_top = preferred_top

    if panel_left + SPAWN_SETTINGS_PANEL_WIDTH > viewport_size[0]:
        panel_left = menu_left - SPAWN_SETTINGS_PANEL_WIDTH - SPAWN_SETTINGS_PANEL_OFFSET_X
    if panel_top + SPAWN_SETTINGS_PANEL_HEIGHT > viewport_size[1]:
        panel_top = viewport_size[1] - SPAWN_SETTINGS_PANEL_HEIGHT - 12

    panel_left = max(12, panel_left)
    panel_top = max(12, panel_top)

    return SpawnSettingsState(
        is_open=True,
        panel_left=panel_left,
        panel_top=panel_top,
        selected_template_id=selected_template.template_id,
        draft=create_spawn_draft(selected_template),
        note_text=None,
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


def handle_spawn_settings_click(
    state: SpawnSettingsState,
    point: Point,
) -> Tuple[SpawnSettingsState, bool]:
    if not state.is_open:
        return state, False

    if is_point_in_rect(point, spawn_settings_cancel_button_rect(state)):
        return close_spawn_settings_panel(), True
    if is_point_in_rect(point, spawn_settings_set_button_rect(state)):
        return replace(state, note_text=SETTINGS_PENDING_NOTE), True
    if is_point_in_spawn_settings_panel(state, point):
        return state, True
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


def spawn_settings_display_lines(state: SpawnSettingsState) -> Tuple[str, ...]:
    if not state.is_open or state.draft is None:
        return ()

    draft = state.draft
    volume = compute_volume_m3(draft.radius_m)
    density = compute_density_kg_m3(draft.mass_kg, draft.radius_m)
    lines = [
        f"Configure {draft.custom_name}",
        f"Name: {draft.custom_name}",
        f"Mass kg: {draft.mass_kg:.6e}",
        f"Radius m: {draft.radius_m:.6e}",
        f"Volume m3: {volume:.6e}",
        f"Density: {density:.6e}",
        f"Velocity X: {draft.velocity_x_m_s:.3f}",
        f"Velocity Y: {draft.velocity_y_m_s:.3f}",
        f"Color RGB: {draft.color_rgb}",
    ]
    if state.note_text:
        lines.append(state.note_text)
    return tuple(lines)
