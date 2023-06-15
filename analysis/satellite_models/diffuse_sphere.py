import numpy as np
import lumos.conversions
import lumos.constants
import lumos.calculator

# This code implements the diffuse sphere model for satellite brightness
# Brightness is a function of solar phase angle and satellite range

def get_intensity(area_albedo, sat_height, sat_alt, sat_az, sun_alt, sun_az):

    sat_x, sat_y, sat_z = lumos.conversions.altaz_to_unit(sat_alt, sat_az)
    sun_x, sun_y, sun_z = lumos.conversions.altaz_to_unit(sun_alt, sun_az)

    phi = np.arccos(sat_z) \
        - np.arcsin( np.sqrt(sat_x**2 + sat_y**2) \
        * lumos.constants.EARTH_RADIUS \
        / (lumos.constants.EARTH_RADIUS + sat_height) )
    
    satellite_range = np.sqrt(
        lumos.constants.EARTH_RADIUS**2
        + (lumos.constants.EARTH_RADIUS + sat_height)**2
        - 2 * lumos.constants.EARTH_RADIUS * (lumos.constants.EARTH_RADIUS + sat_height)
        * np.cos(phi)
        )
    
    solar_phase_angle = np.arccos( - (sat_x * sun_x + sat_y * sun_y + sat_z * sun_z) )

    intensity = (np.pi - solar_phase_angle) * np.cos(solar_phase_angle) + np.sin(solar_phase_angle)
    intensity = intensity * 2 * area_albedo / 3 / np.pi**2
    intensity = intensity * lumos.constants.SUN_INTENSITY / satellite_range**2

    _, _, _, apt = lumos.calculator.get_brightness_coords(
        sat_alt,
        sat_az,
        sat_height,
        sun_alt,
        sun_az
        )

    shadowed = apt > np.arccos(lumos.constants.EARTH_RADIUS 
                               / (lumos.constants.EARTH_RADIUS + sat_height))
    
    if isinstance(intensity, np.ndarray):
        intensity[shadowed] = 0
    elif shadowed:
        intensity = 0

    return intensity