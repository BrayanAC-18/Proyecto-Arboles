class Screen:
    def __init__(self, display, config):
        self.display = display
        self.config = config

    def handle_event(self, event):
        """Procesar eventos de teclado y mouse"""
        pass

    def update(self, dt_ms):
        """Actualizar estado del escenario"""
        pass

    def draw(self):
        """Dibujar todos los elementos en pantalla"""
        pass