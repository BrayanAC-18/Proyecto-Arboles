import pygame
import os

class Obstacle:
    def __init__(self, id_, tipo, posX, posY, ancho, alto, imagen="", daño=0):
        self.id = id_
        self.tipo = tipo
        self.posX = posX
        self.posY = posY
        self.ancho = ancho
        self.alto = alto
        self.daño = daño
        self.tocado = False

        # Si se pasa una imagen válida, cargarla
        if imagen and os.path.exists(imagen):
            self.image = pygame.image.load(imagen)
            self.image = pygame.transform.scale(self.image, (self.ancho, self.alto))
            self.use_text = False
        else:
            # Crear un rectángulo de color y usar texto
            self.image = pygame.Surface((self.ancho, self.alto))
            self.image.fill((200, 100, 100))  # color del rectángulo
            self.use_text = True

        self.rect = pygame.Rect(self.posX, self.posY, self.ancho, self.alto)

    # Dibujar obstáculo
    def draw(self, surface, offset_x=0):
        surface.blit(self.image, (self.posX + offset_x, self.posY))
        if self.use_text:
            # Fuente pequeña para mostrar el nombre
            font = pygame.font.SysFont(None, 20)
            text_surf = font.render(self.tipo, True, (0, 0, 0))
            text_rect = text_surf.get_rect(center=(self.posX + offset_x + self.ancho//2, self.posY + self.alto//2))
            surface.blit(text_surf, text_rect)

    def __repr__(self):
        return f"Obstacle(id={self.id}, tipo={self.tipo}, pos=({self.posX},{self.posY}))"
    
    def __eq__(self, other):
        return isinstance(other, Obstacle) and (self.posX, self.posY) == (other.posX, other.posY)

    def __lt__(self, other):
        return isinstance(other, Obstacle) and (self.posX, self.posY) < (other.posX, other.posY)

    def __gt__(self, other):
        return isinstance(other, Obstacle) and (self.posX, self.posY) > (other.posX, other.posY)
