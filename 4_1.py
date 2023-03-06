import arcpy
from arcpy.sa import *
import math
ws = arcpy.env.workspace

# 1a) ein Fangraster und die Zellgroesse definieren, welche den Ergebnisrastern von Uebung 3
# entsprechen (z.B. SRTM_Saale_GK4), es muss ein spezifisches Band als snapRaster
# ausgewaehlt werden, hier SRTM_Saale_GK4.tif_Band_1
arcpy.env.snapRaster = "SRTM_Saale_GK4.tif_Band_1"
cellSize = arcpy.sa.Raster(arcpy.env.snapRaster).meanCellHeight

# MQ_Saale_HAD_GK4 zeigt die mittlere Abflusshoehe in [mm/a]
# Resampling der mittleren Abflusshoehe mit bilinearer Methode
MQ_Saale_HAD_GK4_Resample = arcpy.management.Resample("MQ_Saale_HAD_GK4",
    "MQ_Saale_HAD_GK4_Resample", cellSize, "BILINEAR")

# 1b) die resampelte Abflusshoehe ist noch in [mm/a] angegeben, es muss also noch eine
# Umrechnung in [m3/a] erfolgen
runoff = Raster("MQ_Saale_HAD_GK4_Resample") * 0.001 * cellSize * cellSize

# speichern
runoff.save(ws + "\\runoff")
