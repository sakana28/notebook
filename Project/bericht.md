#文档草稿

## ITK Engineering
Die ITK Engineering GmbH (zunächst als Ingenieurbüro für technische Kybernetik) wurde 1994 gegründet und ist ein international tätiger Entwicklungsdienstleister mit Kunden aus den Branchen Automotive, Luft- und Raumfahrt sowie Medizintechnik. Seit 2017 ist sie ein Tochterunternehmen der Robert Bosch GmbH. 
ITK bietet Dienstleistungen in den Bereichen Produktentwicklung, Industrielösungen, Consulting & Coaching und technische Beratung an. Die Produktentwicklung umfasst ein breites Spektrum von physischen eingebetteten Geräten über Anwendungen auf Laptops oder Tablets bis hin zu Lösungen in der Cloud. Egal, ob es sich um die Vorentwicklung, die Prototypenentwicklung oder die Serienfertigung von Produkten handelt, ITK kann technische Unterstützung bieten.
## Vorbereitung
An meinem ersten Arbeitstag im ITK Braunschweig verbrachte ich die meiste Zeit damit, gemeinsam mit meinem Betreuer meinen Arbeitslaptop einzurichten und mich mit den verwendeten Programmen wie Outlook als E-Mail- und Kalenderprogramm und Microsoft Teams als internes Kommunikationstool vertraut zu machen. Durch die Anleitung meines Betreuers lernte ich viele wichtige Regeln für das Informationsmanagement im Unternehmensalltag kennen. Zum Beispiel müssen die Mitarbeiter regelmäßig ihre Passwörter auf den Arbeitscomputern ändern und eine spezielle Software zur Passwortverwaltung nutzen. Außerdem müssen die Mitarbeiter bei der Installation neuer Software auf den Arbeitsrechnern prüfen, ob diese Software auf der Whitelist steht usw.

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
4. Weitere benötigte IP-Cores hinzufügen und konfigurieren.
5. Konfigurieren und Markieren der I/O-Schnittstellen für die externe Verbindung.
6. „Run Connection Automation“ klicken, wodurch Vivado automatisch die Verbindungen zwischen PS und IP-Cores herstellt und die benötigten Interconnection IPs hinzufügt.
7. „Validate Design“ klicken, um das Design und die Verbindungen zu überprüfen.
8. „Create HDL Wrapper“ klicken, um entsprechende HDL Code Wrapper für das Blockdesign zu erzeugen.
7. Schreiben der Pins-Zuweisungen der I/O-Schnittstellen des PL-Teils in die Constraints-Datei.
9. Durchführung der Synthese, Implementierung und Generierung des Bitstreams wie bei normalen FPGA-Designs.
10. Erstellen und Exportieren einer Datei, die das Hardware-Design enthält, d.h. die Konfiguration des PS-Teils und den Bitstream des PL-Teils, die in eine Plattform wie Vitis importiert werden kann, um das Embedded-Software-Design weiter durchzuführen.
## Versuch
Obwohl ich in den ersten Wochen noch kein Zynq-Entwicklungsboard hatte, konnte ich zuerst am Hardware- und Software-Design arbeiten und dann mein Design debuggen und korrigieren, sobald ich das Entwicklungsboard bekommen hatte.
### Versuch1 LED-Steuerung via AXI-GPIO
AXI-GPIO ist ein offizielles Xilinx IP-Core. Er bietet eine General Purpose Input/Output Schnittstelle zu einem AXI4-Lite Schnittstelle und kann als ein- oder zweikanaliges Gerät konfiguriert werden. Die Breite jedes Kanals ist unabhängig konfigurierbar.
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

### Systemblockdiagramm
TBD
### Softwareentwurf
Weil dieses System mit benutzerdefinierten IPs in Beziehung steht, ist der erste Schritt bei der Softwareentwicklung, die Datei "xparameters.h" im BSP zu finden. Diese Datei enthält die Basisregisteradressen für die Custom IPs. Es gibt auch eine von Vitis generierte Custom-IP-Header-Datei (.h) im Projektverzeichnis der Applikation, die die Makrodefinitionen zum Lesen und Schreiben der Custom-IP-Register umfasst. Mit dem Schreibmakro kann ich eine beliebige Nummer in das Register des Custom Zählers schreiben und den Zähler ab dieser Nummer zählen lassen.


