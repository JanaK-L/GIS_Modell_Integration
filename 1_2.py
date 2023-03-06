# Importieren des Moduls arcpy und den aktuellen Workspace Dateipfad abspeichern
import arcpy
workspace = arcpy.env.workspace

# Im Layer elevlt250_shp werden alle Bereiche mit einer Hoehe <= 250 m gespeichert
# Im Layer slopelt40_shp werden alle Bereiche mit einer Hangneigung <= 40 % gespeichert
# Die ueberschneidung dieser beiden Layer liefert die Gebiete, in welchen eine Hoehe <= 250 m und eine Hangneigung <= 40 % vorliegt.
arcpy.analysis.Intersect(["elevlt250_shp", "slopelt40_shp"], "elevIntersectSlope")

# majorrds: In der Spalte Distance ist der zu den Strassen benoetigte Abstand festgelegt
# Zuerst die kleineren Strassen selektieren und fuer diese einen Buffer mit 820 Feet anlegen
arcpy.SelectLayerByAttribute_management("majorrds_shp", "NEW_SELECTION", "Distance = 820")
arcpy.analysis.Buffer("majorrds_shp", "strassenBuffed820", "820 Feet", "FULL", "ROUND", "ALL")

# Anschliessend die grossen Strassen selektieren und einen Buffer mit 1312 Feet Abstand um die groesseren Strassen legen
arcpy.SelectLayerByAttribute_management("majorrds_shp", "NEW_SELECTION", "Distance = 1312")
arcpy.analysis.Buffer("majorrds_shp", "strassenBuffed1312", "1312 Feet", "FULL", "ROUND", "ALL")

# Die beiden Strassen Layer zusammenfuegen zu einem Layer
arcpy.Merge_management(["strassenBuffed1312", "strassenBuffed820"], "strassenBuffedGesamt")

# Von den moeglichen Gebieten bezueglich Hangneigung und Gelaendehoehe die Strassen inklusive Bufferzone abziehen
arcpy.analysis.Erase("elevIntersectSlope", "strassenBuffedGesamt", "habitateOhneStrassen")

# Klimazone 1 und 2 entsprechen der CLIMATE_ID = 2
arcpy.SelectLayerByAttribute_management("climate_shp", "NEW_SELECTION", "CLIMATE_ID = 2")
# ueberschneidungszone von den Klimazonen 1 und 2 mit den moeglichen Habitaten nach Abzug der Strassenabstaende
arcpy.analysis.Intersect(["climate_shp", "habitateOhneStrassen"], "klima2IntersectHabitate")

# Klimazone 1 und 2 entsprechen der CLIMATE_ID = 3
arcpy.SelectLayerByAttribute_management("climate_shp", "NEW_SELECTION", "CLIMATE_ID = 3")
# ueberschneidungszone von den Klimazonen 3 mit den moeglichen Habitaten nach Abzug der Strassenabstaende
arcpy.analysis.Intersect(["climate_shp", "habitateOhneStrassen"], "klima3IntersectHabitate")

# multi to single fuer Klimazone 1 und 2
arcpy.MultipartToSinglepart_management("klima2IntersectHabitate", "habitateOhneStrassenMultiToSingleKlima2")
# multi to single fuer klimazone 3
arcpy.MultipartToSinglepart_management("klima3IntersectHabitate", "habitateOhneStrassenMultiToSingleKlima3")

# Gebiete der Klimazone 1 und 2 muessen mindestens 1089000 quadratfeet gross sein
arcpy.SelectLayerByAttribute_management("habitateOhneStrassenMultiToSingleKlima2", "NEW_SELECTION", "Shape_Area >= 1089000")
arcpy.CopyFeatures_management("habitateOhneStrassenMultiToSingleKlima2", "habitate2")

