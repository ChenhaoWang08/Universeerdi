from __future__ import annotations

from dataclasses import dataclass
from math import floor, log10
from typing import Dict, List, Optional, Sequence, Tuple

from .body import Body
from .overlay_controls import (
    OverlayControlsState,
    build_overlay_control_rects,
    checkbox_label_text,
    is_point_in_overlay_panel,
    overlay_panel_rect,
)
from .trails import (
    build_dashed_polyline_segments,
    resolve_trail_color,
    update_trail_history_bounded,
)

Point = Tuple[float, float]
Size = Tuple[int, int]
LineSegment = Tuple[Point, Point]
TrailHistory = Dict[str, Tuple[Point, ...]]

BACKGROUND_COLOR = (34, 36, 40)
GRID_MINOR_COLOR = (92, 96, 104)
GRID_MAJOR_COLOR = (188, 192, 200)
UI_PANEL_FILL = (52, 54, 60, 220)
UI_PANEL_BORDER = (208, 212, 220)
UI_TEXT_LINE = (168, 172, 180)
BODY_OUTLINE_COLOR = (244, 246, 250)
LABEL_TEXT_COLOR = (236, 240, 248)
TOGGLE_ON_COLOR = (151, 215, 160)
TOGGLE_OFF_COLOR = (205, 126, 126)
SELECTION_RING_COLOR = (255, 238, 160)
INSPECTOR_PANEL_FILL = (46, 49, 56, 224)
INSPECTOR_PANEL_BORDER = (221, 224, 232)
INSPECTOR_TEXT_COLOR = (238, 241, 248)

MIN_GRID_PIXELS = 48.0
MAX_GRID_PIXELS = 160.0
TARGET_GRID_PIXELS = 96.0
TRAIL_MAX_POINTS = 120
TRAIL_LINE_WIDTH = 2
TRAIL_DASH_LENGTH = 10.0
TRAIL_GAP_LENGTH = 7.0
LABEL_OFFSET_PX = 10.0


@dataclass
class Camera:
    center_x: float = 0.0
    center_y: float = 0.0
    zoom: float = 1.0
    min_zoom: float = 0.2
    max_zoom: float = 4.0
    zoom_step: float = 1.15

    def world_to_screen(self, position: Point, viewport_size: Size) -> Point:
        width, height = viewport_size
        world_x, world_y = position
        screen_x = (world_x - self.center_x) * self.zoom + (width / 2.0)
        screen_y = (world_y - self.center_y) * self.zoom + (height / 2.0)
        return (screen_x, screen_y)

    def screen_to_world(self, position: Point, viewport_size: Size) -> Point:
        width, height = viewport_size
        screen_x, screen_y = position
        world_x = ((screen_x - (width / 2.0)) / self.zoom) + self.center_x
        world_y = ((screen_y - (height / 2.0)) / self.zoom) + self.center_y
        return (world_x, world_y)

    def pan_by_screen_delta(self, delta_x: float, delta_y: float) -> None:
        self.center_x -= delta_x / self.zoom
        self.center_y -= delta_y / self.zoom

    def zoom_by_scroll(
        self, steps: int, anchor_screen: Point, viewport_size: Size
    ) -> None:
        if steps == 0:
            return
        if self.zoom_step <= 1.0:
            raise ValueError("zoom_step must be > 1.0")
        if self.min_zoom <= 0.0:
            raise ValueError("min_zoom must be positive")
        if self.max_zoom < self.min_zoom:
            raise ValueError("max_zoom must be >= min_zoom")

        anchor_before = self.screen_to_world(anchor_screen, viewport_size)

        if steps > 0:
            next_zoom = self.zoom / (self.zoom_step ** steps)
        else:
            next_zoom = self.zoom * (self.zoom_step ** abs(steps))

        self.zoom = max(self.min_zoom, min(self.max_zoom, next_zoom))

        anchor_after = self.screen_to_world(anchor_screen, viewport_size)
        self.center_x += anchor_before[0] - anchor_after[0]
        self.center_y += anchor_before[1] - anchor_after[1]