## Theoretischer Hintergrund
### Sobel
In diesem Abschnitt möchte ich einen kurzen Überblick über den Sobel-Algorithmus geben, der in meinem Projekt verwendet wurde. 
Die Sobel-Kantenerkennung ist ein klassischer Algorithmus in der Bild- und Videoverarbeitung, der dazu dient, Kanten von Objekten zu extrahieren. Eine gängige Methode zur Kantenerkennung besteht darin, die erste Ableitung eines Bildes zu berechnen, um Kanteninformationen zu extrahieren. Durch die Berechnung der x- und y-Ableitungen eines bestimmten Pixels im Vergleich zu den Pixeln in dessen Umgebung können die Grenzen zwischen zwei verschiedenen Elementen in einem Bild extrahiert werden. Da die Berechnung der Ableitungen jedoch sehr rechenintensiv ist, da sie Quadrierungs- und Quadratwurzeloperationen beinhaltet, werden Masken mit festen Koeffizienten, also der Sobel-Operator, als geeignete Annäherung für die Berechnung der Ableitungen an einem bestimmten Punkt verwendet.

Beim Sobel-Filter werden in der Regel zwei 3 x 3-Kerne verwendet. Einer für die Berechnung der horizontalen Variation und einer für die Berechnung der vertikalen Variation. Diese beiden Kerne werden mit dem Originalbild gefaltet, um eine Approximation der Ableitung zu berechnen.

### RGB to grayscale

In diesem Projekt wird die folgende Formel verwendet, um die Grauskala eines Pixels zu berechnen:
Graustufe= (R << 2) + (R << 5) + (G << 1) + (G << 4) + (B << 4) + (B << 5)
Dies ist eine annähernde Form der folgenden Gleichung:
Graustufen = ( (0,3 * R) + (0,59 * G) + (0,11 * B) )

### BMP File
Um sicherzustellen, dass die Pixeldaten zweier Zeilen eines Bitmap-Bildes nicht dieselbe Speicherzelle belegen, muss bei BMP-Bildern die Anzahl der Bytes in einer Zeile mit Pixeldaten ein Vielfaches von 4 sein. Wenn die Anzahl der Bytes nicht durch 4 teilbar ist, werden die nachfolgenden Bytes mit 0 aufgefüllt. Die Anzahl der Bytes in einer Reihe von BMP-Bildern wird nach der folgenden Formel berechnet:
![[Pasted image 20220726102502.png]]
Auf diese Weise wird eine Reihe von Pixeldaten ausgerichtet im Computer gespeichert.

Außerdem werden die ersten 54 Bytes einer BMP-Datei als Header bezeichnet. Der Header enthält Metadaten über das Bild. Durch das Auslesen bestimmter Bytes aus dem Header ist es möglich, wichtige Informationen wie Länge und Breite eines BMP-Bildes zu bestimmen.
![[Pasted image 20220929214255.png]]




## Simulation
Bei der Implementierung einer so komplexen Funktion muss jedes Submodul nach der Fertigstellung getestet werden. Dazu habe ich für jedes Submodul eine einfache Testbench geschrieben und die Ausgangswellenform des Moduls mit den erwarteten Werten verglichen. Ich habe auch darauf geachtet, dass das Modul mit Grenzwerten getestet wurde, um die Robustheit des Designs zu gewährleisten.

Außerdem habe ich dafür gesorgt, dass meine Module parametrisiert sind, um die Menge der benötigten Eingangsdaten zu reduzieren und so den Testaufwand zu minimieren. Dadurch kann ich die Simulation schneller durchführen und die Module leichter an unterschiedliche Anforderungen anpassen.

