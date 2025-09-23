import pygame
import json

with open("config/carrito.json", "r") as file:
    carrito = json.load(file)

class Carrito():
    def __init__(self,x,y,imagenes):
        self.rect = pygame.Rect(0,0,carrito["ancho"],carrito["alto"]) #Creará un rectangulo que determina la forma del carrito
        self.rect.center=(x,y)
        self.imagenes = imagenes
        self.imagen_actual = imagenes[0]
        self.impulso_salto = carrito["salto"]
        self.ha_saltado = False 

    def dibujar(self, interfaz): #colocar carro en pantalla
        interfaz.blit(self.imagen_actual, self.rect) #poner imagen en pantalla
        #pygame.draw.rect(interfaz,carrito["colorDefault"], self.rect, 1)
        
    def movimiento(self, delta_y,salta): 
        if self.ha_saltado:
            self.imagen_actual = self.imagenes[1]
            if self.impulso_salto >= -carrito["salto"]:
                if self.impulso_salto < 0:
                    self.rect.y += (self.impulso_salto**2)*0.5
                else:
                    self.rect.y -= (self.impulso_salto**2)*0.5
                self.impulso_salto -= 1
            else:
                self.ha_saltado = False
                self.impulso_salto = carrito["salto"]
                self.imagen_actual = self.imagenes[0]
        else:
            self.rect.y = self.rect.y + delta_y #cordenada siguiente = la actual + px a mover
            if salta:
                self.ha_saltado = True