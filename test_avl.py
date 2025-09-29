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

# Cargar obstáculos del JSON
for obj in data["obstaculos"]:
    obs = Obstacle(
        obj["id"],
        obj["tipo"],
        obj["posX"],
        obj["posY"],
        obj["ancho"],
        obj["alto"],
        obj["imagen"],
        obj["daño"]
    )
    avl.insert(obs)

pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("AVL Obstáculos")
font = pygame.font.SysFont(None, 18)

running = True
nuevo_id = 100  # ID inicial para nuevos obstáculos
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Insertar un obstáculo de prueba cada ENTER
                obs = Obstacle(
                    nuevo_id,
                    "nuevo",
                    0,  # posX por defecto
                    100,  # posY por defecto
                    50, 50,  # ancho y alto
                    None,  # imagen vacía
                    5  # daño
                )
                obs.id = nuevo_id
                avl.insert(obs)
                print(f"Se insertó el obstáculo {nuevo_id}")
                nuevo_id += 1

    screen.fill((255,255,255))
    draw_avl(screen, avl.root, 400, 50, 150, 80, font)
    pygame.display.flip()

pygame.quit()
