## 动态规划(DP)

#### 最大子段和问题

`dp[i]`表示到前i个数的最大子段和，则：
```
dp[i] = max(nums[i], nums[i] + dp[i-1])
```
注意这里以为数组dp[N]可以简化为一个变量dp，复杂度仅为O(n)。

#### 最大公共子序列问题 与 最长公共子串问题

子序列各个元素不必连续，只要顺序不颠倒；子串则要求是原串中的连续一段。

* 最大公共子序列 (Longest Common Subsequence)

```
dp[i][j] = 0  (i == 0 || j == 0)
         = dp[i-1][j-1] + 1 (s1[i] == s2[j])
         = max(dp[i-1][j], dp[i][j-1])  (s1[i] != s2[j])
```

* 最长公共子串 (Longest Common Substring)

```
dp[i][j] = 0  (i == 0 || j == 0)
         = 0  (s1[i] != s2[j])
         = dp[i-1][j-1] + 1 (s1[i] == s2[j])
```

#### 0-1背包问题

```
// Wi和Vi分别表示第i件物品的价值和体积
// dp[i][j]表示前i件物品在背包容量j的情况下可以获得的最大价值
dp[i][j] = 0              (i == 0 && j < V[i])
         = W[i]           (i == 0 && j >= V[i])  
         = dp[i-1][j] = 0 (j < V[i])
         = max(dp[i-1][j], dp[i-1][j-V[i]] + W[i])
```

实现时dp还可以优化为一维数组，这是因为i会从0到I-1进行遍历，而每次更新`dp[i][j]`时只与`dp[i-1][xxx]`有关，而我们最后只需要`dp[I][J]`的值，所以直接让i从0到I-1在外层循环，而dp数组可以缩减为1维：
```python
for i in range(1, N):
    for v in range(V, Vi, -1):
        dp[v] = max(dp[v], dp[v-Vi] + Wi)
```


