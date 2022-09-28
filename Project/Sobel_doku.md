---
date created: 2022-09-28 10:40
---

## 2 Image Edge Detection

Sobel Edge Detection is used to identify points in a digital image where the brightness changes sharply and discontinues. The  edge detection method reduces the amount of data in an image and preserves the structural properties  for further processing. In a gray level image, the edge is a local feature with in a neighborhood separate regions.The gray level is more or less uniform with in different values on the two sides of the edge. For a  noisy image, it is difficult to detect edges as both edge and noise contains high frequency contents, which\
results in blurred and distorted images.\
Microsemi offers the Image Edge Detection IP that enables designers to use the edge detection for image processing.
The Image Edge Detection IP implements Sobel filter, which is a classical algorithm in the field of image  and video processing for the extraction of object edges. Sobel filter works on the premise of computing  an estimate of the first derivative of an image to extract the edge information. By computing the x and y  direction derivatives of a specific pixel against a neighborhood of surrounding pixels, it is possible to  extract the boundary between two distinct elements in an image. Due to the computational load of calculating derivatives using the squaring and square root operators, fixed coefficient masks are adopted  as a suitable approximation in computing the derivative at a specific point. In the case of Sobel, the  masks used are shown in the following figure.

Figure 1 • Sobel Operator Horizontal and Vertical Kernels

These kernels can be combined together to find the absolute magnitude of the gradient at each point.
The gradient magnitude is computed using:

Typically an approximate magnitude is computed using:

This is much faster to compute. The Sobel operator has the advantage of simplicity in calculation.

## Requirements

Software Tools:

- Vivado ML Edition  2022.1
- Vitis Unified Software Platform 2022.1
- Terminal program (CuteCom)

Hardware Tools:

- ZedBoard (Zynq™ Evaluation and Development

## Resource Utilization

[Documentation Portal](https://docs.xilinx.com/v/u/en-US/xapp890-zynq-sobel-vivado-hls)

![[Pasted image 20220927211645.png]]

## 3 Hardware Implementation

The following figure shows the Image Edge Detection block diagram.

The data is collected from the Line buffer and it is stored in the window[3]. Only 9 values\
are stored in a 3_3 window. It requires 9 clock cycles and one extra cycle to perform the\
computation. Pipelining is used to reduce the clock cycles. When pipelining is used the\
storing of the data in the window can be done in 1 clock cycle. There is a reason for the\
window having matrix size 3_3. Always the middle value of the window is considered to\
perform any computation because the position (1,1) can be compared with any other\
position in the window.

The read submodule generates the read enable signals and the addresses to read from LSRAM. It also
has the 3x3 window logic which reads the 3x3 window from LSRAMs and feeds to the Sobel filter
interpolation block. The pixel at which the edge must be computed is placed at the center of the 3x3
window. Then the window slides right to compute the value of the next pixel in the line.
For the first line of the frame, the first row of the 3x3 window is all zeros, the second row is LSRAM1 data
and third row is LSRAM2 data. For the second line, the first row is LSRAM1 data, second row is LSRAM2
data and third row is LSRAM3 data. For the third line, the first row is LSRAM2 data, second row is
LSRAM3 data and third row is LSRAM1 data and so on.

The Sobel filter performs the Sobel operation (as described in section 2) on the 3x3 window data coming
from Read LSRAM block to produce the edge detected image.

Configuration Parameters

The following figures show the timing diagram of the Image Edge Detection IP.

Simulation
The testbench output image file appears in the Files/simulation folder after the simulation
completes.

This section shows an image before and after being processed using the Image Edge Detection IP.
The following figure shows the input image.

![[Pasted image 20220927211533.png]]

First, the RGB to Grayscale module receives the 32-bit RGB data from the AXI4-Stream interface and converts it approximately to 8-bit grayscale data using shifts, addition, and fixed-value multiplication. In addition, the module has two control signal input ports. The current 32-bit RGB data is considered valid only when both data_ready from the Output_buffer Module and data_valid from AXI-DMA IP are high.

The data output from the RGB to Grayscale module is sequentially written into 4 line buffers. All line buffers are connected to the same data input port, and each line buffer has its own value signal, which marks whether the current input is valid or not. Each line buffer can store up to 1024 8-bit data , which limits the maximum width of the image being processed. Every line buffer can be read and written simultaneously . The control logic ensures that only one write process and only three read processes are valid. It also arranges the output data from line buffers in a specific order so that each valid output is a 3x3 window segmented from the grayscale image.

In the Convolution module, a five-stage pipeline is used to calculate the edge detection value and determine whether the value is greater than the threshold value. If it is greater than the threshold value, 8-bit data 0XFF is output, otherwise 8-bit data 0X00 is output, i.e. the edge is white and the rest is black.