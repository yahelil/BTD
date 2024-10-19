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

# Timer variables for balloon spawning
balloon_spawn_interval = 5000  # Time (milliseconds) between spawning each balloon
last_balloon_spawn_time = pygame.time.get_ticks()
balloon_index = 0  # To track which balloon to spawn next


# Function to draw the map
def draw_map():
    for row in range(const.GRID_HEIGHT):
        for col in range(const.GRID_WIDTH):
            if (col, row) in const.path:
                # pygame.draw.rect(screen, BROWN, rect)  # Draw the path
                const.screen.blit(const.pathImg, (col * const.CELL_SIZE, row * const.CELL_SIZE))
            else:
                const.screen.blit(const.grassImg, (col * const.CELL_SIZE, row * const.CELL_SIZE))
    const.screen.blit(const.buyingdartImg, ((const.GRID_WIDTH - 2) * const.CELL_SIZE, 0))


# Define the size of the selection area (2 grids high and wide)
selection_area_size = const.CELL_SIZE * 2  # Size in pixels (2 cells)
# Define the position of the selection area (top right corner)
selection_area_x = const.SCREEN_WIDTH - selection_area_size  # X position
selection_area_y = 0  # Y position (top of the screen)
selection_area = pygame.Rect(selection_area_x, selection_area_y, selection_area_size, selection_area_size)  # Create the rectangle

# Variable to track if the user is dragging
is_dragging = False
selected_tower = DartMonkey()  # Set the tower type to place
balloon_queue = []
for balloon_data in const.LEVEL1:
    count, balloon_type = balloon_data
    if balloon_type == 'r':
        balloon_queue.extend([RB()] * count)  # Add 'count' number of RedBalloon instances
    elif balloon_type == 'b':
        balloon_queue.extend([BB()] * count)  # Add 'count' number of BlueBalloon instances

running = True
while running:
    current_time = pygame.time.get_ticks()  # Get the current time in milliseconds
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Detect mouse button down to start dragging
        if event.type == pygame.MOUSEBUTTONDOWN:
            if selection_area.collidepoint(event.pos):  # Check if mouse is over selection area
                is_dragging = True

        # Detect mouse button up to place the tower
        if event.type == pygame.MOUSEBUTTONUP:
            if is_dragging:  # Only place tower if we were dragging
                is_dragging = False
                x, y = event.pos  # Get mouse position
                if selected_tower.is_valid_tower_placement(x, y):
                    towers.append((selected_tower, x, y))  # Store the tower and its position in the list

    # Clear the screen
    const.screen.fill((0, 0, 0))

    # Draw the map
    draw_map()

    # Staggered balloon spawning logic
    if balloon_index < len(balloon_queue) and current_time - last_balloon_spawn_time > balloon_spawn_interval:
        balloons.append(balloon_queue[balloon_index])  # Spawn the next balloon
        balloon_index += 1
        last_balloon_spawn_time = current_time  # Reset the spawn timer


    # Move and draw balloons
    for balloon in balloons[:]:  # Iterate over a copy of the list
        balloon.move()
        balloon.draw(const.screen)
        if balloon.is_out_of_bounds() or balloon.health <= 0:
            balloons.remove(balloon)  # Remove the balloon if destroyed or out of bounds

    # Draw all towers from the list
    for tower, x, y in towers:
        tower.place_tower(x, y)

    # If dragging, show a visual representation of where the tower will be placed
    if is_dragging:
        x, y = pygame.mouse.get_pos()
        # Draw a semi-transparent outline of the tower at the mouse position
        const.screen.blit(selected_tower.image, (x // const.CELL_SIZE * const.CELL_SIZE, y // const.CELL_SIZE * const.CELL_SIZE))

    # Update the display
    pygame.display.flip()

pygame.quit()