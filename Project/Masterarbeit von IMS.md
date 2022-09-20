#material

# Laufenden Arbeiten
## Entwurf einer FPGA-Plattform zur automatisierten Messung und Auswertung von Beschleunigungsdaten

Das Fachgebiet Architekturen und Systeme beschäftigt sich unter anderem  mit FPGAs in unterschiedlichen Einsatzgebieten. In dieser Arbeit soll  eine FPGA-Plattform zur automatisierten Messung und Auswertung von  Beschleunigungsdaten in einem Prüfstand entwickelt werden. Dazu gehört  die Anbindung der notwendigen Sensoren, die Implementierung der Firmware  und eine Einbettung an die bestehenden Systeme. Anschließend soll die  Funktion des Prüfstandes evaluiert und validiert werden.

# Abgeschlossene Arbeiten
## Portierung, Kopplung und Optimierung einer generischen Vektorprozessorarchitektur auf ein Xilinx UltraScale+ MPSoC mit eingebettetem ARM Prozessor
Jahr: 2018

Im Automobilbereich und im Kontext der Fahrerassistenzsysteme werden Architekturen für komplexe Berechnungen eingesetzt. Diese unterliegen harten Echtzeitanforderungen und müssen mit geringen Energiebudgets arbeiten können. Zur Situationsnalyse des Fahrzeuges sind unter anderem Information über andere Verkehrsteilnehmer erforderlich. Die massive Anzahl an erforderlichen Operationen zur Analyse der Situation stellt hohe Anforderungen an die eingesetzte Rechnerarchitektur. Neben niedriger Latenz spielt hierbei aber auch eine geringe Verlustleistung eine wichtige Rolle. Standardarchitekturen wie general purpose CPUs oder GPUs bieten hier keine optimale Lösung, da sie entweder nicht die erforderlichen Rechenleistungen erbringen oder aber eine zu hohe Leistungsaufnahme haben. Eine speziell für diesen Bereich der massiv-parallelen Fahrerassistenzanwendungen entwickelte Prozessorarchitektur stellt der VPRO Vektorprozessor dar.

Der für FPGAs optimierte VPRO bietet die notwendige Rechenleistung bei minimalen Energieverbrauch und erlaubt nicht nur eine spätere Modifikation der Hardware sondern durch die Programmierbarkeit eine softwareseitige Flexibilität Anwendungen im Nachhinein zu modifizieren bzw. auszutauschen. Um eine möglichst hohe Abstraktion der Hardware für die Entwicklung der Anwendungen zu bieten bietet sich ein partitioniertes Konzept an: Hierbei werden die rechenintensiven Aufgaben basierend auf hochoptimierten Bibliotheken auf den VPRO ausgelagert. Der Aufruf dieser Funktionen von der eigentlichen Anwendung aus geschieht über einen dedizierten Prozessor im FPGA, auf dem mittels gängiger Toolchains komplexe Aufgaben bis hin zu standardisierten Betriebssystemen implementiert werden können.

Im Rahmen dieser Arbeit soll die generische VPRO Vektorprozessorarchitektur auf das Xilinx UltraScale+ MPSoC portiert werden. Dabei soll auf Basis des AXI4 Standard eine Infrastruktur implementiert werden, welche unter anderem einen Speichercontroller sowie Kommunikationsschnittstellen enthält. Die Kopplung des Vektorprozessors mit dem im FPGA verfügbaren ARM Prozessor soll sowohl hardwareseitig über entsprechende Schnittstellen als auch softwareseitig über Treiber und Bibliotheken implementiert werden.

## Implementation and Evaluation of a Vector-Co-Processor Unit for Efficient Processing of Video-Based Advanced Driver Assistance Systems
Jahr: 2018