Um die Funktionalität des gesamten IP zu garantieren, habe ich neben der Überprüfung der Wellenformdiagramme auch die Bildverarbeitungsfähigkeit getestet. Hierzu schrieb ich zwei C-Programme, eines zur Konvertierung eines BMP-Bildes in eine Textdatei mit binären Informationen und eines zur Konvertierung einer Textdatei in eine BMP-Datei. Schließlich schrieb ich eine Testbench, die in der Lage war, die binären Informationen aus der Textdatei zu lesen und in einen synchronisierten Stimulus umzuwandeln. Am Ende erhielt ich das gewünschte bearbeitete Bild, was bewies, dass der Teil des Hardware-Designs die Erwartungen erfüllte. Diese Erfahrung hat mir geholfen, ein tieferes Verständnis für Bildverarbeitung und automatisierte Testbenches zu entwickeln.

## Schritt 1: Einstieg in Zedboard
Nachdem ich das Entwicklungsboard erhalten hatte, bestand mein erstes Ziel darin, die Bitströme meiner ersten Versuche auf das Board zu übertragen und zu testen. Dazu benutzte ich einen JTAG-USB-Programmierer. Leider schlug der Download immer wieder fehl. Nach einer gründlichen Fehleranalyse fand ich heraus, dass das Problem durch Inkonsistenzen zwischen dem verwendeten Board und der verwendeten Konfigurationsdatei verursacht wurde. Es gibt im Laufe der Zeit zwei verschiedene Versionen des Zedboards, die unterschiedliche DDR-Speichermodule verwenden und daher unterschiedliche Konfigurationsdateien benötigen. Ich konnte den Download erfolgreich durchführen, nachdem ich die richtige Konfigurationsdatei verwendet hatte.

Ein weiteres Problem, das ich bei diesem Projekt hatte, war die Verwendung der UART-Schnittstelle. Ich hatte Schwierigkeiten, die UART-Schnittstelle auf meinem Ubuntu-System zu finden und zu konfigurieren, um sie in meinem Programm zu verwenden. Nach einer Suche in der Web-Community wusste ich, dass ich den richtigen Namen des USB-Gerätes im Verzeichnis /dev finden und es dann im Minicom-Terminalprogramm als serielle Schnittstelle konfigurieren musste. Danach konnte auch ein Terminalprogramm außerhalb von Minicom, wie z.B. das in Vitis eingebaute serielle Terminal, die gewünschte serielle Schnittstelle finden.

Aus den aufgetretenen Problemen habe ich gelernt, dass es eine Vielzahl von komplexen Fehlern gibt, die bei der Verwendung von eingebetteten Systemen auftreten können und die mit verschiedenen Faktoren wie der Entwicklungsumgebung und den Hardware-Geräten zusammenhängen. Um die verschiedenen Herausforderungen zu bewältigen und die Probleme zu lösen, die bei der Arbeit mit diesen Systemen auftreten können, ist es daher notwendig, meine Fähigkeiten im Umgang mit Linux-Systemen und -Tools zu verbessern und die Community und die offizielle Dokumentation gut zu nutzen.
## Schritt 2 : SD-Karte Lesen und Schreiben
Um die Bildverarbeitung auf dem Zynq zu implementieren, muss zunächst ein BMP-Bild von der SD-Karte gelesen und wieder auf die SD-Karte geschrieben werden. Dies erfordert ein Verständnis der Struktur des BMP-Dateiformats und des Dateisystems der SD-Karte.

Während des Experiments hatte ich das Problem, dass das Ausgabebild nicht vollständig angezeigt wurde. Die Anzahl der Bytes in einer Bildzeile in der BMP-Datei muss ein Vielfaches von 4 Bytes sein, um sicherzustellen, dass jede Datenzeile korrekt gespeichert wird. Ich änderte meinen Code, um diese Anforderung zu erfüllen und das Problem zu lösen. Ich stellte auch sicher, dass die Länge und Breite des Bildes genau aus dem Header gelesen werden konnte, indem ich die Datei und die BMP-Spezifikation sorgfältig studierte und die Informationen über die serielle UART-Schnittstelle an den Computer ausgab, um das Programm zu debuggen.

Neben der Fehlersuche lernte ich, wie man eine SD-Karte richtig initialisiert und einsteckt, wie man Dateien darauf liest und schreibt und wie man mit Bitmap-Dateien umgeht und sie in ein Format konvertiert, das von eingebetteten Systemen verarbeitet werden kann.

