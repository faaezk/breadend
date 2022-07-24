class Quad():
    def __init__(self, x: float, y: float, width: float, height: float):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def get_topRight(self) -> tuple:
        return (self.x + self.width, self.y + self.height)
    
    def get_topLeft(self) -> tuple:
        return (self.x, self.y + self.height)
    
    def get_botRight(self) -> tuple:
        return (self.x + self.width, self.y)
    
    def get_botLeft(self) -> tuple:
        return (self.x, self.y)

