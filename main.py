import pygame
import json
from carrito import Carrito

pygame.init() #inicializa pygame

with open("ventana.json", "r") as file: 
    ventana = json.load(file)

with open("carrito.json", "r") as file: 
    carrito = json.load(file)

display = pygame.display.set_mode((ventana["ancho"],ventana["alto"]))
pygame.display.set_caption("Juego del Carrito")
reloj = pygame.time.Clock()

ImagenJugador = pygame.image.load("assets/images/car/car_1.png")
ImagenJugador = pygame.transform.scale(ImagenJugador,
                                       (ImagenJugador.get_width()*carrito["escala"],(ImagenJugador.get_height()*carrito["escala"])))
jugador = Carrito(30,300,ImagenJugador) #crear objeto tipo carrito con posicion 30,300 

#variables de mmovimiento
moverArriba = False
moverAbajo = False
saltar = False

run=True

while run:
    #controlaar frame rate
    reloj.tick(ventana["fps"])
    
    display.fill(ventana["fondo"])
    #calcula movimiento del jugador
    delta_y = 0
    
    if moverArriba == True:
        delta_y = -carrito["velocidad"]
        
    if moverAbajo == True:
        delta_y = carrito["velocidad"]
    
    jugador.movimiento(delta_y)
        
    jugador.dibujar(display) #dibujar en la interfaz deseada
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run = False
        
        #cuando se presiona tecla
        if event.type == pygame.KEYDOWN:
            
            if event.key in (pygame.K_w, pygame.K_UP):
                moverArriba = True
                
            if event.key in (pygame.K_s, pygame.K_DOWN):
                moverAbajo = True
            
            if event.key == pygame.K_SPACE:
                saltar = True
        #cuando se suelta tecla
        if event.type == pygame.KEYUP:
            
            if event.key in (pygame.K_w, pygame.K_UP):
                moverArriba = False
                
            if event.key in (pygame.K_s, pygame.K_DOWN):
                moverAbajo = False
            
            if event.key == pygame.K_SPACE:
                saltar = False 
                
    pygame.display.update() #actualiza los cambios hechos 
    
pygame.quit() #en el momento que sale del ciclo, cierra