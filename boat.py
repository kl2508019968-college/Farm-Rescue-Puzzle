# boat.py
import pygame
import os
from settings import *

class Boat:
    def __init__(self):
        self.x_left = 250
        self.x_right = 510
        self.y = 390
        self.side = "left"
        self.capacity = []

        # Memastikan aset gambar dimuatkan SEKALI sahaja di dalam __init__ demi prestasi kelancaran FPS
        self.image = None
        if os.path.exists("assets/boat.png"):
            try:
                self.image = pygame.image.load("assets/boat.png").convert_alpha()
                self.image = pygame.transform.scale(self.image, (190, 95))
            except Exception:
                self.image = None

    def move(self):
        self.side = "right" if self.side == "left" else "left"

    def get_x(self):
        return self.x_left if self.side == "left" else self.x_right

    def draw(self, screen):
        x = self.get_x()
        if self.image:
            screen.blit(self.image, (x, self.y))
        else:
            pygame.draw.polygon(screen, WOOD_BROWN, [
                (x, self.y + 30), 
                (x + 25, self.y + 85), 
                (x + 165, self.y + 85), 
                (x + 190, self.y + 30)
            ])
