line buffer存储 1920x3 =5760 bytes 约等于40000多bits 是否够用 有没有办法只存储有效

像素进入后先点处理变成灰度，因此一个像素只需要存1byte

解决: ![[Pasted image 20220812132422.png]]
有效区域在PL完成后通过MM2S写回DDR，再一次性把DDR内的1920x1080传输到Monitor

Line Buffer 是RAM不是FIFO，因为FIFO只能被读一次，但此处第一行最后一行之外的 每行都要被用三次
#### register
写4个ram_array，深度假定512
signal wrPtr,512深度，8 downto 0

##### vhdl中定义Line Buffer 



```vhdl
type ram_type is array (NO_OF_COLS - 1 downto 0) of std_logic_vector(DATA_WIDTH -1 downto 0);
signal ram_array : ram_type;

过程中;
ram_array(ColsCounter) <= pdata_in;



```
process 上升，如果reset wrPtr 0 否则如果 valid高 写进line(wrPtr)
读 line(rdPtr),line(rdPtr+1),line(rdPtr+2)

读的是横向的3个像素！然后例化3个linebuffer，读一次得到全部9个像素

最好把assign写在process 外，process内只计算读指针，一旦指针计算出来立刻接到下三个电路，0 latency  注意Timing， 给出rd_ready的第一个周期数据就已经可读


### 设计MAC multiplication and summation operation
选定kernal，假设本模块中line顺序已经排列好
模块conv


reg kernel array (8 downto 0) of signed(3 downto 0)
进了architecture先给kernel赋值 
process 上升时 
for i, i<9,i++
kernel(i) * data (i) 注意两个都是signed (kernel本来就是signed, data补符号位0后是signed)
4bits+9bits=13 bits 12 downto 0, 9个multData寄存器

[[pipelining]]

![[Pasted image 20220815101322.png]]
![[Pasted image 20220815101407.png]]

![[Pasted image 20220815192553.png]]
![[Pasted image 20220815214852.png]]

Buffer时序:
wrPtr的数字就是当前buffer里有多少个数据
rdPtr : 给出rd_en的瞬间立刻读数据，不能等上升


simulation
 all components( without iobuffer)
 #![[Pasted image 20220905122345.png]]
 ![[Pasted image 20220905122551.png]]