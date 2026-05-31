from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Dict, Literal

CameraViewPreset = Literal["normal", "overview", "close"]


@dataclass(frozen=True)
class CameraViewSettings:
    center_x: float
    center_y: float
    zoom: float
    min_zoom: float
    max_zoom: float
    zoom_step: float


NORMAL_VIEW_SETTINGS = CameraViewSettings(
    center_x=260.0,
    center_y=0.0,
    zoom=1.0,
    min_zoom=0.02,
    max_zoom=40.0,
    zoom_step=1.15,
)

OVERVIEW_VIEW_SETTINGS = CameraViewSettings(
    center_x=260.0,
    center_y=0.0,
    zoom=0.25,
    min_zoom=0.005,
    max_zoom=40.0,
    zoom_step=1.2,
)

CLOSE_VIEW_SETTINGS = CameraViewSettings(
    center_x=260.0,
    center_y=0.0,
    zoom=4.0,
    min_zoom=0.02,
    max_zoom=100.0,
    zoom_step=1.1,
)

CAMERA_VIEW_PRESETS: Dict[CameraViewPreset, CameraViewSettings] = {
    "normal": NORMAL_VIEW_SETTINGS,
    "overview": OVERVIEW_VIEW_SETTINGS,
    "close": CLOSE_VIEW_SETTINGS,
}

CAMERA_VIEW_PRESET_CYCLE = ("normal", "overview", "close")


@dataclass(frozen=True)
class CameraViewState:
    preset: CameraViewPreset = "normal"


def cycle_camera_view_preset(state: CameraViewState) -> CameraViewState:
    current_index = CAMERA_VIEW_PRESET_CYCLE.index(state.preset)
    next_index = (current_index + 1) % len(CAMERA_VIEW_PRESET_CYCLE)
    return replace(state, preset=CAMERA_VIEW_PRESET_CYCLE[next_index])


def camera_view_settings_for_preset(preset: CameraViewPreset) -> CameraViewSettings:
    return CAMERA_VIEW_PRESETS[preset]


def camera_view_status_text(state: CameraViewState) -> str:
    return f"View: {state.preset}"


def apply_camera_view_preset(camera: object, state: CameraViewState) -> None:
    settings = camera_view_settings_for_preset(state.preset)
    camera.center_x = settings.center_x
    camera.center_y = settings.center_y
    camera.zoom = settings.zoom
    camera.min_zoom = settings.min_zoom
    camera.max_zoom = settings.max_zoom
    camera.zoom_step = settings.zoom_step
