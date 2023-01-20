#文档草稿

## ITK Engineering

## Vorbereitung
An meinem ersten Arbeitstag verbrachte ich die meiste Zeit damit, gemeinsam mit meinem Betreuer meinen Arbeitslaptop einzurichten und mich mit den verwendeten Programmen wie Outlook als E-Mail- und Kalenderprogramm und Microsoft Teams als internes Kommunikationstool vertraut zu machen. Durch die Anleitung meines Betreuers lernte ich viele wichtige Regeln für das Informationsmanagement im Unternehmensalltag kennen. Zum Beispiel müssen die Mitarbeiter regelmäßig ihre Passwörter auf den Arbeitscomputern ändern und eine spezielle Software zur Passwortverwaltung nutzen. Außerdem müssen die Mitarbeiter bei der Installation neuer Software auf den Arbeitsrechnern prüfen, ob diese Software auf der Whitelist steht usw.

In Confluence, einer Wiki-Software, die als Unternehmenswiki dient, stehen den Mitarbeitern zahlreiche Materialien und Projektdokumentationen zur Verfügung. Nachdem ich das Handbuch für neue Mitarbeiter gelesen hatte, fand ich im Wiki-Bereich der RTA-Gruppe Schulungspläne und Materialien zum Thema FPGA. In meiner ersten Arbeitswoche habe ich die offiziellen Tutorials von Xilinx und The Zynq Book, ein Einführungsbuch, das man unbedingt lesen sollte, wenn man sich mit Zynq vertraut machen will, grob durchgelesen.
## Ziel
Meine Hauptaufgabe während des Praktikums besteht darin, ein komplettes Bildverarbeitungsprojekt auf der Zynq-Plattform zu implementieren und zu dokumentieren. In früheren Laboren an der Universität habe ich bereits Erfahrungen mit dem Einsatz von FPGAs zur Realisierung von Audioverarbeitungsprojekten gesammelt. Aber Zynq ist eine Architektur, die sowohl FPGAs als auch einen Prozessor kombiniert, und für die Entwicklung muss ich die von Xilinx bereitgestellten Entwicklungsumgebungen Vivado und Vitis verwenden. Ich muss mich also schnell mit der Zynq-Architektur und der neuen Entwicklungsumgebung vertraut machen. Deshalb hat mein Betreuer die Hauptaufgabe in mehrere kleine Aufgaben aufgeteilt. Jede Woche hatte ich ein Online-Meeting mit meinem Betreuer, um über den Fortschritt meiner Aufgaben und Probleme zu berichten.

## Xilinx Zynq SoC-Architectur
Zynq ist ein All Programmable System-on-Chip (APSoC) von Xilinx, das die Software-Programmierbarkeit eines Prozessors mit der Hardware-Programmierbarkeit eines FPGA kombiniert und somit eine hohe Systemleistung, Flexibilität und Skalierbarkeit bietet.Es vereint einen Dual-Core ARM Cortex-A9 Prozessor und traditionellen FPGA-Logikkomponenten.Während des Praktikums habe ich ein Entwicklungsboard verwendet, das auf einem Zynq-7000 Chip basiert. Der FPGA-Teil des Chips basiert auf der Xilinx 28nm 7 Serie FPGA, daher wird „7000 “ dem Produktnamen dieser Serie hinzugefügt, was mit der 7-Serie übereinstimmt.
Zynq besteht aus zwei Hauptkomponenten: der programmierbaren Logik (PL) und dem Verarbeitungssystem (PS). Der Bootvorgang des Zynq beginnt immer mit dem PS, gefolgt von der Konfiguration des PL. Das PS kann als eingebetteter Prozessor betrachtet werden, der Betriebssysteme wie Linux ausführen kann, während das PL, ein FPGA, als Peripherie des eingebetteten Systems dient.
![[Pasted image 20230119015205.png]]

## Designprozess
Der vereinfachte Hardware-Entwurfsprozess umfasst die folgenden Schritte:

