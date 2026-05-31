from __future__ import annotations

from dataclasses import dataclass, replace

DEFAULT_PAUSED = False
DEFAULT_TIME_SCALE = 1.0
DEFAULT_MIN_TIME_SCALE = 0.1
DEFAULT_MAX_TIME_SCALE = 4.0
DEFAULT_TIME_SCALE_STEP = 0.1
DEFAULT_DT_CLAMP_SECONDS = 0.1


@dataclass(frozen=True)
class TimeControlState:
    paused: bool = DEFAULT_PAUSED
    time_scale: float = DEFAULT_TIME_SCALE
    min_time_scale: float = DEFAULT_MIN_TIME_SCALE
    max_time_scale: float = DEFAULT_MAX_TIME_SCALE
    dt_clamp_seconds: float = DEFAULT_DT_CLAMP_SECONDS


def toggle_pause(state: TimeControlState) -> TimeControlState:
    return replace(state, paused=not state.paused)


def increase_time_scale(
    state: TimeControlState, *, step: float = DEFAULT_TIME_SCALE_STEP
) -> TimeControlState:
    return replace(state, time_scale=_clamp_time_scale(state, state.time_scale + step))


def decrease_time_scale(
    state: TimeControlState, *, step: float = DEFAULT_TIME_SCALE_STEP
) -> TimeControlState:
    return replace(state, time_scale=_clamp_time_scale(state, state.time_scale - step))


def reset_time_scale(state: TimeControlState) -> TimeControlState:
    return replace(state, time_scale=_clamp_time_scale(state, DEFAULT_TIME_SCALE))


def compute_simulation_dt(state: TimeControlState, frame_dt_seconds: float) -> float:
    if state.paused:
        return 0.0
    clamped_frame_dt = _clamp_frame_dt(frame_dt_seconds, state.dt_clamp_seconds)
    return clamped_frame_dt * state.time_scale


def format_time_status_text(state: TimeControlState) -> str:
    mode = "PAUSED" if state.paused else "RUNNING"
    return f"Time: {mode} x{state.time_scale:.1f}"


def _clamp_time_scale(state: TimeControlState, value: float) -> float:
    return max(state.min_time_scale, min(state.max_time_scale, value))


def _clamp_frame_dt(frame_dt_seconds: float, max_dt_seconds: float) -> float:
    if max_dt_seconds <= 0.0:
        raise ValueError("max_dt_seconds must be positive")
    non_negative = max(0.0, frame_dt_seconds)
    return min(non_negative, max_dt_seconds)
