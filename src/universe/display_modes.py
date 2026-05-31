from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Tuple

DEFAULT_WINDOWED_SIZE = (1280, 720)


@dataclass(frozen=True)
class DisplayModeState:
    is_fullscreen: bool = False
    windowed_size: Tuple[int, int] = DEFAULT_WINDOWED_SIZE


def toggle_fullscreen(
    state: DisplayModeState,
    *,
    current_size: Tuple[int, int],
) -> DisplayModeState:
    if state.is_fullscreen:
        return replace(state, is_fullscreen=False)
    return replace(state, is_fullscreen=True, windowed_size=_normalize_size(current_size))


def exit_fullscreen(
    state: DisplayModeState,
    *,
    current_size: Tuple[int, int],
) -> DisplayModeState:
    _ = current_size
    if not state.is_fullscreen:
        return state
    return replace(state, is_fullscreen=False)


def update_windowed_size(
    state: DisplayModeState,
    *,
    windowed_size: Tuple[int, int],
) -> DisplayModeState:
    if state.is_fullscreen:
        return state
    return replace(state, windowed_size=_normalize_size(windowed_size))


def display_mode_status_text(state: DisplayModeState) -> str:
    return "Display: FULLSCREEN" if state.is_fullscreen else "Display: WINDOWED"


def _normalize_size(size: Tuple[int, int]) -> Tuple[int, int]:
    return (max(1, int(size[0])), max(1, int(size[1])))
