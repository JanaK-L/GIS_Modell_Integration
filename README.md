# GIS-Modell-Integration
Wissenschaft und Management benötigen vielfach Methoden zur Bearbeitung raumzeitlicher Fragestellungen. Daher ist die Verknüpfung räumlicher Aspekte (GIS) mit formalisierten Abbildern der Wirklichkeit und zeitlichen Aspekten (Modelle) ein wichtiges Thema. Die Anwendungsbereiche sind zahlreich und höchst divers:
* Landschaftsmodellierung: Stoffhaushalt, Wasserhaushalt, Landnutzung, Biotope, Habitate, ...
* Verkehrsplanung: Mobilitätsnachfrage, Verkehrsaufkommen, Verkehrssteuerung/-lenkung ...
* Emissions-/Immissionsabschätzung: Emittenten, Emissionsmengen, Eintragswege, Eliminationsprozesse ...

Dieses Projekt beinhaltet eine Habitatanalyse in Form eines multikriteriellen Klassifikationsmodells, eine empirische Erosionsmodellierung durch die Universal Soil Loss Equation, eine hydrologische Analyse, welche als Basis für die Frachtmodellierung und die Expositionsmodellierung von E. Coli Bakterien dient, und zuletzt ein Zellulärer Automat für die Modellierung des Urban Growth erstellt.

Genauere Details zu einzelnen Modellergebnissen sind im <a href="https://github.com/JanaK-L/GIS_Modell_Integration/blob/main/GMI_Protokoll.pdf" target="_blank" rel="noreferrer">Protokoll</a> zu finden.

# 1.) Habitatsanalyse 🐦🦁🐬🦒🦈🐆🐺🐻🐝 
Die Intergovernmental Science-Policy Platform on Biodiversity and Ecosystem Services (IPBES) hat die fünf Hauptursachen für das derzeitige Artensterben identifiziert: die Umweltverschmutzung, invasive Arten, die veränderte Nutzung von Meer und Land, die Ausbeutung von Organismen (Jagd, Wilderei, Überfischung, ...) und der Klimawandel [vgl. <a href="https://www.ipbes.net/global-assessment" target="_blank" rel="noreferrer">Global Assessment Report on Biodiversity and Ecosystem Services 2022</a>]. Systemwissenschaftlich gesehen bilden der Klimawandel und das Artensterben innerhalb unseres Ökosystems zusammen einen sich gegenseitig verstärkenden Rückkopplungskreis, welcher tendenziell eine eskalierende Auswirkung auf das Gesamtsystem zur Folge hat. Eine von vielen wichtigen Gegenmaßnahmen besteht darin, mindestens 30% aller Landflächen und aller Meere unter Schutz zu stellen [vgl. <a href="https://github.com/JanaK-L/GIS_Modell_Integration/blob/main/WWF-lpr-living-planet-report-2022-full-version-english.pdf" target="_blank" rel="noreferrer">Living Planet Report 2022</a>]. Welche Flächen für möglichst viele Arten einen potenziellen Lebensraum darstellen, kann durch Habitatsanalysen ermittelt werden. Beispiele: die Habitatsanalyse für den Mückenfänger in den USA oder die <a href="https://github.com/JanaK-L/GIS_Modell_Integration/blob/main/Habitatsmodellierung.pdf" target="_blank" rel="noreferrer">Präsentation über eine Beispielstudie einer Habitatsanalyse für pazifische Austernriffe in der chinesischen Laizhou Bucht</a> betrachtet werden.
<p align="center">
   <img src="https://github.com/JanaK-L/GIS_Modell_Integration/blob/main/images/Habitatsanalyse_Ergebnis.png" width="350" title="Ergebnis der Habitatsanalyse für den Mückenfänger">
</p>

# 2.) Universal Soil Loss Equation (USLE)
Neben der Vernässung und Versalzung sowie der chemischen, physikalischen und biologischen Degradation ist die Erosion ein treibender Faktor für die Bodendegradation (Verschlechterung der Bodenqualität). Seit 1945 sind weltweit ca. 12 Mio quadratkilometer betroffen. Für diese Flächen besteht die Möglichkeit des vollständigen Verlusts der landwirtschaftlichen Nutzbarkeit. Die Bodenerosion führt zum Abtrag fruchtbarer und humusreicher Feinerde durch abfließenden Niederschlag und Wind sowie zu dem Verlust der Nährstoff-und Wasserspeicherung. Nach dem Abtrag erfolgt die Deposition an anderer Stelle. Der jährliche Verlust liegt weltweit bei ca. 23-26 Milliarden Tonnen.
Die Bodenerosion wird durch unsachgemäße anthropogene Landnutzung (entfernen schützender Vegetation, vor allem Überweidung, Abholzung und zu kurzen Brachezeiten) begünstigt. Insbesondere der Verlust des Oberbodens ist problematisch. Die Erosion und der Sedimenttransport werden durch Wasser, Wind und Schwerkraft hervorgerufen und sind abhängig von der Niederschlagsintensität, dem Oberflächenabfluss, der Bodenerodierbarkeit, dem Gelände, und der Landbedeckung und Landnutzung. Für die Berechnung der Faktoren der USLE gibt es jeweils verschiedene empirische Formeln. In diesem Modell wird die RUSLE3D (Revised Universal Soil Loss Equation–3D) angewendet.
<p align="center">
   <img src="https://github.com/JanaK-L/GIS_Modell_Integration/blob/main/images/SoilLoss_Untersuchungsgebiet.png" width="350" title="Das Untersuchungsgebiet ist das Einzugsgebiet der Fränkischen Saale. Hier mit dem entsprechenden senkenlosen digitalen Gelände Modell (DGM) im Hintergrund dargestellt.">
   <img src="https://github.com/JanaK-L/GIS_Modell_Integration/blob/main/images/SoilLoss_KundCFaktor.png" width="545" title="Darstellung des K und des C Faktors (K = Bodenerodierbarkeitsfaktor [t*h*(1/mm)*(1/ha)], C = Bodenbedeckungs- und Managementfaktor [Wert zwischen 0 und 1, Beispiele: 0,5 = Kartoffeln/Karotten oder 0.02 = Weide/ Wiese)]).">
   <img src="https://github.com/JanaK-L/GIS_Modell_Integration/blob/main/images/SoilLoss_LSFaktor.png" width="350" title="Darstellungs des kombinierten LS Faktors (L = Hanglängenfaktor [L = 1 für eine Hanglänge von 22m (Standardhang)], S = Hangneigungsfaktor [S = 1 für eine Hangneigung von 9% (Standardhang)]).">
   <img src="https://github.com/JanaK-L/GIS_Modell_Integration/blob/main/images/SoilLoss_Abtrag.png" width="350" title="Der berechnete Abtrag [t*(1/ha)∙(1/a] im Untersuchungsgebiet.">
</p>

# 3.) 
Work in Progress

# 4.) 
Work in Progress
