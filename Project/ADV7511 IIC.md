[https://www.analog.com/media/en/technical-documentation/user-guides/ADV7511_Programming_Guide.pdf](https://www.analog.com/media/en/technical-documentation/user-guides/ADV7511_Programming_Guide.pdf)
The ADV7511 uses four I2C register maps. The SDA/SCL programming address for the Main Register Map is 0x72 or 0x7A,  
based on whether PD/AD is pulled high (10KΩ resistor to power supply = 0x7A) or pulled low (10KΩ resistor to GND =  0x72)
zed_hdmi_display.c中配置方式 
```C
Xuint8 carrier_hdmi_out_config[CARRIER_HDMI_OUT_CONFIG_LEN][3] =
{
	{ADV7511_ADDR>>1, 0x15, 0x01}, // Input YCbCr 4:2:2 with seperate syncs
	{ADV7511_ADDR>>1, 0x16, 0x38}, // Output format 444, Input Color Depth = 8
                                   //    R0x16[  7] = Output Video Format = 0 (444)
                                   //    R0x16[5:4] = Input Video Color Depth = 11 (8 bits/color)
                                   //    R0x16[3:2] = Input Video Style = 10 (style 1)
                                   //    R0x16[  1] = DDR Input Edge = 0 (falling edge)
                                   //    R0x16[  0] = Output Color Space = 0 (RGB)
#if 0
    // HDTV YCbCr (16to235) to RGB (0to255)
	{ADV7511_ADDR>>1, 0x18, 0xE7}, // Color Space Conversion
                                   //    R0x18[  7] = CSC enable = 1 (CSC enabled)
                                   //    R0x18[6:5] = CSC Scaling Factor = 11 (+/- 4.0, -16384 - 16380)
                                   //    R0x18[4:0] = CSC coefficient A1[12:8] = 00111
	{ADV7511_ADDR>>1, 0x19, 0x34}, //    R0x19[7:0] = CSC coefficient A1[ 7:0] =      00110100
	{ADV7511_ADDR>>1, 0x1A, 0x04}, //    R0x1A[  5] = CSC coefficient update
                                   //    R0x1A[4:0] = CSC coefficient A2[12:8] = 00100
	{ADV7511_ADDR>>1, 0x1B, 0xAD}, //    R0x1B[7:0] = CSC coefficient A2[ 7:0] =      10101101
	{ADV7511_ADDR>>1, 0x1C, 0x00}, //    R0x1C[4:0] = CSC coefficient A3[12:8] = 00000
	{ADV7511_ADDR>>1, 0x1D, 0x00}, //    R0x1D[7:0] = CSC coefficient A3[ 7:0] =      00000000
	{ADV7511_ADDR>>1, 0x1E, 0x1C}, //    R0x1E[4:0] = CSC coefficient A4[12:8] = 11100
	{ADV7511_ADDR>>1, 0x1F, 0x1B}, //    R0x1F[7:0] = CSC coefficient A4[ 7:0] =      00011011
	{ADV7511_ADDR>>1, 0x20, 0x1D}, //    R0x20[4:0] = CSC coefficient B1[12:8] = 11101
	{ADV7511_ADDR>>1, 0x21, 0xDC}, //    R0x21[7:0] = CSC coefficient B1[ 7:0] =      11011100
	{ADV7511_ADDR>>1, 0x22, 0x04}, //    R0x22[4:0] = CSC coefficient B2[12:8] = 00100
	{ADV7511_ADDR>>1, 0x23, 0xAD}, //    R0x23[7:0] = CSC coefficient B2[ 7:0] =      10101101
	{ADV7511_ADDR>>1, 0x24, 0x1F}, //    R0x24[4:0] = CSC coefficient B3[12:8] = 11111
	{ADV7511_ADDR>>1, 0x25, 0x24}, //    R0x25[7:0] = CSC coefficient B3[ 7:0] =      00100100
	{ADV7511_ADDR>>1, 0x26, 0x01}, //    R0x26[4:0] = CSC coefficient B4[12:8] = 00001
	{ADV7511_ADDR>>1, 0x27, 0x35}, //    R0x27[7:0] = CSC coefficient B4[ 7:0] =      00110101
	{ADV7511_ADDR>>1, 0x28, 0x00}, //    R0x28[4:0] = CSC coefficient C1[12:8] = 00000
	{ADV7511_ADDR>>1, 0x29, 0x00}, //    R0x29[7:0] = CSC coefficient C1[ 7:0] =      00000000
	{ADV7511_ADDR>>1, 0x2A, 0x04}, //    R0x2A[4:0] = CSC coefficient C2[12:8] = 00100
	{ADV7511_ADDR>>1, 0x2B, 0xAD}, //    R0x2B[7:0] = CSC coefficient C2[ 7:0] =      10101101
	{ADV7511_ADDR>>1, 0x2C, 0x08}, //    R0x2C[4:0] = CSC coefficient C3[12:8] = 01000
	{ADV7511_ADDR>>1, 0x2D, 0x7C}, //    R0x2D[7:0] = CSC coefficient C3[ 7:0] =      01111100
	{ADV7511_ADDR>>1, 0x2E, 0x1B}, //    R0x2E[4:0] = CSC coefficient C4[12:8] = 11011
	{ADV7511_ADDR>>1, 0x2F, 0x77}, //    R0x2F[7:0] = CSC coefficient C4[ 7:0] =      01110111
#else
	// HDTV YCbCr (16to235) to RGB (16to235)
	{ADV7511_ADDR>>1, 0x18, 0xAC},
	{ADV7511_ADDR>>1, 0x19, 0x53},
	{ADV7511_ADDR>>1, 0x1A, 0x08},
	{ADV7511_ADDR>>1, 0x1B, 0x00},
	{ADV7511_ADDR>>1, 0x1C, 0x00},
	{ADV7511_ADDR>>1, 0x1D, 0x00},
	{ADV7511_ADDR>>1, 0x1E, 0x19},
	{ADV7511_ADDR>>1, 0x1F, 0xD6},
	{ADV7511_ADDR>>1, 0x20, 0x1C},
	{ADV7511_ADDR>>1, 0x21, 0x56},
	{ADV7511_ADDR>>1, 0x22, 0x08},
	{ADV7511_ADDR>>1, 0x23, 0x00},
	{ADV7511_ADDR>>1, 0x24, 0x1E},
	{ADV7511_ADDR>>1, 0x25, 0x88},
	{ADV7511_ADDR>>1, 0x26, 0x02},
	{ADV7511_ADDR>>1, 0x27, 0x91},
	{ADV7511_ADDR>>1, 0x28, 0x1F},
	{ADV7511_ADDR>>1, 0x29, 0xFF},
	{ADV7511_ADDR>>1, 0x2A, 0x08},
	{ADV7511_ADDR>>1, 0x2B, 0x00},
	{ADV7511_ADDR>>1, 0x2C, 0x0E},
	{ADV7511_ADDR>>1, 0x2D, 0x85},
	{ADV7511_ADDR>>1, 0x2E, 0x18},
	{ADV7511_ADDR>>1, 0x2F, 0xBE},
```

定义二维数组，1byte baseaddr, 1byte reg offset 1byte data 这样的寄存器有40个，通过下面iic写函数传输

```c
fpIicWrite( &(pDemo->hdmi_out_iic), carrier_hdmi_out_config[i][0], carrier_hdmi_out_config[i][1], &(carrier_hdmi_out_config[i][2]), 1 );
```
