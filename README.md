# GIS-Modell-Integration
Wissenschaft und Management benötigen vielfach Methoden zur Bearbeitung raumzeitlicher Fragestellungen. Daher ist die Verknüpfung räumlicher Aspekte (GIS) mit formalisierten Abbildern der Wirklichkeit und zeitlichen Aspekten (Modelle) ein wichtiges Thema. Die Anwendungsbereiche sind zahlreich und höchst divers:
* Landschaftsmodellierung: Stoffhaushalt, Wasserhaushalt, Landnutzung, Biotope, Habitate, ...
* Verkehrsplanung: Mobilitätsnachfrage, Verkehrsaufkommen, Verkehrssteuerung/-lenkung ...
* Emissions-/Immissionsabschätzung: Emittenten, Emissionsmengen, Eintragswege, Eliminationsprozesse ...

Dieses Projekt beinhaltet eine Habitatanalyse in Form eines multikriteriellen Klassifikationsmodells, eine empirische Erosionsmodellierung durch die Universal Soil Loss Equation, eine hydrologische Analyse, welche als Basis für die Frachtmodellierung und die Expositionsmodellierung von E. Coli Bakterien dient, und zuletzt ein Zellulärer Automat für die Modellierung des Urban Growth erstellt.

Genauere Details zu einzelnen Modellergebnissen sind im <a href="https://github.com/JanaK-L/GIS_Modell_Integration/blob/main/GMI_Protokoll.pdf" target="_blank" rel="noreferrer">Protokoll</a> zu finden.

# 1.) Habitatsanalyse 🐦🐊🦉🦈🦒🐺🐆🐍🐻🐝🐬🦬🐇
Die Intergovernmental Science-Policy Platform on Biodiversity and Ecosystem Services (IPBES) hat die fünf Hauptursachen für das derzeitige Artensterben identifiziert: die Umweltverschmutzung, invasive Arten, die veränderte Nutzung von Meer und Land, die Ausbeutung von Organismen (Jagd, Wilderei, Überfischung, ...) und der Klimawandel [vgl. <a href="https://www.ipbes.net/global-assessment" target="_blank" rel="noreferrer">Global Assessment Report on Biodiversity and Ecosystem Services 2022</a>]. Systemwissenschaftlich gesehen bilden der Klimawandel und das Artensterben innerhalb unseres Ökosystems zusammen einen sich gegenseitig verstärkenden Rückkopplungskreis, welcher tendenziell eine eskalierende Auswirkung auf das Gesamtsystem zur Folge hat. Eine von vielen wichtigen Gegenmaßnahmen besteht darin, mindestens 30% aller Landflächen und aller Meere unter Schutz zu stellen [vgl. <a href="https://github.com/JanaK-L/GIS_Modell_Integration/blob/main/WWF-lpr-living-planet-report-2022-full-version-english.pdf" target="_blank" rel="noreferrer">Living Planet Report 2022</a>]. Welche Flächen für möglichst viele Arten einen potenziellen Lebensraum darstellen, kann durch Habitatsanalysen ermittelt werden. Beispiele: die Habitatsanalyse für den Mückenfänger in den USA oder die <a href="https://github.com/JanaK-L/GIS_Modell_Integration/blob/main/Habitatsmodellierung.pdf" target="_blank" rel="noreferrer">Präsentation über eine Beispielstudie einer Habitatsanalyse für pazifische Austernriffe in der chinesischen Laizhou Bucht</a> betrachtet werden.
<p align="center">
   <img src="https://github.com/JanaK-L/GIS_Modell_Integration/blob/main/images/Habitatsanalyse_Ergebnis.png" width="350" title="Ergebnis der Habitatsanalyse für den Mückenfänger">
</p>