1. Erstellen einer neuen Projektdatei in Vivado.
2. Hinzufügen eines neuen Blockdesigns zum Projekt.
3. Hinzufügen des ZYNQ7 Processing System IP-Cores in das Diagramm und Konfigurieren (auch möglich durch Laden einer Konfigurationsdatei, die vom Hersteller des Entwicklungsboards zur Verfügung gestellt wird).
4. Weitere benötigte IP Cores hinzufügen und konfigurieren.
5. Konfigurieren und Markieren der I/O-Schnittstellen für die externe Verbindung.
6. „Run Connection Automation“ klicken, wodurch Vivado automatisch die Verbindungen zwischen PS und IP Cores herstellt und die benötigten Interconnection IPs hinzufügt.
7. „Validate Design“ klicken, um das Design und die Verbindungen zu überprüfen.
8. „Create HDL Wrapper“ klicken, um entsprechende HDL Code Wrapper für das Blockdesign zu erzeugen.
7. Schreiben der Pins-Zuweisungen der I/O-Schnittstellen des PL-Teils in die Constraints-Datei.
9. Durchführung der Synthese, Implementierung und Generierung des Bitstreams wie bei normalen FPGA-Designs.
10. Erstellen und Exportieren einer Datei, die das Hardware-Design enthält, d.h. die Konfiguration des PS-Teils und den Bitstream des PL-Teils, die in eine Plattform wie Vitis importiert werden kann, um das Embedded-Software-Design weiter durchzuführen.
## Versuch
Obwohl ich in den ersten Wochen noch kein Zynq-Entwicklungsboard hatte, konnte ich zuerst am Hardware- und Software-Design arbeiten und dann mein Design debuggen und korrigieren, sobald ich das Entwicklungsboard bekommen hatte.
### Versuch1 LED-Steuerung via AXI-GPIO
AXI-GPIO ist ein offizielles Xilinx IP Core. Er bietet eine General Purpose Input/Output Schnittstelle zu einem AXI4-Lite Schnittstelle und kann als ein- oder zweikanaliges Gerät konfiguriert werden. Die Breite jedes Kanals ist unabhängig konfigurierbar.
Die Ports werden dynamisch als Ein- oder Ausgang konfiguriert, indem der Tri-State aktiviert oder deaktiviert wird. Die Kanäle können so konfiguriert werden, dass sie einen Interrupt erzeugen, wenn ein Datenübergang an einem ihrer Eingänge auftritt. Kurz gesagt, mit diesem IP-Core ist der PS-Teil in der Lage, den Zustand der IO-Schnittstellen, die mit dem PL-Teil verbunden sind, zu überwachen und zu kontrollieren.
### Systemblockdiagramm
TBD
Wie im Blockschaltbild des Systems dargestellt, gibt der PS die Steuersignale für die LED aus und leitet sie über das AXI-Interconnect-Interconnect-Modul an das AXI-GPIO-Modul weiter. Das AXI-GPIO-Modul empfängt die Steuersignale über das AXI4-Lite-Protokoll, generiert die entsprechenden Signale und gibt sie an die LED-Pins des FPGAs aus, um die LED anzusteuern.
#### Konfigurieren
In meinem Design wird nur eine LED verwendet. Deshalb habe ich die GPIO Width auf 1 konfiguriert. Es gibt auch die Möglichkeit, die Richtung aller GPIOs als Input oder Output Interface im Hardware Design festzulegen. In diesem Fall werde ich die Richtung der GPIOs nicht vorab im Hardwaredesign festlegen, da ich versuchen möchte, dies dynamisch per Software zu konfigurieren.
Obwohl ich zu diesem Zeitpunkt keinen Zugang zu einem Entwicklungsboard hatte, entnahm ich dem Datenblatt des ZedBoard-Entwicklungsboards die Pin-Nummern für den Anschluss der LEDs und füllte die Constraints-Datei aus.
Das Design ist sehr einfach, da ich nur zwei IPs, PS und AXI-GPIO, manuell hinzufügen musste, aber es beinhaltet die Kommunikation zwischen PS und PL und erfordert auch ein einfaches Softwaredesign, um die GPIO-Schnittstelle dynamisch zu konfigurieren und Steuersignale zu senden. Es ist ein geeignetes Einstiegsprojekt in das SoC Co-Design von Hardware und Software.
### Softwareentwurf
Der Softwareentwurf erfolgt in Vitis, der Softwareentwicklungsumgebung von Xilinx. Nach dem Import der von Vivado generierten Hardware-Design-Dateien wird in Vitis eine neue Hardware-Plattform erstellt. Auf einer Hardwareplattform können mehrere Softwareapplikationsprojekte erstellt werden. Unter dem Verzeichnis der Hardware-Plattform befindet sich eine Liste von Board Support Packages (BSP), die die Dokumentationen und Beispiele von Treibern für die im Hardware-Design verwendete offizielle IP enthalten. Diese Materialien sind für Anfänger sehr hilfreich. Das Beispiel xgpio_example in der Dokumentation ist ein Beispiel für die Verwendung von GPIO zur Ansteuerung einer LED und war eine wertvolle Referenz für meine Versuche.
Die Hauptaufgabe der Software ist es, den GPIO zu initialisieren, ihn mit der Funktion XGpio_SetDataDirection als Ausgangsschnittstelle zu konfigurieren und dann mit der Funktion XGpio_DiscreteWrite einen Wert von 1 oder 0 in den GPIO zu schreiben, um die LED zum Leuchten oder Erlöschen zu bringen. 
## Versuch2
Nachdem ich das erste Experiment abgeschlossen hatte, konzentrierte ich mich darauf, mich weiter mit der Embedded-Programmierung vertraut zu machen. Mein zweites Versuch war die Implementierung eines Zählers, der über den AXI-Bus beschrieben werden kann. Im Gegensatz zum ersten Experiment, bei dem nur offizielle IP-Cores verwendet werden mussten, musste ich bei diesem Versuch einen Zähler mit Registern, die über eine AXI-Lite-Schnittstelle konfiguriert werden können, selbst entwerfen und in das Systemdiagramm einfügen.

