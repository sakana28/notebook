#文档草稿
1.了解公司的设备管理，密码定期，IT系统，各项制度，zynq book ，Xilinx 官方文档，安装并配置开发环境，
2.熟悉Vivado与Vitis开发环境，了解项目，Confluence 
3.在无硬件的环境下理解SOC的设计流程，完成实验项目，通过EMIO-GPIO控制LED灯
4.继续学习嵌入式编程，完成实验项目 在PL实现一个可以通过AXI总线读写寄存器的计数器
5.得到硬件，尝试不同方法的下载，解决开发板两个生产版本带来的BUG，解决Linux下无法识别uart的问题
6.通过SD卡读写BMP图片，图片显示不全。查找资料后 BMP补0 在与领导与同事的交流中注意了C代码的规范书写
7.完全使用内嵌ARM实现Sobel处理，并将处理结果写入SD卡，了解SOBEL的原理及限制运算速度的因素
8.学习AXI DMA 和AXI FIFO IP实现图片的回环处理，实现ARM和PL的通信
9.学习搭建HDMI输出 查找官方文档和事例设计 解决问题：版本 按照脚本重新构建系统
色彩偏差→图像是按照RBG的顺序 无输出：时序，提高时钟，位宽匹配
10 SOBEL IP实现，完成大部分并进行简单测试
11 写testbench，写c程序实现预处理bmp txt bmp，封装IP
12构建系统 写软件
13写文档，做PPT
14 学习Zynq运行Linux
15 参与FPGA Cop，展示项目。Petalinux定制系统，实现在Zynq上SD卡读取Linux镜像并通过串口通信，实现在Zynq上挂载SD卡存储区并运行Hello World程序
16完成收尾工作，把文件 文档存放进项目archive，归还设备


Am ersten Tag meines Praktikums kam ich um neun Uhr morgens im Büro in Braunschweig an. Während ich meine Kollegen kennenlernte und die ITK-Regeln las, wurde mir auch ein Computer mit dem Linux-Betriebssystem Ubuntu für das Projekt zur Verfügung gestellt.

Die Sobel-Kantenerkennung ist ein klassischer Algorithmus in der Bild- und Videoverarbeitung, der dazu dient, Kanten von Objekten zu extrahieren. Eine gängige Methode zur Kantenerkennung besteht darin, die erste Ableitung eines Bildes zu berechnen, um Kanteninformationen zu extrahieren. Durch die Berechnung der x- und y-Ableitungen eines bestimmten Pixels im Vergleich zu den Pixeln in dessen Umgebung können die Grenzen zwischen zwei verschiedenen Elementen in einem Bild extrahiert werden. Da die Berechnung der Ableitungen jedoch sehr rechenintensiv ist, da sie Quadrierungs- und Quadratwurzeloperationen beinhaltet, werden Masken mit festen Koeffizienten, also der Sobel-Operator, als geeignete Annäherung für die Berechnung der Ableitungen an einem bestimmten Punkt verwendet.

Der Sobel-Filter verwendet im Allgemeinen zwei 3 x 3-Kerne. Einen für die Berechnung der horizontalen Variation und einen anderen für die Berechnung der vertikalen Variation. Diese beiden Kerne werden mit dem Originalbild gefaltet, um eine Annäherung an die Ableitung zu berechnen.

### RGB to grayscale

In diesem Projekt wird die folgende Formel verwendet, um die Grauskala eines Pixels zu berechnen:
Graustufe= (R << 2) + (R << 5) + (G << 1) + (G << 4) + (B << 4) + (B << 5)
Dies ist eine annähernde Form der folgenden Gleichung:
Graustufen = ( (0,3 * R) + (0,59 * G) + (0,11 * B) )

### BMP File
Die Anzahl der Bytes in einer Reihe von BMP-Bildern wird nach der folgenden Formel berechnet:
![[Pasted image 20220726102502.png]]
Nach allen Datenbytes wird der Rest der Position mit 0 aufgefüllt, um sicherzustellen, dass eine Reihe von BMP-Bildern ausgerichtet im Computer gespeichert werden kann. 
Der Header einer BMP-Datei enthält Metadaten über das Bild. Durch Auslesen bestimmter Bytes im Header ist es möglich, die Länge und Breite eines BMP-Bildes zu ermitteln.
![[Pasted image 20220929214255.png]]

## System Structure

