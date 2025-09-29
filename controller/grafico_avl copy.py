import pygame

def draw_avl(surface, node, x, y, dx, dy, font, radius=10, level=0):
    if node is None:
        return

    # Dibujar ramas
    if node.left:
        pygame.draw.line(surface, (0, 0, 0), (x, y), (x - dx, y + dy), 2)
        draw_avl(surface, node.left, x - dx, y + dy, int(dx*0.6), dy, font, radius, level+1)
    if node.right:
        pygame.draw.line(surface, (0, 0, 0), (x, y), (x + dx, y + dy), 2)
        draw_avl(surface, node.right, x + dx, y + dy, int(dx*0.6), dy, font, radius, level+1)

    # Nodo
    pygame.draw.circle(surface, (200, 200, 255), (x, y), radius)
    pygame.draw.circle(surface, (0, 0, 0), (x, y), radius, 2)

    # Texto coordenadas
    coords_text = font.render(f"({node.obstacle.posX},{node.obstacle.posY})", True, (0, 0, 0))
    coords_rect = coords_text.get_rect(center=(x, y))
    surface.blit(coords_text, coords_rect)

    # Texto tipo
    name_text = font.render(node.obstacle.tipo, True, (0, 0, 0))
    name_rect = name_text.get_rect(center=(x, y + radius + 12))
    surface.blit(name_text, name_rect)
