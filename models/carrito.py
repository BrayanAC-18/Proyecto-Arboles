import pygame

class Carrito():
    def __init__(self,x,y,imagenes, config):
        self.config = config
        self.rect = pygame.Rect(0,0,self.config["carrito"]["ancho"],self.config["carrito"]["alto"]) #Creará un rectangulo que determina la forma del carrito
        self.rect.center=(x,y)
        self.imagenes = imagenes
        self.imagen_actual = imagenes[0]
        
        # Variables de salto simplificadas
        self.esta_saltando = False
        self.velocidad_salto = 0
        self.gravedad = 1  # Ajusta este valor para cambiar la altura del salto
        self.fuerza_salto = -self.config["carrito"]["salto"]*self.config["carretera"]["pixeles_metro"]  # Valor negativo porque Y aumenta hacia abajo en pygame
        self.posicion_base_y = y  # Guardamos la posición original en Y
        
    
    def dibujar(self, interfaz): #colocar carro en pantalla
        interfaz.blit(self.imagen_actual, self.rect) #poner imagen en pantalla
        #pygame.draw.rect(interfaz,carrito["colorDefault"], self.rect, 1)
        
    def movimiento(self, delta_y, salta):
        # Si no está saltando, aplicamos el movimiento normal
        if not self.esta_saltando:
            self.rect.y += delta_y
            self.posicion_base_y = self.rect.y  # Actualizamos la posición base
            
            # Si se presiona salto y no está saltando
            if salta:
                self.esta_saltando = True
                self.velocidad_salto = self.fuerza_salto
                self.imagen_actual = self.imagenes[1]
        else:
            # Lógica del salto
            self.rect.y += self.velocidad_salto
            self.velocidad_salto += self.gravedad
            
            # Si vuelve a la posición base, termina el salto
            if self.rect.y >= self.posicion_base_y:
                self.rect.y = self.posicion_base_y
                self.esta_saltando = False
                self.velocidad_salto = 0
                self.imagen_actual = self.imagenes[0]