[FPGA 读取SD卡图片数据(top_sd_photo) - 知乎](https://zhuanlan.zhihu.com/p/452203686)
#FPGA
#Tutorial

主函数比较简单，即 先初始化HDMI(配置IIC) ->配置并启动VDMA->从SD卡中读取图片并存入DDR中->VDMA从DDR中读取数据并输出 