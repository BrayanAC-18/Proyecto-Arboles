class Colision:
    def __init__(self, carrito, obstaculo):
        self.carrito = carrito
        self.obstaculo = obstaculo

    def check_colision(self):
        if (self.carrito.x < self.obstaculo.x + self.obstaculo.width and
            self.carrito.x + self.carrito.width > self.obstaculo.x and
            self.carrito.y < self.obstaculo.y + self.obstaculo.height and
            self.carrito.y + self.carrito.height > self.obstaculo.y):
            return True
        return False
    
    def __repr__(self):
        return f"Colision(carrito={self.carrito}, obstaculo={self.obstaculo})"
    