# menu.py
import pygame
from settings import *
from button import Button

class Menu:
    def __init__(self):
        self.title_font = pygame.font.SysFont("arial", 52, bold=True)
        self.font = pygame.font.SysFont("arial", 22, bold=True)
        self.lang = "EN"
        self.refresh_buttons()

    def refresh_buttons(self):
        lbl_start = "START GAME" if self.lang == "EN" else "MULA PERMAINAN"
        lbl_inst = "INSTRUCTIONS" if self.lang == "EN" else "ARAHAN"
        lbl_lang = "LANGUAGE: EN" if self.lang == "EN" else "BAHASA: MY"
        lbl_exit = "EXIT" if self.lang == "EN" else "KELUAR"

        self.start_btn = Button(WIDTH//2 - 140, 240, 280, 55, lbl_start, UI_NAVY, GOLD)
        self.inst_btn = Button(WIDTH//2 - 140, 315, 280, 55, lbl_inst, UI_NAVY, WHITE)
        self.lang_btn = Button(WIDTH//2 - 140, 390, 280, 55, lbl_lang, UI_NAVY, WHITE)
        self.exit_btn = Button(WIDTH//2 - 140, 465, 280, 55, lbl_exit, CRIMSON, WHITE)

    def draw_menu(self, screen):
        screen.fill(BLACK)

        title = self.title_font.render("FARM RESCUE ADVENTURE", True, GOLD)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))

        self.start_btn.draw(screen)
        self.inst_btn.draw(screen)
        self.lang_btn.draw(screen)
        self.exit_btn.draw(screen)

    def draw_instructions(self, screen):
        screen.fill(BLACK)
        title_text = "GAME INSTRUCTIONS" if self.lang == "EN" else "ARAHAN PERMAINAN"
        title = self.title_font.render(title_text, True, GOLD)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))

        lines_en = [
            "Objective:",
            "  Move the Farmer and all resources safely to the right bank side.",
            "",
            "Rules:",
            "  - The boat holds a maximum capacity of 2 items.",
            "  - The Farmer must always navigate inside the boat to row it.",
            "  - Do NOT leave the Chicken alone with the Corn (The Chicken eats Corn).",
            "  - Do NOT leave the Wolf with the Chicken (The Wolf hunts Chicken).",
            "",
            "Controls: Left Click items to load/unload. Press [SPACE] to move the boat.",
            "Press ESC to return to main menu."
        ]
        
        lines_my = [
            "Objektif:",
            "  Pindahkan Petani dan semua item dengan selamat ke tebing kanan.",
            "",
            "Peraturan:",
            "  - Bot hanya boleh memuatkan maksimum 2 item pada satu masa.",
            "  - Petani mesti berada di dalam bot untuk mendayung menyeberang.",
            "  - JANGAN tinggalkan Ayam bersama Jagung (Ayam mematuk Jagung).",
            "  - JANGAN tinggalkan Serigala bersama Ayam (Serigala menyerang).",
            "",
            "Kawalan: Klik Kiri item untuk muat/turun. Tekan [SPACE] untuk gerakkan bot.",
            "Tekan ESC untuk kembali ke tetingkap Menu Utama."
        ]

        active_lines = lines_en if self.lang == "EN" else lines_my
        y = 150
        for line in active_lines:
            text = self.font.render(line, True, WHITE)
            screen.blit(text, (60, y))
            y += 35
