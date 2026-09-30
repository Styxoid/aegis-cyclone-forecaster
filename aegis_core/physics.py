"""
physics.py - Mathematical modeling for tropical cyclone wind field and storm surge dynamics.
Implements:
1. Holland Parametric Radial Wind Field Model (Holland 1980 / 2010).
2. Asymmetric wind field correction via forward translation velocity.
3. Kaplan-DeMaria inland decay modeling post-landfall.
4. Hydrodynamic storm-surge setup (Inverse Barometer Effect + Onshore Wind Stress Setup).
5. Micro-topography inundation depth calculation against asset plinth heights.
"""

import math
from typing import Dict, Any, Tuple

EARTH_RADIUS_KM = 6371.0
RHO_AIR = 1.15         # Air density in kg/m^3 (tropical marine boundary layer)
RHO_WATER = 1025.0     # Seawater density in kg/m^3
GRAVITY = 9.80665      # Acceleration due to gravity in m/s^2
P_AMBIENT_HPA = 1013.25 # Standard ambient sea level pressure in hPa
OMEGA_EARTH = 7.2921e-5 # Earth's angular rotation rate in rad/s

def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates great-circle distance between two coordinates in kilometers."""
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2.0)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2.0)**2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return EARTH_RADIUS_KM * c

def calculate_azimuth_deg(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates forward compass bearing from point 1 to point 2 in degrees [0, 360)."""
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dlambda = math.radians(lon2 - lon1)

    y = math.sin(dlambda) * math.cos(phi2)
    x = math.cos(phi1) * math.sin(phi2) - math.sin(phi1) * math.cos(phi2) * math.cos(dlambda)
    bearing = math.degrees(math.atan2(y, x))
    return (bearing + 360.0) % 360.0

def holland_wind_speed_kmph(
    r_km: float,
    p_central_hpa: float,
    p_ambient_hpa: float = P_AMBIENT_HPA,
    r_max_km: float = 30.0,
    lat_deg: float = 19.8,
    forward_speed_kmph: float = 0.0,
    storm_bearing_deg: float = 0.0,
    azimuth_to_asset_deg: float = 0.0
) -> float:
    """
    Computes surface wind speed at distance r_km from cyclone eye center using
    the Holland (1980, 2010) parametric formulation with asymmetric translation correction.
    
    Returns:
        Wind speed in km/h.
    """
    if r_km <= 0.5:
        # In the very center of the eye, wind speed drops towards zero
        return max(5.0, 15.0 * (r_km / max(1.0, r_max_km)))

    delta_p_hpa = max(5.0, p_ambient_hpa - p_central_hpa)
    delta_p_pa = delta_p_hpa * 100.0  # Convert hPa to Pa (N/m^2)

    # Holland Shape Parameter B (typically 1.1 to 2.2 in North Indian Ocean)
    # Empirical formulation: B = 1.0 + delta_p / 100.0
    b_param = max(1.05, min(2.35, 1.0 + (delta_p_hpa / 90.0)))

    # Coriolis parameter: f = 2 * Omega * sin(lat)
    f_coriolis = 2.0 * OMEGA_EARTH * math.sin(math.radians(lat_deg))

    # Convert radial distances from km to meters for SI equation
    r_m = r_km * 1000.0
    r_max_m = max(5.0, r_max_km) * 1000.0

    ratio = r_max_m / r_m
    ratio_pow_b = math.pow(ratio, b_param)

    # Holland gradient wind equation:
    # V(r) = sqrt( (B / rho_a) * (Rmax / r)^B * delta_P * exp(-(Rmax / r)^B) + (r * f / 2)^2 ) - (r * f / 2)
    bracket_term = (b_param / RHO_AIR) * ratio_pow_b * delta_p_pa * math.exp(-ratio_pow_b)
    coriolis_term = (r_m * f_coriolis / 2.0) ** 2

    # Numerical safeguard
    inner_val = max(0.0, bracket_term + coriolis_term)
    v_gradient_ms = math.sqrt(inner_val) - (r_m * f_coriolis / 2.0)
    v_gradient_ms = max(0.0, v_gradient_ms)

    # Reduction from gradient to 10m surface wind (standard boundary layer reduction ~0.80 - 0.85)
    v_surface_ms = 0.82 * v_gradient_ms
    v_surface_kmph = v_surface_ms * 3.6

    # Asymmetry correction due to storm forward translation:
    # In the Northern Hemisphere, right-front quadrant experiences enhanced winds (counter-clockwise cyclonic)
    if forward_speed_kmph > 0.0:
        # Cyclonic tangential wind direction is perpendicular to radius (azimuth + 90 deg)
        tangential_bearing = (azimuth_to_asset_deg + 90.0) % 360.0
        angle_diff = math.radians(tangential_bearing - storm_bearing_deg)
        asymmetry_kmph = 0.55 * forward_speed_kmph * math.cos(angle_diff)
        v_surface_kmph = max(0.0, v_surface_kmph + asymmetry_kmph)

    return round(v_surface_kmph, 1)

