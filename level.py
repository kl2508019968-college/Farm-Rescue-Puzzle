# level.py
from entity import Entity
from settings import *

class Level:
    def __init__(self, level_num):
        self.level_num = level_num

    def get_time_limit(self):
        limits = {1: 120, 2: 90, 3: 60}
        return limits.get(self.level_num, 60)

    def get_entities(self):
        if self.level_num == 1:
            return [
                Entity("Farmer", "Petani", "assets/farmer.png", 180, UI_NAVY),
                Entity("Cow", "Lembu", "assets/cow.png", 270, WHITE),
                Entity("Corn", "Jagung", "assets/corn.png", 360, GOLD)
            ]
        elif self.level_num == 2:
            return [
                Entity("Farmer", "Petani", "assets/farmer.png", 180, UI_NAVY),
                Entity("Wolf", "Serigala", "assets/wolf.png", 270, BLACK),
                Entity("Chicken", "Ayam", "assets/chicken.png", 360, CRIMSON),
                Entity("Corn", "Jagung", "assets/corn.png", 450, GOLD)
            ]
        else:
            return [
                Entity("Farmer", "Petani", "assets/farmer.png", 160, UI_NAVY),
                Entity("Wolf", "Serigala", "assets/wolf.png", 235, BLACK),
                Entity("Cow", "Lembu", "assets/cow.png", 310, WHITE),
                Entity("Chicken", "Ayam", "assets/chicken.png", 385, CRIMSON),
                Entity("Corn", "Jagung", "assets/corn.png", 460, GOLD)
            ]
