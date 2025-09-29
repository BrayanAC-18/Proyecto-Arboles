import pygame, json
import sys, os
from models.obstaculos import Obstacle

# Agregar la raíz del proyecto al path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

pygame.init()
from models.screen import Screen
from models.carrito import Carrito
from models.carretera import Carretera
from controller.grafico_avl import draw_avl
from avl.avl import AVL  

# Colores
NEGRO = (0, 0, 0)
GRIS = (200, 200, 200)

def tree_height(node):
    if not node:
        return 0
    return 1 + max(tree_height(node.left), tree_height(node.right))

class GameScreen(Screen):
    def __init__(self, display, config, game, avl_tree=None):
        super().__init__(display, config)
        self.fuente = pygame.font.Font(None, 25)
        self.game = game
        
        # Carretera
        self.carretera = Carretera(config["carretera"]["sprite"], config["ventana"]["alto"], config["ventana"]["ancho"], self.config)
        limite_sup, limite_inf = self.carretera.obtener_limites()
        posicion_inicial_y = (limite_sup + limite_inf) // 2
        
        # Inicializar árbol AVL
        self.avl_tree = avl_tree or AVL()
        for i, obstacle in enumerate(self.carretera.obstacles):
            if not hasattr(obstacle, 'id'):
                obstacle.id = i
            self.avl_tree.insert(obstacle)

        # Jugador
        imagenes = [
            self.escalarImagen(pygame.image.load(config["carrito"]["colorDefault"])),
            self.escalarImagen(pygame.image.load(config["carrito"]["colorSalto"]))
        ]
        self.jugador = Carrito(30, posicion_inicial_y, imagenes, self.config)

        # Inputs
        zona_inputs_y = config["ventana"]["alto"] - 250
        self.input_rects = [pygame.Rect(150, zona_inputs_y + i*50 + 20, 100, 32) for i in range(4)]
        self.labels = ["Distancia (m):", "Salto (m):", "Velocidad (m):", "(ms):"]
        self.input_texts = [""]*4
        self.active_input = None

        # Movimiento
        self.moverArriba = False
        self.moverAbajo = False
        self.salto = False

    def escalarImagen(self, imagen, scale=None):
        scale = scale or self.config["carrito"]["escala"]
        return pygame.transform.scale(imagen, (int(imagen.get_width()*scale), int(imagen.get_height()*scale)))

    # -------------------- Manejo de eventos --------------------
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active_input = None
            for i, rect in enumerate(self.input_rects):
                if rect.collidepoint(event.pos):
                    self.active_input = i
                    break

        elif event.type == pygame.KEYDOWN:
            if self.active_input is not None:
                if event.key == pygame.K_BACKSPACE:
                    self.input_texts[self.active_input] = self.input_texts[self.active_input][:-1]
                elif event.key == pygame.K_RETURN:
                    claves = [
                        ("carretera", "longitud"),
                        ("carrito", "salto"),
                        ("carrito", "avance_m"),
                        ("carrito", "avance_ms")
                    ]
                    try:
                        clave_principal, subclave = claves[self.active_input]
                        self.config[clave_principal][subclave] = float(self.input_texts[self.active_input])
                        with open("config/config.json", "w") as f:
                            json.dump(self.config, f, indent=4)
                        self.game.set_screen(GameScreen(self.game.display, self.config, self.game, self.avl_tree))
                    except ValueError:
                        print("Ingrese un número válido")
                    self.input_texts[self.active_input] = ""
                else:
                    if event.unicode.isdigit() or event.unicode == ".":
                        self.input_texts[self.active_input] += event.unicode

            if event.key in (pygame.K_w, pygame.K_UP):
                self.moverArriba = True
            if event.key in (pygame.K_s, pygame.K_DOWN):
                self.moverAbajo = True
            if event.key == pygame.K_SPACE:
                self.salto = True

        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_w, pygame.K_UP):
                self.moverArriba = False
            if event.key in (pygame.K_s, pygame.K_DOWN):
                self.moverAbajo = False
            if event.key == pygame.K_SPACE:
                self.salto = False

    # -------------------- Actualización --------------------
    def update(self, dt_ms):
        self.carretera.actualizar(dt_ms)

        delta_y = -self.config["carrito"]["avance_m"] if self.moverArriba else (
                   self.config["carrito"]["avance_m"] if self.moverAbajo else 0)

        limite_sup, limite_inf = self.carretera.obtener_limites()
        nueva_y = max(limite_sup, min(self.jugador.rect.y + delta_y, limite_inf - self.jugador.rect.height))
        self.jugador.movimiento(nueva_y - self.jugador.rect.y, self.salto)

        for obst in list(self.carretera.obstacles):
            if self.jugador.rect.colliderect(obst.rect) and not obst.tocado:
                obst.tocado = True
                if self.avl_tree:
                    self.avl_tree.delete(obst)
                if not self.jugador.esta_saltando:
                    self.jugador.getDamage(int(obst.daño))
                    if self.jugador.dañado:
                        self.game.running = False

        self.limpiar_obstaculos_pasados()

    def limpiar_obstaculos_pasados(self):
        jugador_left = self.jugador.rect.left
        pasados = [obst for obst in self.carretera.obstacles if obst.rect.right < jugador_left]
        for obst in pasados:
            if self.avl_tree:
                self.avl_tree.delete(obst)
                self.exportar_arbol(f"arbol_{obst.id}.png") # guarda uno distinto por obstáculo
            if obst in self.carretera.obstacles:
                self.carretera.obstacles.remove(obst)

    def exportar_arbol(self, filename="arbol_actual.png"):
        if not self.avl_tree or not self.avl_tree.root:
            return
        
        # Crear carpeta si no existe
        folder = "imagenes_avl"
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        # Crear una superficie temporal solo para el árbol
        ancho = 800
        alto = 600
        superficie = pygame.Surface((ancho, alto))
        superficie.fill((255, 255, 255))  # fondo blanco
        
        # Parámetros de dibujo compactos
        font = pygame.font.SysFont(None, 16)
        dx = 125
        dy = 60
        radius = 18
        start_x = ancho // 2
        start_y = 50
        
        draw_avl(superficie, self.avl_tree.root, start_x, start_y, dx, dy, font, radius)
        
         # Guardar imagen en la carpeta
        filepath = os.path.join(folder, filename)
        pygame.image.save(superficie, filepath)
        print(f"Árbol exportado en {filepath}")

    # -------------------- Dibujado --------------------
    def draw(self):
        self.display.fill(self.config["ventana"]["fondo"])
        self.carretera.dibujar(self.display)
        self.jugador.dibujar(self.display)
        self.barraSalud()

        for i, rect in enumerate(self.input_rects):
            pygame.draw.rect(self.display, GRIS, rect)
            pygame.draw.rect(self.display, NEGRO, rect, 2)
            self.display.blit(self.fuente.render(self.labels[i], True, NEGRO), (20, rect.y + 5))
            self.display.blit(self.fuente.render(self.input_texts[i], True, NEGRO), (rect.x + 5, rect.y + 5))

        if self.avl_tree and self.avl_tree.root:
            # Fuente pequeña
            font = pygame.font.SysFont(None, 16)

            # Valores fijos para que siempre se vea compacto
            dx = 100        # separación horizontal entre nodos
            dy = 50        # separación vertical entre niveles
            radius = 25    # tamaño de los círculos

            # Posición inicial del árbol (zona inferior de la pantalla)
            start_x = int(self.config["ventana"]["ancho"] * 0.6)
            start_y = int(self.config["ventana"]["alto"] * 0.55)

            # Dibujo estático
            draw_avl(self.display, self.avl_tree.root, start_x, start_y, dx, dy, font, radius)


        node_count = len(self.avl_tree.inorder()) if self.avl_tree and self.avl_tree.root else 0
        info_surface = self.fuente.render(f"Nodos en árbol: {node_count}", True, NEGRO)
        self.display.blit(info_surface, (10, self.config["ventana"]["alto"] - 30))
        pygame.display.flip()

    def barraSalud(self):
        pygame.draw.rect(self.display, (255, 0, 0), (10, 10, self.jugador.energia_actual, 20))
