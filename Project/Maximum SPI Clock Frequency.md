# Maximum SPI Clock Frequency

![](http://www.elm-chan.org/docs/mmc/m/spi_timing.png)

MMC/SDC can work at the clock frequency upto 20/25 MHz. Of course all native interfaces guarantee to work at the maximum clock frequency. However generic SPI interface integrated in the microcontrollers may not work at high clock frequency due to a timing issue. Right image shows the timing diagram of the SPI interface. In SPI mode 0/3, the data is shifted out by falling edge of the SCLK and latched by following rising edge. _td_ is the SCLK to DO propagation delay at the SDC, 14ns maximum. _tsu_ is the minimum setup time of the MISO input on the SPI interface. Therefore the maximum allowable SCLK frequency can be calculated as:

FSCLK(max) = 0.5 / (td + tsu)

Some microcontrollers I have used are limited the allowable clock frequency around 10 MHz according to the timing specs.