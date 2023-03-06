# 5a), Berechnung des Parameters S
S = Divide(Minus(25400,Times(254,"GCN250_ARCII_Saale_GK4.tif")),"GCN250_ARCII_Saale_GK4.tif")

# Parameter fuer Resampling bestimmen
# Wichtig ist es ein snapRaster zu setzen, da ansonsten das Resampling spaeter nicht funktioniert
arcpy.env.snapRaster = "CatchID"
cellSize = arcpy.sa.Raster(arcpy.env.snapRaster).meanCellHeight

# 5b) Laden des Multiband-Raster der Niederschlaege, extrahieren der einzelnen Monatsraster
# und Berechnung des Runoff pro Zelle [mm/month] nach Formel
monthlyRasters = arcpy.sa.Raster("HYRAS_2019_Saale_months_GK4.tif", True).getRasterBands()
for i in range(1,13):
    # Extrahieren eines Bands fuer einen Monat
    # monat = arcpy.ia.ExtractBand("HYRAS_2019_Saale_months_GK4.tif", [i])
    monat = monthlyRasters[i-1]
    # Berechnung des Runoffs Pe nach gegebener Formel in [mm/month]
    monat = ((monat - 0.2 * S) **2) / (monat + 0.8 * S)
    # Resampeln
    monat = arcpy.management.Resample(monat, "monat_res", cellSize, "BILINEAR")
    # Umrechnung in [m3/a]
    monat = Times(Times(Divide("monat_res", 1000), cellSize), cellSize)
    # Tabellen fuer die Catchment Aggregation berechnen
    ZonalStatisticsAsTable("CatchID", "Value", monat, ws +"\\PeCatchmentMonat" + str(i))

# 5c) Man kann leider nicht einfach so ein schoenes Balkendiagramm von der benoetigten Zeile erstellen, da ansonsten der Rest der Tabelle sonst
# ebenfalls mit in das Diagramm gepackt wird. Mit nur einer Zeile selektiert funktioniert es leider auch nicht. Deshalb nun Erstellung einer neuen
# Tabelle mit zwei Spalten (Monat und Abflussmenge), welche nur die eine Zeile fuer den Abflusslink beinhalten soll.
arcpy.management.CreateTable(ws, "Jahresverlauf")

# Spalte fuer Monate hinzufuegen
arcpy.management.AddField("Jahresverlauf", "Monat", "SHORT")
arcpy.management.AddField("Jahresverlauf", "Abflussmenge", "FLOAT")

# Die eine gesuchte Zeile in der Tabelle schema_link suchen und benoetigte Werte fuer die 12 Monate merken
fields = ["DownLinkID", "P_Monat1", "P_Monat2", "P_Monat3", "P_Monat4", "P_Monat5", "P_Monat6", "P_Monat7", "P_Monat8", "P_Monat9", "P_Monat10", "P_Monat11", "P_Monat12"]
cursor = arcpy.da.SearchCursor("schema_link", fields)

for i in cursor:
    if i[0] == -2:  # Auslasslinkzeile suchen
        gesuchteZeile = i # Zeile merken
        break   # Abbrechen, da das Gesuchte bereits gefunden wurde

# 12 neue Zeilen erstellen mit den Zahlen 1 - 12 fuer jeden Monat
fields = ["Monat", "Abflussmenge"]
cursor = arcpy.da.InsertCursor("Jahresverlauf", fields)
for i in range(1, 13):
    # Abflussmenge reinschreiben
    cursor.insertRow((i, gesuchteZeile[i]))

# cursor object loeschen
del cursor

# 5e) Berechnen der Differenz
arcpy.CalculateField_management("schema_link", "DifferenzNovZuJahr", "!P_Monat11! - (!Runoff!/12)", "PYTHON3", "", "FLOAT")
