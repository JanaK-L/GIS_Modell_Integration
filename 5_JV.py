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

    # Diese Funktion wird implizit vor dem Aufruf von execute aufgerufen und definiert ein eingabefeld als Parameterübergabe.
    def getParameterInfo(self):
        """Define parameter definitions"""
        # schema links
        param_links = arcpy.Parameter(
            displayName="Schema links",
            name="in_schema_links",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input")

        # 2a) Erweiterung um drei weitere Parameter, Feld wird per klicken an die Attributtabelle dran gehängt
        # außerdem hinzufügen eines Feldes per Hand in die schema_link Tabelle (darauf achten, dass man beim Datentyp Double und nicht
        # Long (Long int) stehen hat!) die Felder nicht innerhalb des Skripts erstellt werden, müssen sie bereits vorher vorhanden sein
        # TODO: noch nicht vorhandene Felder mit insertcursor einfügen
        # Aggregierte Abbaurate als Input vom Typ GPDouble
        param_aggreAbbau = arcpy.Parameter(
            displayName = "Aggregierte Abbaurate",
            name = "in_aggreAbbau",
            datatype = "GPDouble",
            parameterType = "Required",
            direction = "Input"
        )

        # Spaltenname für Frachteinleitung pro Segment als GPString
        param_spaltennameFrachtein = arcpy.Parameter(
            displayName = "Spaltenname für die Frachteinleitung pro Segment",
            name = "in_spaltennameFrachtein",
            datatype = "GPString",
            parameterType = "Required",
            direction = "Input"
        )

        # Spaltenname für das Zielfeld der Berechnung (Frachtausleitung) vom Typ GPString
        param_spaltennameFrachtaus = arcpy.Parameter(
            displayName = "Spaltenname für die Frachtausleitung",
            name = "in_spaltennameFrachtaus",
            datatype = "GPString",
            parameterType = "Required",
            direction = "Input"
        )

        # params wird dann für die execute funktion als parameters übergeben
        params = [param_links, param_aggreAbbau, param_spaltennameFrachtein, param_spaltennameFrachtaus]
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
        arcpy.AddMessage("--------------------------------------------------------------")

        # 2c) Vor der Ein/Ausgabe müssen die Attribute SEQ_NR aufsteigend sortiert werden
        # Schleife schreiben, die die Attribute HydroID und SEQ_NR jedes Segments aufsteigend sortiert nach SEQ_NR ausgibt
        # Art des Cursors: arcpy.da.SearchCursor und als Parameter ist param_links notwendig
        #zeilen = arcpy.da.SearchCursor(parameters[0].valueAsText, ["SEQ_NR", "HydroID"], sql_clause=(None, "ORDER BY SEQ_NR ASC"))
        #for i in zeilen:
            #arcpy.AddMessage("SEQ_NR: {0}, HydroID: {1}".format(i[0], i[1]))
        #arcpy.AddMessage("--------------------------------------------------------------")

        # 2d) Frachtberechnung:
        # zuerst die Frachtausleitung überall auf den Wert 0 setzen
        # Achtung: So lieber nicht machen, weil kein Datentyp angegeben ist und in der Tabelle ein Integer Feld steht!!!
        # Stattdessen in der for Schleife auf 0 setzen!!!!
        # arcpy.management.CalculateField(parameters[0].valueAsText, "Load_g_s", "0")

        # UpdateCursor zum ändern der einzelnen Felder in den Zeilen verwenden, wichtig wieder an die Sortierung denken!
        zeilen = arcpy.da.UpdateCursor(schemaLinks, ["Travel_time_d", lein, load, "SEQ_NR", "HydroID", "DownLinkID"], sql_clause=(None, "ORDER BY SEQ_NR ASC"))

        # Abbaurate von 1/h in 1/s umrechnen, diese ist für alle Zeilen gleich
        abbau = abbaurate / 60 / 60

        # 4e) Initialisierung des NextDownDictonarys
        # Dictonaries bestehen aus Key-Value Paaren
        # ein bestimmter key kann nur maximal einmal im Dictonary vorhanden sein
        #überdenken wann ich den load ins dictonary packen muss, wenn load = 0 ist, dann nicht reinpacken
        NextDownDictonary = {}

        for i in zeilen:
            # zuerst Frachtausleitung (= load) für alle auf 0 setzen
            i[2] = 0
            # wenn nur die Traveltime gleich Null ist und lein ungleich Null ist, gilt load = lein (L1 = L0)
            if i[0] is None and i[1] is not None:
                i[2] = i[1]
                arcpy.AddMessage("nur travel ist null, L1 = L0 | SEQ_NR:" + str(i[3]) + " HydroID: " + str(i[4])) # dieser Fall tritt genau 0 mal auf ... Clowni!
            # wenn traveltime und lein beide Null sind, tue nichts, weil der Load sonst auf Null gesetzet werden würde ... Clowni!
            elif i[0] is None and i[1] is None:
                # i[1] = 0
                # load bleibt lieber 0, überschreiben von i[2] weglassen, da sonst null im load steht
                arcpy.AddMessage("beide null, L1 = Null | SEQ_NR:" + str(i[3]) + " HydroID: " + str(i[4])) # dieser Fall tritt oft auf
            # Wenn die Traveltime ungleich Null ist, Berechnung durchführen:
            else:
                # wenn die Traveltime ungleich Null ist, aber lein gleich Null ist, gibt es ein Problem, da man nicht mit Null rechnen kann
                # daher wird lein auf den Wert 0 gesetzt
                if i[1] is None:
                    i[1] = 0
                # Traveltime von d in s umrechnen
                travel = i[0] * 24 * 60 * 60
                i[2] = i[1] * math.exp(- abbau * travel)
                arcpy.AddMessage(i)

                # 4e) Dictonary, i[4] = HydroID, i[5] = NextDownID = DownLinkID
                # steht der Link (HydroID) bereichts im Dictonary drinnen?
                if i[4] in NextDownDictonary:
                    add_emission = NextDownDictonary[i[4]]
                else:
                    add_emission = 0
                # Kommen bereits Frachten von dem Oberliegersegment in dem Unterliegersegment vor?
                if i[5] in NextDownDictonary:
                    NextDownDictonary[i[5]] = NextDownDictonary[i[5]] + i[2]
                else:
                    NextDownDictonary[i[5]] = i[2]

            # dem cursor Objekt sagen, dass es die Zeile speichern/updaten soll
            zeilen.updateRow(i)

        arcpy.AddMessage(NextDownDictonary)
        # return
