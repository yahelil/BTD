from Constants import Constants as const


# Function to draw the map
def draw_map():
    for row in range(const.GRID_HEIGHT):
        for col in range(const.GRID_WIDTH):
            if (col, row) in const.path:
                const.screen.blit(const.pathImg, (col * const.CELL_SIZE, row * const.CELL_SIZE))
            else:
                const.screen.blit(const.grassImg, (col * const.CELL_SIZE, row * const.CELL_SIZE))
    const.screen.blit(const.buyingdartImg, ((const.GRID_WIDTH - 2) * const.CELL_SIZE, 0))

