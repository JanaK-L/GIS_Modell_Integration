# 4d) Simulation mit Gewichtung, Weight muss selbst ausgerechnet werden
# uebernimmt nur das feld reallength in die schema link tabelle
arcpy.management.JoinField("schema_link", "FeatureID", "drain_line", "HydroID", "RealLength")

# Berechnen von Q
arcpy.CalculateField_management("schema_link", "Q", "!Runoff!/(365*24*60*60)", "PYTHON3", "", "FLOAT")

# Berechnen von der Fliessgeschwindigkeit V, ** fuer exponenten
arcpy.CalculateField_management("schema_link", "V", "0.7376 * (35.3147 * !Q!) ** 0.1035", "PYTHON3", "", "FLOAT")

# Traveltime: RealLength / V (anschliessend in 1/Tag)
arcpy.CalculateField_management("schema_link", "Traveltime", "!RealLength! / !V! /(60*60*24)", "PYTHON3", "", "FLOAT")

# Weight berechnen
arcpy.CalculateField_management("schema_link", "Weight", "math.e ** (-1.5 * !Traveltime!)", "PYTHON3", "", "FLOAT")

# 4e) Berechnung der Konzentration
arcpy.CalculateField_management("schema_link", "Konzentration", "!LandTierAbbau! / !Runoff!", "PYTHON3", "", "FLOAT")

# Nach 4e) noch fuer die anderen 3 Szenarien die Konzentration berechnen
arcpy.CalculateField_management("schema_link", "KonzBakLand", "!BakLand! / !Runoff!", "PYTHON3", "", "FLOAT")
arcpy.CalculateField_management("schema_link", "KonzBakTier", "!BakTier! / !Runoff!", "PYTHON3", "", "FLOAT")
arcpy.CalculateField_management("schema_link", "KonzBakLandTier", "!BakLandTier! / !Runoff!", "PYTHON3", "", "FLOAT")