Während meines Praktikums erhielt ich auch Feedback von meinem Mentor und meinen Kollegen. Sie halfen mir, meinen Code zu verbessern, und wiesen mich darauf hin, was ich verbessern könnte, um die Qualität meines Codes zu erhöhen. Sie sagten mir auch, welche Codierungsstandards ich befolgen sollte, um sicherzustellen, dass mein Code gut strukturiert und leicht verständlich ist.
## Schritt 3: Sobel-C Implementierung
Nachdem ich das Lesen und Schreiben der Bilder von der SD-Karte erfolgreich implementiert habe, habe ich mit den Aufgaben im Zusammenhang mit der Sobel-Filtern begonnen. Zuerst verarbeitete ich die von der SD-Karte gelesenen Bildinformationen, indem ich sie vollständig durch die eingebettete C auf dem ARM-Prozessor laufen ließ und das verarbeitete Ergebnis zurück in dieselbe SD-Karte schrieb.

Ein wichtiger Aspekt bei der Implementierung des Sobel-Filter-Algorithmus ist die Verwendung einer Faltungsmatrix zur Bestimmung der Gradientenrichtung und -intensität. Der Algorithmus verarbeitet das Bild Pixel für Pixel und berechnet die Richtung und Intensität des Gradienten für jedes Pixel aus den Werten der benachbarten Pixel. Es ist wichtig anzumerken, dass es mehrere Optimierungsmethoden für den Sobel-Algorithmus gibt, aber ich habe hier keine Optimierungen an der ursprünglichen Implementierung vorgenommen, da dies nicht der Schwerpunkt meines Projekts ist. In meinem Fall dauerte die Sobel-Verarbeitung 201225057 ns.

Obwohl dieser Teil der Arbeit nicht in das Endergebnis einfließt, sondern nur eine Vergleichszahl liefert, hat er mir geholfen, mein Verständnis von Bildverarbeitungskonzepten und -techniken zu vertiefen und mir gezeigt, wie man sie auf einem eingebetteten System implementiert.

## Schritt 4: AXI-DMA und AXI-FIFO
Um die Übertragung von Bilddaten zwischen PS und PL zu implementieren, habe ich mich mit den IP-Cores AXI-DMA und AXI-FIFO von Xilinx sowie dem AXI4-Stream-Protokoll auseinandergesetzt. Anschließend habe ich eine Bildverarbeitungsapplikation implementiert, die jeweils einen dieser beiden IP-Cores verwendet. Sie realisiert die Funktion, ein Bild von der SD-Karte zu lesen, es in PL zwischenzuspeichern, danach zurück in PS zu übertragen und schließlich wieder in die SD-Karte zu schreiben.
![[Pasted image 20230126084524.png]]
![[Pasted image 20230126084938.png]]
Im Folgenden werden die Unterschiede und Gemeinsamkeiten zwischen dem AXI-DMA IP-Core und dem AXI-Stream FIFO IP-Core erklärt. Beide IP-Cores können über die AXI4-Schnittstelle adressierte Daten empfangen, eine bestimmte Datenmenge im IP-Core zwischenspeichern, die Daten dann in unadressierte Daten umwandeln und diese über das AXI4-Streamsignal aus dem IP ausgeben. Der Unterschied zwischen AXI-DMA IP und FIFO besteht jedoch darin, dass bei Verwendung von AXI-DMA IP keine manuelle Datenübertragung vom Prozessor zum IP-Core erforderlich ist. Stattdessen muss der Anwender lediglich ein DMA-Steuersignal in das IP schreiben und damit den DMA-Controller im IP-Core konfigurieren. Der DMA-Controller kann dann Daten direkt aus dem DDR-Speicher des PS über die High-Performance Ports (HP) zwischen PS und PL abrufen.
Mein Hauptziel war es, die Unterschiede zwischen den beiden IP-Cores zu verstehen und zu analysieren, welcher für mein Projekt besser geeignet ist. Durch die Verwendung des AXI-DMA-IP-Cores war es möglich, die Daten direkt aus dem DDR-Speicher des PS auf die PL zu übertragen, ohne den Prozessor zu benutzen. Der Prozessor kann während des Datentransfers andere Operationen ausführen, so dass er die Peripherie nicht ständig abfragen muss.

