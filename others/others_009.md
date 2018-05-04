# 机器学习
# 机器学习


## 1. 分类模型和参数估计问题

[[ml_001.png]]

### 1.1 生成式模型和判别式模型

例如，生成式模型包括最大似然估计（MLE）、朴素贝叶斯（Naive Bayes, NB）、KNN等；而判别式模型包括线性回归、逻辑回归、BP神经网络、决策树、SVM等。

生成式对 ![f13] 建模，进而可以由贝叶斯公式 ![f14] 得出 ![f15] ，这种分类器会输出当前的特征值 ![f12] 在各个类别的模型的概率值，一般可以分类为 ![f12] 特征下概率最大的类别。一个样本进入生成式分类器时，对于每个类别，生成式分类器会给出概率，每个比如朴素贝叶斯中，先对类别a、b和c分别计算分类概率值（各个特征的概率连乘），取最大的一个概率打类别标签；MLE最大似然估计中，可能会假定每个类都服从高斯分布，估计出这些参数后，再直接用高斯分布求出对应样本属于各个类别的概率，再像朴素贝叶斯一样，取一个概率最大的作为分类结果。

判别式对 ![f10] 建模，其中 ![f11] 是类别， ![f12] 是样本的特征，这种分类器直接输出样本属于各个类别的概率，若不考虑各个类别的错误分类代价差异，则应该分类为概率最大的那一类。


[f10]: http://chart.apis.google.com/chart?cht=tx&chl=P(c_i|\vec{x})
[f11]: http://chart.apis.google.com/chart?cht=tx&chl=c_i
[f12]: http://chart.apis.google.com/chart?cht=tx&chl=\vec{x}
[f13]: http://chart.apis.google.com/chart?cht=tx&chl=P(c_i,\vec{x})
[f14]: http://chart.apis.google.com/chart?cht=tx&chl=P(\vec{x}|c_i)=\frac{P(c_i,\vec{x})}{P(\vec{x})}
[f15]: http://chart.apis.google.com/chart?cht=tx&chl=P(\vec{x}|c_i)

### 1.2 参数估计和非参数估计


举例来说：

生成式模型中：参数密度估计包括最大似然估计（MLE）等，非参数密度估计包括朴素贝叶斯（Naive Bayes, NB）？、K近邻（KNN）、核函数估计（KDE）等。

判别式模型中：参数估计包括逻辑回归（属于分类问题）、线性回归（属于回归问题）、多层感知器、神经网络等；非参数估计包括分类决策树CART等。

简单说，参数估计可以假定某类符合某种分布，比如高斯分布由均值μ和协方差![f20]两个参数决定，估计各个类对应的两个参数，就估计出了各个类的高斯模型。而非参数估计并不预先服从某个分布，由训练样本直接进行估计

[f20]: http://chart.apis.google.com/chart?cht=tx&chl=\sum


### 1.3 回归和分类

线性回归用于回归，而逻辑回归用于分类。








[f2]: http://chart.apis.google.com/chart?cht=tx&chl=\sum