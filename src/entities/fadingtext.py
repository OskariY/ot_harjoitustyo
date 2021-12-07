from settings import BLACK, WHITE
from functions import print_text

fadey = 0
class FadingText():
    """
    A fading text popup that appears above the player, rises and disappears
    """
    
    def __init__(self, x, y, text, current_biome=1, color=BLACK):
        global fadey
        self.x = x
        self.y = y - fadey
        self.size = 16
        self.text = text
        self.color = color
        if current_biome == 3 and color == BLACK:
            self.color = WHITE
        fadey += 10

    def update(self, popups):
        global fadey
        self.size -= 0.3
        self.y -= 2
        if self.size < 8:
            popups.remove(self)
            fadey -= 10

    def draw(self, display, scrollx, scrolly):
        print_text(self.text, int(self.x - scrollx), int(round(self.y) - scrolly), 
                   display, 1, int(round(self.size)), self.color)


