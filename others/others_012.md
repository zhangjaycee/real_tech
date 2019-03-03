# 二叉树的遍历

## 1. 非递归：

#### 前序

```cpp
vector<int> preorderTraversal(TreeNode* root) {
    vector<int> res;
    if (!root)
        return res;
    stack<TreeNode *> st;
    TreeNode *p = root;
    while (p != nullptr || !st.empty()) {
        while (p != nullptr) {
            res.push_back(p->val);
            st.push(p);
            p = p->left;
        }
        if (!st.empty()) {
            p = st.top();
            st.pop();
            p = p->right;
        }
    }
    return res;
}
```

#### 中序

```cpp
vector<int> inorderTraversal(TreeNode* root) {
    vector<int> res;
    if (!root)
        return res;
    stack<TreeNode *> st;
    TreeNode *cur = root;
    while (!st.empty() || cur != NULL) {
        if (cur != NULL) {
            st.push(cur);
            cur = cur->left;
        } else if (!st.empty()) {
            cur = st.top();
            st.pop();
            res.push_back(cur->val);
            cur = cur->right;
        }
    }
    return res;
}
```

#### 后序

```cpp


```


## 2. 二叉树 --> 双向链表