## Schritt 5: HDMI
Nachdem ich die Übertragung und Zwischenspeicherung der Bilddaten auf der PS- und PL-Seite erfolgreich implementiert habe, bestand meine nächste Aufgabe darin, den HDMI-Ausgangspfad zu konfigurieren, um die Bilder auf einem externen Display anzuzeigen. Der HDMI-Ausgang wurde mit einem externen Codec, dem ADV7511 von ADI, auf dem Zedboard Entwicklungsboard implementiert. Der Codec verfügt über eine I2C-Schnittstelle, so dass der Benutzer den Codec konfigurieren kann. Daher muss ich einen I2C Interface IP-Core auf der PL-Seite erstellen und ihn mit der PS-Seite verbinden.

Der HDMI-Ausgangspfad besteht aus folgenden IP-Kernen: dem VDMA-Kern, dem Video Timing Controller IP-Core (VTC), dem AXI-VDMA IP-Core und dem Video Output IP-Core (Vid_Out). Der AXI-VDMA-IP-Core hat ähnliche Funktionen wie der AXI-DMA-Core, bietet aber zusätzlich eine Schnittstelle zu videorelevanten Synchronisationssignalen und eine Bildpufferfunktion. Der VTC-IP-Core kann als Timing-Generator betrachtet werden, der die für den Monitorausgang notwendigen Zeitimpulse erzeugt. Der Vid_Out-Core wandelt den als AXI4-Stream-Protokoll übertragenen Datenstrom in Videodaten um und synchronisiert diese Daten mit den vom VTC bereitgestellten Timing-Signalen, so dass sie für externe Videoempfänger (z.B. Monitore) verfügbar sind.

Meine Aufgabe war es nun, die verschiedenen IP-Cores für den HDMI-Ausgangspfad zu implementieren und zu konfigurieren, um eine erfolgreiche Übertragung der Videodaten zu garantieren. Dabei bin ich auf einige Probleme gestoßen, wie z.B. die fehlende Ausgabe des Videosignals durch den Vid_Out IP. Um diese Probleme zu lösen, war es notwendig, die technische Dokumentation gründlich zu studieren und ein tiefes Verständnis der Funktionsweise der verschiedenen IP-Cores zu erlangen.

Nachdem ich die Unstimmigkeit in der Datenbreite und den Underflow im internen FIFO von Vid_Out behoben habe, konnte ich die vom Vid_Out IP-Core erzeugte Wellenform erfolgreich über den Integrated Logic Analyzer (ILA) IP-Core auslesen. Dies war jedoch erst der Anfang einer Reihe von Herausforderungen. Die generierten Daten wurden auf dem Bildschirm nicht korrekt als Bild dargestellt. Als nächstes musste ich sicherstellen, dass das Bildsignal auch in hoher Qualität angezeigt wird, das heißt, dass das Bild klar und in der richtigen Farbe ist.

Laut Datenblatt unterstützt der HDMI-Ausgang des Zedboards 16-Bit-Daten im YCbCr4:2:2-Modus. Also musste ich die 24-bit RGB-Bilddaten in 16-Bit YCbCr4:2:2-Bilddaten umwandeln. Dazu verwendete ich das Video Processing Subsystem IP-Core von Xilinx. Nach der Konfiguration und dem Anschluss dieser IP an das System und dem Hinzufügen des Treibercodes zur Software wurden die Bilder angezeigt. Die Farben der Bilder waren jedoch nicht korrekt. Bei der Überprüfung wurde entdeckt, dass die RGB-Daten über PS mit den drei Kanälen in der falschen Reihenfolge an den PL übertragen wurden, was zu Farbabweichungen im Video führte. Nach der Fehlerbehebung wurde das Bild korrekt dargestellt.

Bei diesem Projekt musste der HDMI-Ausgangspfad nicht an ein anderes Display angepasst werden. Die Video-Ausgangsauflösung wurde auf 1080p60 festgelegt. Ein dynamisch konfigurierbarer IP-Core zur Taktgenerierung war auch im Videoausgangspfad erforderlich, wenn eine andere Videoauflösung ausgegeben werden sollte.

