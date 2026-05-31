from __future__ import annotations

from typing import Literal, Optional, Sequence

from .universe.body import Body
from .universe.demo_simulation import (
    ControlledDemoState,
    controlled_demo_to_render_bodies,
    create_controlled_demo_state,
    step_controlled_demo_state,
)
from .universe.overlay_controls import OverlayControlsState, handle_overlay_click
from .universe.physics import step_placeholder_bodies
from .universe.rendering import (
    Camera,
    body_contains_screen_point,
    draw_scene_with_overlays,
    is_point_in_ui_placeholder,
    update_trail_history,
)
from .universe.simulation import DEFAULT_WINDOW_SIZE, MIN_WINDOW_SIZE, create_placeholder_bodies

SimulationMode = Literal["placeholder", "controlled_demo"]
DEFAULT_SIMULATION_MODE: SimulationMode = "controlled_demo"


def main() -> int:
    pygame = _load_pygame()
    pygame.init()

    screen = pygame.display.set_mode(DEFAULT_WINDOW_SIZE, pygame.RESIZABLE)
    pygame.display.set_caption("universeerdi")
    clock = pygame.time.Clock()

    camera = Camera(center_x=260.0, center_y=0.0, zoom=1.0)
    demo_state: Optional[ControlledDemoState] = None
    if DEFAULT_SIMULATION_MODE == "controlled_demo":
        demo_state = create_controlled_demo_state()
        bodies = controlled_demo_to_render_bodies(demo_state)
    else:
        bodies = create_placeholder_bodies()
    overlay_controls = OverlayControlsState()
    trail_history = {}
    dragging = False

    try:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    size = _clamp_window_size(event.size)
                    screen = pygame.display.set_mode(size, pygame.RESIZABLE)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        overlay_controls, was_overlay_click = handle_overlay_click(
                            overlay_controls,
                            event.pos,
                            screen.get_size(),
                        )
                        if was_overlay_click:
                            dragging = False
                        else:
                            dragging = _can_start_drag(bodies, camera, event.pos, screen.get_size())
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    dragging = False
                elif event.type == pygame.MOUSEMOTION and dragging:
                    camera.pan_by_screen_delta(event.rel[0], event.rel[1])
                elif event.type == pygame.MOUSEWHEEL:
                    camera.zoom_by_scroll(event.y, pygame.mouse.get_pos(), screen.get_size())

            delta_seconds = clock.tick(60) / 1000.0
            if DEFAULT_SIMULATION_MODE == "controlled_demo":
                # Demo motion is physics-driven and intentionally separate from real dataset motion.
                assert demo_state is not None
                demo_state = step_controlled_demo_state(demo_state, delta_seconds)
                bodies = controlled_demo_to_render_bodies(demo_state)
            else:
                bodies = step_placeholder_bodies(bodies, delta_seconds)
            if DEFAULT_SIMULATION_MODE == "controlled_demo":
                trail_history = update_trail_history(trail_history, bodies)
            else:
                trail_history = {}

            draw_scene_with_overlays(
                screen,
                pygame,
                camera,
                bodies,
                trail_history=trail_history,
                show_trails=DEFAULT_SIMULATION_MODE == "controlled_demo" and overlay_controls.show_trails,
                show_labels=DEFAULT_SIMULATION_MODE == "controlled_demo" and overlay_controls.show_labels,
                overlay_controls=overlay_controls,
            )
            pygame.display.flip()
    finally:
        pygame.quit()

    return 0


def _load_pygame():
    try:
        import pygame
    except ModuleNotFoundError as error:
        raise SystemExit(
            "pygame is not installed. Install pygame to run the viewer foundation."
        ) from error

    return pygame


def _clamp_window_size(size: Sequence[int]) -> tuple[int, int]:
    width = max(MIN_WINDOW_SIZE[0], int(size[0]))
    height = max(MIN_WINDOW_SIZE[1], int(size[1]))
    return (width, height)


def _can_start_drag(
    bodies: Sequence[Body],
    camera: Camera,
    mouse_position: tuple[int, int],
    viewport_size: tuple[int, int],
) -> bool:
    if is_point_in_ui_placeholder(mouse_position, viewport_size):
        return False

    return not any(
        body_contains_screen_point(body, camera, mouse_position, viewport_size)
        for body in bodies
    )


if __name__ == "__main__":
    raise SystemExit(main())
