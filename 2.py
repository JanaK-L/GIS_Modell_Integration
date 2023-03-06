import arcpy
import math
# importiert alles aus dem Spatial Analyst Tool, ansonsten muesste man ueber arcpy.sa. vor eine Funktion schreiben
from arcpy.sa import*

# 1.3 Raster, welches in der aktuellen Map geladen ist in Python laden, dgm = digitales Gelaendemodell, damit man mit dem Raster Rechnungen durchfuehren kann
dgm = Raster("SRTM_Saale_GK4.tif")

#senkenloses DGM erzeugen
senkenlosDGM = Fill(dgm)

# Fliessrichtung aus dem senkenlosen DGM ableiten
fliessrichtung = FlowDirection(senkenlosDGM)
fliessakkumulation = FlowAccumulation(fliessrichtung)

# Ermitteln Sie die Hangneigung als Gradangaben aus dem senkenlosen
hangneigung = Slope(senkenlosDGM, "DEGREE")

# Berechnung des kombinierten ls Faktors von RUSLE3D
cellSize = 77
ls = ((fliessakkumulation * (cellSize ** 2) * (1 / 22.1)) ** 0.4) * ((Sin(hangneigung * 0.01745) * (1 / 0.0896))** 1.3) * 1.4

# Statistiken vom ls berechnen
lsMax = arcpy.management.GetRasterProperties(ls, "MAXIMUM")
lsMittel = arcpy.management.GetRasterProperties(ls, "MEAN")
lsMin = arcpy.management.GetRasterProperties(ls, "MINIMUM")

# Berechnung des mittleren progostizierten Bodenabtrags: A = R * K * L * S * C * P
# R und P werden aufgrund homogener Bedingungen vernachlaessigt: A = K * L * S * C
abtrag = Raster("K_factor_Saale.tif") * ls * Raster("C_factor_Saale.tif")

# Statistiken von abtrag berechnen [t * ha-1 * a-1]
abtragMax = arcpy.management.GetRasterProperties(abtrag, "MAXIMUM")
abtragMean = arcpy.management.GetRasterProperties(abtrag, "MEAN")
abtragMin = arcpy.management.GetRasterProperties(abtrag, "MINIMUM")
