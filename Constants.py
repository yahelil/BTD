import pygame

pygame.init()


class Constants:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    CELL_SIZE = 40  # Size of each cell in the grid
    GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE
    GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE
    path = [
        (0, 3), (1, 3), (2, 3), (3, 3),
        (4, 3), (5, 3), (6, 3), (7, 3),
        (7, 4), (7, 5), (6, 5), (5, 5),
        (5, 6), (5, 7), (6, 7), (7, 7),
        (8, 7), (9, 7), (9, 6), (10, 6),
        (11, 6), (11, 5), (12, 5), (13, 5),
        (13, 6), (14, 6), (15, 6), (15, 7),
        (16, 7), (17, 7), (18, 7), (19, 7)
    ]
    LEVEL1 = ((10, 'r'), (5, 'b'))
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tower Defense Map")

    pathImg = pygame.image.load('images/path.png')
    pathImg = pygame.transform.scale(pathImg, (CELL_SIZE, CELL_SIZE))  # Scale to cell size
    grassImg = pygame.image.load('images/grass.png')
    grassImg = pygame.transform.scale(grassImg, (CELL_SIZE, CELL_SIZE))  # Scale to cell size
    buyingdartImg = pygame.image.load('images/buyingdartmonkey.png')
    buyingdartImg = pygame.transform.scale(buyingdartImg, (2*CELL_SIZE, 2*CELL_SIZE))  # Scale to cell size