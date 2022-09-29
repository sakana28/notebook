---
date created: 2022-09-28 10:40
date updated: 2022-09-29 20:43
---

## Sobel Edge Detection
sobel edge detection is a classical algorithm in the field of image and video processing for the extraction of object edges. Edge detection using Sobel operators works on the premise of computing an estimate of the first derivative of an image to extract edge information . By computing the x and y direction derivatives of a specific pixel against a neighborhood of surrounding pixels, it is possible to extract the boundary between two distinct elements in an image. Due to the computational load of calculating derivatives using squaring and square root operators, fixed coefficient masks have been adopted as a suitable approximation in computing
the derivative at a specific point. In the case of Sobel, the masks used are shown in Table 1.

the sobel filter uses two 3 x 3 kernels. One for changes in the
horizontal direction, and one for changes in the vertical direction.
The two kernels are convolved with the original image to calculate the
approximations of the derivatives.

Sobel edge detection is a classical algorithm in the field of image and video processing for extracting the edges of objects. The premise of edge detection using the Sobel operator is to compute an estimate of the first-order derivative of an image to extract edge information. The boundary between two different elements in an image can be extracted by computing the derivatives of a particular pixel in the x and y directions compared to the neighborhood of the surrounding pixels. Due to the computational effort of using square operation and square root operation to calculate the derivatives, fixed coefficient masks have been used as a suitable approximation to calculate the derivatives at a specific point.
In general, the Sobel filter uses two 3 x 3 kernels. One for the horizontal variation, one for the horizontal variation and the other for the vertical variation.
These two kernels are convolved with the original image to calculate an approximation of the derivative.
## Requirements

Software Tools:

- Vivado ML Edition  2022.1
- Vitis Unified Software Platform 2022.1
- Terminal program (CuteCom)

Hardware Tools:

- ZedBoard

## System Structure

The communication between Zynq PS and PL is based on the AXI4 protocol. As shown in the figure below, the configurable registers of the Sobel IP are connected to the General Propose port of the PS by the AXI Lite bus. And the image data is sent to AXI DMA IP through the AXI4 bus through the High performance port. This IP moves the data direct from the memory and streams it to other peripherals with the AXI4-Stream protocol.

![[Pasted image 20220927211645.png]]
In this system, the original image is read from the SD card by the processor and pre-processed (Zero-Padding and data rearrangement). The pre-processed data is then stored in the DDR and transferred to the Sobel IP by the AXI DMA IP. The processed binary images are written back to the DDR again by the AXI DMA. After sending a specific amount of data, the AXI DMA notifies the PS with an interrupt signal.

The original and the processed image are then moved from the DDR by AXI VDMA IP and buffered in PL. Then the data is transferred to Xilinx VPSS IP for processing and later synchronized with the timing signals in AXIS to video out IP. Finally, the 16-bit YCbCr video signal is sent to the ADV7511 HDMI Transmitter on  Zedboard and displayed on a monitor.

![[Pasted image 20220927211533.png]]

## Hardware Implementation

First, the RGB to Grayscale module receives the 32-bit RGB data from the AXI4-Stream interface and converts it approximately to 8-bit grayscale data using shifts, addition, and fixed-value multiplication. In addition, the module has two control signal input ports. The current 32-bit RGB data is considered valid only when both data_ready from the Output_buffer Module and data_valid from AXI-DMA IP are high.

The data output from the RGB to Grayscale module is sequentially written into 4 line buffers. All line buffers are connected to the same data input port, and each line buffer has its own value signal, which marks whether the current input is valid or not. Each line buffer can store up to 1024 8-bit data , which limits the maximum width of the image being processed. Every line buffer can be read and written simultaneously . The control logic ensures that only one write process and only three read processes are valid. It also arranges the output data from line buffers in a specific order so that each valid output is a 3x3 window segmented from the grayscale image. Before each read, the FSM checks if there is enough data being stored in the line buffers. If there is not enough data, the FSM will remain in the Idle state and notify the PS processor by a PL-PS Interrupt signal.