Der aufkommende Bereich der fortgeschrittenen Fahrerassistenzsysteme (ADAS) impliziert komplexe Berechnungen unter harten Echtzeitbedingungen. Die aktuellen Forschungstrendskonzentrieren sich auf erweiterte Szenenanalyse, wobei die sogenannten Convolutional Neural Networks (CNNs) eine State-of-the-art Bild- und Videoerkennungstechnik darstellen. Um mit der enormen Nachfrage nach Rechenleistung Schritt zu halten, stellen parallele Prozessorarchitekturen eine praktikable Lösung dar. Viele kommerzielle Plattformen basierend auf GPUs oder auf CPUs mit parallelen Datenverarbeitungserweiterungen wie SSE für die x86-Plattform. Speziell für den Einsatz im Automobilbereich sind niedrige Kosten und Energieeffizienz jedoch entscheidende Faktoren. Daher ist die Implementierung einer parallelen ASIP-Architektur (Application-Specific Instruction Set Processor) erforderlich.  
  
Basierend auf früheren Arbeiten soll in dieser Arbeit eine bestehende Instruction-Se-Architektur (ISA) für eine Xilinx Virtex-6 FPGA ml605 Plattform implementiert werden. Die ISA wurde allgemein für das Gebiet der fortgeschrittenen Fahrerassistenzsysteme entworfen und insbesondere für die effiziente Berechnung der Szenenklassifikation unter Verwendung von CNNs ausgelegt. Die Architektur soll für den Rechendurchsatz optimiert werden. Daher muss das Prozessor-Design mit tiefen Pipelines ausgestattet werden. Weiterhin muss eine explizite Instanziierung von dedizierten FPGA-Makros verwendet werden, um so das Timing zu optimieren. Die erreichbare Leistungsfähigkeit der implementierten Architektur soll mit dem IMS UEMU Framework evaluiert und mit einem beispielhaften 2D-Faltungsverarbeitungskern verifiziert werden.

## Konzeptionierung und Implementierung einer hybriden MAC-Layer-Architektur für Paket-basierte Powerline Kommunikation auf einem FPGA
Jahr: 2017

Am Fachgebiet „Architekturen und Systeme“ des Instituts für Mikroelektronische Systeme werden VLSI-Architekturen für Algorithmen der digitalen Signalverarbeitung mit besonderen Anforderungen an Echtzeitfähigkeit und Verlustleistung konzipiert und implementiert. Ein Forschungsschwerpunkt ist dabei die digitale Signalverarbeitung in der Kommunikationstechnik.

Heutige Anwendungen elektronischer Systeme setzen vermehrt auf die drahtlose Kommunikation und den Austausch von immer größer werdenden Datenmengen untereinander. Am Institut für Mikroelektronische Systeme werden unter anderem OFDM-basierte Kommunikationssysteme für diese Anforderungen konzeptioniert und evaluiert. Ein besonders interessantes Verfahren ist hier die
Powerline Kommunikation. Diese ist ein Paket-basiertes Verfahren, welches nach dem Prinzip des Ethernet-Stacks einen MAC- und einen PHY-Layer definiert.

Der MAC-Layer übernimmt hierbei eine steuernde Rolle und leitet die Pakete an die PHY-Layer
weiter, bewertet die frequenzbezogenen Eigenschaften des Übertragungskanals und kontrolliert den Verbindungsstatus zur Gegenstelle. Die Über- und Weitergabe von Paketen erfolgt hierbei über so genannte FIFO-Interfaces, jeweils zur darüber liegenden Schicht und dem PHY-Layer. Außerdem regelt der MAC-Layer den Medienzugriff auf die Powerline, wobei dieser parallel den Status des Mediums abfragen und Daten für das Senden vorbereiten muss.

