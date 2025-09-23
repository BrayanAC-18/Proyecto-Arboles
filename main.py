import json
from models.carrito import Carrito
from models.carretera import Carretera
import pygame

pygame.init() #inicializa pygame

pantalla = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Configurar antes de jugar")
fuente = pygame.font.Font(None, 32)


with open("config/config.json", "r") as file: 
    config = json.load(file)



display = pygame.display.set_mode((config["ventana"]["ancho"],config["ventana"]["alto"]))
pygame.display.set_caption("Juego del Carrito")
reloj = pygame.time.Clock()

def escalarImagen(imagen, scale=config["carrito"]["escala"]):
    return pygame.transform.scale(
        imagen, 
        (int(imagen.get_width()*scale), int(imagen.get_height()*scale))
    )

imagenes = [
    escalarImagen(pygame.image.load(config["carrito"]["colorDefault"])),
    escalarImagen(pygame.image.load(config["carrito"]["colorSalto"]))
]

# Crear carretera
carretera = Carretera(config["carretera"]["sprite"], config["ventana"]["alto"], config["ventana"]["ancho"])

limite_sup, limite_inf = carretera.obtener_limites() #obetener limites para limitar el movimiento del carro
posicion_inicial_y = (limite_sup + limite_inf) // 2

jugador = Carrito(30, posicion_inicial_y, imagenes)

#variables de mmovimiento
moverArriba = False
moverAbajo = False
salto = False

run=True

while run:
    #controlaar frame rate
    dt_ms = reloj.tick(config["ventana"]["fps"])
    
    display.fill(config["ventana"]["fondo"])
    
     # Actualizar carretera
    carretera.actualizar(dt_ms)
    carretera.dibujar(display)

    
    
    #calcula movimiento del jugador
    delta_y = 0
    
    if moverArriba:
        delta_y = -config["carrito"]["avance_m"]
        
    if moverAbajo:
        delta_y = config["carrito"]["avance_m"]
        
    # Obtener límites actuales de la carretera
    limite_superior, limite_inferior = carretera.obtener_limites()
    
    # Calcular nueva posición Y del jugador
    nueva_y = jugador.rect.y + delta_y
    
    # Limitar movimiento dentro de la carretera (considerando el tamaño del carro)
    if nueva_y < limite_superior:
        nueva_y = limite_superior
    elif nueva_y + jugador.rect.height > limite_inferior:
        nueva_y = limite_inferior - jugador.rect.height
    
    # Aplicar movimiento limitado
    delta_y_limitado = nueva_y - jugador.rect.y
    
    jugador.movimiento(delta_y_limitado, salto)
    
    # Dibujar jugador
    jugador.dibujar(display)
    
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
                salto = True
        #cuando se suelta tecla
        if event.type == pygame.KEYUP:
            
            if event.key in (pygame.K_w, pygame.K_UP):
                moverArriba = False
                
            if event.key in (pygame.K_s, pygame.K_DOWN):
                moverAbajo = False
            
            if event.key == pygame.K_SPACE:
                salto = False 
                
    pygame.display.update() #actualiza los cambios hechos 
    
pygame.quit() #en el momento que sale del ciclo, cierra