import pygame
from Constants import Constants as const


class Tower:
    def __init__(self):
        self.image = None

    @staticmethod
    def is_valid_tower_placement(x, y):
        # Convert pixel coordinates to grid coordinates
        col = x // const.CELL_SIZE
        row = y // const.CELL_SIZE
        # Return True if the selected cell is not part of the path
        return (col, row) not in const.path

    def place_tower(self, x, y):
        if self.is_valid_tower_placement(x, y):
            # Convert pixel coordinates to grid and draw a tower
            col = x // const.CELL_SIZE
            row = y // const.CELL_SIZE
            const.screen.blit(self.image, (col * const.CELL_SIZE, row * const.CELL_SIZE))


class DartMonkey(Tower):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(f'images/dartmonkey.png')
        self.image = pygame.transform.scale(self.image, (const.CELL_SIZE, const.CELL_SIZE))  # Scale to cell size
        self.speed = 1  # A dart per second
        self.damage = 1  # Deals 1 damage per hit
        self.rage = 32  # Radius of 32 pixels
        self.position = None

    def attack(self):
        # Define specific attack behavior for DartMonkey
        pass  # Implement your attack logic here

    def upgrade(self):
        # Define upgrade behavior for DartMonkey
        pass  # Implement your upgrade logic here