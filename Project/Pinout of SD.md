# Pinout of SD
#SD #引脚
![SDC/MMC contact surface](http://www.elm-chan.org/docs/mmc/m/sdmm_contact.jpeg)  

Right photo shows the contact surface of the SDC/MMC. The MMC has seven contact pads. The SDC has nine contact pads that two additional contacts to the MMC. The three of the contacts are assigned for power supply, so that the number of effective signals are four (MMC) and six (SDC). Therfore the data transfer between the host and the card is done via a synchronous serial interface.

The working supply voltage range is indicated by the **operation conditions register 操作条件寄存器** (OCR) and it should be read and comfirmed the operating voltage range at card initialization. However, the supply voltage can also be fixed to 3.0 to 3.3 volts without any confirmation because the all MMC/SDCs work at _2.7 to 3.6 volts_ at least. Do not supply 5.0 volts to the card, or the card will be broken instantly. The current consumption at write operation can reach up to 100 miliamperes, so that the host system should consider to supply 100 miliamperes to tha card at least.

上图展示了SD卡和MMC的接触表面。MMC有7个接触板。SD卡有9个触点，比MMC多了两个。其中三个触点是电源，所以对于信号传输有效的触点，MMC有4个，SD卡有6个。从主机到卡的数据传输是通过一个同步串口界面进行的。  
  
工作供电的电压的范围由操作条件寄存器（OCR）得知，并且你在初始化卡并且准备操作的时候需要读取它并确保你提供的电压处于范围内。然而，在确定它的供电电压范围前，你可以认为它一定会在3.0v到3.3v之间正确工作。因为至少所有的SD卡和MMC都工作在*2.7v到3.6v*之间。但不要给它直接供5v的电，否则存储卡就地死亡。在写入操作中电流损耗能达到10毫安以上，所以主机系统应该考虑至少要提供100毫安以上的电源到卡上。  

下图是miniSD和microSD的Pin的图。
![[Pasted image 20220712134243.png]]

![[Pasted image 20220712134258.png]]

