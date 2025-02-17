import pygame
import time
import asyncio

# Constants
grid_size = 7
cell_size = 50
width, height = grid_size * cell_size + 400, grid_size * cell_size + 150  # Extra space for hints and keyboard

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Hardcoded solution crossword
solution_crossword = [
    ["J", "E", "R", "O", "M", "E", ""],
    ["H", "Y", "M", "N", "", "P", "M"],
    ["A", "", "S", "E", "", "I", "U"],
    ["N", "O", "E", "M", "I", "C", "S"],
    ["S", "M", "", "A", "I", "", "L"],
    ["I", "A", "", "N", "I", "T", "I"],
    ["", "R", "H", "Y", "T", "H", "M"]
]

editable_grid = [[" " if cell != "" else "" for cell in row] for row in solution_crossword]

# Virtual keyboard layout
keyboard_keys = [
    ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
    ['K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T'],
    ['U', 'V', 'W', 'X', 'Y', 'Z', 'del']
]

# Smaller button size
key_width = 25  # Reduced from 30
key_height = 25  # Reduced from 30
key_gap = 5

def generate_numbers():
    numbering = [[None for _ in range(grid_size)] for _ in range(grid_size)]
    num = 1
    hints_across = {}
    hints_down = {}

    for row in range(grid_size):
        for col in range(grid_size):
            if solution_crossword[row][col] != "" and (
                (row == 0 or solution_crossword[row-1][col] == "") and (row != grid_size - 1 and solution_crossword[row+1][col] != "") or
                (col == 0 or solution_crossword[row][col-1] == "") and (col != grid_size - 1 and solution_crossword[row][col+1] != "")
            ):
                numbering[row][col] = num
                num += 1

    hints_across[1] = "He has the most expensive 'Good Afternoon'"
    hints_across[6] = "What Coldplay occupy themselves with on the weekend"
    hints_across[7] = "Air quality measure"
    hints_across[9] = "Dhano isn't autistic, per __, just a little special"
    hints_across[10] = "A metric for pharma stuff"
    hints_across[11] = "Intellectual Science (no chance you're getting this)"
    hints_across[14] = "A common message after fumbling: Uk ily __"
    hints_across[15] = "Current talk of the town"
    hints_across[16] = "A suffix of several countries"
    hints_across[17] = "Policy"
    hints_across[19] = "I don't need no vowels"

    hints_down[1] = "Home to perhaps the bravest woman"
    hints_down[2] = "One of the Big 4"
    hints_down[3] = "Or the standard deviation, kind of"
    hints_down[4] = "An antonym pair, and a type of relation"
    hints_down[5] = "Ramayan and Mahabharat, for two"
    hints_down[8] = "He must get a circumcision"
    hints_down[12] = "Kashmir's chief minister"
    hints_down[13] = "Technical institute that focuses on IT"
    hints_down[18] = "A suffix for non-podium finishers"

    return numbering, hints_across, hints_down

numbering, hints_across, hints_down = generate_numbers()

def check_solution():
    for row in range(grid_size):
        for col in range(grid_size):
            if solution_crossword[row][col] != "" and editable_grid[row][col] != solution_crossword[row][col]:
                return False
    return True

def is_filled():
    for row in range(grid_size):
        for col in range(grid_size):
            if solution_crossword[row][col] != "" and editable_grid[row][col] == " ":
                return False
    return True

