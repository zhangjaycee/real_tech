# 无损压缩能否突破信息熵的限制

无损压缩就是数据在压缩后的还能原样恢复到压缩前的样子。信息熵则被定义来衡量信源所生成信息的信息量。信息熵确实是熵编码的上限，但并非损压缩算法的上限，所以“信息压缩极限为信息熵”是一种误解。


### 1. 信息熵

若不考虑序列的相关性(dependencies)，认为每个元素独立同分布，则信息熵(即信息量)是一阶的，**一阶信息熵** 相对考虑信源相关性的信源熵更大。

我们以序列S = {X1, X2 ... Xn}为例，求一下的**一阶熵**和**实际信源熵**，其中Xi可能的字符为{1, 2, ..., m}：

* 一阶信息熵 (独立同分布i.i.d.)

![f4]

![f5]

其中，Gn 为整个{X1, X2 ... Xn}序列的总信息量，H(S)为每个字符的平均信息量。

* 信源的熵

![f1]

![f2]

其中，Gn 为整个序列的总信息量，Hn为每个字符的平均信息量。香农证明，当n->+∞时，这个值将收敛于实际信源的熵H(S)，即：

![f3]

(这里书中为![f30]，并不是![f3]，按我理解为![f3])

[f1]: http://chart.apis.google.com/chart?cht=tx&chl=G_n=-n\sum_{i_1=1}^{i_1=m}\sum_{i_2=1}^{i_2=m}...\sum{}P(X_1=i_1,X_2=i_2,...,X_n=i_n)\times\log{P(X_1=i_1,X_2=i_2,...,X_n=i_n)}

[f2]: http://chart.apis.google.com/chart?cht=tx&chl=H_n=\frac{1}{n}G_n

[f3]: http://chart.apis.google.com/chart?cht=tx&chl=H(S)=\lim_{n\to+\infty}{H_n}

[f30]: http://chart.apis.google.com/chart?cht=tx&chl=H(S)=\lim_{n\to+\infty}{\frac{1}{n}H_n}

[f4]: http://chart.apis.google.com/chart?cht=tx&chl=G_n=-\sum_{i_1=1}^{i_1=m}P(X_1=i_1)\log{P(X_1=i_1)}

[f5]: http://chart.apis.google.com/chart?cht=tx&chl=H(S)=\frac{1}{n}G_n=-\sum{}P(X_i)\log{P(X_i)}

### 2. 无损压缩

应该注意的是，实际信源的熵我们几乎无法准确得知，只能估计，这个“估计”即我们对信源序列结构的假定(建立模型)。若我们假定这个序列的每个符号是独立同分布的(iid)，那么我们所估计的熵就是**一阶熵**；若我们观察到信源序列符合某种规律，那么我们可以降低对信源熵的估计值，[1]中举了两例：

1. 考虑序列`1 2 3 2 3 4 5 4 5 6 7 8 9 8 9 10`，若按照iid进行“建模”，那么单符号的熵为3.25 bit；若考虑到相邻之间最多差1，转换为`1 1 1 -1 1 1 1 -1 1 1 1 1 1 -1 1 1`，则只有两种符号，消除了一些相关性，再根据iid进行编码，则但符号熵仅为0.7 bit。

2. 考虑序列`1 2 1 2 3 3 3 3 1 2 3 3 3 3 1 2 3 3 1 2`，若一个字符为一个符号看做iid，则一阶熵为1.5 bit / 符号。若发现序列只存在`1 2`和`3 3`这两种字符对，一两个字符为一种符号进行计算，那么一阶熵为1 bit / 符号。

### 3. 信源建模

上一小节中提到我们只能估计信源的熵，这节所讲的数据模型基于我对书[1]中2.3节的理解。

估计所基于的模型决定了我们所观测到信息序列的熵，也是我们进行编码所需要存储空间的下界，所以一个好的模型(与实际状态更接近)可以开发出更高效的压缩算法。

**书[1]中提到的常见的建模思路包括：**

* **物理模型**
如声音产生的过程。

* **概率模型**
如iid一阶熵模型。

* **马尔可夫模型**
这一时刻的各符号概率不是独立的，和最近一个或者最近多个符号有关，比如k阶马尔可夫模型：![f6] 即当前的各符号概率分布只与最近k个符号有关，若k=1，则为一阶马尔可夫模型，只与上一时刻有关。举个例子，语音和图像编码算法常会用到一个受白噪声驱动的线性滤波器输出可以用一下差分方成表示：![f7]，其中ϵn是个白噪声过程。

[f6]:http://chart.apis.google.com/chart?cht=tx&chl=P(X_n|X_{n-1},...,x_{n-k})=P(x_n|x_{n-1},...,x_{n-k},...)

[f7]:http://chart.apis.google.com/chart?cht=tx&chl=x_n=\rho{}x_{n-1}%2B\epsilon_n

**书[2]中的第三章给出几种消灭相关性的常见方法：**

* **delta encoding**

有顺序的序列进行delta编码，平均信息熵会下降，考虑序列`0 1 2 3 4 5 6 7`，delta后为`0 1 1 1 1 1 1`，这样再编码H为1 bit。

* **符号分组**

同本文第二节中的例2。

* **重排**
类似于delta encoding的思想，如果允许对一个序列进行重排列，那么有利于压缩。


### 4. 算法信息论和Kolmogorov复杂度

[1]的2.5节和[2]的第三章中还提到了Kolmogorov复杂度：

序列x的Kolmogorov复杂度K(x)是生成x所需要的程序规模，这里的程序规模包括程序可能用到的所有输入。

Kologorov复杂度的一个分支为MDL原则(minimum desciption length)。假设我们有n个待选模型Mj可以表示序列x，那么最好的模型是所需描述比特数最小的模型，即MDL原则：

![f8]

[f8]:http://chart.apis.google.com/chart?cht=tx&chl=MDL=min_{j=1}^{n}(D_M_j%2BR_M_j(x))

上式中，Dmj是描述模型j需要的bit数，Rmj(x)是用模型j描述序列x所需要的bit数。这个式子可以说明，有些模型虽然可以拟合序列x特别好(即Rmj(x)很小)，但是可能模型太复杂，描述模型本身需要的空间(Dmj)太大，两者加和反而不是最优，用一些非最优的简单模型可能会达到更优的压缩效果。

---
[1] 《数据压缩导论(第4版)》第二章

[2] Understanding
Compression - DATA COMPRESSION FOR MODERN DEVELOPERS, https://books.google.com/books?id=Ii6rDAAAQBAJ&pg=PT46&lpg=PT46&dq=information+entropy+delta+encoding&source=bl&ots=GvI9ggE2jr&sig=ACfU3U0ptV_F8TgS0acePTDKak_QaEtApw&hl=en&sa=X&ved=2ahUKEwjTu8Pr_vbgAhUPKawKHeucACUQ6AEwD3oECAQQAQ#v=onepage&q=information%20entropy%20delta%20encoding&f=true

[3] 如何插入公式：https://developers.google.com/chart/infographics/docs/formulas?hl=en