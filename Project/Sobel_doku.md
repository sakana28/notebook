---
date created: 2022-09-26 16:41
---

1. INTRODUCTION

1.1 Overview
For the implementation of image processing algorithms, it is essential for embedded systems to achieve low power and high performance at the same time. The implementation process involves several steps. The initial step of implementing image processing algorithms is software written in
a high-level language like C or C++. Validation and development are much easier in high-level
languages. The ultimate goal is a Hardware Description Language (HDL). However, producing
optimized HDL code from that a high-level software is not easy. For this task there are High-level
Synthesis tools that convert the high-level code into the hardware description language
automatically.
We describe the design and implementation of an image edge detection hardware accelerator. The
target platform is the Zynq-7000 SoC. Here the Sobel image edge detection algorithm is developed
in the Vivado HLS tool and then it is exported to Vivado to use it as an Intellectual Property (IP).
After that the implementation of the generated IP is synthesized and tested on Zynq7000 Zedboard.
Finally an application in the Software Development Kit is created to use this peripheral in order to
apply a Sobel filter in an image which is read from a SD card connected to the board.
The thesis is organized as following. Sobel edge detection is introduced in chapter 2. A brief
description of Vivado HLS, different optimization techniques and libraries is given in chapter 3.
Chapter 4 describes the Zynq-7000 in short. The development of the image processing algorithm
in Vivado HLS and the hardware implementation on the Zynq platform, and performance
comparison are shown in chapter 5.

1.2 Advantages of the Developed Implementation
Zynq-7000 SoC, on a single chip, is a combination of FPGA fabric in a Programmable Logic
domain and dual-core ARM Cortex-A9 CPUs with a rich set of standard I/O peripherals and a
multi-ported memory controller in an SoC Processing System domain. Over 2,000 interconnects
interface the Processing System to the Programmable Logic. This provides the high-performance,
low-latency communication, extension, flexibility, and capability between processing and
programmable logic that other systems connecting discrete processor-based devices to FPGAs
through printed circuit boards cannot achieve.
We implement the Sobel filter as a HLS Kernel. This is more efficient than a straightforward
implementation like implementation using general processors. We create a unique HLS kernel
using very limited resources. For example we use only 1173 Flip Flops from 106400 available Flip
Flops. This helps to execute the operation very fast. HLS provides a technique for migrating
algorithms into the FPGA logic from a processor. Therefore, it helps moving code from the Cortex
ARM A9 processor to the FPGA logic.
There are two more reasons for fast operation. We add the right amount of pragmas and techniques
in order to achieve better performance both in memory transactions and computations. A pragma
is a technique that helps speed up the code. Block RAM is used to store and process the input data
and then write it back to the DDR. To transfer data with bursts we use the ‘memcpy’ com1.4.2 Sobel Edge Detection
Sobel Edge Detection is a technique based on two kernels, one kernel detects the horizontal edges
and the other kernel recognizes the vertical edges. Each kernel has the effect of calculating the
gradient in both a horizontal and a vertical direction. The image is read initially after start i.e. the
pixel values are read. The image is then convolved with the filter. After that horizontal and vertical
kernels of the operator are convolved with the original image [5].mand for
the transactions.
In the following sections we will introduce image processing, edge detection, Zedboard and related
previous work.

1.4.2 Sobel Edge Detection
Sobel Edge Detection is a technique based on two kernels, one kernel detects the horizontal edges
and the other kernel recognizes the vertical edges. Each kernel has the effect of calculating the
gradient in both a horizontal and a vertical direction. The image is read initially after start i.e. the
pixel values are read. The image is then convolved with the filter. After that horizontal and vertical
kernels of the operator are convolved with the original image [5].