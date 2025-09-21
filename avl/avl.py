from .node import Node

class Avl:
    def _init_(self):
        self.root = None
    
    def insert(self, obstacle):
        node = self.search(obstacle)
        if node is not None :
            print("Node with obstacle", obstacle, "already exists." )
        else:
            new_node = Node(obstacle)
            if self.root is None:
                self.root = new_node
            else:
                self._insert(self.root, new_node)
                self._balance(new_node)
            
    def _insert(self, current_node, new_node):
        if new_node.obstacle < current_node.obstacle:
            if current_node.left is None:
                current_node.left = new_node
                new_node.parent = current_node
            else:
                self._insert(current_node.left, new_node)
        else:
            if current_node.right is None:
                current_node.right = new_node
                new_node.parent = current_node
            else:
                self._insert(current_node.right, new_node)   
    
    # Search for a obstacle in the AVL
    def search(self, obstacle):
        if(self.root is None):
            print("The tree is empty.")
            return None
        else:
            return self._search(self.root, obstacle)

    def _search(self, current_node, obstacle):
        if current_node is Node or current_node.obstacle == obstacle:
            return current_node
        elif obstacle < current_node.obstacle and current_node.left is not None:
            return self._search(current_node.left, obstacle)
        elif obstacle > current_node.obstacle and current_node.right is not None:
            return self._search(current_node.right, obstacle)
        return None
    
    #  balance node by obstacle
    def _balance(self, node):
        while node is not None:
            self._update_height(node)
            balance = self._get_balance(node)

            # Caso LR o LL
            if balance > 1:
                if self._get_balance(node.left) < 0:
                    self._rotate_left(node.left)  # LR 
                self._rotate_right(node) # LL

            # Caso RL o RR
            elif balance < -1:
                if self._get_balance(node.right) > 0:
                    self._rotate_right(node.right) # RL
                self._rotate_left(node) # RR
            node = node.parent
    
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
        if y.parent is None:  # y was root
            self.root = x
        elif y == y.parent.left:
            y.parent.left = x
        else:
            y.parent.right = x
        y.parent = x

        # Update heights
        self._update_height(y)
        self._update_height(x)
    
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
        if x.parent is None:  # x was root
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        x.parent = y

        # Update heights
        self._update_height(x)
        self._update_height(y)
    

    # Find the inorder predecessor (the maximum in the left subtree)
    def _getPredecessor(self, node):
        if node.left is not None:
            current = node.left
            while current.right is not None:
                current = current.right
            return current
        return None

    # Replace one subtree with another (adjusts parent references)
    def changeNodePosition(self, node_to_replace, new_subtree_root):
        if node_to_replace.parent is None:  # If replacing the root
            self.root = new_subtree_root
        else:
            if node_to_replace == node_to_replace.parent.left:
                node_to_replace.parent.left = new_subtree_root
            else:
                node_to_replace.parent.right = new_subtree_root
        if new_subtree_root is not None:
            new_subtree_root.parent = node_to_replace.parent

    # Delete a node by obstacle
    def delete(self, obstacle):
        node_to_delete = self.search(obstacle)
        if node_to_delete is not None:
            parent = node_to_delete.parent
            self._delete(node_to_delete)
            # balancear hacia arriba
            if parent:
                self._balance(parent)
            elif self.root:  # Si el nodo eliminado era la raíz
                self._balance(self.root)

    def _delete(self, node_to_delete):
        parent = node_to_delete.parent
        # Case 1: node is a leaf (no children)
        if node_to_delete.left is None and node_to_delete.right is None:  
            self.changeNodePosition(node_to_delete, None)
            return
    
        # Case 2: node has two children
        if node_to_delete.left is not None and node_to_delete.right is not None:
            predecessor = self._getPredecessor(node_to_delete)
            if predecessor.parent != node_to_delete:  # predecessor is not a direct child
                self.changeNodePosition(predecessor, predecessor.left)
                predecessor.left = node_to_delete.left
                predecessor.left.parent = predecessor
                
            self.changeNodePosition(node_to_delete, predecessor)
            predecessor.right = node_to_delete.right
            predecessor.right.parent = predecessor
            return

        # Case 3: node has only one child
        if node_to_delete.left is not None:
            self.changeNodePosition(node_to_delete, node_to_delete.left)
        else:
            self.changeNodePosition(node_to_delete, node_to_delete.right)

        # Actualizar altura y balancear desde el padre hacia arriba
        if parent:
            self._update_height(parent)
            self._balance(parent)
        elif self.root:   # Si eliminaste la raíz
            self._update_height(self.root)
            self._balance(self.root)
