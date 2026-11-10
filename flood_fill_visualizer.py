# flood fill visualizer (dfs only)
# click a cell to fill, press r for a new grid

import random
import pygame

# grid size
cols = 24
rows = 18
cell = 32
width = cols * cell
height = rows * cell
fps = 60
steps_per_frame = 1   # how many cells to fill each frame

# colors (the number in the grid is the index of this list)
colors = [
    (231, 76, 60),
    (46, 204, 113),
    (52, 152, 219),
    (241, 196, 15),
    (155, 89, 182),
    (230, 126, 34),
]
line_color = (20, 22, 27)

# up, down, left, right
dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def make_grid():
    # start with one background color
    bg = random.randrange(len(colors))
    grid = [[bg for c in range(cols)] for r in range(rows)]

    # draw some random blobs on top
    for i in range(14):
        color = random.randrange(len(colors))
        r = random.randrange(rows)
        c = random.randrange(cols)
        for j in range(random.randint(15, 60)):
            grid[r][c] = color
            # random walk, stay inside the grid
            dr, dc = random.choice(dirs)
            r = max(0, min(rows - 1, r + dr))
            c = max(0, min(cols - 1, c + dc))
    return grid


def flood_fill(grid, row, col, new_color):
    # dfs with a stack
    # yield after each cell so we can draw it
    old_color = grid[row][col]
    if old_color == new_color:
        return

    stack = [(row, col)]
    visited = {(row, col)}

    while stack:
        r, c = stack.pop()       # take the newest cell (dfs)
        grid[r][c] = new_color

        # check the 4 neighbors
        for dr, dc in dirs:
            nr = r + dr
            nc = c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if (nr, nc) not in visited and grid[nr][nc] == old_color:
                    visited.add((nr, nc))
                    stack.append((nr, nc))

        yield


def draw_grid(screen, grid):
    for r in range(rows):
        for c in range(cols):
            rect = pygame.Rect(c * cell, r * cell, cell, cell)
            pygame.draw.rect(screen, colors[grid[r][c]], rect)
            pygame.draw.rect(screen, line_color, rect, 1)


def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Flood Fill (DFS) - click to fill, R = new grid")
    clock = pygame.time.Clock()

    grid = make_grid()
    gen = None   # the running flood fill (None = not filling)

    running = True
    while running:
        clock.tick(fps)

        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    grid = make_grid()
                    gen = None

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # only start a new fill if nothing is running
                if gen is None:
                    mx, my = event.pos
                    row = my // cell
                    col = mx // cell
                    # pick a random new color that is different from the old one
                    old_color = grid[row][col]
                    options = [i for i in range(len(colors)) if i != old_color]
                    new_color = random.choice(options)
                    gen = flood_fill(grid, row, col, new_color)

        # update
        if gen is not None:
            for i in range(steps_per_frame):
                try:
                    next(gen)
                except StopIteration:
                    gen = None
                    break

        # draw
        draw_grid(screen, grid)
        pygame.display.flip()

    pygame.quit()


main()
