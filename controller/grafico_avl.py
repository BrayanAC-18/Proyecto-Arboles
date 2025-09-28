import pygame

import pygame

def draw_avl(surface, node, x, y, dx, dy, font):
    if node is None:
        return

    # Dibujar ramas
    if node.left:
        pygame.draw.line(surface, (0,0,0), (x, y), (x - dx, y + dy), 2)
        draw_avl(surface, node.left, x - dx, y + dy, dx//2, dy, font)
    if node.right:
        pygame.draw.line(surface, (0,0,0), (x, y), (x + dx, y + dy), 2)
        draw_avl(surface, node.right, x + dx, y + dy, dx//2, dy, font)

    # Dibujar nodo (círculo)
    pygame.draw.circle(surface, (200,200,255), (x, y), 30)
    pygame.draw.circle(surface, (0,0,0), (x, y), 30, 2)

      # Texto dentro del nodo (coordenadas)
    coords_text = font.render(f"({node.obstacle.posX},{node.obstacle.posY})", True, (0,0,0))
    coords_rect = coords_text.get_rect(center=(x, y))
    surface.blit(coords_text, coords_rect)

    # Texto debajo (tipo de obstáculo)
    name_text = font.render(node.obstacle.tipo, True, (0,0,0))
    name_rect = name_text.get_rect(center=(x, y + 35))
    surface.blit(name_text, name_rect)



