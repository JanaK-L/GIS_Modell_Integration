# 2b) mit der Lookup Funktion ein Raster mit den EMC Werten aus dem Datensatz
# CLC_Saale extrahieren, Umrechnung von [cfu/100ml] zu [cfu/m3]
emc = Lookup("CLC_Saale", "EMCs_per_100ml") * 10000

# 2c) Resampling des EMC Rasters, sodass es von der Zellgroesse her zum Abflussraster runoff
# passt, Nearest Neighbour als Resamplingmethode verwenden, da es sich bei den EMC Daten
# um eine nicht numerische Groesse handelt
emc_Resample = Raster(arcpy.management.Resample("emc", "emc_Resample", cellSize, "NEAREST"))

# Berechnung der Bakteriellen Fracht, Einheiten: [cfu/m3] * [m3/a] = [cfu/a]
bakLand = emc_Resample * runoff

# speichern
bakLand.save(ws + "\\bakLand")
