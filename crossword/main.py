import pygame
import time
import asyncio

# Constants
grid_size = 6  # or 15
cell_size = 50
width, height = grid_size * cell_size + 300, grid_size * cell_size + 120  # Extra space for hints and keyboard

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Hardcoded solution crossword
solution_crossword = [
    ['A', 'R', 'R', 'E', 'S', 'T'],
    ['B', 'I', 'N', 'D', 'I', ''],
    ['B', 'A', 'N', 'D', 'R', 'A'],
    ['R', '', '', 'Y', 'E', 'S'],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', '']
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

    hints_across[1] = "What criminals are afraid of"
    hints_across[6] = "Forehead-wear"
    hints_across[7] = "Where people from Khar say they're from"
    hints_across[9] = "A bank that faced crises in 2020"

    hints_down[1] = "It is of itself"
    hints_down[2] = "An Indian name with several spellings"
    hints_down[3] = "Recurring Neural Network"
    hints_down[4] = "Circle your arm in a water tub to form this"
    hints_down[5] = "Respectful addressal"
    hints_down[8] = "Used for comparing"

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

    while running:
        screen.fill(WHITE)
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