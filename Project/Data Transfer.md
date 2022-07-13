# Data Transfer

#### Data Packet and Data Response

![data block](http://www.elm-chan.org/docs/mmc/m/data.png)

In a transaction with data transfer, one or more data blocks will be sent/received after command response. The data block is transferred as a data packet that consist of Token, Data Block and CRC. The format of the data packet is showin in right image and there are three data tokens. Stop Tran token is to terminate a multiple block write transaction, it is used as single byte packet without data block and CRC.

  

#### Single Block Read

![](http://www.elm-chan.org/docs/mmc/m/rs.png)  

The argument specifies the address to start to read in unit of BYTE or BLOCK. The sector address in LBA specified by upper layer must be scaled properly depends on the card's addressing mode. When a CMD17 is accepted, a read operation is initiated and the read data block will be sent to the host. After a valid data token is detected, the host controller receives following data field and CRC. The CRC bytes must be received even if it is not needed. If any error occured during the read operation, an error token will be returned instead of data packet.

#### Multiple Block Read

![](http://www.elm-chan.org/docs/mmc/m/rm.png)  

The CMD18 is to read data blocks in sequense start at the specified address. The read operation continues as open-ended. To terminate the read transaciton, a CMD12 needs to be sent to the card. The received byte immediataly following CMD12 is a stuff byte, it should be discarded prior to receive the response of the CMD12. For MMC, if number of transfer blocks has been sepecified by a CMD23 prior to CMD18, the read transaction is initiated as a pre-defined multiple block transfer and the read operation is terminated at last block transfer.

#### Single Block Write

![](http://www.elm-chan.org/docs/mmc/m/ws.png)  

The Single Block Write writes a block to the card. After a CMD24 is accepted, the host controller sends a data packet to the card. The packet format is same as block read operations. Most cards cannot change write block size and it is fixed to 512. The CRC field can have any fixed value unless the CRC function is enabled. The card responds a Data Response immediataly following the data packet from the host. The Data Response trails a busy flag and host controller must suspend the next command or data transmission until the card goes ready.

In principle of the SPI mode, the CS signal must be kept asserted during a transaction. However there is an exception to this rule. When the card is busy, the host controller can deassert CS to release SPI bus for data transfer to other SPI devices on the bus. The card will drive DO low again when reselected during internal process is still in progress. Therefore a preceding busy check, check if card is busy prior to each command and data packet, instead of post wait can eliminate the busy wait time. In addition, the internal write process is initiated a byte after the data response, this means eight SCLK clocks are required to initiate internal write operation. The state of CS signal during the post clocks can be either low or high, so that it can be done with bus release process described below.

#### Multiple Block Write

![](http://www.elm-chan.org/docs/mmc/m/wm.png)  

The Multiple Block Write command writes data blocks in sequense start at the specified address. After a CMD25 is accepted, the host controller sends one or more data packets to the card. The packet format is same as block read operations except for Data Token. The write transaction continues until it terminated with a Stop Tran token. The busy flag will be output after every data block and Stop Tran token. For MMC, the number of blocks to write can be pre-defined by CMD23 prior to CMD25 and the write transaction is terminated at last data block. For SDC, a Stop Tran token is always required to treminate the multiple block write transaction. Number of sectors to pre-erased at start of the write transaction can be specified by an ACMD23 prior to CMD25. It may able to optimize write strategy in the card and it can also be terminated not at the pre-erased blocks but the content of the pre-erased area not written will get undefined.

#### Reading CSD and CID

These are same as Single Block Read except for the data block length. The CSD and CID are sent to the host as _16 byte data block_. For details of the CMD, CID and OCR, please refer to the MMC/SDC specs.