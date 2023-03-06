import arcpy
import math
from arcpy.sa import *
ws = arcpy.env.workspace

# 1a) Ausschnitt von Australien definieren:
# vier Eckpunkte festlegen, Koordinaten koennen aus der Karte abgelesen werden,
# Nord und Ost sind positive Werte, Sued und West sind negative Werte
polyPoints = [arcpy.Point(152.38, -27.44), arcpy.Point(152.44, -27.44),
             arcpy.Point(152.44, -27.41),arcpy.Point(152.38, -27.41)]
# extrahieren des Polygons
extPolygonOut = ExtractByPolygon("globcov2006_aus.tif_Band_1",polyPoints, "INSIDE")

# 1b) nur die vier Zustaende des CA sollen in dem Raster enthalten sein
vierZustaende = Lookup(extPolygonOut, "RECL_VALUE")
# speichern des Rasters ueber die 4 Zustaende
vierZustaende.save(ws + "\\vierZustaende")

# 1c) Cellulaerer Automat
altesRaster_ = Raster(vierZustaende)
zeitschritte = 7

for t in range(1, zeitschritte + 1):
    # neues Raster erstellen, welches als binaere Maske wirkt,
    # eine Zelle darin ist entweder 0 (= nicht urban) oder 1 (= urban)
    binaereMaske_ = Con(altesRaster_, 1, 0, "Value = 4")
    # focalStatistics: berechnet fuer jede Eingabezellenposition eine Statistik der Werte
    # innerhalb einer angegebenen Nachbarschaft. Wenn man diese Funktion mit der Maske
    # aufruft, werden somit alle urbanen Felder um das betrachtete Feld aufsummiert und in
    # einem neuen Raster wird pro Zelle die Anzahl der benachbarten urbanen Felder ge-
    # speichert, da alles nicht urbane 0 in der Maske ist. 3x3 Quadrat = Moore Nachbarschaft
    anzahlUrbaneNachbarn_ = FocalStatistics(binaereMaske_,
        NbrRectangle(3, 3, "CELL"), statistics_type = "SUM")
    # wenn mehr als 4 Nachbarn urban sind UND die Zelle vom Typ 3 (ungeschuetzt) ist, dann
    # wird das Feld auf 4 gesetzt, alle anderen Felder behalten den vorherigen Zustand
    neuesRaster = Con(((anzahlUrbaneNachbarn_ >= 4) & (altesRaster_ == 3)), 4, altesRaster_)
    # speichern des gerade berechneten Zeitschritts
    neuesRaster.save(ws + "\\Zeitschritt" + str(t))
    # altes und neues Raster fuer den naechsten Zeitschritt tauschen
    altesRaster_ = neuesRaster
