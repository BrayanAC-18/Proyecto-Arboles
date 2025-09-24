import json
from models.carrito import Carrito
from models.carretera import Carretera
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

# Suprimir advertencias de libpng
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pygame")

pygame.init() #inicializa pygame

with open("config/ventana.json", "r") as file: 
    ventana = json.load(file)

with open("config/carrito.json", "r") as file: 
    carrito = json.load(file)

with open("config/carretera.json", "r") as file: 
    carretera = json.load(file)

with open("config/obstaculos.json", "r") as file: 
    obstaculos_config = json.load(file)

display = pygame.display.set_mode((ventana["ancho"],ventana["alto"]))
pygame.display.set_caption("Juego del Carrito")
reloj = pygame.time.Clock()

def escalarImagen(imagen, scale=carrito["escala"]):
    return pygame.transform.scale(
        imagen, 
        (int(imagen.get_width()*scale), int(imagen.get_height()*scale))
    )

imagenes = [
    escalarImagen(pygame.image.load(carrito["colorDefault"])),
    escalarImagen(pygame.image.load(carrito["colorSalto"]))
]

# Crear carretera (ajusta la ruta del sprite según tu archivo)
carretera = Carretera(carretera["sprite"], ventana["alto"], ventana["ancho"], obstaculos_config=obstaculos_config)

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
    reloj.tick(ventana["fps"])
    
    display.fill(ventana["fondo"])
    
     # Actualizar carretera
    carretera.actualizar()
    carretera.dibujar(display)

    # 🚗💥 Colisiones con obstáculos
    for obst in carretera.obstacles:
        if jugador.rect.colliderect(obst.rect):
            if obst.tipo == "hueco":
                if not jugador.ha_saltado:  # solo muere si no saltó
                    print("❌ Caíste en un hueco. GAME OVER")
                    run = False
            else:  # obstáculos sólidos
                print(f"💥 Chocaste contra {obst.tipo}. GAME OVER")
                run = False

    #calcula movimiento del jugador
    delta_y = 0
    
    if moverArriba:
        delta_y = -carrito["velocidad"]
        
    if moverAbajo:
        delta_y = carrito["velocidad"]
        
        
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