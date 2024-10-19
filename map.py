import pygame
from Constants import Constants as const
from Tower import DartMonkey
from Balloon import RedBalloon as RB
from Balloon import BlueBalloon as BB

pygame.init()

# Colors
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)  # For the path

towers = []
balloons = []

# Initialize timing variables
balloon_index = 0
balloon_spawn_interval = 500  # Time in milliseconds between spawns (1 second)
last_balloon_spawn_time = 0  # Start at 0

# Create a clock object to control frame rate
clock = pygame.time.Clock()
FPS = 60  # Frames per second


# Function to draw the map
def draw_map():
    for row in range(const.GRID_HEIGHT):
        for col in range(const.GRID_WIDTH):
            if (col, row) in const.path:
                const.screen.blit(const.pathImg, (col * const.CELL_SIZE, row * const.CELL_SIZE))
            else:
                const.screen.blit(const.grassImg, (col * const.CELL_SIZE, row * const.CELL_SIZE))
    const.screen.blit(const.buyingdartImg, ((const.GRID_WIDTH - 2) * const.CELL_SIZE, 0))

# Define the size of the selection area (2 grids high and wide)
selection_area_size = const.CELL_SIZE * 2
selection_area_x = const.SCREEN_WIDTH - selection_area_size
selection_area_y = 0
selection_area = pygame.Rect(selection_area_x, selection_area_y, selection_area_size, selection_area_size)

# Variable to track if the user is dragging
is_dragging = False
selected_tower = DartMonkey()  # Set the tower type to place

# Create a queue of balloons based on LEVEL1
balloon_queue = []
for type in const.LEVEL1:
    if type[1] == 'r':
        balloon_queue.extend([RB() for _ in range(type[0])])
    elif type[1] == 'b':
        balloon_queue.extend([BB() for _ in range(type[0])])

running = True
while running:
    # Control the frame rate
    delta_time = clock.tick(FPS) / 1000.0  # Time passed since last frame in seconds

    current_time = pygame.time.get_ticks()  # Get the current time in milliseconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Detect mouse button down to start dragging
        if event.type == pygame.MOUSEBUTTONDOWN:
            if selection_area.collidepoint(event.pos):
                is_dragging = True

        # Detect mouse button up to place the tower
        if event.type == pygame.MOUSEBUTTONUP:
            if is_dragging:
                is_dragging = False
                x, y = event.pos
                if selected_tower.is_valid_tower_placement(x, y):
                    towers.append((selected_tower, x, y))

    # Clear the screen
    const.screen.fill((0, 0, 0))

    # Draw the map
    draw_map()

    # Spawn balloons at intervals
    if balloon_index < len(balloon_queue):
        if current_time - last_balloon_spawn_time > balloon_spawn_interval:
            balloons.append(balloon_queue[balloon_index])
            balloon_index += 1
            last_balloon_spawn_time = current_time  # Reset the spawn timer

    # Move and draw balloons
    for balloon in balloons[:]:  # Iterate over a copy of the list
        balloon.move(delta_time)  # Pass delta_time to adjust movement speed
        balloon.draw(const.screen)
        if balloon.is_out_of_bounds() or balloon.health <= 0:
            balloons.remove(balloon)  # Remove the balloon if destroyed or out of bounds

    # Draw all towers from the list
    for tower, x, y in towers:
        tower.place_tower(x, y)

    # If dragging, show a visual representation of where the tower will be placed
    if is_dragging:
        x, y = pygame.mouse.get_pos()
        const.screen.blit(selected_tower.image, (x // const.CELL_SIZE * const.CELL_SIZE, y // const.CELL_SIZE * const.CELL_SIZE))

    # Update the display
    pygame.display.flip()

pygame.quit()