Die Implementierung eines Zählers in VHDL ist relativ einfach, aber die größte Herausforderung war das Hinzufügen der AXI-Lite-Schnittstelle zum Custom Modul. Nach dem Tutorial habe ich den New IP Wizard von Vivado verwendet, um ein neues AXI4-Gerät zu erstellen. Während des Erstellungsprozesses kann der Benutzer Parameter wie den Schnittstellentyp und die Anzahl der Register festlegen. Anschließend fügte ich die Codedateien des bereits fertiggestellten Zählers zum Projekt hinzu und modifizierte den vom Wizard generierten Code manuell, um die Ports des Zählermoduls mit den Registern zu verbinden. Schließlich habe ich das Modul als IP verpackt.

## Schluss
Während des 16-wöchigen Praktikums habe ich eine Bildverarbeitungsanwendung auf der Basis von Zynq implementiert. Die Anwendung ermöglichte den Austausch von Informationen zwischen der SD-Karte und dem Prozessor, dem Prozessor und den FPGAs sowie den FPGAs und dem Display. Darüber hinaus führte sie Bildfaltungsoperationen parallel aus und verbesserte so die Leistung des Algorithmus zur Sobel-Kantenerkennung. Während dieser Zeit habe ich den Programmable Logic (PL) Teil des Zynq entworfen und VHDL Code geschrieben, wobei ich das theoretische Wissen aus der Vorlesung FPGA-Entwurfstechnik und die praktische Erfahrung aus den Laboren FPGA-Entwurfstechnik und Mikroelektronik - Chipdesign verwendet habe. Mit Hilfe der offiziellen Beispiele und Tutorials von Xilinx und Avnet habe ich mir die Grundkenntnisse in Embedded C selbst angeeignet und den Softwareteil mit Hilfe des von Xilinx bereitgestellten Treibercodes implementiert.

Neben der erfolgreichen Umsetzung des Projektes konnte ich auch einen Einblick in die Arbeitsabläufe und die Struktur eines Unternehmens gewinnen. Außerdem habe ich gelernt, wie wichtig es ist, sich ständig weiterzubilden und sich den Veränderungen in der Elektrotechnikbranche anzupassen.

