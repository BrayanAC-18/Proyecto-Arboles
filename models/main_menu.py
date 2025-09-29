# main_menu.py
import pygame
from models.screen import Screen
from avl.avl import AVL
from models.obstaculos import Obstacle
from models.gamescreen import GameScreen
import json

NEGRO = (0, 0, 0)
GRIS = (200, 200, 200)
VERDE = (0, 200, 0)

class MainMenuScreen(Screen):
    def __init__(self, display, config, game):
        super().__init__(display, config)
        self.game = game
        self.fuente = pygame.font.Font(None, 30)

        # -------------------- Inputs del juego --------------------
        zona_inputs_y = 50
        self.input_rects = [pygame.Rect(300, zona_inputs_y + i*60, 200, 40) for i in range(4)]
        self.labels = ["Distancia (m):", "Salto (m):", "Velocidad (m):", "(ms):"]
        self.input_texts = [""]*4
        self.active_input = None

        # -------------------- Inputs de obstáculos (ID + 6) --------------------
        zona_obs_y = 320
        self.obstacle_labels = ["ID:", "Tipo:", "Pos X:", "Pos Y:", "Ancho:", "Alto:", "Daño:"]
        self.obstacle_input_rects = [
            pygame.Rect(200 + (i%2)*300, zona_obs_y + (i//2)*50, 200, 40) for i in range(7)
        ]
        self.obstacle_texts = [""]*7
        self.active_obstacle_input = None

        # Botones
        self.start_button = pygame.Rect(300, zona_obs_y + 200, 180, 50)
        self.add_obstacle_button = pygame.Rect(520, zona_obs_y + 200, 180, 50)

        # Lista de obstáculos temporales
        self.temp_obstacles = []

    # -------------------- Manejo de eventos --------------------
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Inputs juego
            self.active_input = None
            for i, rect in enumerate(self.input_rects):
                if rect.collidepoint(event.pos):
                    self.active_input = i

            # Inputs obstáculos
            self.active_obstacle_input = None
            for i, rect in enumerate(self.obstacle_input_rects):
                if rect.collidepoint(event.pos):
                    self.active_obstacle_input = i

            # Botones
            if self.start_button.collidepoint(event.pos):
                self.iniciar_juego()
            if self.add_obstacle_button.collidepoint(event.pos):
                self.agregar_obstaculo()

        elif event.type == pygame.KEYDOWN:
            # Inputs juego
            if self.active_input is not None:
                if event.key == pygame.K_BACKSPACE:
                    self.input_texts[self.active_input] = self.input_texts[self.active_input][:-1]
                elif event.unicode.isdigit() or event.unicode == ".":
                    self.input_texts[self.active_input] += event.unicode

            # Inputs obstáculos
            if self.active_obstacle_input is not None:
                if event.key == pygame.K_BACKSPACE:
                    self.obstacle_texts[self.active_obstacle_input] = self.obstacle_texts[self.active_obstacle_input][:-1]
                else:
                    self.obstacle_texts[self.active_obstacle_input] += event.unicode

    # -------------------- Actualización --------------------
    def update(self, dt_ms):
        pass

    # -------------------- Dibujado --------------------
    def draw(self):
        self.display.fill((150, 150, 150))

        # Inputs de juego
        for i, rect in enumerate(self.input_rects):
            pygame.draw.rect(self.display, GRIS, rect)
            pygame.draw.rect(self.display, NEGRO, rect, 2)
            self.display.blit(self.fuente.render(self.labels[i], True, NEGRO), (rect.x - 150, rect.y + 10))
            self.display.blit(self.fuente.render(self.input_texts[i], True, NEGRO), (rect.x + 5, rect.y + 10))

        # Inputs de obstáculos
        for i, rect in enumerate(self.obstacle_input_rects):
            pygame.draw.rect(self.display, GRIS, rect)
            pygame.draw.rect(self.display, NEGRO, rect, 2)
            self.display.blit(self.fuente.render(self.obstacle_labels[i], True, NEGRO), (rect.x - 90, rect.y + 10))
            self.display.blit(self.fuente.render(self.obstacle_texts[i], True, NEGRO), (rect.x + 5, rect.y + 10))

        # Botones
        pygame.draw.rect(self.display, VERDE, self.start_button)
        self.display.blit(self.fuente.render("Iniciar juego", True, NEGRO),
                          (self.start_button.x + 15, self.start_button.y + 15))

        pygame.draw.rect(self.display, VERDE, self.add_obstacle_button)
        self.display.blit(self.fuente.render("Agregar Obst.", True, NEGRO),
                          (self.add_obstacle_button.x + 15, self.add_obstacle_button.y + 15))

        # Obstáculos agregados
        y = self.add_obstacle_button.y + 70
        for obs in self.temp_obstacles:
            text_surf = self.fuente.render(f"{obs.id} - {obs.tipo} X:{obs.posX} Y:{obs.posY}", True, NEGRO)
            self.display.blit(text_surf, (300, y))
            y += 25

        pygame.display.flip()

    # -------------------- Funciones de botones --------------------
    def agregar_obstaculo(self):
        try:
            # Leer valores de inputs
            id_ = int(self.obstacle_texts[0])
            tipo = self.obstacle_texts[1]
            posX = int(self.obstacle_texts[2])
            posY = int(self.obstacle_texts[3])
            ancho = int(self.obstacle_texts[4])
            alto = int(self.obstacle_texts[5])
            daño = int(self.obstacle_texts[6])

            imagen_ruta = f"assets/images/obstacle/{tipo.lower()}.png"

            # Crear obstáculo
            obs = Obstacle(
                id_=id_,
                tipo=tipo,
                posX=posX,
                posY=posY,
                ancho=ancho,
                alto=alto,
                imagen=imagen_ruta,
                daño=daño,
                user_created=True
            )

            # Agregar a lista temporal
            self.temp_obstacles.append(obs)
            self.obstacle_texts = [""]*7

            # Guardar en JSON
            try:
                with open("config/config.json", "r") as f:
                    config = json.load(f)
            except FileNotFoundError:
                config = {}

            if "obstaculos" not in config:
                config["obstaculos"] = []

            # Reemplaza si existe el mismo ID
            config["obstaculos"] = [o for o in config["obstaculos"] if o["id"] != id_]
            config["obstaculos"].append({
                "id": obs.id,
                "tipo": obs.tipo,
                "posX": obs.posX,
                "posY": obs.posY,
                "ancho": obs.ancho,
                "alto": obs.alto,
                "imagen": imagen_ruta,
                "daño": obs.daño
            })

            with open("config/config.json", "w") as f:
                json.dump(config, f, indent=4)

        except ValueError:
            print("Ingrese valores válidos para el obstáculo")


    def iniciar_juego(self):
        # Guardar inputs de juego en config
        claves = [
            ("carretera", "longitud"),
            ("carrito", "salto"),
            ("carrito", "avance_m"),
            ("carrito", "avance_ms")
        ]
        for i, text in enumerate(self.input_texts):
            try:
                clave_principal, subclave = claves[i]
                self.config[clave_principal][subclave] = float(text)
            except ValueError:
                pass

        # Crear AVL con obstáculos
        avl = AVL()
        for obs in self.temp_obstacles:
            avl.insert(obs)

        # Cambiar pantalla a GameScreen
        game_screen = GameScreen(self.game.display, self.config, self.game, avl)
        self.game.set_screen(game_screen)