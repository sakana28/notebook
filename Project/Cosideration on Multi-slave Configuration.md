# Cosideration on Multi-slave Configuration

![](http://www.elm-chan.org/docs/mmc/m/do_diag.png)

In the SPI bus, each slave device is selected with separated CS signals, and plural devices can be attached to an SPI bus. Generic SPI slave device enables/disables its DO output by CS signal asynchronously to share an SPI bus. However MMC/SDC enables/disables the DO output in _synchronising to the SCLK_. This means there is a posibility of bus conflict with MMC/SDC and another SPI slave that shares an SPI bus. Right image shows the MISO line drive/release timing of the MMC/SDC (the DO signal is pulled to 1/2 vcc to see the bus state). Therefore to make MMC/SDC release the MISO line, the master device needs to send a byte after the CS signal is deasserted.

There is an important thing needs to be considered that the MMC/SDC is initially NOT the SPI device. Some bus activity to access another SPI device can cause a bus conflict due to an accidental response of the MMC/SDC. Therefore the MMC/SDC should be initialized to put it into the SPI mode prior to access any other device attached to the same SPI bus.