# 2.) Universal Soil Loss Equation (USLE)
Neben der Vernässung und Versalzung sowie der chemischen, physikalischen und biologischen Degradation ist die Erosion ein treibender Faktor für die Bodendegradation (Verschlechterung der Bodenqualität). Seit 1945 sind weltweit ca. 12 Mio quadratkilometer betroffen. Für diese Flächen besteht die Möglichkeit des vollständigen Verlusts der landwirtschaftlichen Nutzbarkeit. Die Bodenerosion führt zum Abtrag fruchtbarer und humusreicher Feinerde durch abfließenden Niederschlag und Wind sowie zu dem Verlust der Nährstoff-und Wasserspeicherung. Nach dem Abtrag erfolgt die Deposition an anderer Stelle. Der jährliche Verlust liegt weltweit bei ca. 23-26 Milliarden Tonnen.
Die Bodenerosion wird durch unsachgemäße anthropogene Landnutzung (entfernen schützender Vegetation, vor allem Überweidung, Abholzung und zu kurzen Brachezeiten) begünstigt. Insbesondere der Verlust des Oberbodens ist problematisch. Die Erosion und der Sedimenttransport werden durch Wasser, Wind und Schwerkraft hervorgerufen und sind abhängig von der Niederschlagsintensität, dem Oberflächenabfluss, der Bodenerodierbarkeit, dem Gelände, und der Landbedeckung und Landnutzung. Für die Berechnung der Faktoren der USLE gibt es jeweils verschiedene empirische Formeln. In diesem Modell wird die RUSLE3D (Revised Universal Soil Loss Equation–3D) mit einem kombinierten LS Faktor angewendet.
<p align="center">
   <img src="https://github.com/JanaK-L/GIS_Modell_Integration/blob/main/images/SoilLoss_Untersuchungsgebiet.png" width="250" title="Das Untersuchungsgebiet ist das Einzugsgebiet der Fränkischen Saale. Hier mit dem entsprechenden senkenlosen digitalen Gelände Modell (DGM) im Hintergrund dargestellt.">
   <img src="https://github.com/JanaK-L/GIS_Modell_Integration/blob/main/images/SoilLoss_KundCFaktor.png" width="420" title="Darstellung des K und des C Faktors (K = Bodenerodierbarkeitsfaktor [t∙h∙(1/mm)∙(1/ha)], C = Bodenbedeckungs- und Managementfaktor [Wert zwischen 0 und 1, Beispiele: 0,5 = Kartoffeln/Karotten oder 0.02 = Weide/ Wiese)]).">
</p>
  
<p align="center"> 
   <img src="https://github.com/JanaK-L/GIS_Modell_Integration/blob/main/images/SoilLoss_LSFaktor.png" width="250" title="Darstellungs des kombinierten LS Faktors (L = Hanglängenfaktor [L = 1 für eine Hanglänge von 22m (Standardhang)], S = Hangneigungsfaktor [S = 1 für eine Hangneigung von 9% (Standardhang)]).">
   <img src="https://github.com/JanaK-L/GIS_Modell_Integration/blob/main/images/SoilLoss_Abtrag.png" width="250" title="Der berechnete Abtrag [t∙(1/ha)∙(1/a)] im Untersuchungsgebiet.">
</p>

# 3.) Hydrologische Analyse, Bacterial Loading Model, SCS-CN Loss Modell, WATER Modell
Die Wasserqualität in europäischen Wasserkörpern wird zunehmend beeinträchtigt. Neben Schadstoffen spielen bakterielle Belastungen eine zunehmende Rolle. Bakterielle Belastungen können durch Fäkalien von Menschen oder Tieren sowie von organischem Material im Boden ausgehen. Potenzielle Eintragspfade sind Luft(-partikel, Aerosole), der Bodenabtrag von organischem Material sowie die Bodenaus-/Bodenabwaschung und Siedlungsabwässer, Landwirtschaft (Gülle) und Abwässer aus Gewerbe- und  Industriegebieten. Die Einträge können sowohl punktuell als auch diffus erfolgen. Während dem Transport finden Eliminationsprozesse (biologischer Abbau, Reinigung, Sorption an Partikeln, Sedmination im Gewässer) statt. Daher werden zusätzlich Informationen zu den Transportprozessen (Durchfluss, Sedimentationsraten, Flussmorphologie, Rauhigkeiten, ...) benötigt.

