#tool
时序图工具
[WaveDrom Editor](https://wavedrom.com/editor.html)

示范代码

```



{ signal : [
  [ '高低电平',
    { name: "0    1",		wave: "0101|0011|0.1."},
    { name: "l    h",		wave: "lhlh|llhh|l.h."},
    { name: "L    H",		wave: "LHLH|LLHH|L.H."},
  ],
  {},
  [ '时钟信号',
    { name: "先高后低: p",	wave: "pp..|hp..|hpp."},
    { name: "先低后高: n",	wave: "nn..|ln..|lnn."},
    { name: "带上升沿: P",	wave: "PP..|hP..|lP.P"},
    { name: "带下降沿: N",	wave: "NN..|lN..|hN.N"},
  ],
  {},   
  { name: "高阻态",		    wave: "z0z1zlzhz=z3z|"}, 
  { name: "上拉下拉",		wave: "zudxdxuhu.ld|u"},
   { name: "数据1",			wave: "zx2..23456789.zx",data:["head"]},
  { name: "数据2",		    wave: "xzxux0xzxhxPxn"}
 ]}

```
