import pygame, json

pygame.init()
from models.screen import Screen
from models.carrito import Carrito
from models.carretera import Carretera


# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (200, 200, 200)


class GameScreen(Screen):
    def __init__(self, display, config, game):
        super().__init__(display, config)
        self.fuente = pygame.font.Font(None, 25)
        self.game = game
        # Carretera
        self.carretera = Carretera(config["carretera"]["sprite"], config["ventana"]["alto"], config["ventana"]["ancho"], self.config)
        limite_sup, limite_inf = self.carretera.obtener_limites()
        posicion_inicial_y = (limite_sup + limite_inf) // 2

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
        if scale is None:
            scale = self.config["carrito"]["escala"]
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
                    try:
                        claves = [
                            ("carretera", "longitud"),
                            ("carrito", "salto"),
                            ("carrito", "avance_m"),
                            ("carrito", "avance_ms")
                        ]
                        clave_principal, subclave = claves[self.active_input]
                        self.config[clave_principal][subclave] = float(self.input_texts[self.active_input])

                        # Guardar en archivo
                        with open("config/config.json", "w") as f:
                            json.dump(self.config, f, indent=4)

                        # Recargar config desde archivo
                        with open("config/config.json", "r") as f:
                            self.config = json.load(f)
                            self.game.config = self.config
                        # REINICIAR la pantalla con la nueva configuración
                        self.game.set_screen(GameScreen(self.game.display, self.config, self.game))
                    except ValueError:
                        print("Ingrese un número válido")

                    self.input_texts[self.active_input] = ""

                else:
                    if event.unicode.isdigit() or event.unicode == ".":
                        self.input_texts[self.active_input] += event.unicode

            # Movimiento del jugador
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

    # -------------------- Actualización de estado --------------------
    def update(self, dt_ms):
        self.carretera.actualizar(dt_ms)
        delta_y = 0
        if self.moverArriba:
            delta_y = -self.config["carrito"]["avance_m"]
        if self.moverAbajo:
            delta_y = self.config["carrito"]["avance_m"]

        limite_sup, limite_inf = self.carretera.obtener_limites()
        nueva_y = self.jugador.rect.y + delta_y
        nueva_y = max(limite_sup, min(nueva_y, limite_inf - self.jugador.rect.height))
        self.jugador.movimiento(nueva_y - self.jugador.rect.y, self.salto)

    # -------------------- Dibujado en pantalla --------------------
    def draw(self):
        self.display.fill(self.config["ventana"]["fondo"])
        self.carretera.dibujar(self.display)
        self.jugador.dibujar(self.display)

        # Dibujar inputs y labels
        for i, rect in enumerate(self.input_rects):
            pygame.draw.rect(self.display, GRIS, rect)
            pygame.draw.rect(self.display, NEGRO, rect, 2)
            self.display.blit(self.fuente.render(self.labels[i], True, NEGRO), (20, rect.y + 5))
            self.display.blit(self.fuente.render(self.input_texts[i], True, NEGRO), (rect.x + 5, rect.y + 5))
