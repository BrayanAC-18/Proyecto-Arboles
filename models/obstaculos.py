import pygame
import os

class Obstacle:
    def __init__(self, id_, tipo, posX, posY, ancho, alto, imagen):
        #Clase para representar un obstáculo en la carretera.
        
        self.id = id_
        self.tipo = tipo
        self.posX = posX
        self.posY = posY
        self.ancho = ancho
        self.alto = alto
        self.imagen = pygame.image.load(imagen).convert_alpha()
        self.imagen = pygame.transform.scale(self.imagen, (self.ancho, self.alto))

        # Para detección de colisiones
        #self.rect = pygame.Rect(self.x, self.y, self.ancho, self.altot)

        # 🔹 Ruta absoluta relativa al proyecto
        base_path = os.path.dirname(os.path.dirname(__file__))  # sube a raíz del proyecto
        image_path = os.path.join(base_path, imagen)

        if not os.path.exists(image_path):
            raise FileNotFoundError(f"No se encontró la imagen: {image_path}")

        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.ancho, self.alto))
        self.rect = pygame.Rect(self.posX, self.posY, self.ancho, self.alto)
        

    def update_rect(self, offset_x=0):
        #Actualizar rectángulo de colisión con el offset de la carretera.
        self.rect.topleft = (self.x + offset_x, self.y)

    def draw(self, surface, offset_x=0):
        #Dibuja el obstáculo en la pantalla considerando el offset de la carretera.
        surface.blit(self.image, (self.posX + offset_x, self.posY))

    def __repr__(self):
        return f"Obstacle(id={self.id}, tipo={self.tipo}, pos=({self.posX},{self.posY}))"
