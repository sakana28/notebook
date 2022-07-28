#Bild 
Slave Master指的是VTC是Slave 还是Master
输入的Stream数据要同步到时序，同步过程中， 输入视频流和时序时间时钟不同，存在相位差。VID控制VTC是Slave模式，VTC free run不受控制输出时间，VID把Stream Buffer起来和时间同步。通常Slave以减少缓冲和延时
控制信号 vid_gen_ce,拉高前不输出时序
内部有一个asy FIFO ，实现了Stream和视频时钟的跨时钟

fid在不interlaced的时候接0
video out的输入match!!!