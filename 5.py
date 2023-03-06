import arcpy
import math

# Toolbox definieren
class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "GMI student"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [WATER_tool]

# erste Funktion der Toolbox, siehe Liste in zeile 12
class WATER_tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "WATER_tool"
        self.description = "Student Version of the WATER Tool."
        arcpy.env.overwriteOutput = True # allow the override of old files

    # Diese Funktion wird implizit vor dem Aufruf von execute aufgerufen und
    # definiert ein eingabefeld als Parameteruebergabe.
    def getParameterInfo(self):
        """Define parameter definitions"""
        # schema links
        param_links = arcpy.Parameter(
            displayName="Schema links",
            name="in_schema_links",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input")

        # 2a) Erweiterung um drei weitere Parameter, dabei auf die Datentypen
        # der Spalten in der Tabelle achten
        # Aggregierte Abbaurate als Input vom Typ GPDouble:
        param_aggreAbbau = arcpy.Parameter(
            displayName = "Aggregierte Abbaurate",
            name = "in_aggreAbbau",
            datatype = "GPDouble",
            parameterType = "Required",
            direction = "Input"
        )

        # Spaltenname fuer Frachteinleitung pro Segment als GPString:
        param_spaltennameFrachtein = arcpy.Parameter(
            displayName = "Spaltenname fuer die Frachteinleitung pro Segment",
            name = "in_spaltennameFrachtein",
            datatype = "GPString",
            parameterType = "Required",
            direction = "Input"
        )

        # Spaltenname fuer das Zielfeld der Berechnung (Frachtausleitung) vom Typ GPString:
        param_spaltennameFrachtaus = arcpy.Parameter(
            displayName = "Spaltenname fuer die Frachtausleitung",
            name = "in_spaltennameFrachtaus",
            datatype = "GPString",
            parameterType = "Required",
            direction = "Input"
        )

        # params wird dann fuer die execute funktion als parameters uebergeben
        params = [param_links, param_aggreAbbau, param_spaltennameFrachtein,
            param_spaltennameFrachtaus]
        return params


    def execute(self, parameters, messages):
        """The source code of the tool."""
        # 1c) Nachricht in View Details ausgeben
        arcpy.AddMessage("Starten des Tools Water_tool.")

        # 2b) Ausgeben der eingegebenen Parameter
        schemaLinks = parameters[0].valueAsText
        abbaurate = parameters[1].value
        lein = parameters[2].valueAsText
        load = parameters[3].valueAsText

        arcpy.AddMessage(schemaLinks)
        arcpy.AddMessage(abbaurate)
        arcpy.AddMessage(lein)
        arcpy.AddMessage(load)
        arcpy.AddMessage("---------------------------------------------------")

        # 2c) Vor der Ein/Ausgabe muessen die Attribute SEQ_NR aufsteigend sortiert werden
        # die Attribute HydroID und SEQ_NR eines jeden Segments aufsteigend sortiert
        # nach der SEQ_NR ausgeben
        zeilen = arcpy.da.SearchCursor(parameters[0].valueAsText, ["SEQ_NR", "HydroID"],
            sql_clause=(None, "ORDER BY SEQ_NR ASC"))
        for i in zeilen:
            arcpy.AddMessage("SEQ_NR: {0}, HydroID: {1}".format(i[0], i[1]))
        arcpy.AddMessage("---------------------------------------------------")

        # 2d) Frachtberechnung:
        # UpdateCursor zum aendern der einzelnen Felder in den Zeilen verwenden,
        # wichtig wieder an die Sortierung denken!
        zeilen = arcpy.da.UpdateCursor(schemaLinks, ["Travel_time_d", lein, load, "SEQ_NR",
            "HydroID", "DownLinkID"], sql_clause=(None, "ORDER BY SEQ_NR ASC"))

        # Abbaurate von 1/h in 1/s umrechnen, diese ist fuer alle Zeilen gleich
        abbau = abbaurate / 60 / 60

        # 2e) Initialisierung des NextDownDictonarys
        # Dictonaries bestehen aus Key-Value Paaren
        # ein bestimmter key kann nur maximal einmal im Dictonary vorhanden sein
        NextDownDictonary = {}

        for i in zeilen:
            # 2e) Dictonary, i[4] = HydroID, i[5] = NextDownID = DownLinkID
            # pruefen, ob der Link (HydroID) bereichts im Dictonary vorhanden ist
            if i[4] in NextDownDictonary:
                # falls ja, wird der zu dem Schluessel HydroID gehoerende Value sich gemerkt
                add_emission = NextDownDictonary[i[4]]
            else:
                # wenn der Link nicht im Dictonary ist, wird die emission auf 0 gesetzt
                add_emission = 0

            # wenn die eigene Frachteinleitung eines Links Null ist, dann erhaelt er
            # nur die Oberfracht (Fracht aus oberen Segmenten)
            if i[1] is None:
                einleitung = add_emission
            # wenn die eigene Frachteinleitung eines Links vorhanden ist, dann wird
            # diese zur Oberfracht dazu addiert
            else:
                einleitung = i[1] + add_emission

            # wenn die Traveltime Null ist, dann ist die ausleitung gleich der
            # einleitung und es findet kein Abbau statt
            if i[0] is None:
                ausleitung = einleitung
            # wenn eine Traveltime vorhanden ist, dann wird der Abbau berkuecksichtigt
            else:
                # Traveltime von 1/tag in sekunden umrechnen
                travel = i[0] * 24 * 60 * 60
                ausleitung = einleitung * math.exp(- abbau * travel)

            # die Ausleitung (Load_g_s) des Links dieser Zeile updaten
            i[2] = ausleitung

            # pruefen, ob bereits Frachten von dem Oberliegersegment in dem
            # Unterliegersegment vorkommen
            if i[5] in NextDownDictonary:
                # falls ja, wird die von diesem Link berechnete Ausleitungsfracht zu den
                # bekannten Frachten des Oberliegersegments aus dem Dictonary dazu addiert
                NextDownDictonary[i[5]] = NextDownDictonary[i[5]] + ausleitung
            else:
                # falls noch keine Frachten von dem Oberliegersegment vermerkt sind, wird
                # nur die Ausleitungsfracht des Segments in das Dictonary eingetragen
                NextDownDictonary[i[5]] = ausleitung

            # dem cursor Objekt sagen, dass es die Zeile speichern/updaten soll
            zeilen.updateRow(i)

        # 5f) Berechnen der Konzentration im neuen Feld Konzentration_ng_L:
        # zuerst die Ausleitung von gramm/s in nanogramm/s, dann in Jahr (damit sich beim
        # Teilen das Jahr herausrauskuerzt) umrechnen, bei runoff: 1 m3 = 1000 Liter
        arcpy.management.CalculateField(schemaLinks, "Konzentration_ng_L",
            "(!Load_g_s! * 1000 * 1000 * 1000 * 3600 * 24 * 365) / (!Runoff_m3_a! * 1000)",
            field_type = "DOUBLE")