# Gebiete der Klimazone 3 muessen mindestens 2178000 quadratfeet gross sein
arcpy.SelectLayerByAttribute_management("habitateOhneStrassenMultiToSingleKlima3", "NEW_SELECTION", "Shape_Area >= 2178000")
arcpy.CopyFeatures_management("habitateOhneStrassenMultiToSingleKlima3", "habitate3")

# moegliche Habitate aus den Klimazonen
arcpy.Merge_management(["habitate2", "habitate3"], "habitate")

# Gebiete mit der Kuestensalbeistaude sind mit HABITAT = 1 gekennzeichnet
arcpy.SelectLayerByAttribute_management("vegtype", "NEW_SELECTION", "HABITAT = 1")
arcpy.CopyFeatures_management("vegtype", "vegetation")

# ueberlappung von Vegetation mit Habitatraeumen feststellen, um Vegetationsflaechen, die ueber die Habitate hinausgehen, zu entfernen
arcpy.analysis.Intersect(["vegetation", "habitate"], "vegetationIntersectHabitate")

# Falls Vegetationsflaechen durch das Entfernen der nicht mit Habitatgebieten ueberlappenden Vegetation getrennt wurden,
# benoetigen diese nun je ein eigenes Polygon
arcpy.MultipartToSinglepart_management("vegetationIntersectHabitate", "vegetationIntersectHabitateMultiToSingle")

#  Ueberschneidung innerhalb der Habitate mit der Vegetation bestimmen
arcpy.analysis.Identity("habitate", "vegetationIntersectHabitateMultiToSingle", "identityVegHab")

# Die FID_habitate sagt, zu welchem habitat die Vegetationszone gehoert
# erstmal Tabelle aufraeumen, klappt noch nicht so ganz, die doppelten Felder sind noch drinnen
arcpy.management.DeleteField("identityVegHab", ["FID_climate_shp", "CLIMATE_ID", "Zone_", "FID_habitateOhneStrassen", "FID_elevlt250_shp",
                                               "FID_slopelt40_shp", "ORIG_FID", "FID_vegetationIntersectHabitateMultiToSingle", "FID_vegetation",
                                               "HOLLAND95", "HABITAT", "VEG_TYPE"])

# Feature Class in ein Array kopieren, dabei nur bestimmte Felder mitnehmen (Objektid und Shape_Area hier)
array = arcpy.da.FeatureClassToNumPyArray("identityVegHab", ["OID@", "FID_habitate", "SHAPE@AREA"])
# print(array)

oid = 0
fid = 0
fidalt = 1
area = 0
veg = []
sum = 0

# neues Array erstellen, indem in array die summen der Vegetation fuer jedes Habitat einzeln berechnet und gespeichert werden
for i in array:
    oid = i[0]
    if oid >= 95: # ab Eintrag 95 fangen die kleineren Vegetationsgebiete in den Habitaten an
        fid = i[1]
        area = i[2]
        if fid == fidalt:
            sum = sum + area
            #print(str(sum) + " bei der oid " + str(oid))
        else :
            veg.append([fidalt, sum])                     # Daten Speichern
            fidalt = fid                                  # jetzt kommt das naechste Habitat dran
            sum = area                                    # Summe mit neuem Startwert updaten

# letzte summe auch noch speichern
veg.append([fidalt, sum])

#for j in veg:
    #print(j[0])

# aus dem normalen Array ein numpy array machen
# numpyveg = numpy.array(veg, dtype=[("oid", int), ("vegarea", float)])
numpyveg = numpy.array(veg)

# anscheinend muessen numpy arrays noch formatiert werden
struct_array = numpy.core.records.fromarrays(numpyveg.transpose(), numpy.dtype([("oid", int), ("vegarea", float)]))
print(struct_array)


# wirft beim ersten mal keinen Fehler, aber ein Read/Write Lock sitzt dann 3 Jahre auf dem Layer und
# man kann den Layer in der Zeit nicht betrachten, Lock verschwand nach Tabel export...
arcpy.da.ExtendTable("habitate", "OBJECTID", struct_array, "oid")
