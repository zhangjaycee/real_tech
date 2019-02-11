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