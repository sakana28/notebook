
#Guideline
![[Pasted image 20220720101041.png]]
![[Pasted image 20220720101118.png]]-   硬件工程师负责设计软件开发（从 Vivado® Design Suite 到 XSA 存档文件）所需的逻辑和导出信息。

- 软件开发者负责通过创建平台来将 XSA 导入 Vitis 软件平台。平台主要供应用加速工程使用。为了给各种应用提供统一的 Vitis 工作空间架构，软件开发工程现在已移植到平台和应用架构。平台包含硬件规格和软件环境设置。
- 软件环境设置称为域，同样属于平台的一部分。
- 软件开发者基于平台和域来创建应用。
- 应用可在 Vitis IDE 中进行调试。
- 在复杂系统中，可能有多个应用同时运行并彼此通信。因此也需要执行系统级别验证。
- 全部就绪后，Vitis IDE 即可帮助创建启动镜像，用于初始化系统和启动应用。
XSA

XSA 是从 Vivado Design Suite 导出的。它包含各种硬件规格，例如，处理器配置属性、外设连接信息、地址映射和器件初始化代码等。创建平台工程时，必须提供 XSA。

系统工程

系统工程用于将任一器件上同时运行的应用组合在一起。在系统工程中，同一个处理器的两个独立应用不能组合在一起。

域

域即板级支持包 (BSP) 或操作系统 (OS)，其中包含软件驱动程序集合，您可在其中构建自己的应用。创建的软件镜像仅包含赛灵思库中的部分内容，即您在自己的嵌入式设计中使用的部分。您可创建多个应用并在同一个域上运行。在平台中，每个域都绑定到单个处理器或者一个由同构处理器组成的集群（例如：A53_0 或 A53）。

![[Pasted image 20220720101447.png]]

学习路径  
1. 逻辑设计和开发
2. 基于ARM的逻辑程序开发和设计 （与MCU类似，根据时序编写外设驱动）
3. 基于嵌入式Linux OS的操作系统的应用和驱动开发
## 小梅哥 教程
DDR 16位数据线位宽32 因为板上使用了两片,地址 和控制都和zynq链接，数据线独立

ps7 process system 7 
base addr 外设的地址段
application system
hallo world 工程基于串口

开发
.bit 是system wrapper

### 重点问题
BD文件中如何确定IP及配置
如何修改配置IP的参数 
如何确定头文件
使用哪些文件实现功能
如何编写程序实现功能

1. 什么是bsp
2. 如何实现对指定地址的读写
3. 如何得知各个外设中的硬件信息 reg地址和位功能
4. 如何实现延时
5. 如何使用跨平台可移植的数据类型

BSP中有很多安全判断和兼容性操作，性能和程序尺寸要求不大时直接用。有要求时自己读写寄存器3

z.b Xil_out32 中 *LocalAddr = Value CPU 编程本质是为特定地址读写特定数值
xil io.h

Register summary中的地址都是偏移地址，要加上模块的BASE ADDR

unistd.h 包含高精度延时函数的头文件 usleep以微秒为单位


跨平台可移植  stdint.h
u32定义在xil types 跨平台后不通用 建议uint8_t等等

Error while launching program: 
Cannot reset APU. AP transaction error, DAP status 0xF0000021
Cannot reset APU. AP transaction error, DAP status 0xF0000021

Error while launching program:  Memory write error at 0x100000. APB AP transaction error, DAP status 0xF0000021 Memory write error at 0x100000. APB AP transaction error, DAP status 0xF0000021

xsct% XSDB Server URL: TCP:localhost:44353
xsct% XSDB Server Channel: tcfchan#0
INFO: [Hsi 55-2053] elapsed time for repository (/tools/Xilinx/Vitis/2022.1/data/embeddedsw) loading 0 seconds
attempting to launch hw_server

****** Xilinx hw_server v2022.1.0
  **** Build date : Apr 10 2022 at 06:24:21
    ** Copyright 1986-2022 Xilinx, Inc. All Rights Reserved.

INFO: hw_server application started
INFO: Use Ctrl-C to exit hw_server application

INFO: To connect to this hw_server instance use url: TCP:127.0.0.1:3121

Info: ARM Cortex-A9 MPCore #0 (target 2) Stopped at 0x0 (Vector Catch)
xsct% Info: ARM Cortex-A9 MPCore #1 (target 3) Stopped at 0x0 (Vector Catch)
xsct% Info: ARM Cortex-A9 MPCore #0 (target 2) Running
xsct% Info: ARM Cortex-A9 MPCore #1 (target 3) Running
xsct% 
initializing

initializing
  0%    0MB   0.0MB/s  ??:?? ETA
 27%    1MB   2.1MB/s  ??:?? ETA
 49%    1MB   1.8MB/s  ??:?? ETA
 75%    2MB   1.7MB/s  ??:?? ETA
100%    3MB   1.8MB/s  00:02    

Downloading Program -- /home/benchmarker/vivado_bsp/helloworld_sw/helloworld/Debug/helloworld.elf
	section, .text: 0x00100000 - 0x001009fb
	section, .init: 0x001009fc - 0x00100a07
	section, .fini: 0x00100a08 - 0x00100a13
	section, .rodata: 0x00100a14 - 0x00100a9b
	section, .data: 0x00100aa0 - 0x00100f0f
	section, .eh_frame: 0x00100f10 - 0x00100f13
	section, .mmu_tbl: 0x00104000 - 0x00107fff
	section, .init_array: 0x00108000 - 0x00108003
	section, .fini_array: 0x00108004 - 0x00108007
	section, .bss: 0x00108008 - 0x0010802f
	section, .heap: 0x00108030 - 0x0010a02f
	section, .stack: 0x0010a030 - 0x0010d82f

  0%    0MB   0.0MB/s  ??:?? ETA