Die Aufgabe dieser Arbeit ist es eine hybride Architektur, bestehend aus Hardwareeinheiten
und ein oder mehreren Softcore-Prozessoren zu konzeptionieren. Die Implementierung eines MAC- Layer nach dem HomePlug V1.0.1 Standard liegt hierbei bereits als VHDL-Hardware-Beschreibung und C-Referenzimplementierung vor. Zunächst soll eine Evaluation der bestehenden Hardware-Architektur hinsichtlich der Umsetzbarkeit einzelner Komponenten auf einem Softcore untersucht werden. Anschließend werden verschiedene Architekturen von Softcore-Prozessoren verglichen und bezüglich ihrer hardwarespezifischen Parameter bewertet. Die am besten geeigneten Softcore-Prozessor-Architekturen werden schließlich in einem Gesamtkonzept als hybride Architektur mit weiteren Hardware-Komponenten auf einem FPGA realisiert und gegen die Referenzimplementierung verifiziert.

## Konzeptionierung, Implementierung und Verifikation eines MAC-Layers für Paket-basierte Powerline Kommunikation
Jahr: 2016

In dieser Arbeit soll ein MAC-Layer nach dem HomePlug V1.0.1 Standard konzeptioniert und  
implementiert werden. Die Implementierung erfolgt hierbei zunächst in einer C-  
Referenzimplementierung, um eine Funktionale Verifikation durchzuführen. Anschließend soll der  MAC-Layer in einer VHDL-Implementierung umgesetzt werden und die Funktionsweise gegen die C- Implementierung verifiziert werden. Zusätzlich soll untersucht werden, wie sich eine hybride Lösung durch die Verwendung eines Soft-Core-Prozessors auf dem FPGA auf Fläche und Durchsatz verhält.  
Am Schluss der Arbeit soll eine echtzeitfähige, verifizierte VHDL-Implementierung vorliegen, welche  sowohl Daten empfangen und verarbeiten als auch für das Senden vorbereiten kann.

## Implementierung und Evaluation eines parametrisierbaren Faltungsencoders und Viterbi-Decoders in VHDL

Jahr: 2017

Heutige Anwendungen elektronischer Systeme setzen vermehrt auf die drahtlose Kommunikation und den Austausch von immer größer werdenden Datenmengen untereinander. Am Institut für Mikroelektronische Systeme werden unter anderem OFDM-basierte Kommunikationssysteme für diese Anforderungen konzeptioniert und evaluiert. Dabei spielt die Vorwärtsfehlerkorrektur der Sendedaten eine wichtige Rolle. Diese sorgt dafür, dass zuverlässig Daten über einen mit Störung behafteten Kanal zu übertragen werden können. Ein gängiges Verfahren für diese Art von Fehlerkorrekturmechanismus ist ein Faltungsencoder auf Senderseite und ein Viterbi-Decoder auf Empfängerseite. 

Ein Faltungsencoder fügt dem Sendesignal Redundanz hinzu um mögliche Übertragungsfehler am Empfänger zu korrigieren. Diese Korrektur geschieht mit Hilfe eines Viterbi-Decoders, welcher durch Berechnung aller möglichen gesendeten Symbolfolgen die auswählt, welche die höchste Wahrscheinlichkeit besitzt. Bei diesem Verfahren lassen sich die Länge des Gedächtnisses, die Art der Wahrscheinlichkeitsberechnung und der Anteil der Redundanz variieren.

In dieser Arbeit soll ein parametrisierbarer Faltungsencoder und zugehöriger Viterbi-Decoder in VHDL implementiert werden, bei dem die oben genannten Eigenschaften zum Zeitpunkt der Synthese eingestellt werden können. Ausgangspunkt der Konzeptionierung ist eine Referenzimplementierung in Matlab, welche als Evaluationsbasis für Hardware-seitige Ergebnisse dient. Nach erfolgreicher Evaluation soll die Echtzeitperformance der Implementierung mit Hilfe einer PXI-Emulationsplattform getestet werden. In dieser lassen sich verschiedene Typen von rauschenden Kanälen modellieren. Zum Abschluss der Arbeit sollen zusätzlich die FPGA-spezifische Kennzahlen extrahiert und verglichen werden.