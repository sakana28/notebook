#vitis
# xintc.h xscugic.h 差别

**Q:**
	When I read the code in xaxicdma_example_simple_intr.c, I saw two interrupt controllers, generic interrupt controller and xilinx interrupt controller, whose drivers defined in xscugic.h and xintc.h. 
	What is the difference? When should I use one over the other?

**A:**
	Xilinx interrupt controller is the PL based interrupt controller IP Xilinx made. [[Generic interrupt controlle]]r is the one built into the ARM SoC side.


举例 AXI stream FIFO 中，Intr要提交给ARM，使ARM停下目前任务开始服务程序，因此使用 xscugic.h 