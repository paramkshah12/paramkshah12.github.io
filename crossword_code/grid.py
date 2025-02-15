import pygame
import time

# Constants
grid_size = 5 # or 15
cell_size = 50
width, height = grid_size * cell_size + 300, grid_size * cell_size  # Extra space for hints

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Hardcoded solution crossword
solution_crossword = None
if grid_size == 5:
    solution_crossword = [
        ["P", "E", "R", "U", ""],
        ["O", "M", "A", "N", ""],
        ["T", "U", "P", "", ""],
        ["", "", "", "", ""],
        ["", "", "", "", ""]
    ]
elif grid_size == 15:
    solution_crossword = [
        ["P", "E", "R", "U", "", "", "", "", "", "", "", "", "", "", ""],
        ["O", "M", "A", "N", "", "", "", "", "", "", "", "", "", "", ""],
        ["T", "U", "P", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
    ]

editable_grid = [[" " if cell != "" else "" for cell in row] for row in solution_crossword]

def generate_numbers():
    numbering = [[None for _ in range(grid_size)] for _ in range(grid_size)]
    num = 1
    hints_across = {}
    hints_down = {}
    
    for row in range(grid_size):
        for col in range(grid_size):
            if solution_crossword[row][col] != "" and (
                row == 0 or col == 0 or solution_crossword[row-1][col] == "" or solution_crossword[row][col-1] == ""
            ):
                numbering[row][col] = num
                num += 1

    hints_across[1] = "A country in South America"
    hints_across[5] = "A country in the Middle East"
    hints_across[6] = "Animal that goes 'mahhhhh'"

    hints_down[1] = "Smoking it makes people high"
    hints_down[2] = "A bird that can't fly"
    hints_down[3] = "Expected from the Blacks"
    hints_down[4] = "One in Spanish"
    
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

def main():
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
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_won:
                x, y = event.pos
                col, row = x // cell_size, y // cell_size
                if col < grid_size and solution_crossword[row][col] != '':
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
            else:
                incorrect_message = True  
        
        clock.tick(30)
    
    pygame.quit()

if __name__ == "__main__":
    main()
