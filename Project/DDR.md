#Dictionary 
DDR SDRAM全称为Double Data Rate SDRAM，中文名为“双倍数据率SDRAM”。

ROM和RAM指的都是半导体存储器，ROM是只读存储器（Read-Only Memory）的简称，是一种只能读出事先所存数据的固态半导体存储器，其特性是一旦储存资料就无法再将之改变或删除。通常用在不需经常变更资料的电子或电脑系统中，资料并不会因为电源关闭而消失。RAM是Random Access Memory的缩写，即随机存储器，随机是指数据不是线性依次存储，而是自由指定地址进行数据读写，通俗来说就是可以以任何顺序访问，而不管前一次访问的是哪一个位置。ROM在系统停止供电的时候仍然可以保持数据，而RAM通常都是在掉电之后就丢失数据，典型的RAM就是计算机的内存。

RAM又分两大类，一种称为静态RAM(Static RAM/SRAM)，是一种具有静止存取功能的内存，不需要刷新电路即能保存它内部存储的数据，也就是说加电情况下，不需要刷新，数据不会丢失。SRAM速度非常快，是早期读写最快的存储设备了，但是SRAM也有它的缺点，即它的集成度较低，相同容量的内存需要很大的体积，且功耗较大；同时它也非常昂贵，所以只在要求很苛刻的地方使用，譬如CPU的一级缓存，二级缓存。另一种称为动态RAM(Dynamic RAM/DRAM)，DRAM 只能将数据保持很短的时间，为了保持数据，DRAM使用电容存储，所以必须隔一段时间刷新（refresh）一次，如果存储单元没有被刷新，存储的信息就会丢失（关机就会丢失数据）；它的速度也比SRAM慢，不过它还是比任何的ROM都要快，但从价格上来说DRAM相比SRAM要便宜很多，计算机内存就是DRAM的。

SDRAM又是在DRAM的基础上发展而来，同时也是属于DRAM中的一种。SDRAM即Synchronous DRAM，同步动态随机存储器，同步是指 Memory工作需要同步时钟，内部命令的发送与数据的传输都以它为基准；

DDR SDRAM又是在SDRAM的基础上发展而来，这种改进型的DRAM和SDRAM是基本一样的，不同之处在于它可以在一个时钟读写两次数据，这样就使得数据传输速度加倍了。这是**目前电脑中用得最多的内存**，而且它有着成本优势。

也就是说我们现在使用的DDR SDRAM其实就是属于DRAM的一种