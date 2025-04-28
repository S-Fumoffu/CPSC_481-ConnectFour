import pygame as pg

class InvisibleButton:
    def __init__(self, x, y, width, height):
        self.rect = pg.Rect(x, y, width, height)
        self.color = (0, 0, 0, 0)  # Fully transparent

    def draw(self, screen):
        # We don't draw anything because it's invisible, but you can still detect clicks
        pass

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)