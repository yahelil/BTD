import math

import pygame
from Constants import Constants as const


class Tower:
    def __init__(self):
        self.image = None
        self.speed = None
        self.damage = None
        self.range = None
        self.x = None
        self.y = None

    @staticmethod
    def is_valid_tower_placement(x, y):
        # Convert pixel coordinates to grid coordinates
        col = x // const.CELL_SIZE
        row = y // const.CELL_SIZE
        # Return True if the selected cell is not part of the path
        return (col, row) not in const.path

    def place_tower(self, x, y):
        if self.is_valid_tower_placement(x, y):
            self.x = x
            self.y = y
            # Convert pixel coordinates to grid and draw a tower
            const.screen.blit(self.image, (x, y))

    def draw_range(self):
        # Calculate the center of the tower
        center_x = self.x + const.CELL_SIZE // 2
        center_y = self.y + const.CELL_SIZE // 2
        # Draw the circle at the center of the tower, with the range as the radius
        pygame.draw.circle(const.screen, (0, 0, 255), (center_x, center_y), self.range, 1)  # Blue circle, 1 pixel thick

    def is_balloon_in_range(self, balloon):
        # Calculate the distance between the tower and the balloon
        distance = math.sqrt((balloon.x - self.x) ** 2 + (balloon.y - self.y) ** 2)

        # Check if the distance is within the tower's range
        return distance <= self.range

class DartMonkey(Tower):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(f'images/dartmonkey.png')
        self.image = pygame.transform.scale(self.image, (const.CELL_SIZE, const.CELL_SIZE))  # Scale to cell size
        self.speed = 1  # A dart per second
        self.damage = 1  # Deals 1 damage per hit
        self.range = 80  # Radius of 32 pixels

    def attack(self):
        # Define specific attack behavior for DartMonkey
        pass  # Implement your attack logic here

    def upgrade(self):
        # Define upgrade behavior for DartMonkey
        pass  # Implement your upgrade logic here