import os 
from colorama import Fore  
import time

def check_adj(grid, coord):
    # Extract row and column from the coordinate tuple
    row, col = coord
    # Get the dimensions of the grid
    rows, cols = len(grid), len(grid[0])
    # Initialize an empty list to store adjacent cells and their values
    adjacents = []
    # Define all possible adjacent positions (including diagonals)
    # Each tuple represents (row_change, column_change) from current position
    directions = [
        (-1, -1), (-1, 0), (-1, 1),  # Top left, top, top right
        (0, -1),           (0, 1),   # Left, right
        (1, -1),  (1, 0),  (1, 1)    # Bottom left, bottom, bottom right
    ]
    # Loop through each direction
    for row_offset, col_offset in directions:
        # Calculate the new row and column by adding the direction changes
        new_row = row + row_offset
        new_col = col + col_offset
        # Check if the new position is within grid boundaries
        # This prevents index errors when checking cells at edges
        if 0 <= new_row < rows and 0 <= new_col < cols:
            # Get the value at this adjacent cell
            value = grid[new_row][new_col]
            # Add the position and its value to our results list
            adjacents.append(((new_row, new_col), value))
            # If we found a "1", print a detection message
            if value == "1":
                print(f"Detected '1' at position ({new_row}, {new_col})")
    # Return the list of adjacent positions and their values
    return adjacents


# Create a 5x5 grid with all "0"s
def print_grid(grid):
    print("+" + "---+" * len(grid[0]))
    for row in grid:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        print("+" + "---+" * len(grid[0]))


Grid = [
    [" ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " "],
    ["1", "1", " ", "1", " ", "1"], 
    [" ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " "], 
    [" ", " ", " ", " ", " ", " "], 
    [" ", " ", " ", " ", " ", " "], 
    [" ", " ", " ", " ", " ", " "]
]
player_coord = [3, 0] 
zombie_coord = [0, 0]

def zombie_sight(zombie_c, grid):
    # First, clear any previous sight markers
    for i in range(len(grid)): 
        for j in range(len(grid[0])):
            if grid[i][j] == Fore.RED + "." + Fore.RESET:
                grid[i][j] = " "

    # Mark vertical line of sight (same column)
    for i in range(zombie_c[0]-1, -1, -1):  # Look upward
        if grid[i][zombie_c[1]] == " ": 
            grid[i][zombie_c[1]] = Fore.RED + "." + Fore.RESET
        elif grid[i][zombie_c[1]] == "Z": 
            continue
        else:  
            break
            
    for i in range(zombie_c[0]+1, len(grid)):  # Look downward
        if grid[i][zombie_c[1]] == " ": 
            grid[i][zombie_c[1]] = Fore.RED + "." + Fore.RESET
        elif grid[i][zombie_c[1]] == "Z": 
            continue
        else:  
            break
    
    # Mark horizontal line of sight (same row)
    for i in range(zombie_c[1]-1, -1, -1):  # Look leftward
        if grid[zombie_c[0]][i] == " ": 
            grid[zombie_c[0]][i] = Fore.RED + "." + Fore.RESET
        elif grid[zombie_c[0]][i] == "Z": 
            continue
        else:  
            break
            
    for i in range(zombie_c[1]+1, len(grid[0])):  # Look rightward
        if grid[zombie_c[0]][i] == " ": 
            grid[zombie_c[0]][i] = Fore.RED + "." + Fore.RESET
        elif grid[zombie_c[0]][i] == "Z": 
            continue
        else:  
            break

def movement(): 
    original_value = Grid[player_coord[0]][player_coord[1]]
    Grid[player_coord[0]][player_coord[1]] = Fore.BLUE + "X" + Fore.RESET 
    Grid[zombie_coord[0]][zombie_coord[1]] = Fore.RED + "Z" + Fore.RESET
    
    print_grid(Grid)

    # Call function to check adjacent cells
    adjacent_cells = check_adj(Grid, player_coord)
    
    # Extract just the positions from adjacent_cells
    adjacent_positions = [pos for pos, val in adjacent_cells]

    movement = ""
    movement_options = ("w","a","s","d")
    while movement not in movement_options:
        movement = input("Which direction would you like to move? (w, a, s, d): ")   
        
        Grid[zombie_coord[0]][zombie_coord[1]] = " "
        zombie_coord[1] += 1
    
        Grid[player_coord[0]][player_coord[1]] = " "  
        if movement == "w" and (player_coord[0]-1, player_coord[1]) in adjacent_positions and Grid[player_coord[0]-1][player_coord[1]] == " ":  
            player_coord[0] -= 1 
        elif movement == "s" and (player_coord[0]+1, player_coord[1]) in adjacent_positions and Grid[player_coord[0]+1][player_coord[1]] == " ":    
            player_coord[0] += 1 
        elif movement == "a" and (player_coord[0], player_coord[1]-1) in adjacent_positions and Grid[player_coord[0]][player_coord[1]-1] == " ":       
            player_coord[1] -= 1 
        elif movement == "d" and (player_coord[0], player_coord[1]+1) in adjacent_positions and Grid[player_coord[0]][player_coord[1]+1] == " ": 
            player_coord[1] += 1 
        else: 
            print("You cant go there! ") 
            continue  
        os.system("clear") 
    #if player_coord[1] == zombie_coord[1]: 
        #print("You have been caught by the zombie! ") 
        #exit()
while True:  
    zombie_sight(zombie_coord,Grid)
    movement()