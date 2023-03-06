import arcpy
import math
from arcpy.sa import *
ws = arcpy.env.workspace

# snapRaster defnieren, alle Raster sollen dann spaeter die gleiche Zellgroesse
# wie das Landnutzungsraster haben
arcpy.env.snapRaster = "DLCD_v2-1_MODIS_EVI_12_20130101-20141231.tif"
cellSize = Raster(arcpy.env.snapRaster).meanCellHeight

# Landnutzungsdaten vorbereiten: Auschnitt definieren, Sueden und Westen sind negativ
polyPoints = [arcpy.Point(150.6980128, -33.5824053), arcpy.Point(150.8270753, -33.5824053),
              arcpy.Point(150.8270753, -33.6749098), arcpy.Point(150.6980128, -33.6749098)]

# extrahieren des Auschnitts
extractedLandnutzung = ExtractByPolygon("DLCD_v2-1_MODIS_EVI_12_20130101-20141231.tif",
    polyPoints, "INSIDE")

# Mit Lookup nur die reklassifizierten 6 Klassen als Raster speichern
sechsZustaende = Lookup(extractedLandnutzung, "Reklass")


# Senken im DEM fuellen
DEM_senkenlos = Fill("output_SRTMGL1.tif")

# Hangneigung in Grad aus dem senkenlosen DEM berechnen
hangneigung = Slope(DEM_senkenlos, "DEGREE")

# Resampeln des Hagneigungsrasters auf die Zellgroesse des Landnutzungsrasters
hangneigungResampled = arcpy.management.Resample(hangneigung, "hangneigungResampled",
    cellSize, "BILINEAR")

# Ausschnitt fuer die Hangneigung extrahieren
extractedHangneigung = ExtractByPolygon(hangneigungResampled, polyPoints, "INSIDE")


# Mergen von Nichtschutzgebieten und Schutzgebieten, fuer ein lueckenloses Raster
arcpy.Merge_management(["capad", "Viereck"], "MergedSchutz")

# Schutzgebietelayer capad von 2014 in ein Raster ueberfuehren
schutzgebiete = arcpy.conversion.FeatureToRaster("MergedSchutz", "Schutz", "schutzgebiete",
    cellSize)

# Ausschnitt fuer die Schutzgebiete extrahieren
extractedSchutz = ExtractByPolygon(schutzgebiete, polyPoints, "INSIDE")


# Implementation des CA: die zu verwendenen Ebenen sind extractedSchutz, extractedHangneigung
# und sechsZustaende
altesRaster = Raster(sechsZustaende)
zeitschritte = 8

for i in range(1, zeitschritte):
    # binaere Maske erstellen, die besagt ob eine Zelle urban(6) ist oder nicht urban ist
    binaereMaske = Con(altesRaster, 1, 0, "Value = 4")
    # Raster mit Anzahl berechneter Nachbarn fuer jede Zelle zuerst mit 3X3
    anzahlUrbaneNachbarnDreiXDrei = FocalStatistics(binaereMaske, NbrRectangle(3, 3, "CELL"),
        statistics_type = "SUM")
    # und danach mit 4X4 Nachbarschaft
    anzahlUrbaneNachbarnVierXVier = FocalStatistics(binaereMaske, NbrRectangle(4, 4, "CELL"),
        statistics_type = "SUM")

    # Regeln umsetzen: wann aendert sich eine zelle zu urban?
    # 1. wenn im 4x4 mindestens 9 Nachbarzellen urban sind, wenn Zelle bebaubar (3) ist,
    #    wenn die Hangneigung <= 8.5 ist, wenn es kein Naturchutzgebiet ist.
    # 2. wenn im 3x3 mindestens 6 Nachbarzellen urban sind, wenn Zelle Wald (2) ist,
    #    wenn die Hangneigung <= 8.5 ist, wenn es kein Naturchutzgebiet ist.
    # 3. wenn im 3x3 mindestens 7 Nachbarzellen urban sind, wenn Zelle Feuchtgebiet (6) ist,
    #    wenn die Hangneigung <= 8.5 ist, wenn es kein Naturchutzgebiet ist.
    # 4. wenn im 3x3 mindestens 8 Nachbarzellen urban sind, wenn Zelle Wasser (1) ist,
    #    wenn die Hangneigung <= 8.5 ist, wenn es kein Naturchutzgebiet ist.
    neuesRaster = Con((extractedHangneigung <= 8.5) & (extractedSchutz == 0) & (((anzahlUrbaneNachbarnVierXVier >= 9) & (altesRaster == 3)) | ((anzahlUrbaneNachbarnDreiXDrei >= 6) & (altesRaster == 2)) | ((anzahlUrbaneNachbarnDreiXDrei >= 7) & (altesRaster == 6)) | ((anzahlUrbaneNachbarnDreiXDrei >= 8) & (altesRaster == 1))), 4, altesRaster)
    # aktuellen Zeitschritt speichern
    neuesRaster.save(ws + "\\zeitschritt" + str(i))
    # auf naechsten Zeitschritt vorbereiten
    altesRaster = neuesRaster
