from __future__ import annotations

from typing import Sequence

from .universe.body import Body
from .universe.physics import step_placeholder_bodies
from .universe.rendering import (
    Camera,
    body_contains_screen_point,
    draw_scene,
    is_point_in_ui_placeholder,
)
from .universe.simulation import DEFAULT_WINDOW_SIZE, MIN_WINDOW_SIZE, create_placeholder_bodies


def main() -> int:
    pygame = _load_pygame()
    pygame.init()

    screen = pygame.display.set_mode(DEFAULT_WINDOW_SIZE, pygame.RESIZABLE)
    pygame.display.set_caption("universeerdi")
    clock = pygame.time.Clock()

    camera = Camera(center_x=260.0, center_y=0.0, zoom=1.0)
    bodies = create_placeholder_bodies()
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
                        dragging = _can_start_drag(bodies, camera, event.pos, screen.get_size())
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    dragging = False
                elif event.type == pygame.MOUSEMOTION and dragging:
                    camera.pan_by_screen_delta(event.rel[0], event.rel[1])
                elif event.type == pygame.MOUSEWHEEL:
                    camera.zoom_by_scroll(event.y, pygame.mouse.get_pos(), screen.get_size())

            delta_seconds = clock.tick(60) / 1000.0
            bodies = step_placeholder_bodies(bodies, delta_seconds)
            draw_scene(screen, pygame, camera, bodies)
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
