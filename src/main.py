from __future__ import annotations

from typing import Optional, Sequence

from .universe.body import Body
from .universe.camera_views import (
    CameraViewState,
    apply_camera_view_preset,
    camera_view_status_text,
    cycle_camera_view_preset,
)
from .universe.demo_simulation import (
    ControlledDemoState,
    controlled_demo_to_render_bodies,
    create_controlled_demo_state,
    step_controlled_demo_state,
)
from .universe.display_modes import (
    DisplayModeState,
    display_mode_status_text,
    exit_fullscreen,
    toggle_fullscreen,
    update_windowed_size,
)
from .universe.focus_camera import (
    FocusCameraState,
    apply_focus_to_camera,
    clear_focus,
    focus_status_text,
    sync_focus_with_render_bodies,
    toggle_focus_from_selection,
)
from .universe.overlay_controls import OverlayControlsState, handle_overlay_click
from .universe.physics_substeps import (
    PhysicsSubstepState,
    decrease_physics_substeps,
    increase_physics_substeps,
    physics_substeps_status_text,
)
from .universe.scale_ruler import build_scale_ruler
from .universe.trail_controls import (
    TrailControlState,
    clear_trail_history,
    decrease_trail_length,
    increase_trail_length,
    trail_length_status_text,
)
from .universe.rendering import (
    Camera,
    body_contains_screen_point,
    draw_scene_with_overlays,
    is_point_in_ui_placeholder,
    update_trail_history,
)
from .universe.trails import trim_trail_history
from .universe.render_scale_presets import (
    RenderScalePresetState,
    cycle_render_scale_preset,
    render_scale_preset_explanation,
    render_scale_policy_for_preset,
    render_scale_preset_status_text,
)
from .universe.selection import (
    SelectionState,
    format_body_inspector_lines,
    get_selected_physics_body,
    handle_body_selection_click,
)
from .universe.solar_mass_experiment import (
    SolarMassExperimentState,
    decrease_solar_mass_multiplier,
    increase_solar_mass_multiplier,
    reset_solar_mass_multiplier,
    solar_mass_experiment_status_text,
)
from .universe.simulation_modes import (
    SimulationModeState,
    simulation_mode_status_text,
    toggle_simulation_mode,
)
from .universe.solar_system_simulation import (
    SolarSystemSimulationState,
    create_solar_system_simulation_state,
    solar_system_to_render_bodies,
    step_solar_system_simulation_state,
)
from .universe.time_controls import (
    TimeControlState,
    compute_simulation_dt,
    decrease_time_scale,
    format_time_status_text,
    increase_time_scale,
    reset_time_scale,
    toggle_pause,
)
from .universe.simulation import DEFAULT_WINDOW_SIZE, MIN_WINDOW_SIZE


