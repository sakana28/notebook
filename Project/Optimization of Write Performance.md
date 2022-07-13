# Optimization of Write Performance

MMC/SDC employs [NAND Flash Memory](http://www.elm-chan.org/docs/dev/sm_e.html) as a memory array. The NAND flash memory is cost effective and it can read/write _large chunk_ of data fast, but on the other hand, there is a disadvantage that rewriting a _small part_ of data is inefficient. Generally the flash memory requires to erase existing data prior to re-write a new data, and minimum unit of erase operation, called erase block, is larger than write block size. The typical NAND flash memory has a block size of 512/16K bytes for write/erase operation, and recent cards lager than 128MB employs large block chip (2K/128K). This means that re-writing entire data in the erase block is done in the card even if write only a sector (512 bytes).

#### Benchmark

I examined the read/write performance of [some MMC/SDC](http://www.elm-chan.org/docs/mmc/m/sdmm.jpeg) with a cheap 8 bit MCU (ATmega64 @9.2MHz) on the assumption that an embedded system _with limited memory size_. For reason of memory size, write() and read() ware performed in 2048 bytes at a time. The result is: Write: 77kB/sec, Read: 328kB/sec on the [128MB SDC](http://www.elm-chan.org/docs/mmc/m/sd128.txt), Write: 28kB/sec, Read: 234kB/sec on the [512MB SDC](http://www.elm-chan.org/docs/mmc/m/sd512.txt) and Write: 182kB/sec, Read: 312kB/sec on the [128MB MMC](http://www.elm-chan.org/docs/mmc/m/mm128.txt).

_By [some benchmarks](http://www.elm-chan.org/fsw/ff/img/rwtest1.png) later, I guess MMC tends to be faster than SDC in write throughput._

Therefor the write performance of the 512MB SDC was very poor that one third value of 128MB SDC. Generally the read/write performance of the mass storage device increases proportional to its recording density, however it sometimes appears a tendency of opposite on the memory card. As for the MMC, it seems to be several times faster than SDC, it is not bad performance. After that time, I examined some SDCs supplied from different makers, and I found that PQI's SDC was as fast as Hitachi's MMC but Panasonic's and Toshiba's one was very poor performances.

#### Erase Block Size

To analys detail of write operation, busy time (number of polling cycles) after sent a write data is typed out to console in the low level disk write function. Multiple numbers on a line indicates data blocks and a Stop Tran token that issued by a multiple block write transaction.

In resulut of the analysis, there is a different of internal process between 128MB SDC and 512MB SDC. The 128MB SDC rewrites erase block at end of the mutiple block write transaction. The 512MB SDC seems have 4K bytes data buffer and it rewrites erase block every 4K bytes boundary. Therefor it cannot compared directly but the processing time of rewriting an erase block can be read 3800 for 128MB SDC and the 512MB SDC taeks 30000 that 8 times longer than 128MB SDC. Judging from this resulut, it seems the 128MB SDC uses a small block chip and the 512MB SDC uses a large block or MLC chip. Ofcourse the larger block size decreases the performance on pertial block rewriting. In 512MB SDC, only an area that 512K bytes from top of the memory is relatively fast. This can be read from write time in close(). It might any special processing is applied to this area for fast FAT accsess.

#### Improving Write Performance

![write transactions](http://www.elm-chan.org/docs/mmc/m/f6.png)

To avoid this bottleneck and increase the write performance, number of blocks per write transaction must be large as possible. Of course all layers between the application and the media must support multiple sector write feature. For low level SDC/MMC write function, it should inform number of write sectors to the card prior to the write transaction for efficient internal write process. This method called `pre-defined multiple block write'. The pre-definition command is not the same between MMC (CMD23) and SDC (ACMD23).

The memory cards are initially patitioned and formatted to align the allocation unit to the erase block boundary. When re-patition or re-format the memory card with a device that not compliant to MMC/SDC (this is just a PC) with no care, the optimization will be broken and the write performance might be lost. I tried to re-format a 512MB SDC in FAT32 with a generic format function of the PC, the write performance measured in file copy was decreased to one several. Therefore the re-formatting the card should be done with SD format utility or SDC/MMC compliant equipments.