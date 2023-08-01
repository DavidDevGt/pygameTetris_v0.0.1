import pygame
import random
import time

# Basic setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
COLORS = [(0,0,0), (120,37,179), (100,179,179), (80,34,22), (80,134,22), (180,34,22), (180,34,122)]
SHAPES = [[1, 1, 1, 1]], [[1, 1], [1, 1]], [[1, 1, 0], [0, 1, 1]], [[0, 1, 1], [1, 1]], [[1, 1, 1], [0, 1, 0]], [[1, 1, 1], [0, 0, 1]], [[1, 1, 1], [1, 0, 0]]

class Shape:
    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = random.randint(1, len(COLORS)-1)

    def rotate(self):
        self.shape = [list(i) for i in zip(*self.shape[::-1])]

def create_shape():
    return Shape(GRID_WIDTH // 2, 0, random.choice(SHAPES))

def is_valid_position(shape, grid):
    for i in range(4):
        for j in range(4):
            if i < len(shape.shape) and j < len(shape.shape[i]) and shape.shape[i][j]:
                if i + shape.y > GRID_HEIGHT - 1 or j + shape.x > GRID_WIDTH - 1 or j + shape.x < 0 or grid[i + shape.y][j + shape.x] != 0:
                    return False
    return True

def freeze_shape(shape, grid):
    for i in range(4):
        for j in range(4):
            if i < len(shape.shape) and j < len(shape.shape[i]) and shape.shape[i][j]:
                grid[shape.y + i][shape.x + j] = shape.color

def clear_rows(grid):
    full_rows = [i for i, row in enumerate(grid) if 0 not in row]
    for i in full_rows:
        del grid[i]
        grid.insert(0, [0 for _ in range(GRID_WIDTH)])
    return len(full_rows)

def draw_grid(screen, grid):
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            pygame.draw.rect(screen, COLORS[cell], (j*GRID_SIZE, i*GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)

def draw_shape(screen, shape):
    for i, row in enumerate(shape.shape):
        for j, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, COLORS[shape.color], ((j+shape.x)*GRID_SIZE, (i+shape.y)*GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)

def game_loop():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    current_shape = create_shape()
    running = True
    last_move_down_time = time.time()

    while running:
        screen.fill((0, 0, 0))

        if time.time() - last_move_down_time > 0.5:  # Move the shape down every half second
            current_shape.y += 1
            if not is_valid_position(current_shape, grid):
                current_shape.y -= 1
                freeze_shape(current_shape, grid)
                current_shape = create_shape()
                if not is_valid_position(current_shape, grid):
                    running = False  # Game over if a new shape can't be placed
            last_move_down_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                handle_keydown(event, current_shape, grid)

        clear_rows(grid)

        draw_grid(screen, grid)
        draw_shape(screen, current_shape)
        pygame.display.update()
        clock.tick(60)

    pygame.quit()

def handle_keydown(event, shape, grid):
    x, y = shape.x, shape.y

    if event.key == pygame.K_UP:
        shape.rotate()
    elif event.key == pygame.K_DOWN:
        shape.y += 1
    elif event.key == pygame.K_LEFT:
        shape.x -= 1
    elif event.key == pygame.K_RIGHT:
        shape.x += 1

    if not is_valid_position(shape, grid):
        shape.x, shape.y = x, y  # Undo movement/rotation if invalid

game_loop()
