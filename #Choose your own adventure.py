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

def clear_all_sight_markers(grid):
    """Clear all sight markers (red dots) from the grid"""
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == Fore.RED + "." + Fore.RESET:
                grid[i][j] = " "
Grid = [
    [" ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " "],
    ["1", "1", " ", "1", "1", "1"], 
    [" ", " ", " ", " ", " ", " "],
    [" ", " ", " ", "1", " ", " "], 
    [" ", " ", " ", " ", " ", " "], 
    [" ", " ", " ", " ", " ", " "], 
    [" ", " ", " ", " ", " ", " "]
]
player_coord = [3, 0] 
zombie_coord = [0, 0] 
zombie_2_coord = [0, 5]

def zombie_sight(zombie_c, grid):
    print(f"Updating sight for zombie at {zombie_c}")  # Debugging statement
    
    # Check if player is directly at the same position as zombie (unlikely but a safeguard)
    if grid[zombie_c[0]][zombie_c[1]] == Fore.BLUE + "X" + Fore.RESET:
        print("You have been caught by the zombie! ") 
        exit()
        
    # Mark vertical line of sight (same column)
    # Look upward
    for i in range(zombie_c[0] - 1, -1, -1):  
        # Check for player before changing cell
        if grid[i][zombie_c[1]] == Fore.BLUE + "X" + Fore.RESET: 
            print("You have been caught by the zombie! ") 
            exit()
        elif grid[i][zombie_c[1]] == " " or grid[i][zombie_c[1]] == Fore.RED + "." + Fore.RESET:
            grid[i][zombie_c[1]] = Fore.RED + "." + Fore.RESET
        elif grid[i][zombie_c[1]] == Fore.RED + "Z" + Fore.RESET:  # Skip other zombies
            continue 
        else:
            break

    # Look downward
    for i in range(zombie_c[0] + 1, len(grid)):  
        # Check for player before changing cell
        if grid[i][zombie_c[1]] == Fore.BLUE + "X" + Fore.RESET: 
            print("You have been caught by the zombie! ") 
            exit()
        elif grid[i][zombie_c[1]] == " " or grid[i][zombie_c[1]] == Fore.RED + "." + Fore.RESET:
            grid[i][zombie_c[1]] = Fore.RED + "." + Fore.RESET
        elif grid[i][zombie_c[1]] == Fore.RED + "Z" + Fore.RESET:  # Skip other zombies
            continue 
        else:
            break

    # Mark horizontal line of sight (same row)
    # Look leftward
    for i in range(zombie_c[1] - 1, -1, -1):  
        # Check for player before changing cell
        if grid[zombie_c[0]][i] == Fore.BLUE + "X" + Fore.RESET: 
            print("You have been caught by the zombie! ") 
            exit()
        elif grid[zombie_c[0]][i] == " " or grid[zombie_c[0]][i] == Fore.RED + "." + Fore.RESET:
            grid[zombie_c[0]][i] = Fore.RED + "." + Fore.RESET
        elif grid[zombie_c[0]][i] == Fore.RED + "Z" + Fore.RESET:  # Skip other zombies
            continue 
        else:
            break

    # Look rightward
    for i in range(zombie_c[1] + 1, len(grid[0])):  
        # Check for player before changing cell
        if grid[zombie_c[0]][i] == Fore.BLUE + "X" + Fore.RESET: 
            print("You have been caught by the zombie! ") 
            exit()
        elif grid[zombie_c[0]][i] == " " or grid[zombie_c[0]][i] == Fore.RED + "." + Fore.RESET:
            grid[zombie_c[0]][i] = Fore.RED + "." + Fore.RESET
        elif grid[zombie_c[0]][i] == Fore.RED + "Z" + Fore.RESET:  # Skip other zombies
            continue 
        else:
            break

    print(f"Grid updated for zombie at {zombie_c}")

def movement():   

    movement = ""
    movement_options = ("w","a","s","d") 

    # Call function to check adjacent cells
    adjacent_cells = check_adj(Grid, player_coord)
    # Extract just the positions from adjacent_cells
    adjacent_positions = [pos for pos, val in adjacent_cells]


    while movement not in movement_options:
        movement = input("Which direction would you like to move? (w, a, s, d): ")   
        Grid[zombie_2_coord[0]][zombie_2_coord[1]] = " "
        Grid[zombie_coord[0]][zombie_coord[1]] = " "  
        if zombie_2_coord[0] == len(Grid)-1: 
            zombie_2_coord[0] = 0 
        else: 
            zombie_2_coord[0] += 1
        if zombie_coord[1] == len(Grid[0])-1:  
            zombie_coord[1] = 0
        else: 
            zombie_coord[1] += 1
    
        Grid[player_coord[0]][player_coord[1]] = " "  
        if movement == "w" and (player_coord[0]-1, player_coord[1]) in adjacent_positions and Grid[player_coord[0]-1][player_coord[1]] != "1":  
            player_coord[0] -= 1 
        elif movement == "s" and (player_coord[0]+1, player_coord[1]) in adjacent_positions and Grid[player_coord[0]+1][player_coord[1]] != "1":    
            player_coord[0] += 1 
        elif movement == "a" and (player_coord[0], player_coord[1]-1) in adjacent_positions and Grid[player_coord[0]][player_coord[1]-1] != "1":       
            player_coord[1] -= 1 
        elif movement == "d" and (player_coord[0], player_coord[1]+1) in adjacent_positions and Grid[player_coord[0]][player_coord[1]+1] != "1": 
            player_coord[1] += 1 
        else: 
            print("You cant go there! ") 
            continue  
        os.system("clear") 

while True:    

    Grid[player_coord[0]][player_coord[1]] = Fore.BLUE + "X" + Fore.RESET 
    Grid[zombie_coord[0]][zombie_coord[1]] = Fore.RED + "Z" + Fore.RESET 
    Grid[zombie_2_coord[0]][zombie_2_coord[1]] = Fore.RED + "Z" + Fore.RESET  

    print_grid(Grid) 

    clear_all_sight_markers(Grid)
    zombie_sight(zombie_2_coord,Grid) 
    zombie_sight(zombie_coord,Grid) 
    
    movement()