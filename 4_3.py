# 3) Akkumulation von Abflusshoehen und Bakterienfrachten auf die Catchments
# das Aggregieren auf die Catchments geschieht mit Hilfe der sa.ZonalStatisticsAsTable
# Funktion, 1=Abflusshoehe, 2=Landnutzungsbakterienfracht, 3=Tierhaltungsbakterienfracht
arcpy.ia.ZonalStatisticsAsTable("CatchID", "Value", "runoff", "ZonalSt_CatchID1", "DATA", "ALL", "CURRENT_SLICE", 90, "AUTO_DETECT")
arcpy.ia.ZonalStatisticsAsTable("CatchID", "Value", "bakLand", "ZonalSt_CatchID2", "DATA", "ALL", "CURRENT_SLICE", 90, "AUTO_DETECT")
arcpy.ia.ZonalStatisticsAsTable("CatchID", "Value", "BactLoad_cattle_g", "ZonalSt_CatchID3", "DATA", "ALL", "CURRENT_SLICE", 90, "AUTO_DETECT")
