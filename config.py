# Pantalla de configuración - Agregar al inicio de tu código principal

# Estados del juego (agregar después de cargar config)
import json
import pygame
with open("config/config.json", "r") as file: 
    config = json.load(file)

# Pantalla de configuración - Agregar al inicio de tu código principal

# Estados del juego (agregar después de cargar config)
ESTADO_CONFIG = "configuracion"
ESTADO_JUEGO = "juego"
estado_actual = ESTADO_CONFIG

# Colores adicionales
VERDE = (0, 200, 0)
AZUL = (0, 100, 200)
fuente_titulo = pygame.font.Font(None, 36)

# Configuración de la pantalla de config
config_keys = [
    ("carretera", "longitud"),
    ("carrito", "salto"),
    ("carrito", "avance_m"),
    ("carrito", "avance_ms")
]

# Reposicionar inputs para la pantalla de config
config_input_rects = [
    pygame.Rect(300, 200, 120, 32),
    pygame.Rect(300, 250, 120, 32),
    pygame.Rect(300, 300, 120, 32),
    pygame.Rect(300, 350, 120, 32)
]

# Botón para iniciar juego
boton_iniciar = pygame.Rect(300, 420, 120, 40)

def cargar_valores_actuales():
    """Carga los valores actuales del config en los inputs"""
    for i, (clave_principal, subclave) in enumerate(config_keys):
        input_texts[i] = str(config[clave_principal][subclave])

def guardar_configuracion():
    """Guarda todos los valores de los inputs en el archivo de configuración"""
    try:
        cambios_realizados = False
        for i, (clave_principal, subclave) in enumerate(config_keys):
            if input_texts[i].strip():  # Solo si hay texto
                valor = float(input_texts[i])
                if valor > 0:  # Validar que sea positivo
                    config[clave_principal][subclave] = valor
                    cambios_realizados = True
        
        if cambios_realizados:
            # Guardar en archivo
            with open("config/config.json", "w") as f:
                json.dump(config, f, indent=4)
            print("Configuración guardada exitosamente")
        return True
    except ValueError:
        print("Error: Ingrese números válidos")
        return False

