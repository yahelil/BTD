import pygame
from Constants import Constants as const


class Balloon:
    def __init__(self):
        # Load the balloon image
        self.image = None
        self.speed = None
        self.health = None
        self.current_point_index = 0
        self.x, self.y = const.path[self.current_point_index]
        self.x *= const.CELL_SIZE
        self.y *= const.CELL_SIZE

    def move(self):
        if self.current_point_index < len(const.path) - 1:
            # Calculate direction to the next point
            next_x, next_y = const.path[self.current_point_index + 1]
            next_y *= const.CELL_SIZE
            next_x *= const.CELL_SIZE
            # Move towards the next point
            if self.x < next_x:
                self.x += self.speed  # Move right
            elif self.x > next_x:
                self.x -= self.speed  # Move left
            if self.y < next_y:
                self.y += self.speed  # Move down
            elif self.y > next_y:
                self.y -= self.speed  # Move up

            # Check if the balloon has reached the next point
            if (self.x, self.y) == (next_x, next_y):
                self.current_point_index += 1  # Move to the next point
        if self.is_out_of_bounds():
            self.destroy()

    def draw(self, screen):
        # Draw the balloon on the screen at its current position
        screen.blit(self.image, (self.x, self.y))

    def is_out_of_bounds(self):
        # Check if the balloon has gone off the screen (or out of the game area)
        return self.x+const.CELL_SIZE > (const.SCREEN_WIDTH - 2) or self.x <= 0 or self.y <= 0 or self.y + const.CELL_SIZE > (const.SCREEN_HEIGHT-2)

    def take_damage(self, amount):
        # Reduce health by the amount of damage taken
        self.health -= amount
        if self.health <= 0:
            self.destroy()  # Call the destroy method if health drops to 0

    @staticmethod
    def destroy():
        # Handle balloon destruction (you might want to remove it from the game)
        print("Balloon destroyed!")


class RedBalloon(Balloon):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/redballoon.png')  # Path to your balloon image
        self.image = pygame.transform.scale(self.image, (const.CELL_SIZE, const.CELL_SIZE))  # Scale to cell size
        self.speed = 4  # Speed at which the balloon moves
        self.health = 1  # Health of the balloon


class BlueBalloon(Balloon):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/blueballoon.png')  # Path to your balloon image
        self.image = pygame.transform.scale(self.image, (const.CELL_SIZE, const.CELL_SIZE))  # Scale to cell size
        self.speed = 2  # Speed at which the balloon moves
        self.health = 2  # Health of the balloon