## Schritt 6: Sobel Hardware Implementation

Der nächste Schritt war die Kernaufgabe des gesamten Projekts, nämlich die Implementierung einer benutzerdefinierten IP mit Sobel-Kantenerkennung in VHDL-Code auf der Zynq-Plattform. 
Die folgende Abbildung zeigt ein Blockdiagramm des Designs innerhalb des Sobel IP:
![[Pasted image 20220927211533.png]]
Zunächst empfängt das RGB to Grayscale Modul die 32-Bit-RGB-Daten von der AXI4-Stream-Schnittstelle und wandelt sie durch Verschieben und Addieren näherungsweise in 8-Bit-Graustufendaten um. Zusätzlich verfügt das Modul über zwei Steuersignaleingänge. Die aktuellen 32-Bit-RGB-Daten werden nur dann als gültig betrachtet, wenn sowohl data_ready vom Output_buffer-Modul als auch data_valid von AXI-DMA IP High sind.

Die vom RGB-zu-Graustufen-Modul ausgegebenen Daten werden sequentiell in 4 Zeilenpuffer geschrieben. Alle Zeilenpuffer sind mit demselben Dateneingangsport verbunden, und jeder Zeilenpuffer verfügt über ein eigenes Wertesignal, das anzeigt, ob die aktuelle Eingabe gültig ist oder nicht. Jeder Zeilenspeicher kann bis zu 1024 8-Bit-Daten speichern, was die maximale Breite des zu verarbeitenden Bildes begrenzt. Jeder Zeilenpuffer kann gleichzeitig gelesen und beschrieben werden. Die Steuerlogik stellt sicher, dass nur ein Schreibvorgang und nur drei Lesevorgänge gültig sind. Außerdem ordnet sie die Ausgabedaten aus den Zeilenpuffern in einer bestimmten Reihenfolge an, so dass jede gültige Ausgabe ein aus dem Graustufenbild segmentiertes 3x3-Fenster ist. Vor jedem Lesevorgang prüft der FSM, ob genügend Daten in den Zeilenpuffern vorhanden sind. Wenn nicht genügend Daten vorhanden sind, bleibt der FSM im Idle-Zustand und informiert den PS-Prozessor mittels eines PL-PS-Interrupt-Signals.

Das IP enthält auch ein Konfigurationsregister, das über die AXI4-Lite-Schnittstelle konfiguriert werden kann. Bevor das IP verwendet wird, muss es vom Anwender auf die Breite des zu verarbeitenden Bildes plus 2 (für Zero-Padding) konfiguriert werden.

Im Faltungsmodul wird eine fünfstufige Pipeline verwendet, um den Kantenerkennungswert zu berechnen und festzustellen, ob der Wert größer als der Schwellenwert ist. Ist der Wert größer als der Schwellenwert, werden 8-Bit-Daten 0XFF ausgegeben, andernfalls werden 8-Bit-Daten 0X00 ausgegeben, d. h. die Kante ist weiß und der Rest ist schwarz.

Der Xilinx FIFO IP-Core wird als Ausgangspuffer verwendet und kann bis zu 32 8-Bit-Daten aufnehmen. Das invertierende programmierbare Full-Signal dieses IP-Cores, das mit einem Schwellenwert von 16 konfiguriert ist, ist mit dem axis_ready-Ausgangsport des Sobel-IP verbunden. Dies bedeutet, dass der Sobel-IP den Empfang von Daten vom vorgeschalteten AXI-DMA-IP stoppt, wenn 16 Daten im Puffer gespeichert sind und nicht durch eine gültige Übertragung an das nächste Modul ausgegeben werden, um eine mögliche Datenverfälschung zu verhindern.

## System Structure

