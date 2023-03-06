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
        arcpy.AddMessage(parameters[0].valueAsText)
        arcpy.AddMessage(parameters[1].value)
        arcpy.AddMessage(parameters[2].valueAsText)
        arcpy.AddMessage(parameters[3].valueAsText)

        # 2c) Vor der Ein/Ausgabe müssen die Attribute SEQ_NR aufsteigend sortiert werden
        # Schleife schreiben, die die Attribute HydroID und SEQ_NR jedes Segments aufsteigend sortiert nach SEQ_NR ausgibt
        # Art des Cursors: arcpy.da.SearchCursor und als Parameter ist param_links notwendig
        #zeilen = arcpy.da.SearchCursor(parameters[0].valueAsText, ["SEQ_NR", "HydroID"], sql_clause=(None, "ORDER BY SEQ_NR ASC"))
        #for i in zeilen:
            #arcpy.AddMessage("SEQ_NR: {0}, HydroID: {1}".format(i[0], i[1]))

        # 2d) Frachtberechnung:
        # zuerst die Frachtausleitung überall auf den Wert 0 setzen
        #arcpy.management.CalculateField(parameters[0].valueAsText, "Load_g_s", "0")

        # UpdateCursor zum ändern der einzelnen Felder in den Zeilen verwenden
        zeilen = arcpy.da.UpdateCursor(parameters[0].valueAsText, ["Travel_time_d", "Emission_g_s", "Load_g_s"])

        for i in zeilen:
            # Zuerst den Load auf 0 setzen
            i[2] = 0
            # Wenn die Traveltime Null ist, soll die WaterGleichung ignoriert werden
            if i[0] is None:
                i[2] = i[1]
            elif i[1] is None:
                i[2] = 0
            else:
                # Wenn die Traveltime ungleich 0 ist
                # Berechnung durchführen:
                # Abbaurate von 1/h in 1/s umrechnen
                #abbau = parameters[1].value * 60 * 60
                # Traveltime von 1/d in 1/s umrechnen
                #travel = i[0] * 24 * 60 * 60
                i[2] = i[1] #* math.exp(- abbau * travel)
                # stehe ich im dictonary drin?, ist da ein wert drinnen?
                arcpy.AddMessage(i)
            zeilen.updateRow(i)
        #return

#überdenken wann ich den load ins dictonary packen muss, wenn loiad = 0 ist, dann nicht rienpacken