def draw_grid(screen, grid, selected_cell, elapsed_time, game_won, incorrect_message):
    for row in range(grid_size):
        for col in range(grid_size):
            rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)

            if solution_crossword[row][col] == '':
                pygame.draw.rect(screen, BLACK, rect)
            else:
                color = WHITE if (row, col) != selected_cell else BLUE
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, GRAY, rect, 1)

                if numbering[row][col] is not None:
                    font = pygame.font.Font(None, 16)
                    text = font.render(str(numbering[row][col]), True, BLACK)
                    screen.blit(text, (col * cell_size + 3, row * cell_size + 3))

                if grid[row][col] != ' ':
                    font = pygame.font.Font(None, 36)
                    text = font.render(grid[row][col], True, BLACK)
                    screen.blit(text, (col * cell_size + 15, row * cell_size + 10))

    font = pygame.font.Font(None, 36)
    time_text = f"Time: {elapsed_time:.1f}s"
    text = font.render(time_text, True, BLACK)
    screen.blit(text, (grid_size * cell_size + 10, 10))

    if game_won:
        message = "You Win!"
        font = pygame.font.Font(None, 48)
        text = font.render(message, True, GREEN)

        # Box settings
        box_width, box_height = 200, 80
        box_x = (grid_size * cell_size - box_width) // 2
        box_y = (grid_size * cell_size - box_height) // 2

        pygame.draw.rect(screen, WHITE, (box_x, box_y, box_width, box_height))  # Box background
        pygame.draw.rect(screen, GREEN, (box_x, box_y, box_width, box_height), 5)  # Border

        text_x = box_x + (box_width - text.get_width()) // 2
        text_y = box_y + (box_height - text.get_height()) // 2

        screen.blit(text, (text_x, text_y))

    # Display Hints
    font = pygame.font.Font(None, 20)
    y_offset = 50
    for num, hint in hints_across.items():
        text = font.render(f"{num}A: {hint}", True, BLACK)
        screen.blit(text, (grid_size * cell_size + 10, y_offset))
        y_offset += 20

    y_offset += 10
    for num, hint in hints_down.items():
        text = font.render(f"{num}D: {hint}", True, BLACK)
        screen.blit(text, (grid_size * cell_size + 10, y_offset))
        y_offset += 20

    if incorrect_message:
        font = pygame.font.Font(None, 20)
        text = font.render("Not quite correct!", True, RED)
        screen.blit(text, (grid_size * cell_size + 10, y_offset + 10))

def draw_keyboard(screen):
    keyboard_y = grid_size * cell_size + 20
    for i, row in enumerate(keyboard_keys):
        keyboard_x = 10
        for j, key in enumerate(row):
            rect = pygame.Rect(keyboard_x, keyboard_y, key_width, key_height)
            pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, GRAY, rect, 1)
            font = pygame.font.Font(None, 20)
            text = font.render(key, True, BLACK)
            screen.blit(text, (keyboard_x + 5, keyboard_y + 5))
            keyboard_x += key_width + key_gap
        keyboard_y += key_height + key_gap

def draw_start_screen(screen):
    screen.fill(BLACK)
    font = pygame.font.Font(None, 48)
    text = font.render("Ready to start?", True, WHITE)
    text_rect = text.get_rect(center=(width // 2, height // 2 - 50))
    screen.blit(text, text_rect)

    button_rect = pygame.Rect(width // 2 - 75, height // 2, 150, 50)
    pygame.draw.rect(screen, GREEN, button_rect)
    font = pygame.font.Font(None, 36)
    text = font.render("HELL YES", True, BLACK)
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)

    return button_rect

async def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Crossword Game")

    selected_cell = None
    clock = pygame.time.Clock()
    running = True
    start_time = time.time()
    game_won = False
    incorrect_message = False
    elapsed_time = 0
    game_started = False

    while running:
        screen.fill(WHITE)
        if not game_started:
            button_rect = draw_start_screen(screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if button_rect.collidepoint(x, y):
                        game_started = True
                        start_time = time.time()
        else:
            if not game_won:
                elapsed_time = time.time() - start_time
            draw_grid(screen, editable_grid, selected_cell, elapsed_time, game_won, incorrect_message)
            draw_keyboard(screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and not game_won:
                    x, y = event.pos
                    if y < grid_size * cell_size:
                        col, row = x // cell_size, y // cell_size
                        if col < grid_size and solution_crossword[row][col] != '':
                            selected_cell = (row, col)
                    else:
                        # Handle keyboard clicks
                        keyboard_y = grid_size * cell_size + 20
                        for i, row_keys in enumerate(keyboard_keys):
                            keyboard_x = 10
                            for j, key in enumerate(row_keys):
                                rect = pygame.Rect(keyboard_x, keyboard_y, key_width, key_height)
                                if rect.collidepoint(x, y):
                                    if selected_cell:
                                        row, col = selected_cell
                                        if key == 'del':
                                            editable_grid[row][col] = " "
                                        else:
                                            editable_grid[row][col] = key
                                        incorrect_message = False
                                keyboard_x += key_width + key_gap
                            keyboard_y += key_height + key_gap
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
                else:
                    incorrect_message = True

        clock.tick(30)
        await asyncio.sleep(0)

    # pygame.quit()

asyncio.run(main())