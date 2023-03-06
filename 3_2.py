# Flow Accumulation
arcpy.archydropro.FlowAccumulation("FdrStrAdj", r"C:\Users\Jana\Dropbox\GIS_Modell_Integration\Uebung\Uebung3\Aufgabe1\Layers\Fac")

# Drainage Point Processing
arcpy.archydropro.DrainagePointProcessing("Fac", "Cat", "Catchment", r"C:\Users\Jana\Dropbox\GIS_Modell_Integration\Uebung\Uebung3\Aufgabe1\Aufgabe1.gdb\Layers\DrainagePoint")

# Create Hydro Network from Catchment
# falls ein Fehler bezueglich einer doppelten FeatureID auftritt,  muss in der Tabelle
# der DrainageLine Featureclass die Spalte FeatureID geLoescht werden
arcpy.archydropro.CreateHydroNetworkfromCatchment("DrainageLine", "Catchment", "DrainagePoint", "ArcHydro", r"C:\Users\Jana\Dropbox\GIS_Modell_Integration\Uebung\Uebung3\Aufgabe1\Aufgabe1.gdb\Layers\HydroEdge", r"C:\Users\Jana\Dropbox\GIS_Modell_Integration\Uebung\Uebung3\Aufgabe1\Aufgabe1.gdb\Layers\HydroJunction")

# Generate Node Link Schema
arcpy.archydropro.GenerateNodeLinkSchema("HydroJunction", "HydroEdge", r"C:\Users\Jana\Dropbox\GIS_Modell_Integration\Uebung\Uebung3\Aufgabe1\Aufgabe1.gdb\Layers\SchemaLink", r"C:\Users\Jana\Dropbox\GIS_Modell_Integration\Uebung\Uebung3\Aufgabe1\Aufgabe1.gdb\Layers\SchemaNode", "Catchment", None)
