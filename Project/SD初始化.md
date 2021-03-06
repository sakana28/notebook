---
date created: 2022-07-13 16:40
date updated: 2022-07-13 17:19
---

# SD2.0初始化

#SD

## 补充资料

[SD卡初始化细节 - 程序员大本营](https://www.pianshen.com/article/3747783139/)
[SD卡的SPI模式的初始化顺序 - 窗外.yu.好大 - 博客园](https://www.cnblogs.com/mrightt/archive/2011/06/23/2088265.html)
[SD卡命令简介 - xxxdk's blog](http://xxxdk.xyz/xxx/2021/01/SD%E5%8D%A1%E5%91%BD%E4%BB%A4%E7%AE%80%E4%BB%8B/)

## 方法1

![[Pasted image 20220712162850.png]]

1. SD卡完成上电后，主机FPGA先对从机SD卡发送至少74个以上的[[同步时钟]]，在上电同步期间，片选CS引脚和MOSI引脚(DI信号)必须为高电平（MOSI引脚除发送命令或数据外，其余时刻都为高电平）；
2. 拉低片选CS引脚(CS低有效)，发送命令CMD0（0x40）复位SD卡，命令发送完成后等待SD卡返回响应数据；
3. SD卡返回响应数据后，先等待8个时钟周期再拉高片选CS信号，此时判断返回的响应数据。如果返回的数据为复位完成信号0x01，其中闲置状态位为1,其余为0。在接收返回信息期间片选CS持续为低电平，此时SD卡进入SPI模式，并开始进行下一步，如果返回的值为其它值，则重新执行第2步；
4. 拉低片选CS引脚，发送命令CMD8（0x48）查询SD卡的版本号，只有SD2.0版本的卡才支持此命令，命令发送完成后等待SD卡返回响应数据；
5. SD卡返回响应数据后，先等待8个时钟周期再拉高片选CS信号，此时判断返回的响应数据。如果返回的电压范围为4’b0001即2.7V~3.6V，说明此SD卡为2.0版本，进行下一步，否则重新执行第4步；拉低片选CS引脚，发送命令CMD55（0x77）告诉SD卡下一次发送的命令是应用相关命令，命令发送完成后等待SD卡返回响应数据；SD卡返回响应数据后，先等待8个时钟周期再拉高片选CS信号，此时判断返回的响应数据。如果返回的数据为空闲信号0x01，开始进行下一步，否则重新执行第6步。拉低片选CS引脚，发送命令ACMD41（0x69）查询SD卡是否初始化完成，命令发送完成后等待SD返回响应数据；SD卡返回响应数据后，先等待8个时钟周期再拉高片选CS信号，此时判断返回的响应数据。如果返回的数据为0x00，此时初始化完成，否则重新执行第6步。

## 方法2

from [[MMC SDC的使用]]
![[Pasted image 20220713144436.png]]

_注意 上图中检测OCR判断SD还是SDHC  SDXC后进行的CMD16作用是设置块读写操作的块长度，SDHC/SDXC card默认值都是 512bytes。即发送argument 0x200即dizimal512_

步骤1**上电或插卡**

在供电达到2.2伏的时候，等待至少1毫秒。设置SPI时钟频率介于100 kHz到400 kHz之间。设置DI和CS高，并向SCLK施加至少74个时钟脉冲。卡片就会进入它的原生操作模式然后准备接收原生命令。

```
DI 即为 MOSI，此时SD卡相对于FPGA主机而言是从机，MOSI即为I口
同理DO口为MISO
  
```

步骤2**软件重置**

拉低CS并发送CMD0来重置存储卡。SD卡从机在收到CMD0信号的时候采样CS信号。如果CS信号为低，卡就会进入SPI模式并应答一个R1应答，并把In Idle State位（闲置状态位）设为1（应答0x01）。由于CMD0命令必须通过它的原生方式发送，CRC域必须是一个有效值(95)。当存储卡进入了SPI模式，CRC特性就不再使用了，存储卡它也不检测CRC值。所以软件重置的CMD0命令，或者带一个值为0的参数的CMD8命令，它们的CRC值可以被硬编码钦定。同时，你也可以通过CMD59来切换CRC特性的开启与关闭。

步骤3**初始化**

在闲置状态，存储卡只接收CMD0，CMD1，ACMD41，CMD58，和CMD59.所有其它的命令都会被拒绝。此时，你要读OCR寄存器并且检查存储卡工作电压的范围。一旦发现系统供电电压不在存储卡的工作电压范围内，这张卡就应该被弹出。注意所有卡都至少在2.7伏到3.6伏之间能工作，所以如果主机控制器也在这个电压范围内，就可以不用检查OCR的电压范围了。存储卡在收到**CMD1**的时候开启初始化过程，所以主机必须发送CMD1然后持续检查它的应答，直到初始化结束。当存储卡初始化成功后，R1应答的In Idle State位会被清零（R1的应答从0x01变为0x00）。初始化过程所需的时间能达到**上百毫秒**（存储卡容量越大，它应该会越长），所以你需要考虑超时的时间。当In Idle State位清零了，通常的读写操作就可以用了。

由于对于SD卡而言推荐用**ACMD41**而不是CMD1，可以先尝试ACMD41，如果被拒绝了再尝试CMD1。这是一种理想的做法，可以让你同时兼容SD卡和MMC卡（MM卡）。

SCLK的频率应该被改为尽可能大，来把读写性能最大化。可以通过CSD寄存器的TRAN_SPEED字段得知存储卡的最大时钟频率。大多数情况下，MMC的最大时钟频率是20MHz，SD卡的最大时钟频率是25MHz。注意在SPI模式下时钟频率可以被固定在20或25MHz，因为没有漏极开路（open-drain）的条件限制时钟的频率。

在2GB的卡上最初的读写块长度有可能是1024，所以为了能支持FAT文件系统，你需要通过CMD16来把块长度重新设置为512字节。

**初始化大容量卡**

在存储卡收到CMD0命令并进入闲置模式后，发送一个参数为0x000001AA的CMD8命令以及正确的CRC值来初始化。如果存储卡拒绝CMD8命令并返回非法指令错误（0x05），这个存储卡应该是版本1的SD卡或版本3的MMC卡。如果它接受，它会返回一个R7应答（R1（0x01）以及一个32位返回值）。返回值低12位如果是0x1AA，意为SD卡的版本是2，并且它能在电压范围2.7伏到3.6伏内工作。如果不是这种情况，这张卡应该被弹出。之后再用带了HCS标识（第30位）的ACMD41命令来开启初始化过程。在初始化完成后，用CMD58读取OCR寄存器并检查CCS标识（第30位）。当它是1，这张卡就是一个大容量卡，也就是SDHC/SDXC。之后描述的存储卡的读写操作是用命令进行块寻址而非字节寻址。在块寻址模式下块的大小被钦定为512字节。

**EN**:

The steps to switch the SD card into SPI mode should therefore be as follows:\
Power-up.\
• Send at least 74 clock pulses to the card with CS and Data Outlines set to logic “1.”\
• Set CD line low.\
• Send 6-byte CMD0 command “40 00 00 00 00 95” to put the card in SPI mode.\
利用CRC计算器[CRC（循环冗余校验）在线计算_ip33.com](http://www.ip33.com/crc.html)
得到40 00 00 00 00 00 CRC为1001010, 补尾数1,得10010101,即0X95
• Check R1 response to make sure there are no error bits set.\
• Send command CMD1 repeatedly until the “in-idle-state” bit in R1 response is set to “0,”  CMD1 设置SD卡到ACTIVATE模式,也就是退出IDLE模式
• and there are no error bits set. The card is now ready for read/write operations.

![[Initialization Procedure for SPI Mode#Initialization]]

## 问题

**为何上述正点和ELM初始化差别如此大**？
解答
[# SD卡 初始化 到底哪一个 才是对的？](https://zhidao.baidu.com/question/552597276.html)
正点的适用于SD SDHC SDXC
ELM适用MMC

## SD卡上电复位及初始化命令时序

![[Pasted image 20220713162941.png]]

上图所示时序1 软件复位，通过MOSI发送CMD0 0X40 00 00 00 00 95 到SD卡，保持CS拉低。等待命令应答时间NCR后接收到响应。R1长1byte，即需要发送8个周期。接收完毕后拉高CS

Init
低有效CS片选后发送CMD55宣告接下来是应用指令。接收结束R1 0X01后等待起码8个CLK，进行下一步操作。发送ACMD41。上述两个指令因为已经工作在SPI，CRC发送FF就可以。接收R1 0X00 结束初始化。否则不断发送CMD55 ACMD41,直到收到0X00为止
