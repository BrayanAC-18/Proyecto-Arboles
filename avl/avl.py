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
        
    # Buscar un obstáculo en el AVL
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
    
    # Balancear un nodo según el obstáculo
    def _balance(self, node):
        balance = self._get_balance(node)

        # Caso LL
        if balance > 1 and self._get_balance(node.left) >= 0:
            return self._rotate_right(node)

        # Caso LR
        if balance > 1 and self._get_balance(node.left) < 0:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        # Caso RR
        if balance < -1 and self._get_balance(node.right) <= 0:
            return self._rotate_left(node)

        # Caso RL
        if balance < -1 and self._get_balance(node.right) > 0:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node
    
    # Actualizar la altura de un nodo
    def _update_height(self, node):
        left_height = node.left.height if node.left else 0
        right_height = node.right.height if node.right else 0
        node.height = 1 + max(left_height, right_height)
    
    # Obtener el factor de balance de un nodo
    def _get_balance(self, node):
        left_height = node.left.height if node.left else 0
        right_height = node.right.height if node.right else 0
        return left_height - right_height
    
    # Realizar una rotación a la derecha
    def _rotate_right(self, y):
        x = y.left
        T2 = x.right

        # Realizar la rotación
        x.right = y
        y.left = T2

        # Actualizar padres
        if T2 is not None:
            T2.parent = y
        x.parent = y.parent
        y.parent = x

        # Actualizar alturas
        self._update_height(y)
        self._update_height(x)

        return x

    # Realizar una rotación a la izquierda
    def _rotate_left(self, x):
        y = x.right
        T2 = y.left

        # Realizar la rotación
        y.left = x
        x.right = T2

        # Actualizar padres
        if T2 is not None:
            T2.parent = x
        y.parent = x.parent
        x.parent = y

        # Actualizar alturas
        self._update_height(x)
        self._update_height(y)

        return y

    # Encontrar el predecesor en inorden (el máximo en el subárbol izquierdo)
    def _getPredecessor(self, node):
        if node.left is not None:
            current = node.left
            while current.right is not None:
                current = current.right
            return current
        return None

    # Eliminar un nodo por obstáculo
    def delete(self, obstacle):
        node_to_delete = self.search(obstacle)
        if node_to_delete is not None:
            self.root = self._delete(self.root, obstacle)

    def _delete(self, node, obstacle):
        if node is None:
            return node

        # Paso 1: realizar eliminación estándar en BST
        if obstacle < node.obstacle:
            node.left = self._delete(node.left, obstacle)
        elif obstacle > node.obstacle:
            node.right = self._delete(node.right, obstacle)
        else:
            # Nodo a eliminar encontrado
            
            # Caso 1: Nodo con solo un hijo o sin hijos
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
            
            # Caso 2: Nodo con dos hijos
            # Obtener el predecesor en inorden (máximo en subárbol izquierdo)
            temp = self._getPredecessor(node)
            
            # Copiar el obstáculo del predecesor en este nodo
            node.obstacle = temp.obstacle
            
            # Eliminar el predecesor en inorden
            node.left = self._delete(node.left, temp.obstacle)

        # Si el árbol solo tenía un nodo, retornar
        if node is None:
            return node

        # Paso 2: Actualizar altura del nodo actual
        self._update_height(node)

        # Paso 3: Obtener el factor de balance
        balance = self._get_balance(node)

        # Paso 4: Balancear el árbol si es necesario
        
        # Caso Left Left
        if balance > 1 and self._get_balance(node.left) >= 0:
            return self._rotate_right(node)

        # Caso Left Right
        if balance > 1 and self._get_balance(node.left) < 0:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        # Caso Right Right
        if balance < -1 and self._get_balance(node.right) <= 0:
            return self._rotate_left(node)

        # Caso Right Left
        if balance < -1 and self._get_balance(node.right) > 0:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    # Recorrido inorden (izquierda → raíz → derecha)
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
    
    # Método para imprimir el árbol en consola
    def print_tree(self, node=None, prefix="", is_left=True):
        if node is None:
            node = self.root
        if node is not None:
            # Imprimir subárbol derecho
            if node.right:
                new_prefix = prefix + ("│   " if is_left else "    ")
                self.print_tree(node.right, new_prefix, False)

            # Imprimir nodo actual
            connector = "└── " if is_left else "┌── "
            print(prefix + connector + str(node.obstacle))

            # Imprimir subárbol izquierdo
            if node.left:
                new_prefix = prefix + ("    " if is_left else "│   ")
                self.print_tree(node.left, new_prefix, True)
