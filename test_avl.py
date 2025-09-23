from avl.avl import AVL

if __name__ == "__main__":
    avl = AVL()

    valores = [50, 30, 70, 20, 40, 60, 80,
               10, 25, 35, 45, 55, 65, 75, 85,
               5, 15, 33, 43, 90, 1]

    for v in valores:
        avl.insert(v)

    print("Original tree")
    avl.print_tree(avl.root)
    print("\n")

    print("Initial inorder traversal (sorted order):")
    avl.inorder()
    print("\n")

     # Test deletions
    print("insert a leaf (91):")
    avl.insert(91)
    avl.print_tree(avl.root)
    avl.inorder()
    print("\n")

     # Test deletions
    print("insert a leaf (15):")
    avl.insert(15)
    avl.print_tree(avl.root)
    avl.inorder()
    print("\n")

    # Test deletions
    print("Delete a leaf (50):")
    avl.delete(50)
    avl.print_tree(avl.root)
    avl.inorder()
    print("\n")

    print("Delete a node with one child (85):")
    avl.delete(85)
    avl.print_tree(avl.root)
    avl.inorder()
    print("\n")

    print("Delete a node with two children (10):")
    avl.delete(10)
    avl.print_tree(avl.root)
    avl.inorder()
    print("\n")

    print("Delete the root (33):")
    avl.delete(33)
    avl.print_tree(avl.root)
    avl.inorder()
    print("\n")

    print("Delete another node with two children (70):")
    avl.delete(70)
    avl.print_tree(avl.root)
    avl.inorder()
    print("\n")

    print("Delete a rightmost node (65):")
    avl.delete(65)
    avl.print_tree(avl.root)
    avl.inorder()
    print("\n")
