from .node import Node

class AVL:
    def __init__(self):
        self.root = None
    
    def insert(self, obstacle):
        node = self.search(obstacle)
        if node is not None:
            print("Node with obstacle", obstacle, "already exists.")
        else:
            new_node = Node(obstacle)
            if self.root is None:
                self.root = new_node
            else:
                self.root = self._insert(self.root, new_node)
            
    def _insert(self, current_node, new_node):
        if new_node.obstacle < current_node.obstacle:
            if current_node.left is None:
                current_node.left = new_node
                new_node.parent = current_node
            else:
                current_node.left = self._insert(current_node.left, new_node)
        else:
            if current_node.right is None:
                current_node.right = new_node
                new_node.parent = current_node
            else:
                current_node.right = self._insert(current_node.right, new_node)

        # 🔹 1. Actualizar altura
        self._update_height(current_node)

        # 🔹 2. Balancear el nodo actual
        return self._balance(current_node)
        
    # Search for a obstacle in the AVL
    def search(self, obstacle):
        if self.root is None:
            print("The tree is empty.")
            return None
        else:
            return self._search(self.root, obstacle)

    def _search(self, current_node, obstacle):
        if current_node is None or current_node.obstacle == obstacle:
            return current_node
        elif obstacle < current_node.obstacle:
            return self._search(current_node.left, obstacle)
        else:
            return self._search(current_node.right, obstacle)
    
    # Balance node by obstacle
    def _balance(self, node):
        balance = self._get_balance(node)

        # LL
        if balance > 1 and self._get_balance(node.left) >= 0:
            return self._rotate_right(node)

        # LR
        if balance > 1 and self._get_balance(node.left) < 0:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        # RR
        if balance < -1 and self._get_balance(node.right) <= 0:
            return self._rotate_left(node)

        # RL
        if balance < -1 and self._get_balance(node.right) > 0:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node
    
    # Update the height of a node
    def _update_height(self, node):
        left_height = node.left.height if node.left else 0
        right_height = node.right.height if node.right else 0
        node.height = 1 + max(left_height, right_height)
    
    # Get the balance factor of a node
    def _get_balance(self, node):
        left_height = node.left.height if node.left else 0
        right_height = node.right.height if node.right else 0
        return left_height - right_height
    
    # Perform a right rotation
    def _rotate_right(self, y):
        x = y.left
        T2 = x.right

        # Perform rotation
        x.right = y
        y.left = T2

        # Update parents
        if T2 is not None:
            T2.parent = y
        x.parent = y.parent
        y.parent = x

        # Update heights
        self._update_height(y)
        self._update_height(x)

        return x

    # Perform a left rotation
    def _rotate_left(self, x):
        y = x.right
        T2 = y.left

        # Perform rotation
        y.left = x
        x.right = T2

        # Update parents
        if T2 is not None:
            T2.parent = x
        y.parent = x.parent
        x.parent = y

        # Update heights
        self._update_height(x)
        self._update_height(y)

        return y

    # Find the inorder predecessor (the maximum in the left subtree)
    def _getPredecessor(self, node):
        if node.left is not None:
            current = node.left
            while current.right is not None:
                current = current.right
            return current
        return None

    # Delete a node by obstacle
    def delete(self, obstacle):
        node_to_delete = self.search(obstacle)
        if node_to_delete is not None:
            self.root = self._delete(self.root, obstacle)

    def _delete(self, node, obstacle):
        if node is None:
            return node

        # Step 1: Perform standard BST delete
        if obstacle < node.obstacle:
            node.left = self._delete(node.left, obstacle)
        elif obstacle > node.obstacle:
            node.right = self._delete(node.right, obstacle)
        else:
            # Node to be deleted found
            
            # Case 1: Node with only one child or no child
            if node.left is None:
                temp = node.right
                if temp:
                    temp.parent = node.parent
                node = None
                return temp
            elif node.right is None:
                temp = node.left
                if temp:
                    temp.parent = node.parent
                node = None
                return temp
            
            # Case 2: Node with two children
            # Get the inorder predecessor (largest in left subtree)
            temp = self._getPredecessor(node)
            
            # Copy the predecessor's obstacle to this node
            node.obstacle = temp.obstacle
            
            # Delete the inorder predecessor
            node.left = self._delete(node.left, temp.obstacle)

        # If the tree had only one node then return
        if node is None:
            return node

        # Step 2: Update height of current node
        self._update_height(node)

        # Step 3: Get the balance factor
        balance = self._get_balance(node)

        # Step 4: Balance the tree if needed
        
        # Left Left Case
        if balance > 1 and self._get_balance(node.left) >= 0:
            return self._rotate_right(node)

        # Left Right Case
        if balance > 1 and self._get_balance(node.left) < 0:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        # Right Right Case
        if balance < -1 and self._get_balance(node.right) <= 0:
            return self._rotate_left(node)

        # Right Left Case
        if balance < -1 and self._get_balance(node.right) > 0:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    # Inorder traversal (left → root → right)
    def inorder(self, node=None):
        if node is None:
            node = self.root
        result = []
        if node.left:
            result.extend(self.inorder(node.left))
        result.append(node.obstacle)
        if node.right:
            result.extend(self.inorder(node.right))
        return result
    
    # Method to print the tree in console
    def print_tree(self, node=None, prefix="", is_left=True):
        if node is None:
            node = self.root
        if node is not None:
            # Print right subtree
            if node.right:
                new_prefix = prefix + ("│   " if is_left else "    ")
                self.print_tree(node.right, new_prefix, False)

            # Print current node
            connector = "└── " if is_left else "┌── "
            print(prefix + connector + str(node.obstacle))

            # Print left subtree
            if node.left:
                new_prefix = prefix + ("    " if is_left else "│   ")
                self.print_tree(node.left, new_prefix, True)