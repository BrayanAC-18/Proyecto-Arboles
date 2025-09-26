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

    # Texto con tipo y coordenadas
    text = font.render(
        f"{node.obstacle.tipo} ({node.obstacle.posX},{node.obstacle.posY})",
        True,
        (0,0,0)
    )
    rect = text.get_rect(center=(x,y))
    surface.blit(text, rect)




