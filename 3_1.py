# Importieren des Moduls arcpy und der Toolbox Arc_Hydro_Tools_Pro
import arcpy
arcpy.ImportToolbox("C:\Program Files\ArcGIS\Pro\Resources\ArcToolBox\Toolboxes\Arc_Hydro_Tools_Pro")

# 1) Create Drainage Line Structures
with arcpy.EnvManager(scratchWorkspace=r"C:\Users\Jana\Dropbox\GIS_Modell_Integration\Uebung\Uebung3\Aufgabe1\Aufgabe1.gdb", workspace=r"C:\Users\Jana\Dropbox\GIS_Modell_Integration\Uebung\Uebung3\Aufgabe1\Aufgabe1.gdb"):
    arcpy.archydropro.CreateDrainageLineStructures("SRTM_Saale_GK4.tif", "Saale_rivers", r"C:\Users\Jana\Dropbox\GIS_Modell_Integration\Uebung\Uebung3\Aufgabe1\Layers\FdrStr", r"C:\Users\Jana\Dropbox\GIS_Modell_Integration\Uebung\Uebung3\Aufgabe1\Layers\StrLnk", r"C:\Users\Jana\Dropbox\GIS_Modell_Integration\Uebung\Uebung3\Aufgabe1\Aufgabe1.gdb\Layers\DrainageLine", r"C:\Users\Jana\Dropbox\GIS_Modell_Integration\Uebung\Uebung3\Aufgabe1\Aufgabe1.gdb\DrainageLine_FS", r"C:\Users\Jana\Dropbox\GIS_Modell_Integration\Uebung\Uebung3\Aufgabe1\Aufgabe1.gdb\Layers\EditPoint", "CLEAR_ANGLES_NO", "USE_RASTER_EXTENT_FALSE", None, 448.747618514969)

# 2) Fill Sinks
arcpy.archydropro.FillSinks("SRTM_Saale_GK4.tif", "SinksFilled", None, None, "ISSINK_NO")

# 3) DEM Reconditioning
arcpy.archydropro.DEMReconditioning("SRTM_Saale_GK4.tif", "StrLnk", 5, 10, 1000, r"C:\Users\Jana\Dropbox\GIS_Modell_Integration\Uebung\Uebung3\Aufgabe1\Layers\AgreeDEM", "NEGATIVE_NO")

# 4) Fill Sinks, nochmal da beim Einbrennen neue Senken entstanden sein koennen
arcpy.archydropro.FillSinks("AgreeDEM", r"C:\Users\Jana\Dropbox\GIS_Modell_Integration\Uebung\Uebung3\Aufgabe1\Layers\Fil", None, None, "ISSINK_NO")

#5) Flow Direction
arcpy.archydropro.FlowDirection("Fil", r"C:\Users\Jana\Dropbox\GIS_Modell_Integration\Uebung\Uebung3\Aufgabe1\Layers\Fdr", None)

#6) Adjust Flow Direction in Streams
arcpy.archydropro.AdjustFlowDirectioninStreams("Fdr", "FdrStr", r"C:\Users\Jana\Dropbox\GIS_Modell_Integration\Uebung\Uebung3\Aufgabe1\Layers\FdrStrAdj")

#7) Catchment Grid Delineation
arcpy.archydropro.CatchmentGridDelineation("FdrStrAdj", "StrLnk", r"C:\Users\Jana\Dropbox\GIS_Modell_Integration\Uebung\Uebung3\Aufgabe1\Layers\Cat")

#8) Catchment Polygon Processing
arcpy.archydropro.CatchmentPolygonProcessing("Cat", r"C:\Users\Jana\Dropbox\GIS_Modell_Integration\Uebung\Uebung3\Aufgabe1\Aufgabe1.gdb\Layers\Catchment")

#9) Adjoint Catchment Processing
arcpy.archydropro.AdjointCatchmentProcessing("DrainageLine", "Catchment", r"C:\Users\Jana\Dropbox\GIS_Modell_Integration\Uebung\Uebung3\Aufgabe1\Aufgabe1.gdb\Layers\AdjointCatchment", r"C:\Users\Jana\Dropbox\GIS_Modell_Integration\Uebung\Uebung3\Aufgabe1\Aufgabe1.gdb\Catchment_FS", "DrainageLine_FS")
