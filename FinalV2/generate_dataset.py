"""
Run this script ONCE to generate the sample climate dataset.
Command: python generate_dataset.py
"""

import numpy as np
import pandas as pd
import netCDF4 as nc
from datetime import datetime

print("Generating climate dataset...")

# ── Dimensions ────────────────────────────────────────────────────────────────
lats  = np.linspace(-90, 90, 73)       # 2.5 degree grid
lons  = np.linspace(-180, 180, 144)
times = pd.date_range("1990-01-01", periods=120, freq="MS")  # 10 years monthly

lat2d, lon2d = np.meshgrid(lats, lons, indexing="ij")

np.random.seed(42)

# ── Temperature (°C) ──────────────────────────────────────────────────────────
print("  Generating temperature...")
base_temp = 30 - 0.5 * np.abs(lat2d)
temp_data = np.zeros((len(times), len(lats), len(lons)), dtype=np.float32)
for t, time in enumerate(times):
    seasonal = 10 * np.cos(2 * np.pi * (time.month - 7) / 12) * (lat2d / 90)
    noise    = np.random.normal(0, 1.5, lat2d.shape).astype(np.float32)
    trend    = 0.02 * t   # warming trend ~0.2°C/decade
    temp_data[t] = (base_temp + seasonal + noise + trend).astype(np.float32)

# ── Precipitation (mm/day) ────────────────────────────────────────────────────
print("  Generating precipitation...")
precip_data = np.zeros_like(temp_data)
for t, time in enumerate(times):
    itcz = 8 * np.exp(-((lat2d - 5) ** 2) / (2 * 15**2))   # ITCZ near 5°N
    monsoon = 3 * np.exp(-((lat2d - 15)**2) / (2*10**2)) * \
              np.exp(-((lon2d - 80)**2) / (2*30**2)) * \
              max(0, np.sin(2 * np.pi * (time.month - 3) / 12))
    noise = np.abs(np.random.normal(0, 0.8, lat2d.shape))
    precip_data[t] = np.clip(itcz + monsoon + noise, 0, None).astype(np.float32)

# ── Wind Speed (m/s) ──────────────────────────────────────────────────────────
print("  Generating wind speed...")
wind_data = np.zeros_like(temp_data)
for t in range(len(times)):
    jet_n = 12 * np.exp(-((lat2d - 50)**2) / (2 * 8**2))   # Northern jet ~50°N
    jet_s = 14 * np.exp(-((lat2d + 50)**2) / (2 * 8**2))   # Southern jet ~50°S
    noise = np.abs(np.random.normal(0, 2, lat2d.shape))
    wind_data[t] = (jet_n + jet_s + noise).astype(np.float32)

# ── Write NetCDF ──────────────────────────────────────────────────────────────
print("  Writing climate_data.nc ...")
ds = nc.Dataset("climate_data.nc", "w", format="NETCDF4")

# Dimensions
ds.createDimension("time", len(times))
ds.createDimension("lat",  len(lats))
ds.createDimension("lon",  len(lons))

# Coordinate variables
t_var = ds.createVariable("time", "f8", ("time",))
t_var.units    = "days since 1990-01-01"
t_var.calendar = "standard"
t_var.long_name = "time"
t_var[:] = nc.date2num(
    [datetime(d.year, d.month, d.day) for d in times],
    units=t_var.units, calendar=t_var.calendar
)

lat_var = ds.createVariable("lat", "f4", ("lat",))
lat_var.units    = "degrees_north"
lat_var.long_name = "latitude"
lat_var[:] = lats

lon_var = ds.createVariable("lon", "f4", ("lon",))
lon_var.units    = "degrees_east"
lon_var.long_name = "longitude"
lon_var[:] = lons

# Data variables
temp_v = ds.createVariable("temperature", "f4", ("time","lat","lon"),
                            zlib=True, complevel=4)
temp_v.units     = "degC"
temp_v.long_name = "Surface Temperature"
temp_v[:]        = temp_data

precip_v = ds.createVariable("precipitation", "f4", ("time","lat","lon"),
                               zlib=True, complevel=4)
precip_v.units     = "mm/day"
precip_v.long_name = "Precipitation Rate"
precip_v[:]        = precip_data

wind_v = ds.createVariable("wind_speed", "f4", ("time","lat","lon"),
                            zlib=True, complevel=4)
wind_v.units     = "m/s"
wind_v.long_name = "Wind Speed"
wind_v[:]        = wind_data

# Global attributes
ds.title       = "PyClimaExplorer Sample Dataset"
ds.institution = "Cosmos_Sync — GLA University, Mathura"
ds.source      = "Synthetic climate data for Technex '26 — Hack It Out"
ds.history     = f"Created {datetime.now().strftime('%Y-%m-%d')}"
ds.Conventions = "CF-1.8"

ds.close()

print("\n✅ Done! File saved: climate_data.nc")
print("   Variables : temperature, precipitation, wind_speed")
print("   Grid      : 73 x 144 (2.5° resolution)")
print("   Time      : 120 months (Jan 1990 – Dec 1999)")
print("\nNow upload climate_data.nc into the PyClimaExplorer app!")