aborting, 2 pending requests... 
aborting, 1 pending requests... 
Failed to download /home/benchmarker/vivado_bsp/helloworld_sw/helloworld/Debug/helloworld.elf
Info: ARM Cortex-A9 MPCore #0 (target 2) Running (APB AP transaction error, DAP status 0xF0000021)
xsct% 
initializing
  0%    0MB   0.0MB/s  ??:?? ETA
 27%    1MB   1.9MB/s  ??:?? ETA
 50%    1MB   1.8MB/s  ??:?? ETA
 73%    2MB   1.8MB/s  ??:?? ETA
 95%    3MB   1.7MB/s  ??:?? ETA
100%    3MB   1.8MB/s  00:02    

Downloading Program -- /home/benchmarker/vivado_bsp/helloworld_sw/helloworld/Debug/helloworld.elf
	section, .text: 0x00100000 - 0x001009fb
	section, .init: 0x001009fc - 0x00100a07
	section, .fini: 0x00100a08 - 0x00100a13
	section, .rodata: 0x00100a14 - 0x00100a9b
	section, .data: 0x00100aa0 - 0x00100f0f
	section, .eh_frame: 0x00100f10 - 0x00100f13
	section, .mmu_tbl: 0x00104000 - 0x00107fff
	section, .init_array: 0x00108000 - 0x00108003
	section, .fini_array: 0x00108004 - 0x00108007
	section, .bss: 0x00108008 - 0x0010802f
	section, .heap: 0x00108030 - 0x0010a02f
	section, .stack: 0x0010a030 - 0x0010d82f

  0%    0MB   0.0MB/s  ??:?? ETA
aborting, 2 pending requests... 
aborting, 1 pending requests... 
Failed to download /home/benchmarker/vivado_bsp/helloworld_sw/helloworld/Debug/helloworld.elf
Info: ARM Cortex-A9 MPCore #0 (target 2) Running (APB AP transaction error, DAP status 0xF0000021)
xsct% 
initializing
  0%    0MB   0.0MB/s  ??:?? ETA
 25%    1MB   1.9MB/s  ??:?? ETA
 50%    1MB   1.9MB/s  ??:?? ETA
 70%    2MB   1.7MB/s  ??:?? ETA
 95%    3MB   1.8MB/s  ??:?? ETA
100%    3MB   1.8MB/s  00:02    

Downloading Program -- /home/benchmarker/vivado_bsp/helloworld_sw/helloworld/Debug/helloworld.elf
	section, .text: 0x00100000 - 0x001009fb
	section, .init: 0x001009fc - 0x00100a07
	section, .fini: 0x00100a08 - 0x00100a13
	section, .rodata: 0x00100a14 - 0x00100a9b
	section, .data: 0x00100aa0 - 0x00100f0f
	section, .eh_frame: 0x00100f10 - 0x00100f13
	section, .mmu_tbl: 0x00104000 - 0x00107fff
	section, .init_array: 0x00108000 - 0x00108003
	section, .fini_array: 0x00108004 - 0x00108007
	section, .bss: 0x00108008 - 0x0010802f
	section, .heap: 0x00108030 - 0x0010a02f
	section, .stack: 0x0010a030 - 0x0010d82f

  0%    0MB   0.0MB/s  ??:?? ETA
aborting, 2 pending requests... 
aborting, 1 pending requests... 
Failed to download /home/benchmarker/vivado_bsp/helloworld_sw/helloworld/Debug/helloworld.elf
Info: ARM Cortex-A9 MPCore #0 (target 2) Running (APB AP transaction error, DAP status 0xF0000021)
xsct% 
initializing
  0%    0MB   0.0MB/s  ??:?? ETA
 26%    1MB   2.0MB/s  ??:?? ETA
 50%    1MB   1.9MB/s  ??:?? ETA
 72%    2MB   1.8MB/s  ??:?? ETA
 95%    3MB   1.8MB/s  ??:?? ETA
100%    3MB   1.8MB/s  00:02    

Downloading Program -- /home/benchmarker/vivado_bsp/helloworld_sw/helloworld/Debug/helloworld.elf
	section, .text: 0x00100000 - 0x001009fb
	section, .init: 0x001009fc - 0x00100a07
	section, .fini: 0x00100a08 - 0x00100a13
	section, .rodata: 0x00100a14 - 0x00100a9b
	section, .data: 0x00100aa0 - 0x00100f0f
	section, .eh_frame: 0x00100f10 - 0x00100f13
	section, .mmu_tbl: 0x00104000 - 0x00107fff
	section, .init_array: 0x00108000 - 0x00108003
	section, .fini_array: 0x00108004 - 0x00108007
	section, .bss: 0x00108008 - 0x0010802f
	section, .heap: 0x00108030 - 0x0010a02f
	section, .stack: 0x0010a030 - 0x0010d82f

  0%    0MB   0.0MB/s  ??:?? ETA
aborting, 2 pending requests... 
aborting, 1 pending requests... 
Failed to download /home/benchmarker/vivado_bsp/helloworld_sw/helloworld/Debug/helloworld.elf
Info: ARM Cortex-A9 MPCore #0 (target 2) Running (APB AP transaction error, DAP status 0xF0000021)
xsct% 
