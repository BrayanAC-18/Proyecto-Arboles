import pygame
import json
from models.game import Game
from models.main_menu import MainMenuScreen  # el menú que creamos

pygame.init()

# Cargar configuración
with open("config/config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

# Iniciar juego
juego = Game(config)
menu = MainMenuScreen(juego.display, config, juego)
juego.set_screen(menu)
