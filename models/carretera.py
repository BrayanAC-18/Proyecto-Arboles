import pygame
from models.carrito import Carrito
from models.obstaculos import Obstacle

pygame.init()

class Carretera:
    def __init__(self, sprite, alto_ventana, ancho_ventana, config):
        self.config = config
        self.sprite = pygame.image.load(sprite)
        self.alto_ventana = alto_ventana
        self.ancho_ventana = ancho_ventana
        self.pixeles_por_metro = self.config["carretera"]["pixeles_metro"]
        self.longitud = self.config["carretera"]["longitud"] * self.pixeles_por_metro
        self.x = 0
        self.en_movimiento = True
        self.posicion_meta = self.longitud
        self.meta_alcanzada = False
        self.pixels_por_metro = 50
        self.obstacles = []
        self.y = 100
        self._cargar_obstaculos(self.config["obstaculos"])
        
        
    # Escalar la carretera a la longitud especificada
        self.sprite_escalado = pygame.transform.scale(
        self.sprite, 
        (self.longitud, self.config["carretera"]["altura"])
    )
        
        self.ancho_sprite = self.sprite_escalado.get_width()
        self.alto_sprite = self.sprite_escalado.get_height()
        
        # Calcular posición Y para centrar verticalmente la carretera
        self.y = 100
        
        # Definir márgenes donde el carro SÍ puede moverse
        self.margen_superior = 20  # píxeles desde el borde superior de la carretera
        self.margen_inferior = 50  # píxeles desde el borde inferior de la carretera
        
        # Límites corregidos
        self.limite_superior = self.y + self.margen_superior
        self.limite_inferior = self.y + self.alto_sprite - self.margen_inferior
        
        # Calcular cuántas repeticiones necesitamos para cubrir la pantalla
        self.repeticiones_necesarias = (ancho_ventana // self.ancho_sprite) + 3
        
    def actualizar(self, dt_ms):
        desplazamiento = 0  # valor por defecto

        if not self.meta_alcanzada:
            # calcular velocidad del carro en m/s
            avance_m = self.config["carrito"]["avance_m"]
            avance_ms = self.config["carrito"]["avance_ms"]
            velocidad_m_s = avance_m / (avance_ms / 1000.0)  # metros por segundo

            # convertir a píxeles/s
            velocidad_px_s = velocidad_m_s * self.pixeles_por_metro

            # desplazar carretera en píxeles según el dt
            desplazamiento = velocidad_px_s * (dt_ms / 1000.0)
            self.x -= desplazamiento

            # reiniciar ciclo de repetición
            if self.x <= -self.ancho_sprite:
                self.x = 0

            # actualizar la posición de la meta
            self.posicion_meta -= desplazamiento
            if self.posicion_meta <= 0:
                self.meta_alcanzada = True
    
    def dibujar_contador_metros(self, surface):
        # Calcular metros recorridos y restantes con la escala fija
        metros_recorridos = int((self.longitud - self.posicion_meta) / self.pixeles_por_metro)
        metros_restantes = int(self.posicion_meta / self.pixeles_por_metro)

        # Fuente y texto
        font = pygame.font.Font(None, 36)
        texto = font.render(f"{metros_recorridos} m | faltan: {metros_restantes} m", True, (255, 255, 255))

        # Casilla
        casilla_width, casilla_height = 280, 40
        casilla_x = (self.ancho_ventana - casilla_width) // 2  # centrado en X
        casilla_y = 20  # fijo arriba
        pygame.draw.rect(surface, (0, 0, 0), (casilla_x, casilla_y, casilla_width, casilla_height), border_radius=8)
        pygame.draw.rect(surface, (255, 255, 255), (casilla_x, casilla_y, casilla_width, casilla_height), 2, border_radius=8)

        # Centrar texto
        text_rect = texto.get_rect(center=(casilla_x + casilla_width // 2, casilla_y + casilla_height // 2))
        surface.blit(texto, text_rect)

    def _cargar_obstaculos(self, obstaculos_config):
        #Cargar obstáculos desde el JSON.
        for o in obstaculos_config:
            obst = Obstacle(
                id_=o["id"],
                tipo=o["tipo"],
                posX=o["posX"],
                posY=self.y + o["posY"],  # se ajusta en relación con la carretera
                ancho=o["ancho"],
                alto=o["alto"],
                imagen=o["imagen"]
            )
            self.obstacles.append(obst)
            print(f"✅ Obstacle {o['tipo']} en ({o['posX']}, {self.y + o['posY']})")
        
    # Cambiar el método dibujar_puntos_referencia por esto:
    def dibujar_meta(self, surface):
        if self.posicion_meta < self.ancho_ventana and self.posicion_meta > -50:
            # Línea de meta a cuadros blancos y negros
            ancho_cuadro = 20
            for i in range(0, self.alto_sprite, ancho_cuadro):
                color = (255, 255, 255) if (i // ancho_cuadro) % 2 == 0 else (0, 0, 0)
                pygame.draw.rect(surface, color, 
                            (self.posicion_meta, self.y + i, 8, ancho_cuadro))
        
        # Solo llamar al contador de metros
        self.dibujar_contador_metros(surface)
             
    def dibujar(self, surface):
        # Dibujar carretera normal
        for i in range(self.repeticiones_necesarias):
            pos_x = self.x + (i * self.ancho_sprite)
            if pos_x < self.ancho_ventana and pos_x > -self.ancho_sprite:
                surface.blit(self.sprite_escalado, (pos_x, self.y))
        # Dibujar obstáculos
        for obst in self.obstacles:
            screen_x = obst.posX + self.x
            screen_y = obst.posY

            # 🔹 Actualizar rect del obstáculo para colisiones
            obst.rect.topleft = (screen_x, screen_y)

            # Solo dibujar si está dentro de la pantalla
            if -100 < screen_x < self.ancho_ventana + 100:
                surface.blit(obst.image, (screen_x, screen_y))

                # Dibujar borde rojo (debug de colisiones)
                pygame.draw.rect(surface, (255, 0, 0), obst.rect, 1)
        
        # Dibujar línea de meta si está visible
        self.dibujar_meta(surface)

    
    def obtener_limites(self):
        return self.limite_superior, self.limite_inferior
    
    def actualizar_longitud(self, nueva_longitud):
        self.longitud = nueva_longitud * self.pixeles_por_metro
        self.posicion_meta = self.longitud
        self.sprite_escalado = pygame.transform.scale(self.sprite, (int(self.longitud), self.config["carretera"]["altura"]))
        
    