Die Kommunikation zwischen Zynq PS und PL basiert auf dem AXI4-Protokoll. Wie in der Abbildung unten dargestellt, sind die konfigurierbaren Register der Sobel-IP über den AXI-Lite-Bus mit dem General-Propose-Port des PS verbunden. Und die Bilddaten werden über den AXI4-Bus durch den Hochleistungsport an die AXI DMA IP gesendet. Diese IP überträgt die Daten direkt aus dem Speicher und streamt sie mit dem AXI4-Stream-Protokoll an andere Peripheriegeräte.
![[Pasted image 20220927211645.png]]
In diesem System wird das Originalbild vom Prozessor von der SD-Karte gelesen und vorverarbeitet (Zero-Padding und Umordnung der Daten). Die vorverarbeiteten Daten werden dann im DDR gespeichert und über die AXI-DMA-IP an die Sobel-IP übertragen. Die verarbeiteten Binärbilder werden von AXI DMA wieder in den DDR zurückgeschrieben. Nach dem Senden einer bestimmten Datenmenge benachrichtigt der AXI-DMA den PS mit einem Interrupt-Signal.

Das Original und das verarbeitete Bild werden dann von AXI VDMA IP aus dem DDR verschoben und im PL gepuffert. Dann werden die Daten zur Verarbeitung an Xilinx VPSS IP übertragen und später mit den Timing-Signalen in AXIS to video out IP synchronisiert. Schließlich wird das 16-Bit-YCbCr-Videosignal an den ADV7511 HDMI-Transmitter auf dem Zedboard gesendet und auf einem Monitor angezeigt.

![[Pasted image 20220927211533.png]]

## Hardware Implementation

Zunächst empfängt das RGB to Grayscale-Modul die 32-Bit-RGB-Daten von der AXI4-Stream-Schnittstelle und wandelt sie mithilfe von Verschiebungen und Additionen ungefähr in 8-Bit-Graustufendaten um. Darüber hinaus verfügt das Modul über zwei Steuersignaleingänge. Die aktuellen 32-Bit-RGB-Daten werden nur dann als gültig angesehen, wenn sowohl data_ready vom Output_buffer-Modul als auch data_valid von AXI-DMA IP High sind.

Die vom RGB-zu-Graustufen-Modul ausgegebenen Daten werden sequentiell in 4 Zeilenpuffer geschrieben. Alle Zeilenspeicher sind mit demselben Dateneingangsport verbunden, und jeder Zeilenspeicher hat sein eigenes Wertesignal, das angibt, ob die aktuelle Eingabe gültig ist oder nicht. Jeder Zeilenspeicher kann bis zu 1024 8-Bit-Daten speichern, was die maximale Breite des zu verarbeitenden Bildes begrenzt. Jeder Zeilenspeicher kann gleichzeitig gelesen und beschrieben werden. Die Steuerlogik sorgt dafür, dass nur ein Schreibvorgang und nur drei Lesevorgänge gültig sind. Außerdem ordnet sie die Ausgabedaten aus den Zeilenpuffern in einer bestimmten Reihenfolge an, so dass jede gültige Ausgabe ein aus dem Graustufenbild segmentiertes 3x3-Fenster ist. Vor jedem Lesevorgang prüft der FSM, ob genügend Daten in den Zeilenspeichern vorhanden sind. Wenn nicht genügend Daten vorhanden sind, verbleibt der FSM im Idle-Zustand und benachrichtigt den PS-Prozessor durch ein PL-PS-Interrupt-Signal.

Die IP enthält auch ein Register, das über die AXI4-Lite-Schnittstelle konfiguriert werden kann. Vor der Bildverarbeitung sollte der Benutzer es auf die Breite des zu verarbeitenden Bildes + 2 konfigurieren (d.h. die Breite des Bildes mit Null-Padding)

Im Faltungsmodul wird eine fünfstufige Pipeline verwendet, um den Kantenerkennungswert zu berechnen und festzustellen, ob der Wert größer als der Schwellenwert ist. Ist er größer als der Schwellenwert, werden 8-Bit-Daten 0XFF ausgegeben, andernfalls werden 8-Bit-Daten 0X00 ausgegeben, d. h. die Kante ist weiß und der Rest ist schwarz.

Der Xilinx FIFO IP-Core wird als Ausgangspuffer verwendet und kann bis zu 32 8-Bit-Daten aufnehmen. Das invertierende programmierbare Full-Signal dieses IP-Cores, das mit einem Schwellenwert von 16 konfiguriert ist, wird mit dem Ausgangsport axis_ready des Sobel-IP verbunden. Das bedeutet, dass der Sobel-IP den Empfang von Daten vom vorgeschalteten AXI-DMA-IP stoppt, wenn 16 Daten im Puffer gespeichert sind und nicht durch eine gültige Übertragung an das nächste Modul ausgegeben werden, um eine mögliche Datenverfälschung zu verhindern.