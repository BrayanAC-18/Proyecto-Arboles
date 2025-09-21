class Node:
    def __init__(self,  obstacle, parent=None):
        self.obstacle = obstacle
        self.left = None
        self.right = None
        self.parent = parent
        self.height = 1

    #Clave del nodo (x1, y1) usada para ordenar en el AVL
    def key(self):
        return self.obstacle.id
    
    def __repr__(self):
        return f"Node({self.obstacle})"