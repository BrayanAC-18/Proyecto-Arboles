import pygame

pygame.init()

class Game:
    def __init__(self, config):
        self.config = config
        self.display = pygame.display.set_mode((config["ventana"]["ancho"], config["ventana"]["alto"]))
        pygame.display.set_caption("Juego del Carrito")
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_screen = None

    def set_screen(self, screen):
        self.current_screen = screen
        print(self.config)
        self.run()

    def run(self):
        while self.running:
            dt_ms = self.clock.tick(self.config["ventana"]["fps"])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif self.current_screen:
                    self.current_screen.handle_event(event)

            if self.current_screen:
                self.current_screen.update(dt_ms)
                self.current_screen.draw()

            pygame.display.update()
        pygame.quit()