The IP also contains a register that can be configured through AXI4-Lite interface. Before image processing, the user should configure it to the width of the image to be processed + 2 (i.e. the width of the image with zero-padding)

In the Convolution module, a five-stage pipeline is used to calculate the edge detection value and determine whether the value is greater than the threshold value. If it is greater than the threshold value, 8-bit data 0XFF is output, otherwise 8-bit data 0X00 is output, i.e. the edge is white and the rest is black.

The Xilinx FIFO IP core is used as an output buffer and can hold up to 32 8-bit data. The inverting programmable full signal of this IP core, which is configured with a threshold of 16, is connected to the Sobel IP's output port axis_ready. This means that the Sobel IP stops receiving data from the upstream AXI-DMA IP when 16 data are stored in the buffer and are not output to the next module by a valid transfer, to prevent potential data corruption.

## Generate the hardware design with Vivado Design Suite

file list:

- sobel_system.tcl -- script to generate the system block design
- sobel_v1_0 -- packaged Sobel custom IP
- zedboard_hdmi_display.xdc -- constraints file for Zedboard HDMI output

## Simulation

A test bench and two C programs are provided to generate appropriate stimuli and to check the functionality of the image edge detection IP.
files list:

- tb_kontrolle_file.vhd -- A test bench that instantiates all modules in Sobel IP except the Output_buffer module. It can read a text file as stimulus and generate another output text file.
- rgb32_zero_gen.c -- A C program to pad 0 and convert a 100x100 BMP image file to a text file.
  - Arguments: rgb32_zero_gen file_in file_out
- txttobmp.c -- A C program to convert a text file to a 100x100 BMP image file.
  - Arguments: txt2bmp file_in file_out

The following figure shows the input image
![[Pasted image 20220928214551.png]]
The following figure shows the output image after being processed using the Sobel test modules.
![[Pasted image 20220928214629.png]]
By comparing the waveforms resulting from the simulation with the designed waveforms, we conclude that the tested module implements the designed functions without errors.
![[Pasted image 20220929191705.png]]
![[Pasted image 20220929191937.png]]

## Software

files list:

- main.c
- platform.c
- platform.h
- platform_config.h
- rgbtoyuv422.c
- rgbtoyuv422.h
- SDoperation.h
- SDoperation.c
- sobel_dma.h
- sobel_dma.c
- sobel.h

Standalone drivers from Avnet example design:

- video_frame_buffer.h
- video_generator.h
- video_generator.c
- video_resolution.c
- video_resolution.h
- zed_iic.h
- zed_iic_axi.c
- video_frame_buffer.c
- zed_hdmi_display.c
- zed_hdmi_display.h

In file sobel_dma.c, the software design to finish a complete image filtering process consists of the following steps:

- Initialize the DMA.
- configurate the Sobel IP width register
- Setup interrupt system
- enable S2MM interrupt
- flush the cache
- Start DMA simple transfer DMA to device
- enbale Sobel INTR interrupt (Optional)
- receive S2MM interrupt, set Done_flag to 1 and disable Sobel INTR interrupt in the S2MM interrupt service routine
- flush the cache

## Resource Utilization

The following table shows the resource utilization of all modules of PL:
![[Pasted image 20220929192510.png]]
resources utilization of Sobel custom IP is given by:
![[Pasted image 20220929192736.png]]

## Test Results

![[Pasted image 20220929184849.png]]
The above figure shows the original and processed edge images.
It takes 837299 ns from the DMA started moving the original image data until all the processed data were written back to the DDR . In comparison, a Sobel operation software implementation without hardware acceleration takes 201225057 ns.

## potential improvement points

The Xilinx VPSS IP is configured to full fledged mode, but actually only the color space conversion function is required. However, in color space conversion only mode, the AXI Lite interface has no clock of its own. This results in lots of unnecessary resource consumption and latency.
Is it possible to replace it with other IPs or custom IP?
![[Pasted image 20220929203550.png]]
![[Pasted image 20220929203609.png]]