Nachdem ich das Design, die Verifikation und das Packaging der Sobel-IP abgeschlossen habe, fügte ich sie dem zuvor fertiggestellten Hardwaresystem hinzu. Wie zuvor beschrieben, basiert die Kommunikation zwischen Zynq PS und PL auf dem AXI4-Protokoll. Wie in der Abbildung unten dargestellt, sind die konfigurierbaren Register der Sobel-IP über den AXI-Lite-Bus, der eine geringe Anzahl von Signalen überträgt, mit den General Purpose Ports des PS verbunden. Die Bilddaten werden über den AXI4-Bus an die AXI-DMA-IP über die High-Performance-Ports gesendet. Diese IP überträgt die Daten direkt aus dem Speicher und leitet sie über das AXI4-Stream-Protokoll, das den Datenstrom überträgt, an die anderen Peripheriegeräte weiter.
Die folgende Abbildung zeigt das Systemblockdiagramm des gesamten Hardwarebereichs:
![[Pasted image 20220927211645.png]]
Bei diesem System wird das Rohbild vom Prozessor von der SD-Karte gelesen und vorverarbeitet (Null-Füllung und Neuordnung der Daten). Die vorverarbeiteten Daten werden dann im DDR gespeichert und über die AXI-DMA-IP an die Sobel-IP übertragen, die die verarbeiteten Binärdaten zurück an die AXI-DMA sendet, um die Daten zurück in den DDR zu schreiben. Nachdem alle Daten für ein Bild zurückgeschrieben wurden, informiert die AXI-DMA den PS mit einem Interrupt-Signal, dass der Übertragungsprozess abgeschlossen ist.

Das Originalbild und das verarbeitete Bild werden dann über die AXI VDMA IP aus dem DDR gelesen und im PL zwischengespeichert. Sie werden zur Verarbeitung an die Xilinx VPSS IP übertragen und mit dem Timing-Signal von AXIS an die Videoausgabe-IP synchronisiert. Schließlich wird das 16-Bit-YCbCr-Videosignal an den ADV7511 HDMI Codec auf dem Zedboard gesendet und auf dem Monitor angezeigt.

## Schluss
Während des 16-wöchigen Praktikums habe ich eine Bildverarbeitungsanwendung auf der Basis von Zynq implementiert. Die Anwendung ermöglichte den Austausch von Informationen zwischen der SD-Karte und dem Prozessor, dem Prozessor und den FPGAs sowie den FPGAs und dem Display. Darüber hinaus führte sie Bildfaltungsoperationen parallel aus und verbesserte so die Leistung des Algorithmus zur Sobel-Kantenerkennung. Während dieser Zeit habe ich den Programmable Logic (PL) Teil des Zynq entworfen und VHDL Code geschrieben, wobei ich das theoretische Wissen aus der Vorlesung FPGA-Entwurfstechnik und die praktische Erfahrung aus den Laboren FPGA-Entwurfstechnik und Mikroelektronik - Chipdesign verwendet habe. Mit Hilfe der offiziellen Beispiele und Tutorials von Xilinx und Avnet habe ich mir die Grundkenntnisse in Embedded C selbst angeeignet und den Softwareteil mit Hilfe des von Xilinx bereitgestellten Treibercodes implementiert.

Neben der erfolgreichen Umsetzung des Projektes konnte ich auch einen Einblick in die Arbeitsabläufe und die Struktur eines Unternehmens gewinnen. Außerdem habe ich gelernt, wie wichtig es ist, sich ständig weiterzubilden und sich den Veränderungen in der Elektrotechnikbranche anzupassen.

Die Mitarbeiter von ITK waren sehr freundlich und immer bereit, bei Problemen zu helfen. Sie kümmerten sich auch um meine Anpassung an die Arbeitsumgebung und boten mir Hilfe beim Erlernen der Sprache, bei der Kommunikation mit anderen und beim Erwerb von Fachkenntnissen an. Ich habe wertvolle Erfahrungen gesammelt. Ich möchte allen Beteiligten meinen herzlichsten Dank aussprechen.

Insgesamt war dieses Praktikum für mich eine sehr lehr- und erfahrungsreiche Zeit. Ich bin dankbar für die Möglichkeit, bei ITK zu arbeiten und bin mir sicher, dass ich die erworbenen Fähigkeiten und Kenntnisse für meine Abschlussarbeit und meine zukünftige Karriere nutzen werde.