Die Mitarbeiter von ITK waren sehr freundlich und immer bereit, bei Problemen zu helfen. Sie kümmerten sich auch um meine Anpassung an die Arbeitsumgebung und boten mir Hilfe beim Erlernen der Sprache, bei der Kommunikation mit anderen und beim Erwerb von Fachkenntnissen an. Ich habe wertvolle Erfahrungen gesammelt. Ich möchte allen Beteiligten meinen herzlichsten Dank aussprechen.

Insgesamt war dieses Praktikum für mich eine sehr lehr- und erfahrungsreiche Zeit. Ich bin dankbar für die Möglichkeit, bei ITK zu arbeiten und bin mir sicher, dass ich die erworbenen Fähigkeiten und Kenntnisse für meine Abschlussarbeit und meine zukünftige Karriere nutzen werde.
## Sobel
Die Sobel-Kantenerkennung ist ein klassischer Algorithmus in der Bild- und Videoverarbeitung, der dazu dient, Kanten von Objekten zu extrahieren. Eine gängige Methode zur Kantenerkennung besteht darin, die erste Ableitung eines Bildes zu berechnen, um Kanteninformationen zu extrahieren. Durch die Berechnung der x- und y-Ableitungen eines bestimmten Pixels im Vergleich zu den Pixeln in dessen Umgebung können die Grenzen zwischen zwei verschiedenen Elementen in einem Bild extrahiert werden. Da die Berechnung der Ableitungen jedoch sehr rechenintensiv ist, da sie Quadrierungs- und Quadratwurzeloperationen beinhaltet, werden Masken mit festen Koeffizienten, also der Sobel-Operator, als geeignete Annäherung für die Berechnung der Ableitungen an einem bestimmten Punkt verwendet.

Beim Sobel-Filter werden in der Regel zwei 3 x 3-Kerne verwendet. Einer für die Berechnung der horizontalen Variation und einer für die Berechnung der vertikalen Variation. Diese beiden Kerne werden mit dem Originalbild gefaltet, um eine Approximation der Ableitung zu berechnen.

### RGB to grayscale

In diesem Projekt wird die folgende Formel verwendet, um die Grauskala eines Pixels zu berechnen:
Graustufe= (R << 2) + (R << 5) + (G << 1) + (G << 4) + (B << 4) + (B << 5)
Dies ist eine annähernde Form der folgenden Gleichung:
Graustufen = ( (0,3 * R) + (0,59 * G) + (0,11 * B) )

### BMP File
Die Anzahl der Bytes in einer Reihe von BMP-Bildern wird nach der folgenden Formel berechnet:
![[Pasted image 20220726102502.png]]
Nach allen Datenbytes wird der Rest der Position mit 0 aufgefüllt, um sicherzustellen, dass eine Reihe von BMP-Bildern ausgerichtet im Computer gespeichert werden kann. 
Der Header einer BMP-Datei enthält Metadaten über das Bild. Durch das Auslesen bestimmter Bytes aus dem Header ist es möglich, die Länge und Breite eines BMP-Bildes zu bestimmen.
![[Pasted image 20220929214255.png]]

## System Structure

Die Kommunikation zwischen Zynq PS und PL basiert auf dem AXI4-Protokoll. Wie in der Abbildung unten dargestellt, sind die konfigurierbaren Register des Sobel-IP über den AXI-Lite-Bus mit dem General-Purpose-Anschluss des PS verbunden. Die Bilddaten werden über den AXI4-Bus durch den High-Performance-Port an die AXI-DMA-IP gesendet. Diese IP überträgt die Daten direkt aus dem Speicher und gibt sie über das AXI4-Stream-Protokoll an andere Peripheriegeräte weiter.
![[Pasted image 20220927211645.png]]
Bei diesem System wird das Originalbild vom Prozessor von der SD-Karte gelesen und vorverarbeitet (Zero-Padding und Neuordnung der Daten). Die vorverarbeiteten Daten werden dann im DDR gespeichert und über das AXI-DMA-IP an das Sobel-IP übertragen. Die verarbeiteten Binärdaten werden über AXI-DMA wieder in den DDR zurückgeschrieben. Nach dem Senden einer bestimmten Datenmenge benachrichtigt der AXI-DMA den PS mit einem Interrupt-Signal.

