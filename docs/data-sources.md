# Data Sources

`PR3` introduces source-backed baseline constants for the Sun and eight planets.

Active sources used in this repository:

- JPL Solar System Dynamics planetary physical parameters:
  `https://ssd.jpl.nasa.gov/planets/phys_par.html`
- JPL Solar System Dynamics approximate planetary positions:
  `https://ssd.jpl.nasa.gov/planets/approx_pos.html`
- JPL Solar System Dynamics astrodynamic parameters:
  `https://ssd.jpl.nasa.gov/astro_par.html`
- NASA Science Sun facts:
  `https://science.nasa.gov/sun/facts/`

Source policy for `PR3`:

- masses, mean radii, sidereal rotation periods, and sidereal orbital periods for planets are taken from JPL Solar System Dynamics
- mean orbital radii are taken from JPL semi-major axis values and converted with the IAU astronomical unit
- Sun mass is derived from JPL heliocentric GM and CODATA G
- Sun mean radius and rotation period are approximate NASA Science values
- values are rounded for simulation readability after conversion to SI units
- future PRs may replace these constants with a more structured, source-verified dataset or later JPL Horizons integration

NSSDCA note:

- NASA's NSSDCA fact-sheet site was temporarily unavailable during `PR3`
- the public status page used during implementation was:
  `https://www.nasa.gov/nssdc/`
- because of that outage, JPL Solar System Dynamics and NASA Science were used as the active official sources
