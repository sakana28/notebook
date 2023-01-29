#文档草稿 
1.了解公司的设备管理，密码定期，IT系统，各项制度，zynq book ，Xilinx 官方文档，安装并配置开发环境，
2.熟悉Vivado与Vitis开发环境，了解项目，Confluence 
3.在无硬件的环境下理解SOC的设计流程，完成实验项目，通过AXI-GPIO控制LED灯
4.继续学习嵌入式编程，完成实验项目 在PL实现一个可以通过AXI总线读写寄存器的计数器
5.得到硬件，尝试不同方法的下载，解决开发板两个生产版本带来的BUG，解决Linux下无法识别uart的问题
6.通过SD卡读写BMP图片，图片显示不全。查找资料后 BMP补0 在与领导与同事的交流中注意了C代码的规范书写
7.完全使用内嵌ARM实现Sobel处理，并将处理结果写入SD卡，了解SOBEL的原理及限制运算速度的因素
8.学习AXI DMA 和AXI FIFO IP实现图片的回环处理，实现ARM和PL的通信
9.学习搭建HDMI输出 查找官方文档和事例设计  ![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%2730%27%20height=%2730%27/%3e)![ruoshui chen](https://chat.openai.com/_next/image?url=https%3A%2F%2Flh3.googleusercontent.com%2Fa%2FAEdFTp6--94TU2JbpO_9jFR8aEv9pNhdEmh_eJ47vhY%3Ds96-c&w=64&q=75)

请你根据下面的梗概用德语扩写一段报告，400词以上。在完成PS与PL端大量数据的传输与缓存后，我的下一个任务是学习搭建HDMI输出路径。Zedboard开发板使用了外部编解码器，即ADI公司的ADV7511。 解决问题：版本 按照脚本重新构建系统
色彩偏差→图像是按照RBG的顺序 无输出：时序，提高时钟，位宽匹配
10 SOBEL IP实现，完成大部分并进行简单测试
11 写testbench，写c程序实现预处理bmp txt bmp，封装IP
12构建系统 写软件
13写文档，做PPT
14 学习Zynq运行Linux
15 参与FPGA Cop，展示项目。Petalinux定制系统，实现在Zynq上SD卡读取Linux镜像并通过串口通信，实现在Zynq上挂载SD卡存储区并运行Hello World程序
16完成收尾工作，把文件 文档存放进项目archive，归还设备
