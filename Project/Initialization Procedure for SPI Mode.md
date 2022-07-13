# Initialization Procedure for SPI Mode

After a power-up sequence, MMC/SDC enters its native operating mode. To put it SPI mode, follwing procedure must be performed as shown in [this flow](http://www.elm-chan.org/docs/mmc/m/sdinit.png).
![](https://www.0xaa55.com/data/attachment/forum/201902/12/190936gi92nc2ixpc8ijan.png)  
#### Power ON or card insersion

After supply voltage reached above 2.2 volts, wait for one millisecond at least. Set SPI clock rate between 100 kHz and 400 kHz. Set DI and CS high and apply 74 or more clock pulses to SCLK. The card will enter its native operating mode and go ready to accept native command.

#### Software reset

Send a _CMD0 with CS low_ to reset the card. The card samples CS signal on a CMD0 is received successfully. If the CS signal is low, the card enters SPI mode and responds R1 with In Idle State bit set (0x01). Since the CMD0 must be sent as a native command, the CRC field must have a valid value. When once the card enters SPI mode, the CRC feature is disabled and the command CRC and data CRC are not checked by the card, so that command transmission routine can be written with the hardcorded CRC value that valid for only CMD0 and CMD8 used in the initialization process. The CRC feature can also be switched on/off with CMD59.

#### Initialization

In idle state, the card accepts only CMD0, CMD1, CMD8, ACMD41, CMD58 and CMD59. Any other commands will be rejected. In this time, OCR register should be read with CMD58 to check the working voltage range of the card. In case of the system sypply voltage is out of working voltage range, the card must be rejected. Note that all cards work at supply voltage in range of 2.7 to 3.6 volts at least, so that the host contoller does not need to check the OCR if supply voltage is in this range. The card initiates the initialization process when a _CMD1_ is received. To detect end of the initialization process, the host controller needs to send CMD1 and check the response until end of the initialization. When the card is initialized successfuly, In Idle State bit in the R1 response is cleared (R1 resp changes 0x01 to 0x00). The initialization process can take _hundreds of milliseconds_ (large cards tend to longer), so that this is a consideration to determin the time out value. After the In Idle State bit cleared, the card gets ready to accept the generic read/write commands. ^lgvwpy

Because _ACMD41_ instead of CMD1 is recommended for SDC, trying ACMD41 first and retry with CMD1 if rejected, is ideal to support both type of the cards.

The SCLK frequency should be changed to fast as possible to maximize the read/write performance. The TRAN_SPEED field in the CSD register indicates the maximum clock frequency of the card. It is 20MHz for MMC, 25MHz for SDC in most case. Note that the clock freqency will able to be fixed to 20/25MHz in SPI mode because there is no open-drain condition that restricts the clock frequency.

The initial read/write block length might be set 1024 on 2 GB cards, so that the block size should be re-initialized to 512 with CMD16 to work with FAT file system.

#### High-capacity SDC and Initialization

SDSC card supports 8MB to 2GB. This is from the maximum capacity of regular file system, FAT. (FAT supports up to 4GB theoritically but MS-DOS supports up to 2GB.)

SDHC card supports 4GB to 32GB. This is from the maximum capacity of regular file system, FAT32. (FAT32 supports up to 2TB theoritically but it seemed to be affected by Microsoft's wishes that they recommend to use FAT32 for the volumes in 32GB or smaller.)

SDXC card supports 64GB to 2TB. This is from the addressing mode in read/write commands, 32-bit LBA. (The regular file system, exFAT, supports over 2TB.)

SDUC card supports 4TB to 128TB. The addressing mode is extended to 38-bit LBA. However the SDUC card might not support SPI mode because the 38-bit LBA is a new feature defined after SDC Ver.2.

Now, the initialization process for high-capacity SDCs differs from the process described above. After the card goes idle state with a CMD0, host controller sends a _CMD8_ with an argument 0x000001AA and correct CRC prior to initialization process. If it is rejected with illigal command error (0x05), the card is SDC Ver.1 or MMC Ver.3. The card will be initialized as described above. If the CMD8 is accepted, R7 response (R1(0x01) + 32-bit return value) will be returned. The lower 12-bit in the return value 0x1AA means that the card is SDC Ver.2+ and it can work at supply voltage range of 2.7 to 3.6 volts. If it is not the case, the card should be rejected. And then initiate initialization with ACMD41 with HCS[bit30] flag in the argument. After the initialization completed, read OCR register with CMD58 and check CCS[bit30] flag. When it is set, the card is a high-capacity card known as _SDHC/SDXC_. The data read/write operations described below are commanded in block addressing (LBA) insted of byte addressing. The size of data block at block addressing mode is fixed to 512 bytes.