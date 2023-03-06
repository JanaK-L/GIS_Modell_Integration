# Importieren des Moduls arcpy
import arcpy

# Variablen initialisieren
laubwald = "CLC_c311"
nadelwald = "CLC_c312"
mischwald = "CLC_c313"
verkehr = "ver02l_lk"

# Zeilen fuer den Nahverkehr auswaehlen (OBA = 3101 AND BDU = 1001)
arcpy.SelectLayerByAttribute_management(verkehr, "NEW_SELECTION","OBA = 3101 AND BDU = 1002")
# aus den selektierten Zeilen im Layer Verkehr einen neuen Layer erstellen
nahverkehr = arcpy.CopyFeatures_management(verkehr, "nahverkehr")

# ebenso fuer Fernverkehr und fuer Bahnlinien je einen neuen Layer erstellen
# fernverkehr:
arcpy.SelectLayerByAttribute_management(verkehr, "NEW_SELECTION","OBA = 3101 AND BDU = 1001")
fernverkehr = arcpy.CopyFeatures_management(verkehr, "fernverkehr")
# bahnlinien:
arcpy.SelectLayerByAttribute_management(verkehr, "NEW_SELECTION", "OBA = 3201")
bahn = arcpy.CopyFeatures_management(verkehr, "bahn")

# Funktion schreiben, die als Parameter einen Abstand x, sowie In- und Outputlayer erhaelt
# ein Buffer mit dem uebergebenen Abstand wird um den Inputlayer gelegt
def baueBuffer(abstand, inputlayer, outputlayer):
    return arcpy.analysis.Buffer(inputlayer, outputlayer, abstand, "FULL", "ROUND", "ALL")

# Funktion fuer jede Verkehrsart einmal aufrufen und Output speichern
nahverkehrBuff = baueBuffer("200 Meters", nahverkehr, "nahverkehrBuff")
fernverkehrBuff = baueBuffer("500 Meters", fernverkehr, "fernverkehrBuff")
bahnBuff = baueBuffer("300 Meters", bahn, "bahnBuff")

# die drei Output Layer bezueglich der Buffer zu einem Layer zusammenfassen
# erster Parameter ist eine Liste der Layer, die zusammengefasst werden sollen
gesamtVerkehrBuff = arcpy.Merge_management([nahverkehrBuff, fernverkehrBuff, bahnBuff], "gesamtVerkehrBuff")

# anschliessend werden die Grenzen innerhalb des Verkehrspufferlayers entfernt
gesamtVerkehrBuffDissolved = arcpy.Dissolve_management(gesamtVerkehrBuff, "gesamtVerkehrBuffDissolved")

# ebenso werden die drei Waldarten zu einem Layer zusammengefuegt
gesamtWald = arcpy.Merge_management([nadelwald, mischwald, laubwald], "gesamtWald")
# danach werden die inneren Grenzen aufgeloest
gesamtWaldDissolved = arcpy.Dissolve_management(gesamtWald, "gesamtWaldDissolved")

# Ueberschneidung von Wald und Strassen als Polygon erstellen
intersectWaldStrassen = arcpy.analysis.Intersect([gesamtWaldDissolved, gesamtVerkehrBuffDissolved], "intersectWaldStrassen")

# von dem Wald die ueberlappenden Gebiete abziehen
waldOhneStrassen = arcpy.analysis.Erase(gesamtWaldDissolved, intersectWaldStrassen,                                           "waldOhneStrassen")

# das grosse Waldpolygon in mehrere einzelne Polygone aufteilen
waldMultiToSingle = arcpy.MultipartToSinglepart_management(waldOhneStrassen,                        "waldMultiToSingle")

# Feature Class in ein Array kopieren, nur die OBJECTID und Shape_Area als Felder mitnehmen
array = arcpy.da.FeatureClassToNumPyArray(waldMultiToSingle, ["OID@", "SHAPE@AREA"])

maximum = 0     # bisher groesste zusammenhaengende Waldflaeche
oid = 0         # OBJECTID
# array durchlaufen mit Laufvariable i, dabei groesste zusammenhaengende Waldflaeche suchen
for i in array:
    maximum = maximum + 1
    if i[1] > maximum:
        maximum = i[1]
        oid = i[0]

print(oid)      # Polygon mit der OBJECTID 183 hat die groesste Waldflaeche

# Selektieren der groessten Waldflaeche,
groessteWaldflaeche = arcpy.SelectLayerByAttribute_management(waldMultiToSingle,                     "NEW_SELECTION", "OBJECTID = 183")
# Folgendes funktioniert leider nicht:
# whereClause = "OBJECTID = " + str(oid)    # integer zu einem String casten
# arcpy.SelectLayerByAttribute_management(waldMultiToSingle, "NEW_SELECTION", whereClause)
