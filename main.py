import json
from models.game import Game
from models.gamescreen import GameScreen

# Cargar configuración
with open("config/config.json", "r", encoding="utf-8") as file:
    config = json.load(file)

# -------------------- Ejecutar el juego --------------------
if __name__ == "__main__":
    juego = Game(config)
    pantalla_juego = GameScreen(juego.display, config, juego)
    juego.set_screen(pantalla_juego)

