# score.py
class Score:
    def __init__(self):
        self.value = 5000

    def add(self, amount):
        self.value += amount

    def minus(self, amount):
        self.value = max(0, self.value - amount)

    def reset(self):
        self.value = 5000
