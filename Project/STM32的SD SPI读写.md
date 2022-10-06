
#SD #Tutorial #MCU
[STM32的简单的SD卡读写（不带文件系统，SPI方式）](https://blog.csdn.net/z_jinye/article/details/23276877?spm=1001.2101.3001.6661.1&utm_medium=distribute.pc_relevant_t0.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-1-23276877-blog-122073446.pc_relevant_aa2&depth_1-utm_source=distribute.pc_relevant_t0.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-1-23276877-blog-122073446.pc_relevant_aa2&utm_relevant_index=1)

SD卡一般支持两种读写模式，SPI和SDIO模式，SD卡的引脚排序如下图所示。
![[Pasted image 20220712125130.png]]


SPI模式下有几个重要的操作命令，分别是：

![[Pasted image 20220712125109.png]]

![[Pasted image 20220712125115.png]]
SD卡R1回应的格式如下

![[Pasted image 20220712125121.png]]
SPI模式下的典型初始化过程如下：

1、初始化硬件配置，SPI配置，IO配置等。

2、上电延时。（>74CLK）

3、复位卡。（CMD0）

4、激活卡，内部初始化并获取卡的类型。

5、查询OCR，获取供电情况。

6、是否使用CRC（CMD59）。

7、设置读写块数据长度（CMD16）。

8、读取CSD，获取存储卡的其他信息（CMD9）

9、发送8CLK后，禁止片选。

SPI模式下的典型读取数据的过程如下，这里采用CMD17来实现。

1、发送CMD17。

2、接收卡响应R1。

3、接收数据起始令牌0XFE。

4、接收数据。

5、接收两个字节的CRC，如果没有开启CRC。这两个字节在读取后可以丢掉。

6、8CLK之后禁止片选。

SPI模式下的典型写数据的过程如下，这里采用CMD24来实现。

1、发送CMD24。

2、接收卡响应R1。

3、接收数据起始令牌0XFE。

4、接收数据。

5、发送两个字节的伪CRC。

6、8CLK之后禁止片选。

具体代码实现如下。


```c
/*******************************************************************************
* Function Name  : SPI_FLASH_Init
* Description    : Initializes the peripherals used by the SPI FLASH driver.
* Input          : None
* Output         : None
* Return         : None
*******************************************************************************/
void SPI_SD_Init(void)
{
 
  GPIO_InitTypeDef GPIO_InitStructure;
 
  /* 使能SPI对应引脚的时钟  使能SPI1的时钟 */
  RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA | RCC_APB2Periph_SPI1, ENABLE);
 
  /*配置SPI的时钟线SCK和SPI的MOSI线和SPI的MISO线 */
  GPIO_InitStructure.GPIO_Pin = GPIO_Pin_5 | GPIO_Pin_6 | GPIO_Pin_7;
  GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
  GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP; //复用功能的推挽输出
  GPIO_Init(GPIOA, &GPIO_InitStructure);
  /*配置SPI的片选线：CSN */
  GPIO_InitStructure.GPIO_Pin = GPIO_Pin_2|GPIO_Pin_3|GPIO_Pin_4|GPIO_Pin_8;
  GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP; //推挽输出
  GPIO_Init(GPIOA, &GPIO_InitStructure);
  /*  拉高CSN引脚，停止使能SD*/
  GPIO_SetBits(GPIOA,GPIO_Pin_2|GPIO_Pin_3|GPIO_Pin_4|GPIO_Pin_8);
  GPIO_SetBits(GPIOA,GPIO_Pin_5|GPIO_Pin_6|GPIO_Pin_7);

  // 配置SPI,使它适合SD的特性
  SPI_InitStructure.SPI_Direction = SPI_Direction_2Lines_FullDuplex;  //双线双向全双工
  SPI_InitStructure.SPI_Mode = SPI_Mode_Master;  //主器件
  SPI_InitStructure.SPI_DataSize = SPI_DataSize_8b;//8位数据长度
  SPI_InitStructure.SPI_CPOL = SPI_CPOL_High;  //时钟悬空时为高
  SPI_InitStructure.SPI_CPHA = SPI_CPHA_2Edge; //数据捕获于第2个时钟沿
  SPI_InitStructure.SPI_NSS = SPI_NSS_Soft;   //NSS信号由外部管脚管理
  SPI_InitStructure.SPI_BaudRatePrescaler = SPI_BaudRatePrescaler_256;//波特率预分频值为4
  SPI_InitStructure.SPI_FirstBit = SPI_FirstBit_MSB; //数据传输的第一个字节为MSB
  SPI_InitStructure.SPI_CRCPolynomial = 7;  //CRC的多项式
  SPI_Init(SPI1, &SPI_InitStructure);
  /* 使能SPI1  */
  SPI_Cmd(SPI1, ENABLE);
}

/*******************************************************************************
* Function Name  : SPI_FLASH_SendByte
* Description    : 发送一个数据，同时接收从FLASH返回来的数据
* Input          : byte : byte to send.
* Output         : None
* Return         : The value of the received byte.
*******************************************************************************/
u8 SPIx_ReadWriteByte(u8 byte)
{
  /* 等待数据发送寄存器清空 */
  while (SPI_I2S_GetFlagStatus(SPI1, SPI_I2S_FLAG_TXE) == RESET);

  /* 通过SPI发送出去一个字节数据 */
  SPI_I2S_SendData(SPI1, byte);

  /* 等待接收到一个数据（接收到一个数据就相当于发送一个数据完毕） */
  while (SPI_I2S_GetFlagStatus(SPI1, SPI_I2S_FLAG_RXNE) == RESET);

  /* 返回接收到的数据 */
  return SPI_I2S_ReceiveData(SPI1);
}

/*******************************************************************************
* Function Name  : SPI_FLASH_SendHalfWord
* Description    : 发送并接受一个半字数据（16位）
* Input          : Half Word : Half Word to send.
* Output         : None
* Return         : The value of the received Half Word.
*******************************************************************************/
u16 SPIx_ReadWriteHalfWord(u16 HalfWord)
{
  /* 等待数据发送寄存器清空 */
  while (SPI_I2S_GetFlagStatus(SPI1, SPI_I2S_FLAG_TXE) == RESET);

  /* 通过SPI发送出去半个字的数据 */
  SPI_I2S_SendData(SPI1, HalfWord);

  /* 等待接收到一个半字数据（接收到一个数据就相当于发送一个数据完毕） */
  while (SPI_I2S_GetFlagStatus(SPI1, SPI_I2S_FLAG_RXNE) == RESET);

  /* 返回接收到的数据 */
  return SPI_I2S_ReceiveData(SPI1);
}
//SPI 速度设置函数
//SpeedSet:
//SPI_BaudRatePrescaler_2   2分频   (SPI 36M@sys 72M)
//SPI_BaudRatePrescaler_8   8分频   (SPI 9M@sys 72M)
//SPI_BaudRatePrescaler_16  16分频  (SPI 4.5M@sys 72M)
//SPI_BaudRatePrescaler_256 256分频 (SPI 281.25K@sys 72M)
 
void SPIx_SetSpeed(u8 SpeedSet)
{
 SPI_InitStructure.SPI_BaudRatePrescaler = SpeedSet ;
   SPI_Init(SPI1, &SPI_InitStructure);
 SPI_Cmd(SPI1,ENABLE);
}

/******************************END OF INIT_SPI*****************************/


/******************************START OF SD_OPERATION***********************/
/*******************************************************************************
* 函数名称       : SD_Select
* 功能描述       : 选择SD卡，并等待SD卡准备好
* 进入参数       : 无.
* 返回参数       : 0：成功       1：失败
* 备注说明       : SD卡准备好会返回0XFF
*******************************************************************************/
u8 SD_Select(void)
{
 uint32_t t=0;
 SD_CS(OFF);  //片选SD，低电平使能
 do
 {
  if(SD_SPI_ReadWriteByte(0XFF)==0XFF)return 0;//OK
  t++;     
 }while(t<0XFFFFFF);//等待
 SD_DisSelect();  //释放总线
 return 1;//等待失败
}
/*******************************************************************************
* 函数名称       : SD_RecvData
* 功能描述       : 从sd卡读取一个数据包的内容
* 进入参数       : buf：数据缓存数组      len要读取的数据的长度
* 返回参数       : 0：成功       其他：失败
* 备注说明       : 读取时需要等待SD卡发送数据起始令牌0XFE
*******************************************************************************/
u8 SD_RecvData(u8*buf,u16 len)
{ 
 u16 Count=0xF000;//等待次数
 while ((SD_SPI_ReadWriteByte(0XFF)!=0xFE)&&Count)Count--;//等待得到读取数据令牌0xfe
 if    (Count==0)   return MSD_RESPONSE_FAILURE;//获取令牌失败,返回0XFF     
    while(len--)//开始接收数据
    {
        *buf=SPIx_ReadWriteByte(0xFF);
        buf++;
    }
    //下面是2个伪CRC（dummy CRC），假装接收了2个CRC
    SD_SPI_ReadWriteByte(0xFF);
    SD_SPI_ReadWriteByte(0xFF);                    
    return 0;//读取成功
}
/*******************************************************************************
* 函数名称       : SD_SendBlock
* 功能描述       : 向sd卡写入一个数据包的内容 512字节
* 进入参数       : buf:数据缓存区    cmd:数据发送的令牌
* 返回参数       : 0：成功       其他：失败
* 备注说明       : 写数据时需要先发送数据起始令牌0XFE/0XFC/0XFD
*******************************************************************************/
u8 SD_SendBlock(u8*buf,u8 cmd)
{ 
 u32 t,Count=0XFFFFFF; 
 while ((SD_SPI_ReadWriteByte(0XFF)!=0xFF)&&Count)Count--;//等待SD卡准备好
 if    (Count==0)   return MSD_RESPONSE_FAILURE;//SD卡未准备好，失败，返回
 SD_SPI_ReadWriteByte(cmd); //发送数据起始或停止令牌
 if(cmd!=0XFD)//在不是结束令牌的情况下，开始发送数据
 {
  for(t=0;t<512;t++)SPIx_ReadWriteByte(buf[t]);//提高速度,减少函数传参时间
     SD_SPI_ReadWriteByte(0xFF);//发送2字节的CRC
     SD_SPI_ReadWriteByte(0xFF);
  t=SD_SPI_ReadWriteByte(0xFF);//紧跟在CRC之后接收数据写的状态
  if((t&0x1F)!=0x05)return MSD_DATA_WRITE_ERROR;//写入错误                   
 }                          
    return 0;//写入成功
}
/*******************************************************************************
* 函数名称       : SD_SendCmd
* 功能描述       : 向sd卡写入一个数据包的内容 512字节
* 进入参数       : cmd：命令  arg：命令参数  crc：crc校验值及停止位
* 返回参数       : 返回值:SD卡返回的对应相应命令的响应
* 备注说明       : 响应为R1-R7，见SD协议手册V2.0版（2006）
*******************************************************************************/
u8 SD_SendCmd(u8 cmd, u32 arg, u8 crc)
{
    u8 r1; 
 u8 Retry=0;
 SD_DisSelect();//取消上次片选释放总线
 if(SD_Select())return 0XFF;//检查片选信号线是否选择成功
 //发送
    SD_SPI_ReadWriteByte(cmd | 0x40);//分别写入命令
    SD_SPI_ReadWriteByte(arg >> 24);
    SD_SPI_ReadWriteByte(arg >> 16);
    SD_SPI_ReadWriteByte(arg >> 8);
    SD_SPI_ReadWriteByte(arg);  
    SD_SPI_ReadWriteByte(crc);
 if(cmd==CMD12)SD_SPI_ReadWriteByte(0xff);//Skip a stuff byte when stop reading
    //等待响应，或超时退出
 Retry=0X1F;
 do  //发送一定数量的时钟信号，等待SD卡回应0X01（0x01表示命令发送成功，回复0XFF表示失败）
 {
  r1=SD_SPI_ReadWriteByte(0xFF);
 }while((r1&0X80) && Retry--); //等待返回非0XFF的数据
 //返回状态值
    return r1;
}
/*******************************************************************************
* 函数名称       : SD_GetCID
* 功能描述       : 获取SD卡的CID信息，包括制造商信息
* 进入参数       : cid_data(存放CID的内存，至少16Byte
* 返回参数       : 0：成功       其他：失败
* 备注说明       : CID寄存器内容详见SD协议手册V2.0版（2006）
*******************************************************************************/
u8 SD_GetCID(u8 *cid_data)
{
    u8 r1;   
    //发CMD10命令，读CID
    r1=SD_SendCmd(CMD10,0,0x01);
    if(r1==0x00)
 {
  r1=SD_RecvData(cid_data,16);//接收16个字节的数据 
    }
 SD_DisSelect();//取消片选
 if(r1)return 1;
 else return 0;
}
/*******************************************************************************
* 函数名称       : SD_GetCSD
* 功能描述       : 获取SD卡的CSD信息，包括容量和速度信息
* 进入参数       : cid_data(存放CSD的内存，至少16Byte
* 返回参数       : 0：成功       其他：失败
* 备注说明       : CSD寄存器内容详见SD协议手册V2.0版（2006）
*******************************************************************************/
u8 SD_GetCSD(u8 *csd_data)
{
    u8 r1; 
    r1=SD_SendCmd(CMD9,0,0x01);//发CMD9命令，读CSD 
    if(r1==0)
 {
     r1=SD_RecvData(csd_data,16);//接收16个字节的数据
    }
 SD_DisSelect();//取消片选
 if(r1)return 1;
 else return 0;
}
/*******************************************************************************
* 函数名称       : SD_GetSectorCount
* 功能描述       : 获取SD卡的总扇区数（扇区数
* 进入参数       : cid_data(存放CSD的内存，至少16Byte
* 返回参数       : 0：获取容量出错       其他：SD卡的扇区数量值
* 备注说明       : SD卡的容量的计算公式SD协议手册V2.0版（2006）
*******************************************************************************/
u32 SD_GetSectorCount(void)
{
    u8 csd[16];
    u32 Capacity; 
    u8 n;
 u16 csize;          
 //取CSD信息，如果期间出错，返回0 
    if(SD_GetCSD(csd)!=0) return 0;  //获取容量失败  
    //如果为SDHC卡，按照下面方式计算
    if((csd[0]&0xC0)==0x40)  //V2.00的卡
    { 
  csize = csd[9] + ((u16)csd[8] << 8) + 1;
  Capacity = (u32)csize << 10;//得到扇区数      
    }
 else//V1.XX的卡
    { 
  n = (csd[5] & 15) + ((csd[10] & 128) >> 7) + ((csd[9] & 3) << 1) + 2;
  csize = (csd[8] >> 6) + ((u16)csd[7] << 2) + ((u16)(csd[6] & 3) << 10) + 1;
  Capacity= (u32)csize << (n - 9);//得到扇区数  
    }
    return Capacity;
}
/*******************************************************************************
* 函数名称       : SD_ReadDisk
* 功能描述       : 读SD卡
* 进入参数       : buf:数据缓存区        sector:欲读取的地址      cnt:欲读取的扇区数
* 返回参数       : 0：成功       其他：失败
* 备注说明       : 1.读取的地址必须是一个扇区的起始
     2.必须是SD2.0卡，其他的卡不处理
*******************************************************************************/
u8 SD_ReadDisk(u8*buf,u32 sector,u8 cnt)
{
 u8 r1;
 if(cnt==1)
 {
  r1=SD_SendCmd(CMD17,sector,0X01);//读命令
  if(r1==0)//指令发送成功
  {
   r1=SD_RecvData(buf,512);//接收512个字节   
  }
 }
 else
 {
  r1=SD_SendCmd(CMD18,sector,0X01);//连续读命令
  do
  {
   r1=SD_RecvData(buf,512);//接收512个字节 
   buf+=512; 
  }while(--cnt && r1==0);  
  SD_SendCmd(CMD12,0,0X01); //发送停止命令
 }  
 SD_DisSelect();//取消片选
 return r1;//
}
/*******************************************************************************
* 函数名称       : SD_WriteDisk
* 功能描述       : 写SD卡
* 进入参数       : buf:数据缓存区        sector:待写的地址      cnt:待写的扇区数
* 返回参数       : 0：成功       其他：失败
* 备注说明       : 1.写的地址必须是一个扇区的起始
     2.必须是SD2.0卡，其他的卡不处理
*******************************************************************************/
u8 SD_WriteDisk(u8*buf,u32 sector,u8 cnt)
{
 u8 r1;
 if(cnt==1)
 {
  r1=SD_SendCmd(CMD24,sector,0X01);//单个扇区写命令
  if(r1==0)//指令发送成功
  {
   r1=SD_SendBlock(buf,0xFE);//写512个字节   
  }
 }
 else
 {
  if(SD_Type!=SD_TYPE_MMC)
  {
   SD_SendCmd(CMD55,0,0X01); 
   SD_SendCmd(CMD23,cnt,0X01);//发送待写入的扇区的数量，此命令用来预擦除所有待写入的扇区 
  }
   r1=SD_SendCmd(CMD25,sector,0X01);//连续写命令，发送起始地址
  if(r1==0)
  {
   do
   {
    r1=SD_SendBlock(buf,0xFC);//发送512个字节 
    buf+=512; 
   }while(--cnt && r1==0);
   r1=SD_SendBlock(0,0xFD);//发送停止位
  }
 }  
 SD_DisSelect();//取消片选
 return r1;//
}
/*******************************************************************************
* 函数名称       : SD_Initialize
* 功能描述       : 写SD卡
* 进入参数       : 无
* 返回参数       : 0：成功       其他：失败
* 备注说明       : 1.写的地址必须是一个扇区的起始
     2.必须是SD2.0卡，其他的卡不处理
*******************************************************************************/
u8 SD_Initialize(void)
{
    u8 r1;      // 存放SD卡的返回值
    u16 retry;  // 用来进行超时计数
    u8 buf[4]; 
 u16 i;

 SPI_SD_Init();  //初始化IO
  SD_SPI_SpeedLow(); //设置到低速模式   
 for(i=0;i<10;i++)SD_SPI_ReadWriteByte(0XFF);//发送最少74个脉冲,此时保持片选线是高电平
 retry=20;
 do
 {
  r1=SD_SendCmd(CMD0,0,0x95);//进入复位，同时选中了SPI模式（发送CMD0时，CSN为低电平）
 }while((r1!=0X01) && retry--);
  SD_Type=0;//默认无卡
 if(r1==0X01)
 {
  if(SD_SendCmd(CMD8,0x1AA,0x87)==1)//利用V2.0版SD卡特有的命令CMD8检查是否为2.0卡
  {
   for(i=0;i<4;i++)buf[i]=SD_SPI_ReadWriteByte(0XFF); //Get trailing return value of R7 resp
   if(buf[2]==0X01&&buf[3]==0XAA)//卡是否支持2.7~3.6V
   {
    retry=0XFFFE;
    do
    {
     SD_SendCmd(CMD55,0,0X01); //发送CMD55
     r1=SD_SendCmd(CMD41,0x40000000,0X01);//发送CMD41
    }while(r1&&retry--);
    if(retry&&SD_SendCmd(CMD58,0,0X01)==0)//鉴别SD2.0卡版本,读取OCR的值
    {
     for(i=0;i<4;i++)buf[i]=SD_SPI_ReadWriteByte(0XFF);//得到OCR值
     if(buf[0]&0x40)SD_Type=SD_TYPE_V2HC;    //检查CCS (第30位)
     else SD_Type=SD_TYPE_V2;  
    }
   }
  }
  else//不是2.0卡的情况下，检查是否为1.0卡或者mmc卡
  {
   SD_SendCmd(CMD55,0,0X01);  //发送CMD55
   r1=SD_SendCmd(CMD41,0,0X01); //发送CMD41
   if(r1<=1)//发送CMD55和CMD41成功，表示这是1.0卡
   {  
    SD_Type=SD_TYPE_V1;
    retry=0XFFFE;
    do //等待退出IDLE模式
    {
     SD_SendCmd(CMD55,0,0X01); //发送CMD55
     r1=SD_SendCmd(CMD41,0,0X01);//发送CMD41 进行初始化
    }while(r1&&retry--);
   }
   else //不是1.0卡，则考虑是MMC卡
   {
    SD_Type=SD_TYPE_MMC;//先假设是MMC卡
    retry=0XFFFE;
    do //等待退出IDLE模式
    {              
     r1=SD_SendCmd(CMD1,0,0X01);//发送CMD1，利用复位功能判断是否为MMC卡
    }while(r1&&retry--); //发送复位命令，超时则复位失败
   }
   if(retry==0||SD_SendCmd(CMD16,512,0X01)!=0)SD_Type=SD_TYPE_ERR;//MMC卡复位失败
  }
 }
 SD_DisSelect();//取消片选
 SD_SPI_SpeedHigh();//高速
 if(SD_Type)return 0; //初始化成功
 else if(r1)return r1; //初始化失败   
 return 0xaa;//其他错误
}


```

