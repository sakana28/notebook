
[How to Use MMC/SDC](http://www.elm-chan.org/docs/mmc/mmc_e.html)
[如何使用MMC/SD卡](https://www.0xaa55.com/thread-25692-1-1.html)#
[SPI and SD cards](http://www.dejazzer.com/ee379/lecture_notes/lec12_sd_card.pdf)
# How to Use MMC/SDC
[[翻译]]


---

![MMC and SDC](http://www.elm-chan.org/docs/mmc/m/mmsd.jpeg)

The _Secure Digital Memory Card_ (SDC below) is the de facto standard memory card for mobile equipments. The SDC was developped as upper-compatible to _Multi Media Card_ (MMC below). SDC compleant equipments can also use MMCs in most case. There are also reduced size versions, such as _RS-MMC_, _miniSD_ and _microSD_, with the same function. The MMC/SDC has a microcontroller in it. The flash memory controls (block size translation, wearleveling and error correction - known as FTL) are completed inside of the memory card. The data is transferred between the memory card and the host controller as data blocks in unit of 512 bytes, so that it can be seen as a block device like a generic harddisk drive from view point of upper level layers.

This page describes the basic knowledge and miscellaneous things that I become aware, on using MMC/SDC with small embedded system. I believe that this information must be a useful getting started notes for the people who is going to use MMC/SDC on the electronics handiwork projects.

1.  [Pinout](http://www.elm-chan.org/docs/mmc/mmc_e.html#pinout)
2.  [SPI Mode](http://www.elm-chan.org/docs/mmc/mmc_e.html#spimode)
3.  [Initialization Procedure for SPI Mode](http://www.elm-chan.org/docs/mmc/mmc_e.html#spiinit)
4.  [Data Transfer](http://www.elm-chan.org/docs/mmc/mmc_e.html#dataxfer)
5.  [Cosideration to Bus Floating and Hot Insertion](http://www.elm-chan.org/docs/mmc/mmc_e.html#hotplug)
6.  [Cosideration on Multi-slave Configuration](http://www.elm-chan.org/docs/mmc/mmc_e.html#spibus)
7.  [Maximum SPI Clock Frequency](http://www.elm-chan.org/docs/mmc/mmc_e.html#freq)
8.  [File System](http://www.elm-chan.org/docs/mmc/mmc_e.html#fsys)
9.  [Optimization of Write Performance](http://www.elm-chan.org/docs/mmc/mmc_e.html#opti)
10.  [License](http://www.elm-chan.org/docs/mmc/mmc_e.html#license)
11.  [Links](http://www.elm-chan.org/docs/mmc/mmc_e.html#links)

##![[Pinout of SD]]

##![[SPI Mode]]

##![[Initialization Procedure for SPI Mode]]

##![[Data Transfer]]

##![[Cosideration to Bus Floating and Hot Insertion]]

##![[Cosideration on Multi-slave Configuration]]

##![[Maximum SPI Clock Frequency]]

##![[File System]]

##![[Optimization of Write Performance]]

##![[License]]

##![[Links]]


