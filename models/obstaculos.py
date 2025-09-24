import pygame
import os

class Obstacle:
    def __init__(self, id_, tipo, posX, posY, ancho, alto, imagen):
        self.id = id_
        self.tipo = tipo
        self.posX = posX
        self.posY = posY
        self.ancho = ancho
        self.alto = alto

        # Ruta absoluta
        base_path = os.path.dirname(os.path.dirname(__file__))  # sube a raíz del proyecto
        image_path = os.path.join(base_path, imagen)

        if not os.path.exists(image_path):
            raise FileNotFoundError(f"No se encontró la imagen: {image_path}")

        # Cargar imagen
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.ancho, self.alto))

        # Rectángulo de colisión
        self.rect = pygame.Rect(self.posX, self.posY, self.ancho, self.alto)

    #ctualizar rectángulo de colisión con desplazamiento horizontal
    def update_rect(self, offset_x=0):
        self.rect.topleft = (self.posX + offset_x, self.posY)

    #Dibuja el obstáculo en pantalla con desplazamiento opcional
    def draw(self, surface, offset_x=0):
        surface.blit(self.image, (self.posX + offset_x, self.posY))

    def __repr__(self):
        return f"Obstacle(id={self.id}, tipo={self.tipo}, pos=({self.posX},{self.posY}))"

    # 🔹 Métodos de comparación para el AVL
    def __lt__(self, other):
        if self.posX == other.posX:
            return self.posY < other.posY
        return self.posX < other.posX

    def __gt__(self, other):
        if self.posX == other.posX:
            return self.posY > other.posY
        return self.posX > other.posX

    def __eq__(self, other):
        return self.posX == other.posX and self.posY == other.posY
