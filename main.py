import json
from models.carrito import Carrito
from models.carretera import Carretera

import pygame

pygame.init() #inicializa pygame

with open("config/config.json", "r") as file: 
    config = json.load(file)

# Color
BLANCO = (255, 255, 255)
GRIS = (200, 200, 200)
NEGRO = (0, 0, 0)
fuente = pygame.font.Font(None, 25)

# Tamaño y posición de la zona de inputs
zona_inputs_y = config["ventana"]["alto"] - 250

# Recalcular posiciones de inputs dentro de la zona blanca inferior
input_rects = [
    pygame.Rect(150, zona_inputs_y + 20, 100, 32),
    pygame.Rect(150, zona_inputs_y + 70, 100, 32),
    pygame.Rect(150, zona_inputs_y + 120, 100, 32),
    pygame.Rect(150, zona_inputs_y + 170, 100, 32)
]

# Labels y posiciones
labels = ["Distancia (m):", "Salto (m):", "Velocidad (m):", "(ms):"]

input_texts = ["", "", "", ""]
active_input = None


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
    
    # Dibujar labels y cajas de texto
    for i, rect in enumerate(input_rects):
        # Label
        label_render = fuente.render(labels[i], True, NEGRO)
        display.blit(label_render, (20, rect.y + 5))
        
        # Caja de texto
        pygame.draw.rect(display, GRIS, rect, 0)
        pygame.draw.rect(display, NEGRO, rect, 2)
        texto_render = fuente.render(input_texts[i], True, NEGRO)
        display.blit(texto_render, (rect.x + 5, rect.y + 5))
        
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run = False
        # Click sobre input
        if event.type == pygame.MOUSEBUTTONDOWN:
            active_input = None
            for i, rect in enumerate(input_rects):
                if rect.collidepoint(event.pos):
                    active_input = i
                    break
        #cuando se presiona tecla
        if event.type == pygame.KEYDOWN:
            if active_input is not None:
                if event.key == pygame.K_BACKSPACE:
                    input_texts[active_input] = input_texts[active_input][:-1]
                elif event.key == pygame.K_RETURN:
                    # Guardar valor en JSON
                    try:
                        claves = [
                        ("carretera", "longitud"),
                        ("carrito", "salto"),
                        ("carrito", "avance_m"),
                        ("carrito", "avance_ms")
                        ]
                        clave_principal, subclave = claves[active_input]
                        config[clave_principal][subclave] = float(input_texts[active_input])
                        # Guardar en archivo
                        with open("config/config.json", "w") as f:
                            json.dump(config, f, indent=4)
                        
                    except ValueError:
                        print("Ingrese un número válido")
                    input_texts[active_input] = ""  # limpiar la caja
                else:
                    # Agregar caracteres válidos
                    if event.unicode.isdigit() or event.unicode == ".":
                        input_texts[active_input] += event.unicode
                        
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