from __future__ import annotations

KM_M = 1_000.0
DAY_S = 86_400.0
YEAR_S = 365.25 * DAY_S
AU_M = 149_597_870_700.0

NEWTON_G_M3_KG_S2 = 6.67430e-11
SOLAR_GM_M3_S2 = 1.32712440041279419e20


def km_to_m(kilometers: float) -> float:
    return kilometers * KM_M


def days_to_s(days: float) -> float:
    return days * DAY_S


def years_to_s(years: float) -> float:
    return years * YEAR_S


def au_to_m(astronomical_units: float) -> float:
    return astronomical_units * AU_M