def kaplan_demaria_decay(
    v_initial_kmph: float,
    hours_inland: float
) -> float:
    """
    Kaplan & DeMaria (1995) exponential wind decay model after eye makes landfall.
    V(t) = V_b + (V_0 - V_b) * exp(-alpha * t)
    where V_b ~ 48 kmph (background low-pressure circulation), alpha ~ 0.095 hr^-1.
    """
    if hours_inland <= 0:
        return v_initial_kmph

    v_background = 45.0  # kmph
    alpha_decay = 0.095  # hr^-1

    decayed = v_background + (v_initial_kmph - v_background) * math.exp(-alpha_decay * hours_inland)
    return round(max(20.0, decayed), 1)

def calculate_storm_surge_elevation_m(
    p_central_hpa: float,
    max_wind_kmph: float,
    dist_to_coastline_km: float,
    p_ambient_hpa: float = P_AMBIENT_HPA,
    astronomical_tide_m: float = 0.60
) -> float:
    """
    Calculates total storm-surge water surface elevation (above MSL) combining:
    1. Inverse Barometer Effect: ~1 cm rise per 1 hPa pressure drop.
    2. Dynamic Onshore Wind Setup: Proportional to V_max^2 over shallow coastal bathymetry (Bay of Bengal).
    3. Astronomical Tide.
    4. Overland dissipation exponential decay with distance inland.
    """
    delta_p_hpa = max(0.0, p_ambient_hpa - p_central_hpa)

    # 1. Inverse Barometer Effect (m)
    eta_ib_m = 0.0101 * delta_p_hpa

    # 2. Dynamic Wind Setup (m)
    # Bay of Bengal is exceptionally shallow near Puri/Paradip; surge amplifies heavily
    wind_factor = (max_wind_kmph / 100.0) ** 2
    eta_wind_m = 0.65 * wind_factor

    # Total coastal sea level at shoreline
    shoreline_surge_total_m = eta_ib_m + eta_wind_m + astronomical_tide_m

    # 3. Overland exponential dissipation
    # As surge moves inland over coastal topography and vegetation, depth attenuates
    if dist_to_coastline_km <= 0:
        return round(shoreline_surge_total_m, 2)

    dissipation_rate_per_km = 0.18  # ~18% attenuation per inland kilometer
    inland_surge_m = shoreline_surge_total_m * math.exp(-dissipation_rate_per_km * dist_to_coastline_km)
    return round(max(0.0, inland_surge_m), 2)

def calculate_asset_inundation(
    surge_water_level_m: float,
    plinth_height_m: float
) -> float:
    """
    Calculates flood depth above asset foundation plinth.
    If water level does not exceed plinth, inundation is 0.0m.
    """
    depth = surge_water_level_m - plinth_height_m
    return round(max(0.0, depth), 2)
