# import modules/system
import arcpy
import os 
from arcpy.sa import *


# set outputs directory

csv_path = r"C:\Users\coram\Documents\geog4057_coramikolajczyk\Final_Project\final_cfm\Transposed.csv"
tiff_path = r"C:\Users\coram\Documents\geog4057_coramikolajczyk\Final_Project\final_cfm\ncld_2011.tif"

#create xy event layer from csv
arcpy.management.MakeXYEventLayer(csv_path, "BeginLong", "BeginLat", "csv_layer")

# Path to your raster
raster_path = r"C:\Users\coram\Documents\geog4057_coramikolajczyk\Final_Project\final_cfm\nlcd_2011.tif"



# Calculate statistics
arcpy.management.CalculateStatistics(r"C:\Users\coram\Documents\geog4057_coramikolajczyk\Final_Project\final_cfm\nlcd_2011.tif")

# Build attribute table
arcpy.management.BuildRasterAttributeTable(r"C:\Users\coram\Documents\geog4057_coramikolajczyk\Final_Project\final_cfm\nlcd_2011.tif", "OVERWRITE")

#buffer is created
output_gdb = r"C:\Users\coram\Documents\ArcGIS\Projects\final_project\final_project.gdb"
csv_path = r"C:\Users\coram\Documents\geog4057_coramikolajczyk\Final_Project\final_cfm\Transposed.csv"
xy_layer = "points_layer"
projected_layer = "points_projected"
buffer_output = "points_buffer_289m"

# Create XY Event Layer from CSV
arcpy.management.MakeXYEventLayer(
    table=csv_path,
    in_x_field="BeginLong",  
    in_y_field="BeginLat",    
    out_layer=xy_layer,
    spatial_reference=4326  # WGS 1984
)

# Save to feature class
points_fc = f"{output_gdb}\\points"
arcpy.management.CopyFeatures(xy_layer, points_fc)


projected_fc = f"{output_gdb}\\{projected_layer}"
arcpy.management.Project(
    in_dataset=points_fc,
    out_dataset=projected_fc,
    out_coor_system=arcpy.SpatialReference(26960)  
)

# === 5. Create 289-meter buffer ===
buffer_fc = f"{output_gdb}\\{buffer_output}"
arcpy.analysis.Buffer(
    in_features=projected_fc,
    out_feature_class=buffer_fc,
    buffer_distance_or_field="289 Meters"
)

print("✅ Buffer created successfully.")


# Paths
input_raster = r"C:\Users\coram\Documents\geog4057_coramikolajczyk\Final_Project\final_cfm\nlcd2011.tif"
buffer_fc = r"C:\Users\coram\Documents\ArcGIS\Projects\final_project\final_project.gdb"
output_raster = r"C:\Users\coram\Documents\ArcGIS\Projects\final_project\final_project.gdb\nlcd_clipped"

# Clip the raster using the buffer
arcpy.management.Clip(
    in_raster=input_raster,
    rectangle="#",  # Use the feature geometry instead
    out_raster=output_raster,
    in_template_dataset=buffer_fc,
    nodata_value="0",
    clipping_geometry="ClippingGeometry",
    maintain_clipping_extent="NO_MAINTAIN_EXTENT"
)

print("✅ Raster clipped to buffer area.")



# Enable Spatial Analyst extension
arcpy.CheckOutExtension("Spatial")

# Set environment
arcpy.env.overwriteOutput = True

# Inputs
input_raster = r"C:\Users\coram\Documents\geog4057_coramikolajczyk\Final_Project\final_cfm\nlcd2011.tif"
mask_fc = r"C:\Users\coram\Documents\ArcGIS\Projects\final_project\final_project.gdb\points_buffer_289m"
output_masked_raster = r"C:\Users\coram\Documents\ArcGIS\Projects\final_project\final_project.gdb\nlcd_masked2"

# Apply the mask
masked_raster = ExtractByMask(input_raster, mask_fc)
masked_raster.save(output_masked_raster)

print("✅ Raster masked successfully.")


# Enable Spatial Analyst extension
arcpy.CheckOutExtension("Spatial")

# Set environment
arcpy.env.overwriteOutput = True

# Paths
project_folder = r"C:\Users\coram\Documents\ArcGIS\Projects\final_project"
masked_raster_path = fr"{project_folder}\final_project.gdb\nlcd_masked"
buffer_fc = fr"{project_folder}\final_project.gdb\points_buffer_289m"
scratch_gdb = fr"{project_folder}\scratch.gdb"

# Create scratch.gdb if it doesn't exist
if not arcpy.Exists(scratch_gdb):
    arcpy.CreateFileGDB_management(project_folder, "scratch.gdb")

# Load the raster
masked_raster = arcpy.Raster(masked_raster_path)
pixel_area = masked_raster.meanCellWidth * masked_raster.meanCellHeight  # m²

# Dictionary to store results
buffer_class_areas = {}

# Loop through each buffer
with arcpy.da.SearchCursor(buffer_fc, ["OID@", "SHAPE@"]) as buffer_cursor:
    for buffer_id, buffer_geom in buffer_cursor:
        # Extract raster within buffer
        extracted = ExtractByMask(masked_raster, buffer_geom)

        # Save to scratch.gdb with unique name
        temp_raster_path = fr"{scratch_gdb}\temp_extract_{buffer_id}"
        extracted.save(temp_raster_path)

        # Build attribute table
        arcpy.management.BuildRasterAttributeTable(temp_raster_path, "OVERWRITE")

        # Read class values and counts
        class_areas = {}
        with arcpy.da.SearchCursor(temp_raster_path, ["Value", "Count"]) as cursor:
            for value, count in cursor:
                area_sqm = count * pixel_area
                area_ha = area_sqm / 10000
                class_areas[value] = {
                    "count": count,
                    "area_sqm": area_sqm,
                    "area_ha": area_ha
                }

        buffer_class_areas[buffer_id] = class_areas

# Print results
for buffer_id, classes in buffer_class_areas.items():
    print(f"Buffer {buffer_id}:")
    for value, stats in classes.items():
        print(f"  Class {value}: {stats['count']} pixels, {stats['area_sqm']:.2f} m² ({stats['area_ha']:.2f} ha)")

print("✅ Area per class within each buffer calculated.")
