# 二叉树的遍历

## 1. 非递归：

#### 前序
https://leetcode.com/problems/binary-tree-preorder-traversal/
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
https://leetcode.com/problems/binary-tree-inorder-traversal/
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
https://leetcode.com/problems/binary-tree-postorder-traversal/
```cpp
vector<int> postorderTraversal(TreeNode* root) {
    vector<int> res;
    if (!root)
        return res;
    TreeNode *cur = root;
    stack<TreeNode *> st;
    while (!st.empty() || cur != NULL) {
        while (cur != NULL) {
            res.push_back(cur->val);
            st.push(cur);
            cur = cur->right;
        }
        if (!st.empty()) {
            cur = st.top();
            st.pop();
            cur = cur->left;
        }
    }
    reverse(res.begin(), res.end());
    return res;
}
```

## 2. 递归

* 前序

```cpp
vector<int> preorderTraversal(TreeNode* root) {
    vector<int> res;
    if (!root) 
        return res;
    traverse(root, res);
    return res;    
}
void traverse(TreeNode *p, vector<int> &res) {
    if (p == NULL)
        return;
    res.push_back(p->val);
    traverse(p->left, res);
    traverse(p->right, res);
    return;
}
```

* 中序
```cpp
vector<int> inorderTraversal(TreeNode* root) {
    vector<int> res;
    if (!root)
        return res;
    traverse(root, res);
    return res;
}
void traverse(TreeNode *root, vector<int> &res) {
    if (!root)
        return;
    traverse(root->left, res);
    res.push_back(root->val);
    traverse(root->right, res);
}
```

* 后序
```cpp
vector<int> postorderTraversal(TreeNode* root) {
    vector<int> res;
    if (!root)
        return res;
    traverse(root, res);
    return res;
}
void traverse(TreeNode *root, vector<int> &res) {
    if (!root)
        return;
    traverse(root->left, res);
    traverse(root->right, res);
    res.push_back(root->val);
}
```

## 3. 二叉树 --> 双向链表


> 输入一棵二叉搜索树，将该二叉搜索树转换成一个排序的双向链表。要求不能创建任何新的结点，只能调整树中结点指针的指向。

其实是中序遍历的变种：


* 递归

```cpp
class Solution {
public:
    TreeNode* Convert(TreeNode* root)
    {
        if (!root)
            return NULL;
        TreeNode *l = Convert(root->left);
        TreeNode *head = l;
        if (l != NULL) {
            while (l->right) {
                l = l->right;
            }
            l->right = root;
            root->left = l;
        } else {
            head = root;
        }
        TreeNode *r = Convert(root->right);
        root->right = r;
        if (r)
            r->left = root;
        return head;
    }
};
```

* 非递归

```cpp
TreeNode* Convert(TreeNode* root)
{
    if (!root)
        return NULL;
    stack<TreeNode *> st;
    TreeNode *cur = root;
    TreeNode *head = NULL;
    TreeNode *pre_node = NULL;
    while (cur || !st.empty()) {
        while (cur) {
            st.push(cur);
            cur = cur->left;
        }
        if (!st.empty()) {
            cur = st.top(); st.pop();
            if (!head) {
                head = pre_node = cur;
            } else {
                pre_node->right = cur;
                cur->left = pre_node;
                pre_node = cur;
            }
            cur = cur->right;
        }
    }
    return head;
}
```