Das Originalbild und das verarbeitete Bild werden dann von AXI VDMA IP aus dem DDR verschoben und im PL gepuffert. Anschließend werden die Daten zur Verarbeitung an den Xilinx VPSS IP übertragen und mit den Timingsignalen im AXIS to video out IP synchronisiert. Schließlich wird das 16-bit YCbCr Videosignal an den ADV7511 HDMI Transmitter auf dem Zedboard gesendet und auf einem Monitor angezeigt.

![[Pasted image 20220927211533.png]]

## Hardware Implementation

Zunächst empfängt das RGB to Grayscale Modul die 32-Bit-RGB-Daten von der AXI4-Stream-Schnittstelle und wandelt sie durch Verschieben und Addieren näherungsweise in 8-Bit-Graustufendaten um. Zusätzlich verfügt das Modul über zwei Steuersignaleingänge. Die aktuellen 32-Bit-RGB-Daten werden nur dann als gültig betrachtet, wenn sowohl data_ready vom Output_buffer-Modul als auch data_valid von AXI-DMA IP High sind.

Die vom RGB-zu-Graustufen-Modul ausgegebenen Daten werden sequentiell in 4 Zeilenpuffer geschrieben. Alle Zeilenpuffer sind mit demselben Dateneingangsport verbunden, und jeder Zeilenpuffer verfügt über ein eigenes Wertesignal, das anzeigt, ob die aktuelle Eingabe gültig ist oder nicht. Jeder Zeilenspeicher kann bis zu 1024 8-Bit-Daten speichern, was die maximale Breite des zu verarbeitenden Bildes begrenzt. Jeder Zeilenpuffer kann gleichzeitig gelesen und beschrieben werden. Die Steuerlogik stellt sicher, dass nur ein Schreibvorgang und nur drei Lesevorgänge gültig sind. Außerdem ordnet sie die Ausgabedaten aus den Zeilenpuffern in einer bestimmten Reihenfolge an, so dass jede gültige Ausgabe ein aus dem Graustufenbild segmentiertes 3x3-Fenster ist. Vor jedem Lesevorgang prüft der FSM, ob genügend Daten in den Zeilenpuffern vorhanden sind. Wenn nicht genügend Daten vorhanden sind, bleibt der FSM im Idle-Zustand und informiert den PS-Prozessor mittels eines PL-PS-Interrupt-Signals.

Das IP enthält auch ein Register, das über die AXI4-Lite-Schnittstelle konfiguriert werden kann. Vor der Bildverarbeitung muss es vom Anwender auf die Breite des zu verarbeitenden Bildes + 2 (d.h. die Breite des Bildes mit Zero-Padding) konfiguriert werden.

Im Faltungsmodul wird eine fünfstufige Pipeline verwendet, um den Kantenerkennungswert zu berechnen und festzustellen, ob der Wert größer als der Schwellenwert ist. Ist der Wert größer als der Schwellenwert, werden 8-Bit-Daten 0XFF ausgegeben, andernfalls werden 8-Bit-Daten 0X00 ausgegeben, d. h. die Kante ist weiß und der Rest ist schwarz.

Der Xilinx FIFO IP-Core wird als Ausgangspuffer verwendet und kann bis zu 32 8-Bit-Daten aufnehmen. Das invertierende programmierbare Full-Signal dieses IP-Cores, das mit einem Schwellenwert von 16 konfiguriert ist, ist mit dem axis_ready-Ausgangsport des Sobel-IP verbunden. Dies bedeutet, dass der Sobel-IP den Empfang von Daten vom vorgeschalteten AXI-DMA-IP stoppt, wenn 16 Daten im Puffer gespeichert sind und nicht durch eine gültige Übertragung an das nächste Modul ausgegeben werden, um eine mögliche Datenverfälschung zu verhindern.

## Vivado und Vitis
Softwareentwicklungsplatform