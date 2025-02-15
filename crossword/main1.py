import pygame
import time
import asyncio

# Initialize Pygame
pygame.init()

grid_size = 5  # Change to 15 if needed
cell_size = 50
width, height = grid_size * cell_size + 300, grid_size * cell_size

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Crossword Grid
solution_crossword = [
    ["P", "E", "R", "U", ""],
    ["O", "M", "A", "N", ""],
    ["T", "U", "P", "", ""],
    ["", "", "", "", ""],
    ["", "", "", "", ""]
]
editable_grid = [[" " if cell != "" else "" for cell in row] for row in solution_crossword]

# Hints
hints_across = {1: "A country in South America", 5: "A country in the Middle East", 6: "Animal that goes 'mahhhhh'"}
hints_down = {1: "Smoking it makes people high", 2: "A bird that can't fly", 3: "Expected from the Blacks", 4: "One in Spanish"}

def check_solution():
    return all(
        solution_crossword[row][col] == editable_grid[row][col]
        for row in range(grid_size)
        for col in range(grid_size)
        if solution_crossword[row][col] != ""
    )

def is_filled():
    return all(
        editable_grid[row][col] != " "
        for row in range(grid_size)
        for col in range(grid_size)
        if solution_crossword[row][col] != ""
    )

# Setup Screen
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Crossword Game")
clock = pygame.time.Clock()

running = True
selected_cell = None
start_time = time.time()
game_won = False
incorrect_message = False
elapsed_time = 0

def draw_grid():
    screen.fill(WHITE)
    for row in range(grid_size):
        for col in range(grid_size):
            rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
            color = WHITE if (row, col) != selected_cell else BLUE
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, GRAY, rect, 1)
            
            if solution_crossword[row][col] == "":
                pygame.draw.rect(screen, BLACK, rect)
            else:
                font = pygame.font.Font(None, 36)
                text = font.render(editable_grid[row][col], True, BLACK)
                screen.blit(text, (col * cell_size + 15, row * cell_size + 10))
    
    # Timer
    font = pygame.font.Font(None, 36)
    time_text = f"Final Time: {elapsed_time:.1f}s" if game_won else f"Time: {elapsed_time:.1f}s"
    screen.blit(font.render(time_text, True, BLACK), (grid_size * cell_size + 10, 10))
    
    # Hints
    y_offset = 50
    font = pygame.font.Font(None, 20)
    for num, hint in hints_across.items():
        screen.blit(font.render(f"{num}A: {hint}", True, BLACK), (grid_size * cell_size + 10, y_offset))
        y_offset += 20
    for num, hint in hints_down.items():
        screen.blit(font.render(f"{num}D: {hint}", True, BLACK), (grid_size * cell_size + 10, y_offset))
        y_offset += 20
    
    if game_won:
        font = pygame.font.Font(None, 48)
        screen.blit(font.render("You Win!", True, GREEN), (width // 2 - 50, height // 2 - 25))
    elif incorrect_message:
        screen.blit(font.render("Not quite correct!", True, RED), (grid_size * cell_size + 10, y_offset + 10))
    
    pygame.display.flip()

# Game Loop

async def main():
    while running:
        if not game_won:
            elapsed_time = time.time() - start_time
        
        draw_grid()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_won:
                x, y = event.pos
                col, row = x // cell_size, y // cell_size
                if col < grid_size and solution_crossword[row][col] != "":
                    selected_cell = (row, col)
            elif event.type == pygame.KEYDOWN and selected_cell and not game_won:
                row, col = selected_cell
                if event.unicode.isalpha():
                    editable_grid[row][col] = event.unicode.upper()
                elif event.key == pygame.K_BACKSPACE:
                    editable_grid[row][col] = " "
                    incorrect_message = False
        
        if is_filled():
            if check_solution():
                game_won = True
                selected_cell = None  # Disable input
            else:
                incorrect_message = True
        
        clock.tick(30)
        await asyncio.sleep(0) 

asyncio.run(main())
