import pygame
import json

with open("carrito.json", "r") as file:
    carrito = json.load(file)

class Carrito():
    def __init__(self,x,y,image):
        self.forma = pygame.Rect(0,0,carrito["ancho"],carrito["alto"]) #Creará un rectangulo que determina la forma del carrito
        self.forma.center=(x,y)
        self.image = image

    def dibujar(self, interfaz): #colocar carro en pantalla
        interfaz.blit(self.image, self.forma) #poner imagen en pantalla
        #pygame.draw.rect(interfaz,carrito["colorDefault"], self.forma, 1)
        
    def movimiento(self, delta_y): 
        self.forma.y = self.forma.y + delta_y #cordenada siguiente = la actual + px a mover
        