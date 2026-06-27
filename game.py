# game.py
import pygame
from settings import *
from boat import Boat
from rules import Rules
from timer import Timer
from score import Score
from level import Level

class Game:
    def __init__(self, lang="EN"):
        self.font = pygame.font.SysFont("arial", 24, bold=True)
        self.big = pygame.font.SysFont("arial", 54, bold=True)

        self.rules = Rules()
        self.boat = Boat()
        self.score = Score()
        self.timer = Timer(120)

        self.level_num = 1
        self.state = "playing"
        self.lang = lang
        
        self.selected = None
        self.message = ""
        self.load_level()

    def load_level(self):
        self.level = Level(self.level_num)
        self.entities = self.level.get_entities()
        self.timer.reset(self.level.get_time_limit())
        
        self.boat.capacity = []
        self.boat.side = "left"
        self.selected = None
        self.message = ""
        self.align_positions()

    def align_positions(self):
        bx = self.boat.get_x()
        for e in self.entities:
            if e.on_boat:
                idx = self.boat.capacity.index(e)
                e.x = bx + 20 + (idx * 75)
                e.y = self.boat.y - 30
            else:
                e.x = 60 if e.side == "left" else 810
                e.y = e.base_y

    def trigger_boat_movement(self):
        crew = [passenger.name_en for passenger in self.boat.capacity]
        if "Farmer" not in crew:
            self.message = "The Farmer must row the boat!" if self.lang == "EN" else "Petani wajib mengayuh bot!"
            return

        self.boat.move()
        for e in self.boat.capacity:
            e.side = self.boat.side
            
        self.align_positions()
        
        # Semak kalah selepas bot bergerak
        failed, reason_code = self.rules.check_lose(self.entities)
        if failed:
            self.score.minus(1000)
            self.state = "lose"
            reasons = {
                "CHICKEN_CORN": ("The Chicken pecked the Corn!", "Ayam mematuk Jagung!"),
                "WOLF_CHICKEN": ("The Wolf ate the Chicken!", "Serigala memakan Ayam!"),
                "WOLF_COW": ("The Wolf attacked the Cow!", "Serigala menyerang Lembu!")
            }
            msg_en, msg_my = reasons.get(reason_code, ("Mission Failed!", "Misi Gagal!"))
            self.message = msg_en if self.lang == "EN" else msg_my
            return

        # Semak menang selepas bot bergerak
        if self.rules.check_win(self.entities):
            self.check_level_transition()

    def check_level_transition(self):
        if self.level_num < 3:
            self.level_num += 1
            self.load_level()
            self.message = f"Welcome to Level {self.level_num}!" if self.lang == "EN" else f"Selamat datang ke Tahap {self.level_num}!"
        else:
            self.state = "win"

    def update(self, event, dt):
        if self.state != "playing":
            return

        self.timer.update(dt)
        
        # --- TAMBAH LOGIK PENGURANGAN SKOR DI SINI ---
        # Contoh: Tolak 10 mata untuk setiap saat (10 * dt)
        # Fungsi self.score.minus() memastikan skor tidak akan jatuh bawah daripada 0
        if self.timer.time_left > 0:
            self.score.minus(10 * dt)
        # ---------------------------------------------

        if self.timer.is_time_up():
            self.message = "Time Out!" if self.lang == "EN" else "Masa Tamat!"
            self.state = "lose"
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            bx = self.boat.get_x()
            boat_rect = pygame.Rect(bx, self.boat.y, 190, 95)

            # Kekal kapasiti 2 untuk semua tahap (Petani + 1 Item)
            max_boat_capacity = 2

            clicked_on_item = False
            for e in self.entities:
                if e.clicked(pos):
                    clicked_on_item = True
                    if e.on_boat:
                        e.on_boat = False
                        self.boat.capacity.remove(e)
                        self.align_positions()
                        
                        failed, reason_code = self.rules.check_lose(self.entities)
                        if failed:
                            self.state = "lose"
                            self.message = "Left unsecured!" if self.lang == "EN" else "Ditinggalkan tanpa pengawasan!"
                        
                        if self.rules.check_win(self.entities):
                            self.check_level_transition()
                    else:
                        self.selected = e
                        self.message = ""

            if boat_rect.collidepoint(pos) and not clicked_on_item:
                if self.selected:
                    if self.selected.side == self.boat.side and not self.selected.on_boat:
                        if len(self.boat.capacity) < max_boat_capacity:
                            self.selected.on_boat = True
                            self.boat.capacity.append(self.selected)
                            self.selected = None
                            self.align_positions()
                        else:
                            self.message = "Boat is full!" if self.lang == "EN" else "Bot sudah penuh!"
                else:
                    if len(self.boat.capacity) > 0:
                        for passenger in list(self.boat.capacity):
                            passenger.on_boat = False
                        self.boat.capacity.clear()
                        self.align_positions()
                        
                        failed, reason_code = self.rules.check_lose(self.entities)
                        if failed:
                            self.state = "lose"
                            self.message = "Left unsecured!" if self.lang == "EN" else "Ditinggalkan tanpa pengawasan!"

    def draw(self, screen):
        screen.fill(SKY_BLUE)
        pygame.draw.rect(screen, LAND_GREEN, (0, 140, 230, 510))
        pygame.draw.rect(screen, RIVER_BLUE, (230, 140, 490, 510))
        pygame.draw.rect(screen, LAND_GREEN, (720, 140, 230, 510))
        pygame.draw.rect(screen, UI_NAVY, (0, 0, WIDTH, 140))

        self.boat.draw(screen)
        for e in self.entities:
            e.draw(screen, self.lang)

        lbl_lvl = f"LEVEL: {self.level_num}/3"
        lbl_tm = f"TIME REMAINING: {int(self.timer.time_left)}s" if self.lang == "EN" else f"MASA TINGGAL: {int(self.timer.time_left)}s"
        lbl_sc = f"SCORE: {int(self.score.value)}"
        
        screen.blit(self.font.render(lbl_lvl, True, GOLD), (40, 25))
        screen.blit(self.font.render(lbl_tm, True, CRIMSON), (WIDTH//2 - 120, 25))
        screen.blit(self.font.render(lbl_sc, True, WHITE), (WIDTH - 210, 25))

        if self.selected:
            sel_lbl = f"Selected: {self.selected.get_name(self.lang)}" if self.lang == "EN" else f"Dipilih: {self.selected.get_name(self.lang)}"
            screen.blit(self.font.render(sel_lbl, True, GOLD), (40, 80))

        if self.message:
            msg_surf = self.font.render(self.message, True, GOLD)
            screen.blit(msg_surf, (WIDTH//2 - msg_surf.get_width()//2, 80))

        if self.state in ["win", "lose"]:
            screen.fill(LAND_GREEN if self.state == "win" else CRIMSON)
            title_text = "CONGRATULATIONS! YOU WIN!" if self.state == "win" else "MISSION FAILED!"
            if self.lang == "MY":
                title_text = "TAHNIAH! ANDA MENANG!" if self.state == "win" else "MISI GAGAL!"
                
            t_surf = self.big.render(title_text, True, WHITE)
            screen.blit(t_surf, (WIDTH//2 - t_surf.get_width()//2, 180))

            sc_surf = self.font.render(f"Final Score: {int(self.score.value)}", True, GOLD)
            screen.blit(sc_surf, (WIDTH//2 - sc_surf.get_width()//2, 290))

            if self.message:
                m_surf = self.font.render(self.message, True, WHITE)
                screen.blit(m_surf, (WIDTH//2 - m_surf.get_width()//2, 350))

            hint = "Press ESC to return to Main Menu" if self.lang == "EN" else "Tekan ESC untuk kembali ke Menu Utama"
            h_surf = self.font.render(hint, True, WHITE)
            screen.blit(h_surf, (WIDTH//2 - h_surf.get_width()//2, 460))