Für die Modellierung des Transportes von E. Coli Bakterien in dem Untersuchungsgebiet wird das topologisch korrekte Fließgewässernetz, welches im Rahmen der hydrologischen Analyse erzeugt wurde, verwendet. Das Fließgewässernetz dient als Grundlage für die Anwendung des Bacterial Loading Modells, womit die Bakterienfracht und die Bakterienkonzentrationsfracht modelliert wurden.

Die bisher alleinige Betrachtung des langjährigen Jahresmittels des Durchflusses vernachlässigt jedoch monatliche Schwankungen des Durchflusses, sowie jährliche Unterschiede im regionalen Niederschlag. Aus diesem Grund wurde die monatliche Abflussdynamik der Fränkischen Saale für das Jahr 2019 modelliert. Zur Überführung
von Niederschlag in abflusswirksamen Niederschlag wurde das SCS-CN (Soil Conservation Service - Curve Number) Loss Modell verwendet, welches eine empirische Methode zur Schätzung des Gesamtabflusses aus landwirtschaftlichen Wassereinzugsgebieten ist.

Zuletzt wurrde eine Python-Toolbox, welche das WATER Modell beinhaltet, implementiert. Mit WATER kann der Verbleib einer Substanz in Oberflächengewässern im Fließgleichgewicht simuliert werden. Das Modell berechnet für jeden Gewässerabschnitt die Veränderung der Eintragsfracht auf der Fließstrecke. Die Verlustprozesse werden mittels eines exponentiellen Zerfalls mit aggregierter Abbaurate dargestellt. Andere Benutzer können die implementierte Python-Toolbox "WATER_tool" verwenden, ohne sich selbst mit technischen Details rumschlagen zu müssen.

<p align="center">
   <img src="https://github.com/JanaK-L/GIS_Modell_Integration/blob/main/images/ArcHydro_NodesUndLinks.png" width="350" title="Das Ergebnis der hydrologischen Analyse ist ein topologisch korrektes Fließgewässernetz.">
   <img src="https://github.com/JanaK-L/GIS_Modell_Integration/blob/main/images/Bakterien_Frachtkonzentration.png" width="350" title="Der Durchfluss [m^3/a] und die berechnete Bakterienfrachtkonzentration [cfu/a mit cfu = colony forming unit = Zahl coliformer Bakterien] im Untersuchungsgebiet.">
   <img src="https://github.com/JanaK-L/GIS_Modell_Integration/blob/main/images/Bakterien_RunoffDifferenz.png" width="350" title="Die Durchflussdifferenz zwischen November und dem monatlichen Jahresdurchschnitt [m^3/a] im Jahr 2019.">
   <img src="https://github.com/JanaK-L/GIS_Modell_Integration/blob/main/images/Geoprocessing_EingabeInDasTool.png" width="412" title="Der Benutzer kann die implementierte Python-Toolbox WATER_tool (ganz rechts im Bild zu sehen) verwenden, ohne sich selbst mit technischen Details rumschlagen zu müssen.">
</p>


# 4.) Urban Sprawl mit erweitertem CA
Das Wachstum und der Flächenverbrauch in urbanen Räumen steigt rasant an und führt zur Zersiedelung der Landschaft. Die natürlichen Habitate vieler Arten werden durch diese Zersiedlung immer kleiner, welches letzendlich zu einem hohen Populationsdruck und dem Rückgang der ursprünglichen natürlichen Populationsgröße führt. Eine Simulation über 6 Zeitschritte wurde als Beispiel eines Urban Sprawls für ein kleines Gebiet in Australien durchgeführt. Die Modellierung der Stadtausbreitung basiert auf einem zellulären Automaten (CA). Als Basisebene des CA dient die Landnutzung Australiens aus dem Jahr 2014. Durch die Zunahme der thematischen Ebenen Naturschutzgebiet und Hangneigung wird das Modell des CA um zusätzliche Aspekte erweitert.

<p align="center">
   <img src="https://github.com/JanaK-L/GIS_Modell_Integration/blob/main/images/UrbanSprawl_Ergebnis.png" width="500" title="Der Urban Sprawls modelliert durch einen CA nach 6 Zeitschritten.">
</p>
