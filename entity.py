# entity.py
import pygame
import os

class Entity:
    def __init__(self, name_en, name_my, image_path, base_y, color):
        self.name_en = name_en
        self.name_my = name_my
        self.color = color
        
        self.side = "left"
        self.on_boat = False
        self.x = 60
        self.y = base_y
        self.base_y = base_y

        # Sistem semakan imej selamat (Fallback rendering jika tiada fail gambar)
        self.image = None
        if os.path.exists(image_path):
            try:
                self.image = pygame.image.load(image_path).convert_alpha()
                self.image = pygame.transform.scale(self.image, (65, 65))
            except Exception:
                self.image = None

    def get_name(self, lang):
        return self.name_en if lang == "EN" else self.name_my

    def draw(self, screen, lang):
        if self.image:
            screen.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(screen, self.color, (self.x, self.y, 65, 65), border_radius=8)
            pygame.draw.rect(screen, (240, 240, 240), (self.x, self.y, 65, 65), width=2, border_radius=8)

        font = pygame.font.SysFont("arial", 14, bold=True)
        txt_color = (20, 22, 30) if self.color in [(255, 255, 255), (255, 210, 0)] else (255, 255, 255)
        text = font.render(self.get_name(lang), True, txt_color)
        screen.blit(text, (self.x + 4, self.y + 24))

    def clicked(self, pos):
        rect = pygame.Rect(self.x, self.y, 65, 65)
        return rect.collidepoint(pos)
