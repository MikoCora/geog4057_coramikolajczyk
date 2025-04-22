import arcpy
import os

workspace = "C:/Users/coram/Documents/programing/geog4057/data/Ex7"
arcpy.env.workspace = workspace

raster_list = []
for dirpath, dirnames, filenames in arcpy.da.Walk(workspace, datatype="RasterDataset"):
    for filename in filenames:
        raster_list.append(os.path.join(dirpath, filename))

print(raster_list)



for raster in raster_list:
    raster_obj = arcpy.Raster(raster)
    print(f"Raster: {raster}")
    print(f"Number of Bands: {raster_obj.bandCount}")
    print(f"Spatial Resolution: {raster_obj.meanCellWidth} x {raster_obj.meanCellHeight}")
    print(f"Pixel Bit Depth: {raster_obj.pixelType}")
    print(f"Spatial Reference: {raster_obj.spatialReference.name}")



from arcpy.sa import Slope

elevation_path = "C:/Users/coram/Documents/programing/geog4057/data/Ex7/elevation"
slope_raster = Slope(elevation)
slope_raster.save("C:/Users/coram/Documents/programing/geog4057/data/Ex7/slope.tif")

import arcpy

# Define the paths to the input datasets
elevation = "C:/Users/coram/Documents/programing/geog4057/data/Ex7/elevation"
watershed = "C:/Users/coram/Documents/programing/geog4057/data/Ex7/watershed_HUC12.shp"

# Perform the clipping operation using arcpy.Clip_management
clipped_raster = arcpy.Clip_management(elevation, "#", "C:/Users/coram/Documents/programing/geog4057/data/Ex7/clipped_elevation.tif", watershed, "255", "ClippingGeometry", "NO_MAINTAIN_EXTENT")

print("Clipping operation completed and saved successfully.")


import arcpy

# Load the raster
raster_path = "C:/Users/coram/Documents/programing/geog4057/data/Ex7/tm.img"
raster = arcpy.Raster(raster_path)

# Get the number of bands
band_count = raster.bandCount
print(f"Number of bands: {band_count}")

# Describe the raster to get band information
desc = arcpy.Describe(raster_path)
for i, band in enumerate(desc.children, start=1):
    print(f"Band {i} name: {band.name}")



import arcpy
from arcpy.sa import *

# Define the path to the tm.img file
tm_img_path = "C:/Users/coram/Documents/programing/geog4057/data/Ex7/tm.img"

# Create Raster objects for each band
band3 = arcpy.Raster(tm_img_path + "/Layer_3")
band1 = arcpy.Raster(tm_img_path + "/Layer_1")

# Perform the raster calculation
result = (band3 - band1) / (band3 + band1)

# Save the result to your workspace
result.save("C:/Users/coram/Documents/programing/geog4057/data/Ex7/map_algebra_output.tif")





import numpy as np
import arcpy
from arcpy.sa import Raster, RasterCellIterator

# Read the elevation model
dem = Raster("elevation")
arcpy.env.overwriteOutput = True

# Get knowledge about the input raster
raster_info = dem.getRasterInfo()
cell_x = dem.meanCellWidth
cell_y = dem.meanCellHeight

# Change the raster info so the output type is 32-bit unsigned integer
raster_info.setPixelType("U32")

# Create a new raster based on the raster info
elev_reclass = Raster(raster_info)

# Update the raster using cell iterator
with RasterCellIterator({'rasters': [dem, elev_reclass]}) as rci:
    for r, c in rci:
        # Classification of elevation to 1 or 0
        if dem[r, c] > 2000:
            elev_reclass[r, c] = 1
        else:
            elev_reclass[r, c] = 0

# Save the new raster
elev_reclass.save('elev_reclass')


# Display the result in the notebook (if using Jupyter Notebook)
import matplotlib.pyplot as plt
import numpy as np

# Convert the result to a NumPy array for visualization
result_array = arcpy.RasterToNumPyArray(result)

# Plot the result
plt.imshow(result_array, cmap='gray')
plt.colorbar()
plt.title("Raster Calculation Result")
plt.show()



import numpy as np
import arcpy

elevation_raster = arcpy.Raster("C:/Users/coram/Documents/programing/geog4057/data/Ex7/elevation")
elevation_array = arcpy.RasterToNumPyArray(elevation_raster)

print(f"Min: {np.min(elevation_array)}")
print(f"Max: {np.max(elevation_array)}")
print(f"Mean: {np.mean(elevation_array)}")
print(f"Std: {np.std(elevation_array)}")


import arcpy
import numpy as np

# Read the elevation model
dem = arcpy.Raster("elevation")

# Convert the raster to a NumPy array
dem_array = arcpy.RasterToNumPyArray(dem)

# Print the array to verify
print(dem_array)

# Compute statistics
min_value = np.min(dem_array)
max_value = np.max(dem_array)
mean_value = np.mean(dem_array)
std_value = np.std(dem_array)

# Print the statistics
print(f"Min: {min_value}")
print(f"Max: {max_value}")
print(f"Mean: {mean_value}")
print(f"Standard Deviation: {std_value}")