def choose_grid_world_spacing(zoom: float) -> float:
    if zoom <= 0:
        raise ValueError("zoom must be positive")

    target_world_spacing = TARGET_GRID_PIXELS / zoom
    base_exponent = floor(log10(target_world_spacing))

    best_spacing = None
    best_key = None

    for exponent in range(base_exponent - 2, base_exponent + 3):
        magnitude = 10.0 ** exponent
        for scale in (1.0, 2.0, 5.0):
            spacing = scale * magnitude
            pixel_spacing = spacing * zoom
            in_range = MIN_GRID_PIXELS <= pixel_spacing <= MAX_GRID_PIXELS
            key = (0 if in_range else 1, abs(pixel_spacing - TARGET_GRID_PIXELS))
            if best_key is None or key < best_key:
                best_key = key
                best_spacing = spacing

    return float(best_spacing)


def build_grid_segments(
    camera: Camera, viewport_size: Size
) -> Tuple[List[LineSegment], List[LineSegment], float]:
    minor_spacing = choose_grid_world_spacing(camera.zoom)
    major_spacing = minor_spacing * 5.0

    top_left = camera.screen_to_world((0.0, 0.0), viewport_size)
    bottom_right = camera.screen_to_world(
        (float(viewport_size[0]), float(viewport_size[1])), viewport_size
    )

    min_x, min_y = top_left
    max_x, max_y = bottom_right

    minor_segments: List[LineSegment] = []
    major_segments: List[LineSegment] = []

    start_x = floor(min_x / minor_spacing) * minor_spacing
    start_y = floor(min_y / minor_spacing) * minor_spacing

    vertical_count = int((max_x - min_x) / minor_spacing) + 3
    horizontal_count = int((max_y - min_y) / minor_spacing) + 3

    for index in range(vertical_count):
        world_x = start_x + (index * minor_spacing)
        start = camera.world_to_screen((world_x, min_y), viewport_size)
        end = camera.world_to_screen((world_x, max_y), viewport_size)
        target = major_segments if _is_major_line(world_x, major_spacing) else minor_segments
        target.append((start, end))

    for index in range(horizontal_count):
        world_y = start_y + (index * minor_spacing)
        start = camera.world_to_screen((min_x, world_y), viewport_size)
        end = camera.world_to_screen((max_x, world_y), viewport_size)
        target = major_segments if _is_major_line(world_y, major_spacing) else minor_segments
        target.append((start, end))

    return minor_segments, major_segments, minor_spacing


def ui_placeholder_rect(viewport_size: Size) -> Tuple[int, int, int, int]:
    return overlay_panel_rect(viewport_size)


def is_point_in_ui_placeholder(point: Point, viewport_size: Size) -> bool:
    return is_point_in_overlay_panel(point, viewport_size)


def body_contains_screen_point(
    body: Body, camera: Camera, point: Point, viewport_size: Size
) -> bool:
    body_x, body_y = camera.world_to_screen(body.position, viewport_size)
    radius = max(1.0, body.draw_radius * camera.zoom)
    point_x, point_y = point
    return ((point_x - body_x) ** 2) + ((point_y - body_y) ** 2) <= radius ** 2


def draw_scene(surface: object, pygame_module: object, camera: Camera, bodies: Sequence[Body]) -> None:
    surface.fill(BACKGROUND_COLOR)
    draw_grid(surface, pygame_module, camera)
    draw_bodies(surface, pygame_module, camera, bodies)
    draw_ui_placeholder(surface, pygame_module)


def draw_scene_with_overlays(
    surface: object,
    pygame_module: object,
    camera: Camera,
    bodies: Sequence[Body],
    *,
    trail_history: Optional[TrailHistory] = None,
    show_trails: bool = False,
    show_labels: bool = False,
    overlay_controls: Optional[OverlayControlsState] = None,
    time_status_text: Optional[str] = None,
    mode_scale_status_text: Optional[str] = None,
    experiment_status_text: Optional[str] = None,
    camera_view_status_text: Optional[str] = None,
    physics_substeps_status_text: Optional[str] = None,
    selected_body_name: Optional[str] = None,
    inspector_lines: Optional[Sequence[str]] = None,
) -> None:
    surface.fill(BACKGROUND_COLOR)
    draw_grid(surface, pygame_module, camera)
    if show_trails and trail_history:
        draw_trails(surface, pygame_module, camera, bodies, trail_history)
    draw_bodies(
        surface,
        pygame_module,
        camera,
        bodies,
        show_labels=show_labels,
        selected_body_name=selected_body_name,
    )
    draw_ui_placeholder(
        surface,
        pygame_module,
        overlay_controls=overlay_controls,
        time_status_text=time_status_text,
        mode_scale_status_text=mode_scale_status_text,
        experiment_status_text=experiment_status_text,
        camera_view_status_text=camera_view_status_text,
        physics_substeps_status_text=physics_substeps_status_text,
    )
    draw_selection_inspector(surface, pygame_module, inspector_lines)


