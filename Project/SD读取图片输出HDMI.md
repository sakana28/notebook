#Tutorial 

![[Pasted image 20220719094043.png]]

主函数比较简单，即 先初始化HDMI(配置IIC) ->配置并启动VDMA->从SD卡中读取图片并存入DDR中->VDMA从DDR中读取数据并输出
其中初始化HDMI可以在数据手册中查看，以zedboard为例，zedboard中使用了一块ADV7511芯片来控制HDMI接口，因此我们可以直接查看ADV7511手册中的配置要求。

![[Pasted image 20220719102616.png]]