import pygame
from Constants import Constants as const
from Tower import DartMonkey
from map import draw_map
from Balloon import RedBalloon as RB
from Balloon import BlueBalloon as BB

pygame.init()

towers = []
balloons = []

# Initialize timing variables

balloon_index = 0
balloon_spawn_interval = 400  # Time in milliseconds between spawns (1 second)
last_balloon_spawn_time = 0  # Start at 0

# Create a clock object to control frame rate
clock = pygame.time.Clock()
FPS = 60  # Frames per second


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


def draw_money():
    money_text = const.font.render(f'Money: ${const.current_money}', True, (255, 255, 255))  # White color
    const.screen.blit(money_text, (120, 10))  # Position at top left corner


def draw_health():
    health_text = const.font.render(f'Health: {const.current_health}', True, (255, 255, 255))  # White color
    const.screen.blit(health_text, (10, 10))  # Position at top left corner


def initialize_level_one():
    for type in const.LEVEL1:
        if type[1] == 'r':
            balloon_queue.extend([RB() for _ in range(type[0])])
        elif type[1] == 'b':
            balloon_queue.extend([BB() for _ in range(type[0])])


running = True
selected_tower_for_range = None  # Track which tower's range to show

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
            else:
                # Check if a tower is clicked
                clicked_on_tower = False
                for tower, tx, ty in towers:
                    tower_rect = pygame.Rect(tx, ty, const.CELL_SIZE, const.CELL_SIZE)
                    if tower_rect.collidepoint(event.pos):
                        selected_tower_for_range = tower
                        clicked_on_tower = True
                        break
                if not clicked_on_tower:
                    selected_tower_for_range = None  # Deselect the tower if clicked elsewhere

        # Detect mouse button up to place the tower
        if event.type == pygame.MOUSEBUTTONUP:
            if is_dragging:
                is_dragging = False
                x, y = event.pos
                x = x // const.CELL_SIZE * const.CELL_SIZE
                y = y // const.CELL_SIZE * const.CELL_SIZE
                if selected_tower.is_valid_tower_placement(x, y) and const.current_money - 215 >=0:
                    towers.append((selected_tower, x, y))
                    const.current_money -= 215

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
    else:
        balloon_index = 0
        initialize_level_one()
        const.current_money += const.level_money

    # Move and draw balloons
    for balloon in balloons[:]:  # Iterate over a copy of the list
        balloon.move(delta_time)  # Pass delta_time to adjust movement speed
        balloon.draw(const.screen)
        if balloon.is_out_of_bounds():
            balloons.remove(balloon)  # Remove the balloon if destroyed or out of bounds
            const.current_health -= balloon.health
        if balloon.health <= 0:
            balloons.remove(balloon)

    # Draw all towers from the list
    for tower, x, y in towers:
        tower.place_tower(x, y)

    # If dragging, show a visual representation of where the tower will be placed
    if is_dragging:
        x, y = pygame.mouse.get_pos()
        const.screen.blit(selected_tower.image, (x // const.CELL_SIZE * const.CELL_SIZE, y // const.CELL_SIZE * const.CELL_SIZE))

    # If a tower is selected, show its range
    if selected_tower_for_range:
        for tower, x, y in towers:
            if tower == selected_tower_for_range:
                tower.draw_range()  # Show range of the selected tower

    # Checking for balloons to attack
    for tower, x, y in towers:
        balloon_in_range = tower.is_balloon_in_range(balloons)

        if balloon_in_range:
            tower.attack(balloon_in_range)
            # Perform action like attacking this balloon

    # Draw the amount of money
    draw_money()
    # Draw health
    draw_health()
    if const.current_health == 0:
        break
    # Update the display
    pygame.display.flip()

pygame.quit()
