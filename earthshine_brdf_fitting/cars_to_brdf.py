# This file converts CARs data to the appropriate BRDF format for Lumos fitting

import netCDF4
import matplotlib.pyplot as plt
import numpy as np
import os

SURFACES = {1 : 'snow',
            2 : 'vegetation',
            3 : 'clouds',
            4 : 'water',
            5 : 'smoke',
            6 : 'barren',
            7 : 'mixed'}

SAMPLES_PER_FILE = 500
for surface in SURFACES.values():
    filename = f"earthshine_brdf_fitting/processed_data/{surface}.csv"
    with open(filename, 'w') as file:
        file.write("phi_i     theta_i     phi_o     theta_o     brdf\n")

files = os.listdir("earthshine_brdf_fitting/cars_data/")

for file in files:
    dataset = netCDF4.Dataset(f"earthshine_brdf_fitting/cars_data/{file}",'r')
    metadata = dataset.__dict__
    surface_type = int( metadata["Surface_type"] )
    surface_code = SURFACES[surface_type]
    mean_solar_zenith = metadata["MeanSolarZenithAngle"]

    brdf = dataset["brdf_reflectance_479nm"][180:, :]
    azimuth_angles = dataset["AzimuthAngles"][:]
    zenith_angles = dataset["ZenithAngles"][180:]
    azimuth_angles, zenith_angles = np.meshgrid(azimuth_angles, zenith_angles)

    brdf, azimuth_angles, zenith_angles = brdf.flatten(), azimuth_angles.flatten(), zenith_angles.flatten()

    indexes = np.random.choice(brdf.size, size = SAMPLES_PER_FILE)

    brdf = brdf[indexes]
    azimuth_angles = azimuth_angles[indexes]
    zenith_angles = zenith_angles[indexes]

    phi_i, theta_i = mean_solar_zenith * np.ones_like(brdf), 180 * np.ones_like(brdf) 
    phi_o, theta_o = zenith_angles, azimuth_angles

    data = np.column_stack((phi_i, theta_i, phi_o, theta_o, brdf))

    fmt = ['%.3f', '%.3f', '%.3f', '%.3f', '%.5e']

    filename = f"earthshine_brdf_fitting/processed_data/{surface_code}.csv"
    with open(filename, 'a') as file:
        np.savetxt(file, data, delimiter = "     ", fmt = fmt)
