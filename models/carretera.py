import pygame
import json
from models.carrito import Carrito

pygame.init()

# Cargar configuraciones
with open("config/ventana.json", "r") as file:
    ventana = json.load(file)

with open("config/carrito.json", "r") as file:
    carrito = json.load(file)
    
with open("config/carretera.json", "r") as file:
    carretera = json.load(file)

display = pygame.display.set_mode((ventana["ancho"], ventana["alto"]))
pygame.display.set_caption("Juego del Carrito")
reloj = pygame.time.Clock()

class Carretera:
    def __init__(self, sprite, alto_ventana, ancho_ventana):
        self.sprite = pygame.image.load(sprite)
        self.alto_ventana = alto_ventana
        self.ancho_ventana = ancho_ventana
        self.velocidad = carretera["velocidad"]
        self.longitud = carretera["longitud"]
        self.x = 0
        self.en_movimiento = True
        self.posicion_meta = self.longitud
        self.meta_alcanzada = False
        self.pixels_por_metro = 50
        
    # Escalar la carretera a la longitud especificada
        self.sprite_escalado = pygame.transform.scale(
        self.sprite, 
        (self.longitud, carretera["altura"])
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
        
    def actualizar(self):
        if not self.meta_alcanzada:
            # Mover carretera
            self.x -= self.velocidad
            if self.x <= -self.ancho_sprite:
                self.x = 0
            
            # Acercar la meta
            self.posicion_meta -= self.velocidad
            
            # Verificar si se alcanzó la meta
            if self.posicion_meta <= 0:
                self.meta_alcanzada = True
    
    def dibujar_contador_metros(self, surface):
        # Calcular metros recorridos y restantes con la escala fija
        metros_recorridos = int((self.longitud - self.posicion_meta) / self.pixels_por_metro)
        metros_restantes = int(self.posicion_meta / self.pixels_por_metro)

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
        
        # Dibujar línea de meta si está visible
        self.dibujar_meta(surface)

    
    def obtener_limites(self):
        return self.limite_superior, self.limite_inferior
    
    