def main() -> int:
    pygame = _load_pygame()
    pygame.init()

    display_mode_state = DisplayModeState(windowed_size=DEFAULT_WINDOW_SIZE)
    screen = _set_display_mode(pygame, display_mode_state)
    pygame.display.set_caption("universeerdi")
    clock = pygame.time.Clock()

    camera = Camera(center_x=260.0, center_y=0.0, zoom=1.0)
    camera_view_state = CameraViewState()
    apply_camera_view_preset(camera, camera_view_state)
    demo_state: Optional[ControlledDemoState] = create_controlled_demo_state()
    solar_system_state: Optional[SolarSystemSimulationState] = None
    simulation_mode_state = SimulationModeState()
    render_scale_preset_state = RenderScalePresetState()
    bodies = controlled_demo_to_render_bodies(demo_state)
    overlay_controls = OverlayControlsState()
    selection_state = SelectionState()
    time_controls = TimeControlState()
    solar_mass_experiment_state = SolarMassExperimentState()
    physics_substep_state = PhysicsSubstepState()
    focus_camera_state = FocusCameraState()
    trail_control_state = TrailControlState()
    trail_history = {}
    dragging = False
    current_scale_ruler = None
    current_scale_note_text = None

    try:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    if display_mode_state.is_fullscreen:
                        display_mode_state = exit_fullscreen(
                            display_mode_state,
                            current_size=screen.get_size(),
                        )
                        screen = _set_display_mode(pygame, display_mode_state)
                    else:
                        running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                    display_mode_state = toggle_fullscreen(
                        display_mode_state,
                        current_size=screen.get_size(),
                    )
                    screen = _set_display_mode(pygame, display_mode_state)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                    focus_camera_state = toggle_focus_from_selection(
                        focus_camera_state,
                        selection_state.selected_body_name,
                    )
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    time_controls = toggle_pause(time_controls)
                elif event.type == pygame.KEYDOWN and event.key in (
                    pygame.K_LEFTBRACKET,
                ):
                    time_controls = decrease_time_scale(time_controls)
                elif event.type == pygame.KEYDOWN and event.key in (
                    pygame.K_RIGHTBRACKET,
                ):
                    time_controls = increase_time_scale(time_controls)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_MINUS:
                    physics_substep_state = decrease_physics_substeps(physics_substep_state)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_EQUALS:
                    physics_substep_state = increase_physics_substeps(physics_substep_state)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_0:
                    if event.mod & pygame.KMOD_CTRL:
                        time_controls = reset_time_scale(time_controls)
                    else:
                        apply_camera_view_preset(camera, camera_view_state)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                    camera_view_state = cycle_camera_view_preset(camera_view_state)
                    apply_camera_view_preset(camera, camera_view_state)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                    simulation_mode_state = toggle_simulation_mode(simulation_mode_state)
                    if simulation_mode_state.mode == "controlled_demo":
                        demo_state = create_controlled_demo_state()
                        bodies = controlled_demo_to_render_bodies(demo_state)
                    else:
                        solar_system_state = create_solar_system_simulation_state()
                        bodies = solar_system_to_render_bodies(
                            solar_system_state,
                            policy=render_scale_policy_for_preset(render_scale_preset_state.preset),
                        )
                    selection_state = SelectionState()
                    focus_camera_state = FocusCameraState()
                    trail_history = {}
                    dragging = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_v:
                    render_scale_preset_state = cycle_render_scale_preset(render_scale_preset_state)
                    if simulation_mode_state.mode == "solar_system" and solar_system_state is not None:
                        bodies = solar_system_to_render_bodies(
                            solar_system_state,
                            policy=render_scale_policy_for_preset(render_scale_preset_state.preset),
                        )
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_g:
                    solar_mass_experiment_state = increase_solar_mass_multiplier(
                        solar_mass_experiment_state
                    )
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_h:
                    solar_mass_experiment_state = decrease_solar_mass_multiplier(
                        solar_mass_experiment_state
                    )
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    solar_mass_experiment_state = reset_solar_mass_multiplier(
                        solar_mass_experiment_state
                    )
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                    trail_history = clear_trail_history()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_COMMA:
                    trail_control_state = decrease_trail_length(trail_control_state)
                    trail_history = trim_trail_history(
                        trail_history,
                        max_points=trail_control_state.max_points,
                    )
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_PERIOD:
                    trail_control_state = increase_trail_length(trail_control_state)
                elif event.type == pygame.VIDEORESIZE:
                    if not display_mode_state.is_fullscreen:
                        size = _clamp_window_size(event.size)
                        display_mode_state = update_windowed_size(
                            display_mode_state,
                            windowed_size=size,
                        )
                        screen = _set_display_mode(pygame, display_mode_state)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        overlay_controls, was_overlay_click = handle_overlay_click(
                            overlay_controls,
                            event.pos,
                            screen.get_size(),
                        )
                        if was_overlay_click:
                            dragging = False
                        elif simulation_mode_state.mode in ("controlled_demo", "solar_system"):
                            selection_state, was_body_selection = handle_body_selection_click(
                                selection_state,
                                bodies,
                                camera,
                                event.pos,
                                screen.get_size(),
                            )
                            if was_body_selection:
                                dragging = False
                            else:
                                dragging = _can_start_drag(bodies, camera, event.pos, screen.get_size())
                        else:
                            dragging = _can_start_drag(bodies, camera, event.pos, screen.get_size())
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    dragging = False
                elif event.type == pygame.MOUSEMOTION and dragging:
                    camera.pan_by_screen_delta(event.rel[0], event.rel[1])
                    focus_camera_state = clear_focus(focus_camera_state)
                elif event.type == pygame.MOUSEWHEEL:
                    camera.zoom_by_scroll(event.y, pygame.mouse.get_pos(), screen.get_size())

            frame_delta_seconds = clock.tick(60) / 1000.0
            simulation_dt_seconds = compute_simulation_dt(time_controls, frame_delta_seconds)
            current_physics_bodies = ()
            current_scale_ruler = None
            current_scale_note_text = None
            if simulation_mode_state.mode == "controlled_demo":
                # Demo motion is physics-driven and intentionally separate from real dataset motion.
                assert demo_state is not None
                if simulation_dt_seconds > 0.0:
                    demo_state = step_controlled_demo_state(demo_state, simulation_dt_seconds)
                bodies = controlled_demo_to_render_bodies(demo_state)
                current_physics_bodies = demo_state.physics_bodies
            elif simulation_mode_state.mode == "solar_system":
                # PR9 solar_system mode uses deterministic initialization and Newtonian stepping.
                assert solar_system_state is not None
                current_render_scale_policy = render_scale_policy_for_preset(
                    render_scale_preset_state.preset
                )
                if simulation_dt_seconds > 0.0:
                    solar_system_state = step_solar_system_simulation_state(
                        solar_system_state,
                        simulation_dt_seconds,
                        solar_mass_multiplier=solar_mass_experiment_state.solar_mass_multiplier,
                        absorb_into_sun=True,
                        physics_substeps=physics_substep_state.substeps,
                    )
                bodies = solar_system_to_render_bodies(
                    solar_system_state,
                    policy=current_render_scale_policy,
                )
                current_physics_bodies = solar_system_state.physics_bodies
                current_scale_ruler = build_scale_ruler(
                    camera_zoom=camera.zoom,
                    meters_per_world_unit=current_render_scale_policy.meters_per_world_unit,
                )
                current_scale_note_text = render_scale_preset_explanation(
                    render_scale_preset_state.preset
                )
            trail_history = update_trail_history(
                trail_history,
                bodies,
                max_points=trail_control_state.max_points,
            )
            selected_physics_body = get_selected_physics_body(
                current_physics_bodies,
                selection_state.selected_body_name,
            )
            if selection_state.selected_body_name and selected_physics_body is None:
                selection_state = SelectionState()
            focus_camera_state = sync_focus_with_render_bodies(focus_camera_state, bodies)
            _ = apply_focus_to_camera(camera, focus_camera_state, bodies)
            inspector_lines = format_body_inspector_lines(
                selected_physics_body,
                simulation_mode=simulation_mode_state.mode,
            )

            draw_scene_with_overlays(
                screen,
                pygame,
                camera,
                bodies,
                trail_history=trail_history,
                show_trails=overlay_controls.show_trails,
                show_labels=overlay_controls.show_labels,
                overlay_controls=overlay_controls,
                time_status_text=(
                    f"{format_time_status_text(time_controls)}  |  "
                    f"{display_mode_status_text(display_mode_state)}"
                ),
                mode_scale_status_text=(
                    f"{simulation_mode_status_text(simulation_mode_state)}  |  "
                    f"{render_scale_preset_status_text(render_scale_preset_state)}"
                ),
                experiment_status_text=solar_mass_experiment_status_text(
                    solar_mass_experiment_state,
                    active_body_count=len(current_physics_bodies),
                ),
                camera_view_status_text=camera_view_status_text(camera_view_state),
                physics_substeps_status_text=physics_substeps_status_text(physics_substep_state),
                focus_status_text=focus_status_text(focus_camera_state),
                trail_length_status_text=trail_length_status_text(trail_control_state),
                scale_ruler=current_scale_ruler,
                scale_note_text=current_scale_note_text,
                selected_body_name=selection_state.selected_body_name,
                inspector_lines=inspector_lines,
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


def _set_display_mode(pygame_module: object, display_mode_state: DisplayModeState) -> object:
    if display_mode_state.is_fullscreen:
        return pygame_module.display.set_mode((0, 0), pygame_module.FULLSCREEN)
    return pygame_module.display.set_mode(display_mode_state.windowed_size, pygame_module.RESIZABLE)


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
