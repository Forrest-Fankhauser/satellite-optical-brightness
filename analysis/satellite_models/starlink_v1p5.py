# Imports
from lumos.geometry import Surface
from lumos.brdf.library import BINOMIAL, PHONG
import numpy as np

# This code implements two satellite models
# The first model is for a Starlink v1.5 satellite with
# laboratory measured BRDFs.
# The second model is for a Starlink v1.5 satellite with
# BRDFs inferred from on-orbit brightness observations.

# Constants
chassis_area = 3.65 # m^2
solar_array_area = 22 # m^2

chassis_normal = np.array([0, 0, -1])
solar_array_normal = np.array([0, 1, 0])


# ------------- Model with Lab Measured BRDFs -------------------------------------------------------
# These BRDFs were found by fitting to data measured by Scatterworks.
# The script for fitting is "lab_brdf_fits.ipynb"

B = np.array([[3.34, -98.085]])
C = np.array([[-999.999, 867.538, 1000., 1000., -731.248, 618.552, -294.054, 269.248, -144.853, 75.196]])
lab_chassis_brdf = BINOMIAL(B, C, d = 3.0, l1 = -5)

B = np.array([[0.534, -20.409]])
C = np.array([[-527.765, 1000., -676.579, 430.596, -175.806, 57.879]])
lab_solar_array_brdf = BINOMIAL(B, C, d = 3.0, l1 = -3)

SURFACES_LAB_BRDFS = [
    Surface(chassis_area, chassis_normal, lab_chassis_brdf),
    Surface(solar_array_area, solar_array_normal, lab_solar_array_brdf)
]

# ------------- Model with Lab Measured BRDFs -------------------------------------------------------
# These BRDFs were found by fitting to actual satellite brightness observations.
# The script for fitting is "infer_brdfs.ipynb"

SURFACES_INFER_BRDFS = [
    Surface(1.0, chassis_normal, PHONG(0.34, 0.40, 8.9)),
    Surface(1.0, solar_array_normal, PHONG(0.15, 0.25, 0.26))
]
