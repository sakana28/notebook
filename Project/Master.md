cyclostationarity 循环平稳性 
循环平稳性是表现出某种周期行为的非平稳信号的特性
Cyclostationarity encompasses a subclass of non-stationary signals which exhibit some cyclical  
behaviour.循环平稳信号的一个典型示例是随机噪声，其幅度由周期函数调制。 A typical example of a cyclostationary signal is a random noise that is amplitude modulated by a periodic function.循环平稳性的一个多功能例子是不同的周期调制覆盖随机噪声的每个频率分量。这种循环平稳特性非常适合许多旋转和往复机器振动，因为它们在运行过程中会保持固有的周期性调制。clostationarity has been shown to ideally fit  the property of many rotating and reciprocating machine vibrations,

fundamental observation to keep in mind： clostationarity is symptomatic to the presence of faults, owing to the occurrence of repetitive shocks when a defect impacts a rolling surface (a series of repetitive shocks may be seen as a signal periodically amplitude modulated in  time). 基础Mindset: 循环平稳性是缺陷存在的征兆，这是因为缺陷撞击滚动表面时会发生反复冲击。一系列重复的冲击可以看作是周期性地对振幅进行时间调制的信号。这些冲击的重复频率，即循环频率，只指出了origin of the fault。 而循环平稳强度（由稍后引入的一些光谱量测量）可以用来表明其严重性。‘‘intensity’’ (as measured by some spectral quantities to be introduced later) ) may serve to indicate its  severity

(1) which cyclic spectral quantity 1 turns out to be optimal for diagnostics purposes?  
(2) how can such a quantity be efficiently computed from finite length vibration measurements?  
(3) which statistical test should be used in accordance with it in an effort towards automated diagnostics?
（1）哪种循环光谱量最适合诊断（2）如何从有限长度的振动测量中有效地计算出该循环光谱量（3）以及应使用哪种统计测试进行自动诊断。
（本文讨论了使用循环光谱工具诊断轴承故障。事实证明，循环相干性是实现此目的的最佳工具，因为它不仅可以在高水平的背景噪声中检测故障的存在，还可以相对衡量其严重程度。详细探讨了循环相干性的估计问题，以及循环相干性在统计检验和次优简化中的用途。 该论文还表明，方包络谱是循环相干性的特例，具有相似的诊断能力。本文第 6 节使用实际方位信号说明了所提出的方法。）

2,1
突出显示的文本解释了滚动轴承初期故障的原因和影响。这些故障通常是由轴承消光表面的局部材料流失造成的，例如点蚀、剥落、腐蚀、摩擦或污染。当滚动表面与故障接触时，它会产生短时间的脉冲，激发轴承或振动传感器本身的某种结构共振。这会产生一系列脉冲响应，其时间间隔取决于故障类型和轴承的几何形状。 此外，由于断层进入和流出载荷区，初始故障产生的一系列脉冲响应可能会受到振幅调制。调制频率取决于故障类型和轴承的几何形状。例如，对于静止的外部竞赛和存在径向载荷的情况下，外部竞赛断层将经历均匀的振幅调制，内部竞赛将在内部竞赛旋转期间经历周期性振幅调制，滚动元件故障将在笼子旋转期间经历周期性振幅调制。这些调制频率在附录的表 A.1 中列出，该表提供了一些可用于诊断的典型故障频率。 总之，突出显示的文本解释了滚动轴承初期故障的原因和影响，包括脉冲响应的产生和振幅调制的可能性。它还提供与不同类型的故障相关的调制频率以及可用于诊断的典型故障频率的信息。

此外，由于断层进入和流出载荷区，初始故障产生的一系列脉冲响应可能会受到振幅调制。