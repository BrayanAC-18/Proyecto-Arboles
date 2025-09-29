import pygame, os, json
from models.screen import Screen
from models.carrito import Carrito
from models.carretera import Carretera
from controller.grafico_avl import draw_avl
from avl.avl import AVL  

NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)

class GameScreen(Screen):
    def __init__(self, display, config, game, avl_tree=None):
        super().__init__(display, config)
        self.fuente = pygame.font.Font(None, 25)
        self.game = game
        
        # -------------------- Carretera --------------------
        self.carretera = Carretera(
            config["carretera"]["sprite"], 
            config["ventana"]["alto"], 
            config["ventana"]["ancho"], 
            self.config
        )
        limite_sup, limite_inf = self.carretera.obtener_limites()
        posicion_inicial_y = (limite_sup + limite_inf) // 2
        
        # -------------------- Árbol AVL --------------------
        self.avl_tree = avl_tree or AVL()
        for i, obstacle in enumerate(self.carretera.obstacles):
            if not hasattr(obstacle, 'id'):
                obstacle.id = i
            self.avl_tree.insert(obstacle)

        self.exportar_arbol("arbol_inicial.png")

        # -------------------- Jugador --------------------
        imagenes = [
            self.escalarImagen(pygame.image.load(config["carrito"]["colorDefault"])),
            self.escalarImagen(pygame.image.load(config["carrito"]["colorSalto"]))
        ]
        self.jugador = Carrito(30, posicion_inicial_y, imagenes, self.config)

        # -------------------- Movimiento --------------------
        self.moverArriba = False
        self.moverAbajo = False
        self.salto = False

    def escalarImagen(self, imagen, scale=None):
        scale = scale or self.config["carrito"]["escala"]
        return pygame.transform.scale(imagen, (
            int(imagen.get_width()*scale), int(imagen.get_height()*scale))
        )

    # -------------------- Eventos --------------------
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
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
                self.exportar_arbol(f"arbol_{obst.posX, obst.posY}.png")
            if obst in self.carretera.obstacles:
                self.carretera.obstacles.remove(obst)

    # -------------------- Exportar AVL --------------------
    def exportar_arbol(self, filename="arbol_actual.png"):
        if not self.avl_tree or not self.avl_tree.root:
            return

        folder = "imagenes_avl"
        if not os.path.exists(folder):
            os.makedirs(folder)

        ancho, alto = 800, 600
        superficie = pygame.Surface((ancho, alto))
        superficie.fill((255, 255, 255))

        font = pygame.font.SysFont(None, 16)
        dx, dy, radius = 125, 60, 18
        start_x, start_y = ancho // 2, 50
        draw_avl(superficie, self.avl_tree.root, start_x, start_y, dx, dy, font, radius)

        filepath = os.path.join(folder, filename)
        pygame.image.save(superficie, filepath)
        print(f"Árbol exportado en {filepath}")

    # -------------------- Dibujado --------------------
    def draw(self):
        self.display.fill(self.config["ventana"]["fondo"])
        self.carretera.dibujar(self.display)
        self.jugador.dibujar(self.display)
        self.barraSalud()

        # Dibujar árbol AVL
        if self.avl_tree and self.avl_tree.root:
            font = pygame.font.SysFont(None, 16)
            dx, dy, radius = 100, 50, 25
            start_x = int(self.config["ventana"]["ancho"] * 0.50)
            start_y = int(self.config["ventana"]["alto"] * 0.55)
            draw_avl(self.display, self.avl_tree.root, start_x, start_y, dx, dy, font, radius)

        node_count = len(self.avl_tree.inorder()) if self.avl_tree and self.avl_tree.root else 0
        info_surface = self.fuente.render(f"Nodos en árbol: {node_count}", True, NEGRO)
        self.display.blit(info_surface, (10, self.config["ventana"]["alto"] - 30))
        pygame.display.flip()

    def barraSalud(self):
        pygame.draw.rect(self.display, (255, 0, 0), (10, 10, self.jugador.energia_actual, 20))