def draw_grid(surface: object, pygame_module: object, camera: Camera) -> None:
    viewport_size = surface.get_size()
    minor_segments, major_segments, _ = build_grid_segments(camera, viewport_size)

    for start, end in minor_segments:
        pygame_module.draw.line(surface, GRID_MINOR_COLOR, start, end, 1)

    for start, end in major_segments:
        pygame_module.draw.line(surface, GRID_MAJOR_COLOR, start, end, 2)


def draw_bodies(
    surface: object,
    pygame_module: object,
    camera: Camera,
    bodies: Sequence[Body],
    *,
    show_labels: bool = False,
    selected_body_name: Optional[str] = None,
) -> None:
    viewport_size = surface.get_size()
    label_font = pygame_module.font.Font(None, 20) if show_labels else None

    for body in bodies:
        center_x, center_y = camera.world_to_screen(body.position, viewport_size)
        screen_center = (int(round(center_x)), int(round(center_y)))
        radius = max(1, int(round(body.draw_radius * camera.zoom)))
        pygame_module.draw.circle(surface, body.color, screen_center, radius)
        pygame_module.draw.circle(surface, BODY_OUTLINE_COLOR, screen_center, radius, 2)
        if selected_body_name == body.name:
            pygame_module.draw.circle(surface, SELECTION_RING_COLOR, screen_center, radius + 6, 2)
        if label_font is not None:
            label_surface = label_font.render(body.name, True, LABEL_TEXT_COLOR)
            anchor_x, anchor_y = body_label_anchor((center_x, center_y), float(radius))
            surface.blit(label_surface, (int(round(anchor_x)), int(round(anchor_y))))


def draw_trails(
    surface: object,
    pygame_module: object,
    camera: Camera,
    bodies: Sequence[Body],
    trail_history: TrailHistory,
) -> None:
    viewport_size = surface.get_size()
    for body in bodies:
        world_points = trail_history.get(body.name, ())
        if len(world_points) < 2:
            continue
        screen_points = tuple(
            camera.world_to_screen(world_point, viewport_size)
            for world_point in world_points
        )
        dashed_segments = build_dashed_polyline_segments(
            screen_points,
            dash_length=TRAIL_DASH_LENGTH,
            gap_length=TRAIL_GAP_LENGTH,
        )
        trail_color = resolve_trail_color(body.color)
        for segment_start, segment_end in dashed_segments:
            pygame_module.draw.line(
                surface,
                trail_color,
                (
                    int(round(segment_start[0])),
                    int(round(segment_start[1])),
                ),
                (
                    int(round(segment_end[0])),
                    int(round(segment_end[1])),
                ),
                TRAIL_LINE_WIDTH,
            )


def update_trail_history(
    trail_history: TrailHistory,
    bodies: Sequence[Body],
    max_points: int = TRAIL_MAX_POINTS,
) -> TrailHistory:
    points_by_name = {body.name: body.position for body in bodies}
    return update_trail_history_bounded(
        trail_history,
        points_by_name,
        max_points=max_points,
    )


def body_label_anchor(center: Point, radius_px: float) -> Point:
    center_x, center_y = center
    return (
        center_x + radius_px + LABEL_OFFSET_PX,
        center_y - radius_px - LABEL_OFFSET_PX,
    )