def dibujar_pantalla_config():
    """Dibuja la pantalla de configuración"""
    display.fill(BLANCO)
    
    # Título
    titulo = fuente_titulo.render("CONFIGURACIÓN DEL JUEGO", True, NEGRO)
    titulo_rect = titulo.get_rect(center=(config["ventana"]["ancho"]//2, 80))
    display.blit(titulo, titulo_rect)
    
    # Instrucciones
    instruccion = fuente.render("Configura los parámetros del juego y presiona INICIAR:", True, NEGRO)
    instruccion_rect = instruccion.get_rect(center=(config["ventana"]["ancho"]//2, 130))
    display.blit(instruccion, instruccion_rect)
    
    # Dibujar labels, valores actuales y cajas de texto
    for i, rect in enumerate(config_input_rects):
        # Label
        label_render = fuente.render(labels[i], True, NEGRO)
        display.blit(label_render, (50, rect.y + 5))
        
        # Valor actual del config
        clave_principal, subclave = config_keys[i]
        valor_actual = config[clave_principal][subclave]
        valor_texto = f"Actual: {valor_actual}"
        valor_render = fuente.render(valor_texto, True, AZUL)
        display.blit(valor_render, (450, rect.y + 5))
        
        # Caja de texto
        color_borde = VERDE if active_input == i else NEGRO
        pygame.draw.rect(display, BLANCO, rect, 0)
        pygame.draw.rect(display, color_borde, rect, 2)
        texto_render = fuente.render(input_texts[i], True, NEGRO)
        display.blit(texto_render, (rect.x + 5, rect.y + 5))
    
    # Botón iniciar juego
    pygame.draw.rect(display, VERDE, boton_iniciar, 0)
    pygame.draw.rect(display, NEGRO, boton_iniciar, 2)
    boton_texto = fuente.render("INICIAR JUEGO", True, BLANCO)
    boton_texto_rect = boton_texto.get_rect(center=boton_iniciar.center)
    display.blit(boton_texto, boton_texto_rect)
    
    # Instrucciones de uso
    instrucciones = [
        "• Haz clic en una caja para editarla",
        "• Presiona Enter para aplicar el valor",
        "• Los valores deben ser números positivos"
    ]
    
    for i, inst in enumerate(instrucciones):
        inst_render = pygame.font.Font(None, 22).render(inst, True, NEGRO)
        display.blit(inst_render, (50, 500 + i * 25))

# MOVER ESTA LÍNEA DESPUÉS DE QUE input_texts ESTÉ DEFINIDO
# cargar_valores_actuales()  # Comentar temporalmente

# Crear los objetos del juego (mover después de la configuración inicial)
imagenes = [
    escalarImagen(pygame.image.load(config["carrito"]["colorDefault"])),
    escalarImagen(pygame.image.load(config["carrito"]["colorSalto"]))
]

carretera = Carretera(config["carretera"]["sprite"], config["ventana"]["alto"], config["ventana"]["ancho"])
limite_sup, limite_inf = carretera.obtener_limites()
posicion_inicial_y = (limite_sup + limite_inf) // 2
jugador = Carrito(30, posicion_inicial_y, imagenes)

# REEMPLAZAR EL BUCLE PRINCIPAL CON ESTE:
while run:  
    dt_ms = reloj.tick(config["ventana"]["fps"])
    
    if estado_actual == ESTADO_CONFIG:
        dibujar_pantalla_config()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            # Click sobre input o botón
            if event.type == pygame.MOUSEBUTTONDOWN:
                active_input = None
                # Verificar clicks en inputs
                for i, rect in enumerate(config_input_rects):
                    if rect.collidepoint(event.pos):
                        active_input = i
                        break
                
                # Verificar click en botón iniciar
                if boton_iniciar.collidepoint(event.pos):
                    if guardar_configuracion():
                        # Recrear objetos con nueva configuración
                        imagenes = [
                            escalarImagen(pygame.image.load(config["carrito"]["colorDefault"])),
                            escalarImagen(pygame.image.load(config["carrito"]["colorSalto"]))
                        ]
                        carretera = Carretera(config["carretera"]["sprite"], config["ventana"]["alto"], config["ventana"]["ancho"])
                        limite_sup, limite_inf = carretera.obtener_limites()
                        posicion_inicial_y = (limite_sup + limite_inf) // 2
                        jugador = Carrito(30, posicion_inicial_y, imagenes)
                        estado_actual = ESTADO_JUEGO
            
            # Manejo de texto en inputs
            if event.type == pygame.KEYDOWN:
                if active_input is not None:
                    if event.key == pygame.K_BACKSPACE:
                        input_texts[active_input] = input_texts[active_input][:-1]
                    elif event.key == pygame.K_RETURN:
                        # Aplicar valor individual
                        try:
                            if input_texts[active_input].strip():
                                clave_principal, subclave = config_keys[active_input]
                                valor = float(input_texts[active_input])
                                if valor > 0:
                                    config[clave_principal][subclave] = valor
                                    with open("config/config.json", "w") as f:
                                        json.dump(config, f, indent=4)
                                    print(f"Valor actualizado: {labels[active_input]} = {valor}")
                                else:
                                    print("Error: El valor debe ser positivo")
                        except ValueError:
                            print("Error: Ingrese un número válido")
                        active_input = None
                    else:
                        # Agregar caracteres válidos (números y punto decimal)
                        if event.unicode.isdigit() or event.unicode == ".":
                            input_texts[active_input] += event.unicode
    
    elif estado_actual == ESTADO_JUEGO:
        # TU CÓDIGO ORIGINAL DEL JUEGO VA AQUÍ (desde display.fill hasta el final del loop)
        display.fill(config["ventana"]["fondo"])
        
        # Actualizar carretera
        carretera.actualizar(dt_ms)
        carretera.dibujar(display)
        
        # Resto de tu lógica del juego...
        delta_y = 0
        
        if moverArriba:
            delta_y = -config["carrito"]["avance_m"]
            
        if moverAbajo:
            delta_y = config["carrito"]["avance_m"]
            
        limite_superior, limite_inferior = carretera.obtener_limites()
        nueva_y = jugador.rect.y + delta_y
        
        if nueva_y < limite_superior:
            nueva_y = limite_superior
        elif nueva_y + jugador.rect.height > limite_inferior:
            nueva_y = limite_inferior - jugador.rect.height
        
        delta_y_limitado = nueva_y - jugador.rect.y
        jugador.movimiento(delta_y_limitado, salto)
        jugador.dibujar(display)
        
        # Agregar instrucción para volver al menú
        instruccion_menu = pygame.font.Font(None, 20).render("Presiona ESC para configuración", True, BLANCO)
        display.blit(instruccion_menu, (10, 10))
        
        # TUS EVENTOS DEL JUEGO + ESC para volver al menú
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    estado_actual = ESTADO_CONFIG
                    cargar_valores_actuales()
                
                if event.key in (pygame.K_w, pygame.K_UP):
                    moverArriba = True
                if event.key in (pygame.K_s, pygame.K_DOWN):
                    moverAbajo = True
                if event.key == pygame.K_SPACE:
                    salto = True
                    
            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_w, pygame.K_UP):
                    moverArriba = False
                if event.key in (pygame.K_s, pygame.K_DOWN):
                    moverAbajo = False
                if event.key == pygame.K_SPACE:
                    salto = False 
                    
    pygame.display.update()
    
pygame.quit()