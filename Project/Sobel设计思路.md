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
读 