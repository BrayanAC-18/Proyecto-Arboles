import json
from models.game import Game
from models.gamescreen import GameScreen
from avl.avl import AVL
from models.obstaculos import Obstacle


avl = AVL()

# Cargar configuración
with open("config/config.json", "r", encoding="utf-8") as file:
    config = json.load(file)

for obj in config["obstaculos"]:
    obs = Obstacle(
        obj["id"],
        obj["tipo"],
        obj["posX"],
        obj["posY"],
        obj["ancho"],
        obj["alto"],
        obj["imagen"],
        obj["daño"]
    )
    avl.insert(obs)


# -------------------- Ejecutar el juego --------------------
if __name__ == "__main__":
    juego = Game(config)
    pantalla_juego = GameScreen(juego.display, config, juego,  avl.root)
    juego.set_screen(pantalla_juego)


