class Solution:
    def mergeTrees(
        self, root1: TreeNode | None, root2: TreeNode | None
    ) -> TreeNode | None:
        if not root1:
            return root2
        if not root2:
            return root1

        stack = [(root1, root2)]

        while stack:
            n1, n2 = stack.pop()

            if not n1 or not n2:
                continue

            n1.val += n2.val

            if not n1.left:
                n1.left = n2.left
            else:
                stack.append((n1.left, n2.left))

            if not n1.right:
                n1.right = n2.right
            else:
                stack.append((n1.right, n2.right))

        return root1