# button.py
import pygame

class Button:
    def __init__(self, x, y, w, h, text, color, text_color):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.SysFont("arial", 22, bold=True)

    def draw(self, screen):
        # Kesan visual apabila tetikus berada di atas butang (Hover effect)
        mouse_pos = pygame.mouse.get_pos()
        draw_color = tuple(min(c + 25, 255) for c in self.color) if self.rect.collidepoint(mouse_pos) else self.color
        
        pygame.draw.rect(screen, draw_color, self.rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, width=2, border_radius=10)

        text_surface = self.font.render(self.text, True, self.text_color)
        screen.blit(
            text_surface,
            (
                self.rect.centerx - text_surface.get_width() // 2,
                self.rect.centery - text_surface.get_height() // 2
            )
        )

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
