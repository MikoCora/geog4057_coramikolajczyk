import arcpy
from arcpy.sa import *
import os

class Toolbox(object):
    def __init__(self):
        self.label = "Final Project Toolbox"
        self.alias = "final_project"
        self.tools = [BufferAndAnalyzeLandCover]

class BufferAndAnalyzeLandCover(object):
    def __init__(self):
        self.label = "Buffer and Analyze Land Cover"
        self.description = "Creates buffers around points, clips raster, and calculates land cover area per buffer."

    def getParameterInfo(self):
        params = [
            arcpy.Parameter(
                displayName="Input CSV File",
                name="csv_path",
                datatype="DEFile",
                parameterType="Required",
                direction="Input"
            ),
            arcpy.Parameter(
                displayName="Raster File (NLCD)",
                name="raster_path",
                datatype="DERasterDataset",
                parameterType="Required",
                direction="Input"
            ),
            arcpy.Parameter(
                displayName="Output Geodatabase",
                name="output_gdb",
                datatype="DEWorkspace",
                parameterType="Required",
                direction="Input"
            ),
            arcpy.Parameter(
                displayName="Buffer Distance (meters)",
                name="buffer_distance",
                datatype="Double",
                parameterType="Optional",
                direction="Input"
            )
        ]
        params[3].value = 289  # Default buffer distance
        return params

    def execute(self, parameters, messages):
        csv_path = parameters[0].valueAsText
        raster_path = parameters[1].valueAsText
        output_gdb = parameters[2].valueAsText
        buffer_distance = parameters[3].value

        arcpy.CheckOutExtension("Spatial")
        arcpy.env.overwriteOutput = True

        # Step 1: Create XY Event Layer
        xy_layer = "xy_layer"
        arcpy.management.MakeXYEventLayer(csv_path, "BeginLong", "BeginLat", xy_layer, arcpy.SpatialReference(4326))
        points_fc = os.path.join(output_gdb, "points")
        arcpy.management.CopyFeatures(xy_layer, points_fc)

        # Step 2: Project to NAD 1983 UTM Zone 16N
        projected_fc = os.path.join(output_gdb, "points_projected")
        arcpy.management.Project(points_fc, projected_fc, arcpy.SpatialReference(26916))

        # Step 3: Buffer
        buffer_fc = os.path.join(output_gdb, "points_buffer")
        arcpy.analysis.Buffer(projected_fc, buffer_fc, f"{buffer_distance} Meters")

        # Step 4: Clip Raster
        clipped_raster = os.path.join(output_gdb, "nlcd_clipped")
        arcpy.management.Clip(
            in_raster=raster_path,
            rectangle="#",
            out_raster=clipped_raster,
            in_template_dataset=buffer_fc,
            nodata_value="0",
            clipping_geometry="ClippingGeometry",
            maintain_clipping_extent="NO_MAINTAIN_EXTENT"
        )

        # Step 5: Extract by Mask
        masked_raster = ExtractByMask(clipped_raster, buffer_fc)
        masked_raster_path = os.path.join(output_gdb, "nlcd_masked")
        masked_raster.save(masked_raster_path)

        # Step 6: Calculate Area per Class per Buffer
        pixel_area = masked_raster.meanCellWidth * masked_raster.meanCellHeight
        buffer_class_areas = {}
        scratch_gdb = os.path.join(os.path.dirname(output_gdb), "scratch.gdb")
        if not arcpy.Exists(scratch_gdb):
            arcpy.CreateFileGDB_management(os.path.dirname(output_gdb), "scratch.gdb")

        with arcpy.da.SearchCursor(buffer_fc, ["OID@", "SHAPE@"]) as buffer_cursor:
            for buffer_id, buffer_geom in buffer_cursor:
                extracted = ExtractByMask(masked_raster, buffer_geom)
                temp_raster_path = os.path.join(scratch_gdb, f"temp_extract_{buffer_id}")
                extracted.save(temp_raster_path)
                arcpy.management.BuildRasterAttributeTable(temp_raster_path, "OVERWRITE")

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

        # Output results to messages
        for buffer_id, classes in buffer_class_areas.items():
            messages.addMessage(f"Buffer {buffer_id}:")
            for value, stats in classes.items():
                messages.addMessage(f"  Class {value}: {stats['count']} pixels, {stats['area_sqm']:.2f} m² ({stats['area_ha']:.2f} ha)")

        messages.addMessage("✅ Analysis complete.")
