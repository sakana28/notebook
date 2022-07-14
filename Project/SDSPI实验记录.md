---
date created: 2022-07-12 16:25
---
#SD 
来自正点FPGA教程

[【正点原子达芬奇之FPGA开发指南 】第四十一章SD卡读写测试实验 - 知乎](https://zhuanlan.zhihu.com/p/389971282)
[FPGA SD卡读写实验(SPI模式)](http://www.4k8k.xyz/article/qq_39507748/113306920)

## 实验内容

使用FPGA开发板向SD卡指定的扇区地址中写入512个字节的数据，写完后将数据读出，并验证数据是否正确。

## 程序设计

SD卡初始化、写操作以及读操作是相互独立且不能同时进行的，因此我们可以将SD卡的初始化、写操作以及读操作分别划分为三个独立的模块，最后将这三个模块例化在SD卡的控制器模块中，便于在其它工程项目中使用。图 39.4.1是本章实验的系统框图，PLL时钟模块（PLL）为各个模块提供驱动时钟，SD卡测试数据产生模块产生测试数据写入SD卡，写完后从SD卡中读出数据，最终读写测试结果由LED显示模块通过控制LED灯的显示状态来指示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/20210128083123361.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM5NTA3NzQ4,size_16,color_FFFFFF,t_70)

## Architecture

![[Pasted image 20220712162503.png]]由上图可知，SD卡测试数据产生模块产生的开始写入信号（wr_start_en）及数据（wr_data）连接至SD卡控制器模块，数据写完后输出开始读出信号（rd_start_en）即可从SD卡控制器中读出数据（rd_data），数据测试的结果error_flag连接至LED显示模块，完成各模块之间的数据交互。

FPGA顶层模块（top_sd_rw）例化了以下四个模块：PLL时钟模块（pll_clk）、SD卡测试数据产生模块（data_gen）、SD卡控制器模块（sd_ctrl_top）和LED显示模块（led_alarm）。

顶层模块（top_sd_rw）：顶层模块完成了对其它四个模块的例化，SD卡测试数据产生模块产生的开始写入信号及数据连接至SD卡控制器模块，数据写完后从SD卡控制器中读出数据，并验证数据的正确性，将验证的结果连接至LED显示模块。

PLL时钟模块（pll_clk）：PLL时钟模块通过调用锁相环（PLL）IP核来实现，总共输出两个时钟，频率都是50Mhz，但两个时钟相位相差180度。我们知道，SD卡的SPI通信模式为CPOL=1，CPHA=1；即SPI_CLK在空闲时为高电平，数据发送是在时钟的第一个边沿，也就是SPI_CLK由高电平到低电平的跳变，所以数据采集是在上升沿，数据发送是在下降沿。为了在程序代码中统 一使用上升沿，我们使用两个相位相差180度的时钟来对SD卡进行操作。

SD卡测试数据产生模块（data_gen）：SD卡测试数据产生模块产生的开始写入信号和数据写入SD卡控制器模块中，数据写完后从SD卡控制器中读出数据，并验证数据的正确性，将验证的结果发送给LED显示模块。

SD卡控制器模块（sd_ctrl_top）：SD卡控制器模块例化了SD卡初始化模块（sd_init）、SD卡写数据模块（sd_write）和SD卡读数据模块（sd_read）。SD卡初始化模块完成对SD卡的上电初始化操作；SD卡写数据模块完成对SD卡的写操作；SD卡读数据模块完成对SD卡的读操作。由于这三个模块都操作了SD卡的引脚信号，且这三个模块在同一时间内不会同时操作，所以此模块实现了对其它三个模块的例化以及选择SD卡的引脚连接至其中某一个模块。

LED显示模块（led_alarm）：LED显示模块将SD卡测试数据产生模块输出的验证结果值，通过控制LED灯的显示状态来指示。

顶层模块的代码如下：

```verilog

module top_sd_rw(
    input               sys_clk     ,  //系统时钟
    input               sys_rst_n   ,  //系统复位，低电平有效
    
    //SD卡接口
    input               sd_miso     ,  //SD卡SPI串行输入数据信号
    output              sd_clk      ,  //SD卡SPI时钟信号
    output              sd_cs       ,  //SD卡SPI片选信号
    output              sd_mosi     ,  //SD卡SPI串行输出数据信号
    //LED
    output      [3:0]   led            //LED灯
    );

//wire define
wire             clk_ref        ;
wire             clk_ref_180deg ;
wire             rst_n          ;
wire             locked         ;

wire             wr_start_en    ;      //开始写SD卡数据信号
wire     [31:0]  wr_sec_addr    ;      //写数据扇区地址    
wire     [15:0]  wr_data        ;      //写数据            
wire             rd_start_en    ;      //开始写SD卡数据信号
wire     [31:0]  rd_sec_addr    ;      //读数据扇区地址    
wire             error_flag     ;      //SD卡读写错误的标志

wire             wr_busy        ;      //写数据忙信号
wire             wr_req         ;      //写数据请求信号
wire             rd_busy        ;      //读忙信号
wire             rd_val_en      ;      //数据读取有效使能信号
wire     [15:0]  rd_val_data    ;      //读数据
wire             sd_init_done   ;      //SD卡初始化完成信号

//*****************************************************
//**                    main code
//*****************************************************

assign  rst_n = sys_rst_n & locked;

//锁相环
pll_clk u_pll_clk(
    .areset       (1'b0         ),
    .inclk0       (sys_clk      ),
    .c0           (clk_ref       ),
    .c1           (clk_ref_180deg),
    .locked       (locked       )
    );

//产生SD卡测试数据  
data_gen u_data_gen(
    .clk             (clk_ref),
    .rst_n           (rst_n),
    .sd_init_done    (sd_init_done),
    .wr_busy         (wr_busy),
    .wr_req          (wr_req),
    .wr_start_en     (wr_start_en),
    .wr_sec_addr     (wr_sec_addr),
    .wr_data         (wr_data),
    .rd_val_en       (rd_val_en),
    .rd_val_data     (rd_val_data),
    .rd_start_en     (rd_start_en),
    .rd_sec_addr     (rd_sec_addr),
    .error_flag      (error_flag)
    );     

//SD卡顶层控制模块
sd_ctrl_top u_sd_ctrl_top(
    .clk_ref           (clk_ref),
    .clk_ref_180deg    (clk_ref_180deg),
    .rst_n             (rst_n),
    //SD卡接口
    .sd_miso           (sd_miso),
    .sd_clk            (sd_clk),
    .sd_cs             (sd_cs),
    .sd_mosi           (sd_mosi),
    //用户写SD卡接口
    .wr_start_en       (wr_start_en),
    .wr_sec_addr       (wr_sec_addr),
    .wr_data           (wr_data),
    .wr_busy           (wr_busy),
    .wr_req            (wr_req),
    //用户读SD卡接口
    .rd_start_en       (rd_start_en),
    .rd_sec_addr       (rd_sec_addr),
    .rd_busy           (rd_busy),
    .rd_val_en         (rd_val_en),
    .rd_val_data       (rd_val_data),    
    
    .sd_init_done      (sd_init_done)
    );

//led警示 
led_alarm #(
    .L_TIME      (25'd25_000_000)
    )  
   u_led_alarm(
    .clk            (clk_ref),
    .rst_n          (rst_n),
    .led            (led),
    .error_flag     (error_flag)
    );    

endmodule

```
SD卡控制器模块输出的sd_init_done（SD卡初始化完成信号）连接至SD卡测试数据产生模块，只有在SD卡初始化完成之后（sd_init_done为高电平），才能对SD卡进行读写测试。SD卡控制器模块将SD卡的初始化以及读写操作封装成方便用户调用的接口，SD卡测试数据产生模块只需对SD卡控制器模块的用户接口进行操作即可完成对SD卡的读写操作。

在代码的第94行定义了一个参数（L_TIME），用于在读写测试错误时控制LED闪烁的时间， 其单位是1个时钟周期。因为输入的时钟频率为50Mhz，周期为20ns，所以20 * 25’d25_000_000 = 500ms，因此LED灯在读写错误时每500ms闪烁一次。

SD卡控制器模块的代码如下：

```verilog

module sd_ctrl_top(
    input                clk_ref       ,  //时钟信号
    input                clk_ref_180deg,  //时钟信号,与clk_ref相位相差180度
    input                rst_n         ,  //复位信号,低电平有效
    //SD卡接口
    input                sd_miso       ,  //SD卡SPI串行输入数据信号
    output               sd_clk        ,  //SD卡SPI时钟信号    
    output  reg          sd_cs         ,  //SD卡SPI片选信号
    output  reg          sd_mosi       ,  //SD卡SPI串行输出数据信号
    //用户写SD卡接口
    input                wr_start_en   ,  //开始写SD卡数据信号
    input        [31:0]  wr_sec_addr   ,  //写数据扇区地址
    input        [15:0]  wr_data       ,  //写数据                  
    output               wr_busy       ,  //写数据忙信号
    output               wr_req        ,  //写数据请求信号    
    //用户读SD卡接口
    input                rd_start_en   ,  //开始读SD卡数据信号
    input        [31:0]  rd_sec_addr   ,  //读数据扇区地址
    output               rd_busy       ,  //读数据忙信号
    output               rd_val_en     ,  //读数据有效信号
    output       [15:0]  rd_val_data   ,  //读数据    
    
    output               sd_init_done     //SD卡初始化完成信号
    );

//wire define
wire                init_sd_clk   ;       //初始化SD卡时的低速时钟
wire                init_sd_cs    ;       //初始化模块SD片选信号
wire                init_sd_mosi  ;       //初始化模块SD数据输出信号
wire                wr_sd_cs      ;       //写数据模块SD片选信号     
wire                wr_sd_mosi    ;       //写数据模块SD数据输出信号 
wire                rd_sd_cs      ;       //读数据模块SD片选信号     
wire                rd_sd_mosi    ;       //读数据模块SD数据输出信号 

//*****************************************************
//**                    main code
//*****************************************************

//SD卡的SPI_CLK  
assign  sd_clk = (sd_init_done==1'b0)  ?  init_sd_clk  :  clk_ref_180deg;

//SD卡接口信号选择
always @(*) begin
    //SD卡初始化完成之前,端口信号和初始化模块信号相连
    if(sd_init_done == 1'b0) begin     
        sd_cs = init_sd_cs;
        sd_mosi = init_sd_mosi;
    end    
    else if(wr_busy) begin
        sd_cs = wr_sd_cs;
        sd_mosi = wr_sd_mosi;   
    end    
    else if(rd_busy) begin
        sd_cs = rd_sd_cs;
        sd_mosi = rd_sd_mosi;       
    end    
    else begin
        sd_cs = 1'b1;
        sd_mosi = 1'b1;
    end    
end    

//SD卡初始化
sd_init u_sd_init(
    .clk_ref            (clk_ref),
    .rst_n              (rst_n),
    
    .sd_miso            (sd_miso),
    .sd_clk             (init_sd_clk),
    .sd_cs              (init_sd_cs),
    .sd_mosi            (init_sd_mosi),
    
    .sd_init_done       (sd_init_done)
    );

//SD卡写数据
sd_write u_sd_write(
    .clk_ref            (clk_ref),
    .clk_ref_180deg     (clk_ref_180deg),
    .rst_n              (rst_n),
    
    .sd_miso            (sd_miso),
    .sd_cs              (wr_sd_cs),
    .sd_mosi            (wr_sd_mosi),
    //SD卡初始化完成之后响应写操作    
    .wr_start_en        (wr_start_en & sd_init_done),  
    .wr_sec_addr        (wr_sec_addr),
    .wr_data            (wr_data),
    .wr_busy            (wr_busy),
    .wr_req             (wr_req)
    );

//SD卡读数据
sd_read u_sd_read(
    .clk_ref            (clk_ref),
    .clk_ref_180deg     (clk_ref_180deg),
    .rst_n              (rst_n),
    
    .sd_miso            (sd_miso),
    .sd_cs              (rd_sd_cs),
    .sd_mosi            (rd_sd_mosi),    
    //SD卡初始化完成之后响应读操作
    .rd_start_en        (rd_start_en & sd_init_done),  
    .rd_sec_addr        (rd_sec_addr),
    .rd_busy            (rd_busy),
    .rd_val_en          (rd_val_en),
    .rd_val_data        (rd_val_data)
    );

endmodule

```
SD卡控制器模块例化了SD卡初始化模块（sd_init）、SD卡写数据模块（sd_write）和SD卡读数据模块（sd_read）。由于这三个模块都驱动着SD卡的引脚，因此在代码的第42行开始的always块中，用于选择哪一个模块连接至SD卡的引脚。在代码的第40行，init_sd_clk用于初始化SD卡时提供较慢的时钟，在SD卡初始化完成之后，再将较快的时钟clk_ref_180deg赋值给sd_clk。sd_clk从上电之后，是一直都有时钟的，而我们在前面说过SPI_CLK的时钟在空闲时为高电平或者低电平。事实上，为了简化设计，sd_clk在空闲时提供时钟也是可以的，其是否有效主要由片选信号来控制。

在这里主要介绍下SD卡控制器模块的使用方法。当外部需要对SD卡进行读写操作时，首先要判断sd_init_done（SD卡初始化完成）信号，该信号拉高之后才能对SD卡进行读写操作；在对SD卡进行写操作时，只需给出wr_start_en（开始写SD卡数据信号）和wr_sec_addr（写数据扇区地址），此时SD卡控制器模块会拉高wr_busy信号，开始对SD卡发起写入命令；在命令发起成功后SD卡控制器模块会输出wr_req（写数据请求）信号，此时我们给出wr_data（写数据）即可将数据写入SD卡中；待所有数据写入完成后，wr_busy信号拉低，即可再次发起读写操作。SD卡的读操作是给出rd_start_en（rd_start_en）和rd_sec_addr（读数据扇区地址），此时SD卡控制器会拉高rd_busy（读数据忙）信号，开始对SD卡发起读出命令；在命令发起成功后SD卡控制器模块会输出rd_val_en（读数据有效）信号和rd_val_data（读数据），待所有数据读完之后，拉低rd_busy信号。需要注意的是，SD卡单次写入和读出的数据量为512个字节，因 为接口封装为16位数据，所以单次读写操作会有256个16位数据。

SD卡初始化模块完成对SD卡的上电初始化操作，我们在SD卡的简介部分已经详细的介绍了SD卡的初始化流程，我们只需要按照SD卡的初始化步骤即可完成SD卡的初始化。由SD卡的初始化流程可知，其步骤非常适合状态机编写，其状态跳转图如图 39.4.3所示。

![[Pasted image 20220712162850.png]]

由上图可知，我们把SD卡初始化过程定义为7个状态，分别为st_idle（初始状态）、st_send_cmd0（发送软件复位命令）、st_wait_cmd0（等待SD卡响应）、st_send_cmd8（发送CMD8命令）、st_send_cmd55（发送CMD55命令）、st_send_acmd41（发送ACMD41命令）以及st_init_done（SD卡初始化完成）。因为SD卡的初始化只需要上电后执行一次，所以在初始化完成之后，状态机一直处于st_init_done状态。

SD卡初始化模块的代码如下所示：

```verilog

module sd_init(
    input          clk_ref       ,  //时钟信号
    input          rst_n         ,  //复位信号,低电平有效
    
    input          sd_miso       ,  //SD卡SPI串行输入数据信号
    output         sd_clk        ,  //SD卡SPI时钟信号
    output  reg    sd_cs         ,  //SD卡SPI片选信号
    output  reg    sd_mosi       ,  //SD卡SPI串行输出数据信号
    output  reg    sd_init_done     //SD卡初始化完成信号
    );

//parameter define
//SD卡软件复位命令,由于命令号及参数为固定值,CRC也为固定值,CRC = 8'h95
parameter  CMD0  = {
    8'h40,8'h00,8'h00,8'h00,8'h00,8'h95};
//接口状态命令,发送主设备的电压范围,用于区分SD卡版本,只有2.0及以后的卡才支持CMD8命令
//MMC卡及V1.x的卡,不支持此命令,由于命令号及参数为固定值,CRC也为固定值,CRC = 8'h87
parameter  CMD8  = {
    8'h48,8'h00,8'h00,8'h01,8'haa,8'h87};
//告诉SD卡接下来的命令是应用相关命令，而非标准命令, 不需要CRC
parameter  CMD55 = {
    8'h77,8'h00,8'h00,8'h00,8'h00,8'hff};  
//发送操作寄存器(OCR)内容, 不需要CRC
parameter  ACMD41= {
    8'h69,8'h40,8'h00,8'h00,8'h00,8'hff};
//时钟分频系数,初始化SD卡时降低SD卡的时钟频率,50M/250K = 200 
parameter  DIV_FREQ = 200;
//上电至少等待74个同步时钟周期,在等待上电稳定期间,sd_cs = 1,sd_mosi = 1
parameter  POWER_ON_NUM = 5000;
//发送软件复位命令时等待SD卡返回的最大时间,T = 100ms; 100_000us/4us = 25000
//当超时计数器等于此值时,认为SD卡响应超时,重新发送软件复位命令
parameter  OVER_TIME_NUM = 25000;
                        
parameter  st_idle        = 7'b000_0001;  //默认状态,上电等待SD卡稳定
parameter  st_send_cmd0   = 7'b000_0010;  //发送软件复位命令
parameter  st_wait_cmd0   = 7'b000_0100;  //等待SD卡响应
parameter  st_send_cmd8   = 7'b000_1000;  //发送主设备的电压范围，检测SD卡是否满足
parameter  st_send_cmd55  = 7'b001_0000;  //告诉SD卡接下来的命令是应用相关命令
parameter  st_send_acmd41 = 7'b010_0000;  //发送操作寄存器(OCR)内容
parameter  st_init_done   = 7'b100_0000;  //SD卡初始化完成

//reg define
reg    [7:0]   cur_state      ;
reg    [7:0]   next_state     ; 
                              
reg    [7:0]   div_cnt        ;    //分频计数器
reg            div_clk        ;    //分频后的时钟         
reg    [12:0]  poweron_cnt    ;    //上电等待稳定计数器
reg            res_en         ;    //接收SD卡返回数据有效信号
reg    [47:0]  res_data       ;    //接收SD卡返回数据
reg            res_flag       ;    //开始接收返回数据的标志
reg    [5:0]   res_bit_cnt    ;    //接收位数据计数器
                                   
reg    [5:0]   cmd_bit_cnt    ;    //发送指令位计数器
reg   [15:0]   over_time_cnt  ;    //超时计数器  
reg            over_time_en   ;    //超时使能信号 
                                   
wire           div_clk_180deg ;    //时钟相位和div_clk相差180度

//*****************************************************
//**                    main code
//*****************************************************

assign  sd_clk = ~div_clk;         //SD_CLK
assign  div_clk_180deg = ~div_clk; //相位和DIV_CLK相差180度的时钟

//时钟分频,div_clk = 250KHz
always @(posedge clk_ref or negedge rst_n) begin
    if(!rst_n) begin
        div_clk <= 1'b0;
        div_cnt <= 8'd0;
    end
    else begin
        if(div_cnt == DIV_FREQ/2-1'b1) begin
            div_clk <= ~div_clk;
            div_cnt <= 8'd0;
        end
        else    
            div_cnt <= div_cnt + 1'b1;
    end        
end

//上电等待稳定计数器
always @(posedge div_clk or negedge rst_n) begin
    if(!rst_n) 
        poweron_cnt <= 13'd0;
    else if(cur_state == st_idle) begin
        if(poweron_cnt < POWER_ON_NUM)
            poweron_cnt <= poweron_cnt + 1'b1;                   
    end
    else
        poweron_cnt <= 13'd0;    
end    

//接收sd卡返回的响应数据
//在div_clk_180deg(sd_clk)的上升沿锁存数据
always @(posedge div_clk_180deg or negedge rst_n) begin
    if(!rst_n) begin
        res_en <= 1'b0;
        res_data <= 48'd0;
        res_flag <= 1'b0;
        res_bit_cnt <= 6'd0;
    end    
    else begin
        //sd_miso = 0 开始接收响应数据
        if(sd_miso == 1'b0 && res_flag == 1'b0) begin 
            res_flag <= 1'b1;
            res_data <=
             {res_data[46:0],sd_miso};
            res_bit_cnt <= res_bit_cnt + 6'd1;
            res_en <= 1'b0;
        end    
        else if(res_flag) begin
            //R1返回1个字节,R3 R7返回5个字节
            //在这里统一按照6个字节来接收,多出的1个字节为NOP(8个时钟周期的延时)
            res_data <= {
    res_data[46:0],sd_miso};     
            res_bit_cnt <= res_bit_cnt + 6'd1;
            if(res_bit_cnt == 6'd47) begin
                res_flag <= 1'b0;
                res_bit_cnt <= 6'd0;
                res_en <= 1'b1; 
            end                
        end  
        else
            res_en <= 1'b0;         
    end
end                    

always @(posedge div_clk or negedge rst_n) begin
    if(!rst_n)
        cur_state <= st_idle;
    else
        cur_state <= next_state;
end

always @(*) begin
    next_state = st_idle;
    case(cur_state)
        st_idle : begin
            //上电至少等待74个同步时钟周期
            if(poweron_cnt == POWER_ON_NUM)          //默认状态,上电等待SD卡稳定
                next_state = st_send_cmd0;
            else
                next_state = st_idle;
        end 
        st_send_cmd0 : begin                         //发送软件复位命令
            if(cmd_bit_cnt == 6'd47)
                next_state = st_wait_cmd0;
            else
                next_state = st_send_cmd0;    
        end               
        st_wait_cmd0 : begin                         //等待SD卡响应
            if(res_en) begin                         //SD卡返回响应信号
                if(res_data[47:40] == 8'h01)         //SD卡返回复位成功
                    next_state = st_send_cmd8;
                else
                    next_state = st_idle;
            end
            else if(over_time_en)                    //SD卡响应超时
                next_state = st_idle;
            else
                next_state = st_wait_cmd0;                                    
        end    
        //发送主设备的电压范围,检测SD卡是否满足
        st_send_cmd8 : begin 
            if(res_en) begin                         //SD卡返回响应信号  
                //返回SD卡的操作电压,[19:16] = 4'b0001(2.7V~3.6V)
                if(res_data[19:16] == 4'b0001)       
                    next_state = st_send_cmd55;
                else
                    next_state = st_idle;
            end
            else
                next_state = st_send_cmd8;            
        end
        //告诉SD卡接下来的命令是应用相关命令
        st_send_cmd55 : begin     
            if(res_en) begin                         //SD卡返回响应信号  
                if(res_data[47:40] == 8'h01)         //SD卡返回空闲状态
                    next_state = st_send_acmd41;
                else
                    next_state = st_send_cmd55;    
            end        
            else
                next_state = st_send_cmd55;     
        end  
        st_send_acmd41 : begin                       //发送操作寄存器(OCR)内容
            if(res_en) begin                         //SD卡返回响应信号  
                if(res_data[47:40] == 8'h00)         //初始化完成信号
                    next_state = st_init_done;
                else
                    next_state = st_send_cmd55;      //初始化未完成,重新发起 
            end
            else
                next_state = st_send_acmd41;     
        end                
        st_init_done : next_state = st_init_done;    //初始化完成 
        default : next_state = st_idle;
    endcase
end

//SD卡在div_clk_180deg(sd_clk)的上升沿锁存数据,因此在sd_clk的下降沿输出数据
//为了统一在alway块中使用上升沿触发,此处使用和sd_clk相位相差180度的时钟
always @(posedge div_clk or negedge rst_n) begin
    if(!rst_n) begin
        sd_cs <= 1'b1;
        sd_mosi <= 1'b1;
        sd_init_done <= 1'b0;
        cmd_bit_cnt <= 6'd0;
        over_time_cnt <= 16'd0;
        over_time_en <= 1'b0;
    end
    else begin
        over_time_en <= 1'b0;
        case(cur_state)
            st_idle : begin                               //默认状态,上电等待SD卡稳定
                sd_cs <= 1'b1;                            //在等待上电稳定期间,sd_cs=1
                sd_mosi <= 1'b1;                          //sd_mosi=1
            end     
            st_send_cmd0 : begin                          //发送CMD0软件复位命令
                cmd_bit_cnt <= cmd_bit_cnt + 6'd1;        
                sd_cs <= 1'b0;                            
                sd_mosi <= CMD0[6'd47 - cmd_bit_cnt];     //先发送CMD0命令高位
                if(cmd_bit_cnt == 6'd47)                  
                    cmd_bit_cnt <= 6'd0;                  
            end      
            //在接收CMD0响应返回期间,片选CS拉低,进入SPI模式                                     
            st_wait_cmd0 : begin                          
                sd_mosi <= 1'b1;             
                if(res_en)                                //SD卡返回响应信号
                    //接收完成之后再拉高,进入SPI模式                     
                    sd_cs <= 1'b1;                                      
                over_time_cnt <= over_time_cnt + 1'b1;    //超时计数器开始计数
                //SD卡响应超时,重新发送软件复位命令
                if(over_time_cnt == OVER_TIME_NUM - 1'b1)
                    over_time_en <= 1'b1; 
                if(over_time_en)
                    over_time_cnt <= 16'd0;                                        
            end                                           
            st_send_cmd8 : begin                          //发送CMD8
                if(cmd_bit_cnt<=6'd47) begin
                    cmd_bit_cnt <= cmd_bit_cnt + 6'd1;
                    sd_cs <= 1'b0;
                    sd_mosi <= CMD8[6'd47 - cmd_bit_cnt]; //先发送CMD8命令高位       
                end
                else begin
                    sd_mosi <= 1'b1;
                    if(res_en) begin                      //SD卡返回响应信号
                        sd_cs <= 1'b1;
                        cmd_bit_cnt <= 6'd0; 
                    end   
                end                                                                   
            end 
            st_send_cmd55 : begin                         //发送CMD55
                if(cmd_bit_cnt<=6'd47) begin
                    cmd_bit_cnt <= cmd_bit_cnt + 6'd1;
                    sd_cs <= 1'b0;
                    sd_mosi <= CMD55[6'd47 - cmd_bit_cnt];       
                end
                else begin
                    sd_mosi <= 1'b1;
                    if(res_en) begin                      //SD卡返回响应信号
                        sd_cs <= 1'b1;
                        cmd_bit_cnt <= 6'd0;     
                    end        
                end                                                                                    
            end
            st_send_acmd41 : begin                        //发送ACMD41
                if(cmd_bit_cnt <= 6'd47) begin
                    cmd_bit_cnt <= cmd_bit_cnt + 6'd1;
                    sd_cs <= 1'b0;
                    sd_mosi <= ACMD41[6'd47 - cmd_bit_cnt];      
                end
                else begin
                    sd_mosi <= 1'b1;
                    if(res_en) begin                      //SD卡返回响应信号
                        sd_cs <= 1'b1;
                        cmd_bit_cnt <= 6'd0;  
                    end        
                end     
            end
            st_init_done : begin                          //初始化完成
                sd_init_done <= 1'b1;
                sd_cs <= 1'b1;
                sd_mosi <= 1'b1;
            end
            default : begin
                sd_cs <= 1'b1;
                sd_mosi <= 1'b1;                
            end    
        endcase
    end
end

endmodule

```
下面重点讲解一下这段代码：

```verilog
//接收sd卡返回的响应数据
//在div_clk_180deg(sd_clk)的上升沿锁存数据
always @(posedge div_clk_180deg or negedge rst_n) begin
    if(!rst_n) begin
        res_en <= 1'b0;
        res_data <= 48'd0;
        res_flag <= 1'b0;
        res_bit_cnt <= 6'd0;
    end    
    else begin
        //sd_miso = 0 开始接收响应数据
        if(sd_miso == 1'b0 && res_flag == 1'b0) begin 
            res_flag <= 1'b1;
            res_data <= {
    res_data[46:0],sd_miso};
            res_bit_cnt <= res_bit_cnt + 6'd1;
            res_en <= 1'b0;
        end    
        else if(res_flag) begin
            //R1返回1个字节,R3 R7返回5个字节
            //在这里统一按照6个字节来接收,多出的1个字节为NOP(8个时钟周期的延时)
            res_data <= {
    res_data[46:0],sd_miso};     
            res_bit_cnt <= res_bit_cnt + 6'd1;
            if(res_bit_cnt == 6'd47) begin
                res_flag <= 1'b0;
                res_bit_cnt <= 6'd0;
                res_en <= 1'b1; 
            end                
        end  
        else
            res_en <= 1'b0;         
    end
end  
```

在上述代码的always语句块中，我们使用div_clk_180deg（同sd_clk）的上升沿采集SD卡返回的信号，而其它语句块使用div_clk时钟（sd_clk相位偏差180度的时钟）来操作，这是因为SD卡的SPI模式下SD卡的上升沿锁存（采集）数据，在下降沿的时候更新（发送）数据，所 以在SD卡的上升沿采集数据是数据保持稳定的时刻，以确保采集的数据不会发送错误。我们知道，SD卡在初始化过程中共返回三种响应类型，分别为R1、R3和R7，其中返回的R3类型和R7类 型中包含R1类型，R1类型最高位固定为0，而SD_MISO在空闲时是为高电平状态，因此我们可以通过判断SD_MISO引脚拉低作为开始接收响应信号的条件。

图 39.4.4 和图 39.4.5为SD卡初始化过程中SignalTap抓取的波形图，从图中我们可以清晰的看到在SD卡初始化过程中，各个状态的跳转。在初始化完成之后，sd_init_done信号由低电平变为高电平，说明SD卡初始化完成。

![[Pasted image 20220712163037.png]]
SD卡写操作模块的代码如下：

```verilog
module sd_write(
    input                clk_ref       ,  //时钟信号
    input                clk_ref_180deg,  //时钟信号,与clk_ref相位相差180度
    input                rst_n         ,  //复位信号,低电平有效
    //SD卡接口
    input                sd_miso       ,  //SD卡SPI串行输入数据信号
    output  reg          sd_cs         ,  //SD卡SPI片选信号
    output  reg          sd_mosi       ,  //SD卡SPI串行输出数据信号
    //用户写接口    
    input                wr_start_en   ,  //开始写SD卡数据信号
    input        [31:0]  wr_sec_addr   ,  //写数据扇区地址
    input        [15:0]  wr_data       ,  //写数据                          
    output  reg          wr_busy       ,  //写数据忙信号
    output  reg          wr_req           //写数据请求信号
    );

//parameter define
parameter  HEAD_BYTE = 8'hfe    ;         //数据头
                             
//reg define                    
reg            wr_en_d0         ;         //wr_start_en信号延时打拍
reg            wr_en_d1         ;   
reg            res_en           ;         //接收SD卡返回数据有效信号      
reg    [7:0]   res_data         ;         //接收SD卡返回数据                 
reg            res_flag         ;         //开始接收返回数据的标志
reg    [5:0]   res_bit_cnt      ;         //接收位数据计数器                   
                                
reg    [3:0]   wr_ctrl_cnt      ;         //写控制计数器
reg    [47:0]  cmd_wr           ;         //写命令
reg    [5:0]   cmd_bit_cnt      ;         //写命令位计数器
reg    [3:0]   bit_cnt          ;         //写数据位计数器
reg    [8:0]   data_cnt         ;         //写入数据数量
reg    [15:0]  wr_data_t        ;         //寄存写入的数据，防止发生改变
reg            detect_done_flag ;         //检测写空闲信号的标志
reg    [7:0]   detect_data      ;         //检测到的数据

//wire define
wire           pos_wr_en        ;         //开始写SD卡数据信号的上升沿

//*****************************************************
//**                    main code
//*****************************************************

assign  pos_wr_en = (~wr_en_d1) & wr_en_d0;

//wr_start_en信号延时打拍
always @(posedge clk_ref or negedge rst_n) begin
    if(!rst_n) begin
        wr_en_d0 <= 1'b0;
        wr_en_d1 <= 1'b0;
    end    
    else begin
        wr_en_d0 <= wr_start_en;
        wr_en_d1 <= wr_en_d0;
    end        
end 

//接收sd卡返回的响应数据
//在clk_ref_180deg(sd_clk)的上升沿锁存数据
always @(posedge clk_ref_180deg or negedge rst_n) begin
    if(!rst_n) begin
        res_en <= 1'b0;
        res_data <= 8'd0;
        res_flag <= 1'b0;
        res_bit_cnt <= 6'd0;
    end    
    else begin
        //sd_miso = 0 开始接收响应数据
        if(sd_miso == 1'b0 && res_flag == 1'b0) begin
            res_flag <= 1'b1;
            res_data <= {
    res_data[6:0],sd_miso};
            res_bit_cnt <= res_bit_cnt + 6'd1;
            res_en <= 1'b0;
        end    
        else if(res_flag) begin
            res_data <= {
    res_data[6:0],sd_miso};
            res_bit_cnt <= res_bit_cnt + 6'd1;
            if(res_bit_cnt == 6'd7) begin
                res_flag <= 1'b0;
                res_bit_cnt <= 6'd0;
                res_en <= 1'b1; 
            end                
        end  
        else
            res_en <= 1'b0;       
    end
end 

//写完数据后检测SD卡是否空闲
always @(posedge clk_ref or negedge rst_n) begin
    if(!rst_n)
        detect_data <= 8'd0;   
    else if(detect_done_flag)
        detect_data <= {
    detect_data[6:0],sd_miso};
    else
        detect_data <= 8'd0;    
end        

//SD卡写入数据
always @(posedge clk_ref or negedge rst_n) begin
    if(!rst_n) begin
        sd_cs <= 1'b1;
        sd_mosi <= 1'b1; 
        wr_ctrl_cnt <= 4'd0;
        wr_busy <= 1'b0;
        cmd_wr <= 48'd0;
        cmd_bit_cnt <= 6'd0;
        bit_cnt <= 4'd0;
        wr_data_t <= 16'd0;
        data_cnt <= 9'd0;
        wr_req <= 1'b0;
        detect_done_flag <= 1'b0;
    end
    else begin
        wr_req <= 1'b0;
        case(wr_ctrl_cnt)
            4'd0 : begin
                wr_busy <= 1'b0;                          //写空闲
                sd_cs <= 1'b1;                                 
                sd_mosi <= 1'b1;                               
                if(pos_wr_en) begin                            
                    cmd_wr <= {
    8'h58,wr_sec_addr,8'hff};    //写入单个命令块CMD24
                    wr_ctrl_cnt <= wr_ctrl_cnt + 4'd1;      //控制计数器加1
                    //开始执行写入数据,拉高写忙信号
                    wr_busy <= 1'b1;                      
                end                                            
            end   
            4'd1 : begin
                if(cmd_bit_cnt <= 6'd47) begin              //开始按位发送写命令
                    cmd_bit_cnt <= cmd_bit_cnt + 6'd1;
                    sd_cs <= 1'b0;
                    sd_mosi <= cmd_wr[6'd47 - cmd_bit_cnt]; //先发送高字节                 
                end    
                else begin
                    sd_mosi <= 1'b1;
                    if(res_en) begin                        //SD卡响应
                        wr_ctrl_cnt <= wr_ctrl_cnt + 4'd1;  //控制计数器加1 
                        cmd_bit_cnt <= 6'd0;
                        bit_cnt <= 4'd1;
                    end    
                end     
            end                                                                                                     
            4'd2 : begin                                       
                bit_cnt <= bit_cnt + 4'd1;     
                //bit_cnt = 0~7 等待8个时钟周期
                //bit_cnt = 8~15,写入命令头8'hfe        
                if(bit_cnt>=4'd8 && bit_cnt <= 4'd15) begin
                    sd_mosi <= HEAD_BYTE[4'd15-bit_cnt];    //先发送高字节
                    if(bit_cnt == 4'd14)                       
                        wr_req <= 1'b1;                   //提前拉高写数据请求信号
                    else if(bit_cnt == 4'd15)                  
                        wr_ctrl_cnt <= wr_ctrl_cnt + 4'd1;  //控制计数器加1   
                end                                            
            end                                                
            4'd3 : begin                                    //写入数据
                bit_cnt <= bit_cnt + 4'd1;                     
                if(bit_cnt == 4'd0) begin                      
                    sd_mosi <= wr_data[4'd15-bit_cnt];      //先发送数据高位     
                    wr_data_t <= wr_data;                   //寄存数据   
                end                                            
                else                                           
                    sd_mosi <= wr_data_t[4'd15-bit_cnt];    //先发送数据高位
                if((bit_cnt == 4'd14) && (data_cnt <= 9'd255)) 
                    wr_req <= 1'b1;                          
                if(bit_cnt == 4'd15) begin                     
                    data_cnt <= data_cnt + 9'd1;  
                    //写入单个BLOCK共512个字节 = 256 * 16bit             
                    if(data_cnt == 9'd255) begin
                        data_cnt <= 9'd0;            
                        //写入数据完成,控制计数器加1          
                        wr_ctrl_cnt <= wr_ctrl_cnt + 4'd1;      
                    end                                        
                end                                            
            end       
            //写入2个字节CRC校验,由于SPI模式下不检测校验值,此处写入两个字节的8'hff                                         
            4'd4 : begin                                       
                bit_cnt <= bit_cnt + 4'd1;                  
                sd_mosi <= 1'b1;                 
                //crc写入完成,控制计数器加1              
                if(bit_cnt == 4'd15)                           
                    wr_ctrl_cnt <= wr_ctrl_cnt + 4'd1;            
            end                                                
            4'd5 : begin                                    
                if(res_en)                                  //SD卡响应   
                    wr_ctrl_cnt <= wr_ctrl_cnt + 4'd1;         
            end                                                
            4'd6 : begin                                    //等待写完成           
                detect_done_flag <= 1'b1;                   
                //detect_data = 8'hff时,SD卡写入完成,进入空闲状态
                if(detect_data == 8'hff) begin              
                    wr_ctrl_cnt <= wr_ctrl_cnt + 4'd1;         
                    detect_done_flag <= 1'b0;                  
                end         
            end    
            default : begin
                //进入空闲状态后,拉高片选信号,等待8个时钟周期
                sd_cs <= 1'b1;   
                wr_ctrl_cnt <= wr_ctrl_cnt + 4'd1;
            end     
        endcase
    end
end            

endmodule
```


SD卡写数据模块主要完成对SD卡的写操作，在程序的第18定义了一个参数HEAD_BYTE（SD卡写数据头），在开始写入有效数据之前，必须先发送数据头8’hfe。在代码的第60行开始的always语句块中，同样使用clk_ref_180deg（sd_clk）的上升沿采集数据，其原因同SD初始化模块一样，clk_ref_180deg的上升沿是数据保持稳定的时刻，采集的数据不会发生错误。

在代码第100行开始的always语句块中，使用写计数控制器（wr_ctrl_cnt）控制写入的流程。其流程为首先检测开始写入数据信号（wr_start_en）的上升沿，检测到上升沿之后开始发送写命令（CMD24）；写命令发送完成等待SD卡返回响应信号；SD卡返回响应命令后，等待8 个时钟周期，随后写入数据头和数据，注意写数据之前写请求信号要提前拉高，以保证写入数据时刻数据是有效的；发送完数据之后，再次发送两个字节的CRC校验值，由于SPI模式下不对数据做校验，这里发送两个字节的8’hff，然后等待SD卡返回响应数据。在接收完SD卡的响应之后给出标志detect_done_flag，以检测SD卡是否进入空闲状态。当SD卡进入空闲状态后等待8个时钟周期即可重新检测开始写入数据信号（wr_start_en）的上升沿。

图 39.4.6为SD卡写数据过程中SignalTap抓取的波形图。从图中可以看出，在检测到wr_start_en的上升沿（脉冲信号）后，wr_busy（写忙信号）开始拉高，sd_cs片选信号拉低，开始对SD卡写命令和数据，wr_req为请求写入的数据，共请求数据256次。在数据及CRC校验写完后detect_done_flag信号拉高，开始等待SD卡空闲。

![[Pasted image 20220712163149.png]]

图 39.4.7为数据写完后抓取到的SignalTap波形图。从图中可以看出，SD卡返回空闲信号（sd_miso由低电平变为高电平）后，片选信号开始拉高拉高，detect_done_flag信号拉低，wr_busy（写忙信号）拉低，此时可以进行下一次写操作。

![[Pasted image 20220712163227.png]]
SD卡读操作模块的代码如下：

```verilog
module sd_read(
    input                clk_ref       ,  //时钟信号
    input                clk_ref_180deg,  //时钟信号,与clk_ref相位相差180度
    input                rst_n         ,  //复位信号,低电平有效
    //SD卡接口
    input                sd_miso       ,  //SD卡SPI串行输入数据信号
    output  reg          sd_cs         ,  //SD卡SPI片选信号
    output  reg          sd_mosi       ,  //SD卡SPI串行输出数据信号
    //用户读接口    
    input                rd_start_en   ,  //开始读SD卡数据信号
    input        [31:0]  rd_sec_addr   ,  //读数据扇区地址                        
    output  reg          rd_busy       ,  //读数据忙信号
    output  reg          rd_val_en     ,  //读数据有效信号
    output  reg  [15:0]  rd_val_data      //读数据
    );

//reg define
reg            rd_en_d0      ;            //rd_start_en信号延时打拍
reg            rd_en_d1      ;                                
reg            res_en        ;            //接收SD卡返回数据有效信号      
reg    [7:0]   res_data      ;            //接收SD卡返回数据                  
reg            res_flag      ;            //开始接收返回数据的标志            
reg    [5:0]   res_bit_cnt   ;            //接收位数据计数器                  
                             
reg            rx_en_t       ;            //接收SD卡数据使能信号
reg    [15:0]  rx_data_t     ;            //接收SD卡数据
reg            rx_flag       ;            //开始接收的标志
reg    [3:0]   rx_bit_cnt    ;            //接收数据位计数器
reg    [8:0]   rx_data_cnt   ;            //接收的数据个数计数器
reg            rx_finish_en  ;            //接收完成使能信号
                             
reg    [3:0]   rd_ctrl_cnt   ;            //读控制计数器
reg    [47:0]  cmd_rd        ;            //读命令
reg    [5:0]   cmd_bit_cnt   ;            //读命令位计数器
reg            rd_data_flag  ;            //准备读取数据的标志

//wire define
wire           pos_rd_en     ;            //开始读SD卡数据信号的上升沿

//*****************************************************
//**                    main code
//*****************************************************

assign  pos_rd_en = (~rd_en_d1) & rd_en_d0;

//rd_start_en信号延时打拍
always @(posedge clk_ref or negedge rst_n) begin
    if(!rst_n) begin
        rd_en_d0 <= 1'b0;
        rd_en_d1 <= 1'b0;
    end    
    else begin
        rd_en_d0 <= rd_start_en;
        rd_en_d1 <= rd_en_d0;
    end        
end  

//接收sd卡返回的响应数据
//在clk_ref_180deg(sd_clk)的上升沿锁存数据
always @(posedge clk_ref_180deg or negedge rst_n) begin
    if(!rst_n) begin
        res_en <= 1'b0;
        res_data <= 8'd0;
        res_flag <= 1'b0;
        res_bit_cnt <= 6'd0;
    end    
    else begin
        //sd_miso = 0 开始接收响应数据
        if(sd_miso == 1'b0 && res_flag == 1'b0) begin
            res_flag <= 1'b1;
            res_data <= {
    res_data[6:0],sd_miso};
            res_bit_cnt <= res_bit_cnt + 6'd1;
            res_en <= 1'b0;
        end    
        else if(res_flag) begin
            res_data <= {
    res_data[6:0],sd_miso};
            res_bit_cnt <= res_bit_cnt + 6'd1;
            if(res_bit_cnt == 6'd7) begin
                res_flag <= 1'b0;
                res_bit_cnt <= 6'd0;
                res_en <= 1'b1; 
            end                
        end  
        else
            res_en <= 1'b0;        
    end
end 

//接收SD卡有效数据
//在clk_ref_180deg(sd_clk)的上升沿锁存数据
always @(posedge clk_ref_180deg or negedge rst_n) begin
    if(!rst_n) begin
        rx_en_t <= 1'b0;
        rx_data_t <= 16'd0;
        rx_flag <= 1'b0;
        rx_bit_cnt <= 4'd0;
        rx_data_cnt <= 9'd0;
        rx_finish_en <= 1'b0;
    end    
    else begin
        rx_en_t <= 1'b0; 
        rx_finish_en <= 1'b0;
        //数据头0xfe 8'b1111_1110，所以检测0为起始位
        if(rd_data_flag && sd_miso == 1'b0 && rx_flag == 1'b0)    
            rx_flag <= 1'b1;   
        else if(rx_flag) begin
            rx_bit_cnt <= rx_bit_cnt + 4'd1;
            rx_data_t <= {
    rx_data_t[14:0],sd_miso};
            if(rx_bit_cnt == 4'd15) begin 
                rx_data_cnt <= rx_data_cnt + 9'd1;
                //接收单个BLOCK共512个字节 = 256 * 16bit 
                if(rx_data_cnt <= 9'd255)                        
                    rx_en_t <= 1'b1;  
                else if(rx_data_cnt == 9'd257) begin   //接收两个字节的CRC校验值
                    rx_flag <= 1'b0;
                    rx_finish_en <= 1'b1;              //数据接收完成
                    rx_data_cnt <= 9'd0;               
                    rx_bit_cnt <= 4'd0;
                end    
            end                
        end       
        else
            rx_data_t <= 16'd0;
    end    
end    

//寄存输出数据有效信号和数据
always @(posedge clk_ref or negedge rst_n) begin
    if(!rst_n) begin
        rd_val_en <= 1'b0;
        rd_val_data <= 16'd0;
    end
    else begin
        if(rx_en_t) begin
            rd_val_en <= 1'b1;
            rd_val_data <= rx_data_t;
        end    
        else
            rd_val_en <= 1'b0;
    end
end              

//读命令
always @(posedge clk_ref or negedge rst_n) begin
    if(!rst_n) begin
        sd_cs <= 1'b1;
        sd_mosi <= 1'b1;        
        rd_ctrl_cnt <= 4'd0;
        cmd_rd <= 48'd0;
        cmd_bit_cnt <= 6'd0;
        rd_busy <= 1'b0;
        rd_data_flag <= 1'b0;
    end   
    else begin
        case(rd_ctrl_cnt)
            4'd0 : begin
                rd_busy <= 1'b0;
                sd_cs <= 1'b1;
                sd_mosi <= 1'b1;
                if(pos_rd_en) begin
                    cmd_rd <= {
    8'h51,rd_sec_addr,8'hff};    //写入单个命令块CMD17
                    rd_ctrl_cnt <= rd_ctrl_cnt + 4'd1;      //控制计数器加1
                    //开始执行读取数据,拉高读忙信号
                    rd_busy <= 1'b1;                      
                end    
            end
            4'd1 : begin
                if(cmd_bit_cnt <= 6'd47) begin              //开始按位发送读命令
                    cmd_bit_cnt <= cmd_bit_cnt + 6'd1;
                    sd_cs <= 1'b0;
                    sd_mosi <= cmd_rd[6'd47 - cmd_bit_cnt]; //先发送高字节
                end    
                else begin                                  
                    sd_mosi <= 1'b1;
                    if(res_en) begin                        //SD卡响应
                        rd_ctrl_cnt <= rd_ctrl_cnt + 4'd1;  //控制计数器加1 
                        cmd_bit_cnt <= 6'd0;
                    end    
                end    
            end    
            4'd2 : begin
                //拉高rd_data_flag信号,准备接收数据
                rd_data_flag <= 1'b1;                       
                if(rx_finish_en) begin                      //数据接收完成
                    rd_ctrl_cnt <= rd_ctrl_cnt + 4'd1; 
                    rd_data_flag <= 1'b0;
                    sd_cs <= 1'b1;
                end
            end        
            default : begin
                //进入空闲状态后,拉高片选信号,等待8个时钟周期
                sd_cs <= 1'b1;   
                rd_ctrl_cnt <= rd_ctrl_cnt + 4'd1;
            end    
        endcase
    end         
end

endmodule
```

SD卡读数据模块主要完成对SD卡的读操作。在代码的第60行开始的always语句块和第91行开始的always语句块中，同样采用clk_ref_180deg的上升沿采集数据，其原因同SD初始化模块一样，clk_ref_180deg的上升沿是数据保持稳定的时刻，采集的数据不会发生错误。

在代码第144行开始的always语句块中，使用读计数控制器（rd_ctrl_cnt）控制读取数据的流程。其流程为检测开始读取数据信号（rd_start_en）的上升沿，检测到上升沿之后开始发送读命令（CMD17）；读命令发送完成之后等待SD卡返回响应信号；SD卡返回响应命令后，准备接收SD卡的数据头，因为SD卡的数据头为8’hfe = 8’b1111_1110，所以我们只需要检测SD_MISO输入引脚的第一个低电平即可检测到数据头；检测到数据头之后，紧跟后面的就是256个16位数据和两个字节的CRC校验值，我们只需接收有效数据，CRC的校验值可不用关心；CRC校验接收完成后等待8个时钟周期即可检测开始读取数据信号（rd_start_en）的上升沿，再次对SD卡进行读操作。

图 39.4.8为SD卡读数据过程中SignalTap抓取的波形图。从图中可以看出，在检测到rd_start_en的上升沿（脉冲信号）后，rd_busy（读忙信号）开始拉高，sd_cs片选信号拉低，开始对SD卡发送读命令；在SD卡返回读命令响应信号后，拉高rd_data_flag信号，开始检测数据头8’hfe；在检测到数据头8’hfe后，开始接收SD卡返回的有效数据，共返回256个16位数 据；数据接收完成后产生rx_finish_en（接收完成信号）脉冲信号，拉低rd_data_flag和sd_cs（SD片选信号），等待8个时钟周期后拉低rd_busy信号，此时可以进行下一次读操作。

![[Pasted image 20220712163342.png]]

SD卡测试数据产生模块的代码如下：

```verilog
module data_gen(
    input                clk           ,  //时钟信号
    input                rst_n         ,  //复位信号,低电平有效
    input                sd_init_done  ,  //SD卡初始化完成信号
    //写SD卡接口
    input                wr_busy       ,  //写数据忙信号
    input                wr_req        ,  //写数据请求信号
    output  reg          wr_start_en   ,  //开始写SD卡数据信号
    output  reg  [31:0]  wr_sec_addr   ,  //写数据扇区地址
    output       [15:0]  wr_data       ,  //写数据
    //读SD卡接口
    input                rd_val_en     ,  //读数据有效信号
    input        [15:0]  rd_val_data   ,  //读数据
    output  reg          rd_start_en   ,  //开始写SD卡数据信号
    output  reg  [31:0]  rd_sec_addr   ,  //读数据扇区地址
    
    output               error_flag       //SD卡读写错误的标志
    );

//reg define
reg              sd_init_done_d0  ;       //sd_init_done信号延时打拍
reg              sd_init_done_d1  ;       
reg              wr_busy_d0       ;       //wr_busy信号延时打拍
reg              wr_busy_d1       ;
reg    [15:0]    wr_data_t        ;    
reg    [15:0]    rd_comp_data     ;       //用于对读出数据作比较的正确数据
reg    [8:0]     rd_right_cnt     ;       //读出正确数据的个数

//wire define
wire             pos_init_done    ;       //sd_init_done信号的上升沿,用于启动写入信号
wire             neg_wr_busy      ;       //wr_busy信号的下降沿,用于判断数据写入完成

//*****************************************************
//**                    main code
//*****************************************************

assign  pos_init_done = (~sd_init_done_d1) & sd_init_done_d0;
assign  neg_wr_busy = wr_busy_d1 & (~wr_busy_d0);
//wr_data_t变化范围0~256;wr_data范围:0~255
assign  wr_data = (wr_data_t > 16'd0)  ?  (wr_data_t - 1'b1) : 16'd0;
//读256次正确的数据,说明读写测试成功,error_flag = 0
assign  error_flag = (rd_right_cnt == (9'd256))  ?  1'b0 : 1'b1;

//sd_init_done信号延时打拍
always @(posedge clk or negedge rst_n) begin
    if(!rst_n) begin
        sd_init_done_d0 <= 1'b0;
        sd_init_done_d1 <= 1'b0;
    end
    else begin
        sd_init_done_d0 <= sd_init_done;
        sd_init_done_d1 <= sd_init_done_d0;
    end        
end

//SD卡写入信号控制
always @(posedge clk or negedge rst_n) begin
    if(!rst_n) begin
        wr_start_en <= 1'b0;
        wr_sec_addr <= 32'd0;
    end    
    else begin
        if(pos_init_done) begin
            wr_start_en <= 1'b1;
            wr_sec_addr <= 32'd2000;         //任意指定一块扇区地址
        end    
        else
            wr_start_en <= 1'b0;
    end    
end 

//SD卡写数据
always @(posedge clk or negedge rst_n) begin
    if(!rst_n)
        wr_data_t <= 16'b0;
    else if(wr_req) 
        wr_data_t <= wr_data_t + 16'b1;
end

//wr_busy信号延时打拍
always @(posedge clk or negedge rst_n) begin
    if(!rst_n) begin
        wr_busy_d0 <= 1'b0;
        wr_busy_d1 <= 1'b0;
    end    
    else begin
        wr_busy_d0 <= wr_busy;
        wr_busy_d1 <= wr_busy_d0;
    end
end 

//SD卡读出信号控制
always @(posedge clk or negedge rst_n) begin
    if(!rst_n) begin
        rd_start_en <= 1'b0;
        rd_sec_addr <= 32'd0;    
    end
    else begin
        if(neg_wr_busy) begin
            rd_start_en <= 1'b1;
            rd_sec_addr <= 32'd2000;
        end   
        else
            rd_start_en <= 1'b0;          
    end    
end    

//读数据错误时给出标志
always @(posedge clk or negedge rst_n) begin
    if(!rst_n) begin
        rd_comp_data <= 16'd0;
        rd_right_cnt <= 9'd0;
    end     
    else begin
        if(rd_val_en) begin
            //因为是非阻塞，所以第一次比较的值其实还是0
            rd_comp_data <= rd_comp_data + 16'b1;
            if(rd_val_data == rd_comp_data)
                rd_right_cnt <= rd_right_cnt + 9'd1;  
        end    
    end        
end

endmodule
```

在代码的第45行开始的always语句块中，对SD卡控制器的初始化完成信号（sd_init_done） 打两拍，以检测SD卡的上升沿，用于发起SD卡的写入操作。在代码的第57行开始的always块中，当检测到SD卡的上升沿之后，开始发起写入操作，即wr_start_en（开始写SD卡数据信号）和wr_sec_addr（wr_sec_addr）。这里需要注意的是，写扇区地址并没有从0开始写，0扇区地址为SD卡的分区引导记录区，如果从0扇区地址开始写入测试数据会破坏SD卡的FAT文件系统，因此我们随意指定SD卡的中间数据区域开始测试，这里是从扇区地址2000开始写入，读出扇区地 址和写扇区地址保持一致。

测试数据写完后（wr_busy写忙信号的下降沿代表写完数据），就开始从SD卡中读出数据。需要注意的是代码中的error_flag默认是高电平，即错误状态，正确读取到256次（单个扇区为512个字节，因为接口封装成16位，因此需要读取256次）时才会变成低电平，目的是在未插入SD卡时，SD卡无法完成初始化，也就无法对SD卡进行读写测试，如果此时默认低电平的话，会误以为读写测试正确。