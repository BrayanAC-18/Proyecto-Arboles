# from avl.avl import AVL

# if __name__ == "__main__":
#     avl = AVL()

#     valores = [50, 30, 70, 20, 40, 60, 80,
#                10, 25, 35, 45, 55, 65, 75, 85,
#                5, 15, 33, 43, 90, 1]

#     for v in valores:
#         avl.insert(v)

#     print("Original tree")
#     avl.print_tree(avl.root)
#     print("\n")

#     print("Initial inorder traversal (sorted order):")
#     avl.inorder()
#     print("\n")

#      # Test deletions
#     print("insert a leaf (91):")
#     avl.insert(91)
#     avl.print_tree(avl.root)
#     avl.inorder()
#     print("\n")

#      # Test deletions
#     print("insert a leaf (15):")
#     avl.insert(15)
#     avl.print_tree(avl.root)
#     avl.inorder()
#     print("\n")

#     # Test deletions
#     print("Delete a leaf (50):")
#     avl.delete(50)
#     avl.print_tree(avl.root)
#     avl.inorder()
#     print("\n")

#     print("Delete a node with one child (85):")
#     avl.delete(85)
#     avl.print_tree(avl.root)
#     avl.inorder()
#     print("\n")

#     print("Delete a node with two children (10):")
#     avl.delete(10)
#     avl.print_tree(avl.root)
#     avl.inorder()
#     print("\n")

#     print("Delete the root (33):")
#     avl.delete(33)
#     avl.print_tree(avl.root)
#     avl.inorder()
#     print("\n")

#     print("Delete another node with two children (70):")
#     avl.delete(70)
#     avl.print_tree(avl.root)
#     avl.inorder()
#     print("\n")

#     print("Delete a rightmost node (65):")
#     avl.delete(65)
#     avl.print_tree(avl.root)
#     avl.inorder()
#     print("\n")

import json
from models.obstaculos import Obstacle
from avl.avl import AVL
import pygame
from controller.grafico_avl import draw_avl 


# Crear el AVL
avl = AVL()

# Abrir el JSON
with open("config/config.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Tomar la lista de obstáculos
for obj in data["obstaculos"]:
    obs = Obstacle(
        obj["id"],
        obj["tipo"],
        obj["posX"],
        obj["posY"],
        obj["ancho"],
        obj["alto"],
        obj["imagen"],
        obj["daño"]   # cuidado con la tilde en tu JSON
    )
    avl.insert(obs)

pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("AVL Obstáculos")
font = pygame.font.SysFont(None, 18)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255,255,255))

    # Dibujar árbol desde la raíz
    draw_avl(screen, avl.root, 400, 50, 150, 80, font)

    pygame.display.flip()

pygame.quit()