def draw_ui_placeholder(
    surface: object,
    pygame_module: object,
    *,
    overlay_controls: Optional[OverlayControlsState] = None,
    time_status_text: Optional[str] = None,
    mode_scale_status_text: Optional[str] = None,
    experiment_status_text: Optional[str] = None,
    camera_view_status_text: Optional[str] = None,
    physics_substeps_status_text: Optional[str] = None,
) -> None:
    viewport_size = surface.get_size()
    rects = build_overlay_control_rects(viewport_size)
    left, top, width, height = rects.panel_rect

    panel = pygame_module.Surface((width, height), pygame_module.SRCALPHA)
    panel.fill(UI_PANEL_FILL)
    surface.blit(panel, (left, top))
    pygame_module.draw.rect(surface, UI_PANEL_BORDER, (left, top, width, height), 2, border_radius=8)

    state = overlay_controls or OverlayControlsState()
    font = pygame_module.font.Font(None, 24)
    _draw_toggle_row(
        surface,
        pygame_module,
        font,
        rects.labels_rect,
        "Labels",
        state.show_labels,
    )
    _draw_toggle_row(
        surface,
        pygame_module,
        font,
        rects.trails_rect,
        "Trails",
        state.show_trails,
    )
    if time_status_text is not None:
        _draw_status_row(
            surface,
            pygame_module,
            font,
            rects.time_status_rect,
            time_status_text,
        )
    if mode_scale_status_text is not None:
        _draw_status_row(
            surface,
            pygame_module,
            font,
            rects.mode_scale_status_rect,
            mode_scale_status_text,
        )
    if experiment_status_text is not None:
        _draw_status_row(
            surface,
            pygame_module,
            font,
            rects.experiment_status_rect,
            experiment_status_text,
        )
    if camera_view_status_text is not None:
        _draw_status_row(
            surface,
            pygame_module,
            font,
            rects.camera_view_status_rect,
            camera_view_status_text,
        )
    if physics_substeps_status_text is not None:
        _draw_status_row(
            surface,
            pygame_module,
            font,
            rects.physics_substeps_status_rect,
            physics_substeps_status_text,
        )


def _is_major_line(value: float, major_spacing: float) -> bool:
    rounded = round(value / major_spacing)
    return abs(value - (rounded * major_spacing)) <= major_spacing * 1e-6


def _draw_toggle_row(
    surface: object,
    pygame_module: object,
    font: object,
    row_rect: Tuple[int, int, int, int],
    label: str,
    enabled: bool,
) -> None:
    left, top, _width, _height = row_rect
    pygame_module.draw.rect(surface, UI_PANEL_BORDER, row_rect, 1, border_radius=4)
    checkbox_text = checkbox_label_text(label, enabled)
    row_color = TOGGLE_ON_COLOR if enabled else TOGGLE_OFF_COLOR
    checkbox_surface = font.render(checkbox_text, True, row_color)
    surface.blit(checkbox_surface, (left + 8, top + 3))


def _draw_status_row(
    surface: object,
    pygame_module: object,
    font: object,
    row_rect: Tuple[int, int, int, int],
    text: str,
) -> None:
    left, top, _width, _height = row_rect
    pygame_module.draw.rect(surface, UI_PANEL_BORDER, row_rect, 1, border_radius=4)
    text_surface = font.render(text, True, UI_TEXT_LINE)
    surface.blit(text_surface, (left + 8, top + 3))


def draw_selection_inspector(
    surface: object,
    pygame_module: object,
    lines: Optional[Sequence[str]],
) -> None:
    viewport_size = surface.get_size()
    panel_width = min(430, viewport_size[0] - 40)
    panel_height = 332
    panel_left = viewport_size[0] - panel_width - 16
    panel_top = 16

    panel = pygame_module.Surface((panel_width, panel_height), pygame_module.SRCALPHA)
    panel.fill(INSPECTOR_PANEL_FILL)
    surface.blit(panel, (panel_left, panel_top))
    pygame_module.draw.rect(
        surface,
        INSPECTOR_PANEL_BORDER,
        (panel_left, panel_top, panel_width, panel_height),
        2,
        border_radius=8,
    )

    content_lines = lines or ("Selected Body", "Name: None", "Click a demo body to inspect.")
    font = pygame_module.font.Font(None, 22)
    for line_index, line in enumerate(content_lines[:13]):
        text_surface = font.render(line, True, INSPECTOR_TEXT_COLOR)
        surface.blit(text_surface, (panel_left + 12, panel_top + 12 + (line_index * 24)))
