[FPGA 读取SD卡图片数据(top_sd_photo) - 知乎](https://zhuanlan.zhihu.com/p/452203686)
#FPGA
#Tutorial

主函数比较简单，即 先初始化HDMI(配置IIC) ->配置并启动VDMA->从SD卡中读取图片并存入DDR中->VDMA从DDR中读取数据并输出 

WARNING LOG


```
TIMING #1 Critical Warning Invalid clock redefinition on a clock tree. The primary clock design_1_i/clk_wiz_0/inst/clk_in1 is defined downstream of clock clk_fpga_1 and overrides its insertion delay and/or waveform definition
```
solution: clk wiz no buffer (?)

./sobel img.rgb file_out.rgb 512x512 -g file_g.rgb
