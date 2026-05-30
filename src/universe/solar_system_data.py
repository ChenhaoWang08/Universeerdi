from __future__ import annotations

from typing import Dict, Tuple

from .body import CelestialBody
from .units import (
    NEWTON_G_M3_KG_S2,
    SOLAR_GM_M3_S2,
    au_to_m,
    days_to_s,
    km_to_m,
    years_to_s,
)

PLANET_SOURCE_NOTE = (
    "Mass, mean radius, sidereal rotation period, and sidereal orbital period "
    "are from JPL Solar System Dynamics planetary physical parameters. Mean "
    "orbital radius uses JPL Solar System Dynamics semi-major axis values "
    "converted with the IAU astronomical unit. Negative rotation_period_s "
    "indicates retrograde spin. Visual radius is display-only."
)

SUN_SOURCE_NOTE = (
    "Mass is derived from JPL Solar System Dynamics heliocentric GM and CODATA G. "
    "Mean radius and approximate equatorial rotation come from NASA Science Sun "
    "facts. mean_orbital_radius_m and orbital_period_s are set to 0.0 by "
    "convention because the Sun is the system reference body in this project. "
    "Visual radius is display-only."
)

SUN = CelestialBody(
    name="Sun",
    category="star",
    mass_kg=SOLAR_GM_M3_S2 / NEWTON_G_M3_KG_S2,
    mean_radius_m=km_to_m(700_000.0),
    mean_orbital_radius_m=0.0,
    orbital_period_s=0.0,
    rotation_period_s=days_to_s(25.0),
    color_rgb=(242, 201, 103),
    visual_radius_px=30.0,
    source_note=SUN_SOURCE_NOTE,
)

MERCURY = CelestialBody(
    name="Mercury",
    category="terrestrial_planet",
    mass_kg=0.330103e24,
    mean_radius_m=km_to_m(2439.4),
    mean_orbital_radius_m=au_to_m(0.38709927),
    orbital_period_s=years_to_s(0.2408467),
    rotation_period_s=days_to_s(58.6462),
    color_rgb=(182, 176, 168),
    visual_radius_px=7.0,
    source_note=PLANET_SOURCE_NOTE,
)

VENUS = CelestialBody(
    name="Venus",
    category="terrestrial_planet",
    mass_kg=4.86731e24,
    mean_radius_m=km_to_m(6051.8),
    mean_orbital_radius_m=au_to_m(0.72333566),
    orbital_period_s=years_to_s(0.61519726),
    rotation_period_s=days_to_s(-243.018),
    color_rgb=(222, 184, 135),
    visual_radius_px=10.0,
    source_note=PLANET_SOURCE_NOTE,
)

EARTH = CelestialBody(
    name="Earth",
    category="terrestrial_planet",
    mass_kg=5.97217e24,
    mean_radius_m=km_to_m(6371.0084),
    mean_orbital_radius_m=au_to_m(1.00000261),
    orbital_period_s=years_to_s(1.0000174),
    rotation_period_s=days_to_s(0.99726968),
    color_rgb=(111, 163, 245),
    visual_radius_px=10.0,
    source_note=PLANET_SOURCE_NOTE,
)

MARS = CelestialBody(
    name="Mars",
    category="terrestrial_planet",
    mass_kg=0.641691e24,
    mean_radius_m=km_to_m(3389.50),
    mean_orbital_radius_m=au_to_m(1.52371034),
    orbital_period_s=years_to_s(1.8808476),
    rotation_period_s=days_to_s(1.02595676),
    color_rgb=(214, 120, 88),
    visual_radius_px=8.0,
    source_note=PLANET_SOURCE_NOTE,
)

JUPITER = CelestialBody(
    name="Jupiter",
    category="gas_giant",
    mass_kg=1898.125e24,
    mean_radius_m=km_to_m(69911.0),
    mean_orbital_radius_m=au_to_m(5.20288700),
    orbital_period_s=years_to_s(11.862615),
    rotation_period_s=days_to_s(0.41354),
    color_rgb=(205, 161, 111),
    visual_radius_px=18.0,
    source_note=PLANET_SOURCE_NOTE,
)

SATURN = CelestialBody(
    name="Saturn",
    category="gas_giant",
    mass_kg=568.317e24,
    mean_radius_m=km_to_m(58232.0),
    mean_orbital_radius_m=au_to_m(9.53667594),
    orbital_period_s=years_to_s(29.447498),
    rotation_period_s=days_to_s(0.44401),
    color_rgb=(215, 194, 141),
    visual_radius_px=16.0,
    source_note=PLANET_SOURCE_NOTE,
)

URANUS = CelestialBody(
    name="Uranus",
    category="ice_giant",
    mass_kg=86.8099e24,
    mean_radius_m=km_to_m(25362.0),
    mean_orbital_radius_m=au_to_m(19.18916464),
    orbital_period_s=years_to_s(84.016846),
    rotation_period_s=days_to_s(-0.71833),
    color_rgb=(159, 214, 220),
    visual_radius_px=13.0,
    source_note=PLANET_SOURCE_NOTE,
)

NEPTUNE = CelestialBody(
    name="Neptune",
    category="ice_giant",
    mass_kg=102.4092e24,
    mean_radius_m=km_to_m(24622.0),
    mean_orbital_radius_m=au_to_m(30.06992276),
    orbital_period_s=years_to_s(164.79132),
    rotation_period_s=days_to_s(0.67125),
    color_rgb=(84, 126, 218),
    visual_radius_px=13.0,
    source_note=PLANET_SOURCE_NOTE,
)

SOLAR_SYSTEM_BODIES: Tuple[CelestialBody, ...] = (
    SUN,
    MERCURY,
    VENUS,
    EARTH,
    MARS,
    JUPITER,
    SATURN,
    URANUS,
    NEPTUNE,
)

SOLAR_SYSTEM_BODY_MAP: Dict[str, CelestialBody] = {
    body.name: body for body in SOLAR_SYSTEM_BODIES
}


def get_solar_system_bodies() -> Tuple[CelestialBody, ...]:
    return SOLAR_SYSTEM_BODIES


def get_solar_system_body(name: str) -> CelestialBody:
    return SOLAR_SYSTEM_BODY_MAP[name]
