"""
CarbonZero Engine: Real-time and forecasted carbon intensity modeling for Google Cloud regions
and DevSecOps CI/CD runners.
"""

from datetime import datetime, timezone
from typing import Dict, List, Any

# Google Cloud Region Grid Carbon Intensity Baseline (gCO2eq/kWh) & Carbon Free Energy (CFE %)
GCP_REGIONS_EMISSIONS = {
    "europe-north1": {
        "location": "Hamina, Finland",
        "cfe_percentage": 94,
        "base_intensity": 28,  # gCO2eq/kWh
        "diurnal_variance": 5,
        "tier": "ultra_clean"
    },
    "europe-west1": {
        "location": "St. Ghislain, Belgium",
        "cfe_percentage": 82,
        "base_intensity": 98,
        "diurnal_variance": 15,
        "tier": "clean"
    },
    "us-central1": {
        "location": "Council Bluffs, Iowa, USA",
        "cfe_percentage": 78,
        "base_intensity": 180,
        "diurnal_variance": 45,  # heavy wind/solar swings
        "tier": "moderate"
    },
    "us-west1": {
        "location": "The Dalles, Oregon, USA",
        "cfe_percentage": 89,
        "base_intensity": 75,
        "diurnal_variance": 12,
        "tier": "clean"
    },
    "us-east4": {
        "location": "Ashburn, Virginia, USA",
        "cfe_percentage": 52,
        "base_intensity": 365,
        "diurnal_variance": 30,
        "tier": "fossil_heavy"
    },
    "asia-east1": {
        "location": "Changhua County, Taiwan",
        "cfe_percentage": 24,
        "base_intensity": 490,
        "diurnal_variance": 25,
        "tier": "fossil_heavy"
    },
    "asia-south1": {
        "location": "Mumbai, India",
        "cfe_percentage": 30,
        "base_intensity": 545,
        "diurnal_variance": 35,
        "tier": "fossil_heavy"
    }
}

# Average power consumption estimates (Watts)
SERVER_POWER_PER_VCPU = 12.5  # Watts per vCPU
RAM_POWER_PER_GB = 0.38       # Watts per GB RAM
PUE_GCP_AVERAGE = 1.10        # Google Cloud Power Usage Effectiveness average


def get_current_intensity(region: str, hour_offset: int = 0) -> Dict[str, Any]:
    """Calculates carbon intensity for a GCP region with simulated diurnal solar/wind variations."""
    region_info = GCP_REGIONS_EMISSIONS.get(region.lower(), GCP_REGIONS_EMISSIONS["us-central1"])
    now = datetime.now(timezone.utc)
    hour = (now.hour + hour_offset) % 24

    # Solar mid-day drop (hours 10-16 UTC adjustment depending on region)
    # Wind night peaks
    if 10 <= hour <= 16:
        # Solar peak: lower intensity
        variance_factor = -0.15
    elif 18 <= hour <= 22:
        # Evening peak demand: higher intensity
        variance_factor = 0.20
    else:
        variance_factor = 0.0

    calculated_intensity = round(region_info["base_intensity"] * (1 + variance_factor))

    return {
        "region": region,
        "location": region_info["location"],
        "carbon_intensity_gco2_kwh": calculated_intensity,
        "cfe_percentage": region_info["cfe_percentage"],
        "tier": region_info["tier"],
        "timestamp_utc": now.isoformat(),
        "hour_offset": hour_offset,
        "clean_rank": "A+" if calculated_intensity < 50 else ("A" if calculated_intensity < 120 else ("B" if calculated_intensity < 250 else "C"))
    }


def get_all_regions_summary() -> List[Dict[str, Any]]:
    """Returns real-time carbon intensity across all Google Cloud deployment regions."""
    results = []
    for reg in GCP_REGIONS_EMISSIONS.keys():
        results.append(get_current_intensity(reg))
    # Sort from cleanest to dirtiest
    results.sort(key=lambda x: x["carbon_intensity_gco2_kwh"])
    return results


def find_cleanest_gcp_region(exclude_regions: List[str] = None) -> Dict[str, Any]:
    """Identifies the greenest available GCP runner region."""
    all_regs = get_all_regions_summary()
    if exclude_regions:
        all_regs = [r for r in all_regs if r["region"] not in exclude_regions]
    return all_regs[0]


def calculate_pipeline_emissions(
    duration_minutes: float,
    vcpus: int = 4,
    ram_gb: int = 16,
    region: str = "us-central1"
) -> Dict[str, Any]:
    """
    Computes exact carbon footprint for a CI/CD job execution.
    Formula: Energy (kWh) = (Power in Watts * Duration in Hours * PUE) / 1000
             Emissions (gCO2eq) = Energy (kWh) * Carbon Intensity (gCO2eq/kWh)
    """
    intensity_data = get_current_intensity(region)
    intensity_gco2_kwh = intensity_data["carbon_intensity_gco2_kwh"]

    duration_hours = duration_minutes / 60.0
    total_watts = (vcpus * SERVER_POWER_PER_VCPU) + (ram_gb * RAM_POWER_PER_GB)
    total_kwh = (total_watts * duration_hours * PUE_GCP_AVERAGE) / 1000.0

    emissions_gco2 = round(total_kwh * intensity_gco2_kwh, 3)

    # Calculate savings if shifted to the cleanest region (e.g. europe-north1)
    cleanest = find_cleanest_gcp_region()
    cleanest_emissions_gco2 = round(total_kwh * cleanest["carbon_intensity_gco2_kwh"], 3)
    savings_gco2 = max(0.0, round(emissions_gco2 - cleanest_emissions_gco2, 3))
    savings_percentage = round((savings_gco2 / emissions_gco2 * 100), 1) if emissions_gco2 > 0 else 0

    return {
        "pipeline_duration_mins": duration_minutes,
        "vcpus": vcpus,
        "ram_gb": ram_gb,
        "current_region": region,
        "energy_consumed_kwh": round(total_kwh, 4),
        "carbon_emitted_gco2": emissions_gco2,
        "cleanest_region_alternative": cleanest["region"],
        "cleanest_region_emissions_gco2": cleanest_emissions_gco2,
        "potential_savings_gco2": savings_gco2,
        "potential_savings_percentage": savings_percentage,
        "equivalent_car_meters_driven": round(emissions_gco2 * 5.2, 1)  # ~192g CO2 per km for avg petrol car
    }


def forecast_24h_windows(region: str) -> List[Dict[str, Any]]:
    """Forecasts 24-hour carbon intensity windows to identify green time slots."""
    windows = []
    for offset in range(0, 24, 2):
        data = get_current_intensity(region, hour_offset=offset)
        windows.append({
            "hour_offset": offset,
            "intensity_gco2_kwh": data["carbon_intensity_gco2_kwh"],
            "grade": data["clean_rank"],
            "recommended_for_batch": data["carbon_intensity_gco2_kwh"] < 150
        })
    return windows
