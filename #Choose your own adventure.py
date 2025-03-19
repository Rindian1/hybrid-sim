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
                grid[i][j] = " "  # Reset to empty space

# Initialize grid with walls and empty spaces
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

# Add the exit point ('E') at the opposite corner of the grid
exit_coord = [7, 5]
Grid[exit_coord[0]][exit_coord[1]] = Fore.GREEN + "E" + Fore.RESET

player_coord = [3, 0]
zombie_coord = [0, 0]
zombie_2_coord = [0, 5]

def zombie_sight(zombie_c, grid):
    global player_coord
    print(f"Updating sight for zombie at {zombie_c}")  # Debugging statement

    # Check if player is directly at the same position as zombie
    if player_coord[0] == zombie_c[0] and player_coord[1] == zombie_c[1]:
        print("You have been caught by the zombie!")
        exit()
    
    # Mark vertical line of sight (same column)
    # Look upward
    for i in range(zombie_c[0] - 1, -1, -1):
        if i == player_coord[0] and zombie_c[1] == player_coord[1]:
            print("Zombie spotted you vertically!")
            exit()
        elif grid[i][zombie_c[1]] == " " or grid[i][zombie_c[1]] == Fore.RED + "." + Fore.RESET:
            grid[i][zombie_c[1]] = Fore.RED + "." + Fore.RESET
        else:
            break

    # Look downward
    for i in range(zombie_c[0] + 1, len(grid)):
        if i == player_coord[0] and zombie_c[1] == player_coord[1]:
            print("Zombie spotted you vertically!")
            exit()
        elif grid[i][zombie_c[1]] == " " or grid[i][zombie_c[1]] == Fore.RED + "." + Fore.RESET:
            grid[i][zombie_c[1]] = Fore.RED + "." + Fore.RESET
        else:
            break

    # Mark horizontal line of sight (same row)
    # Look leftward
    for i in range(zombie_c[1] - 1, -1, -1):
        if zombie_c[0] == player_coord[0] and i == player_coord[1]:
            print("Zombie spotted you horizontally!")
            exit()
        elif grid[zombie_c[0]][i] == " " or grid[zombie_c[0]][i] == Fore.RED + "." + Fore.RESET:
            grid[zombie_c[0]][i] = Fore.RED + "." + Fore.RESET
        else:
            break

    # Look rightward
    for i in range(zombie_c[1] + 1, len(grid[0])):
        if zombie_c[0] == player_coord[0] and i == player_coord[1]:
            print("Zombie spotted you horizontally!")
            exit()
        elif grid[zombie_c[0]][i] == " " or grid[zombie_c[0]][i] == Fore.RED + "." + Fore.RESET:
            grid[zombie_c[0]][i] = Fore.RED + "." + Fore.RESET
        else:
            break

    print(f"Grid updated for zombie at {zombie_c}")

def movement():
    global player_coord, zombie_coord, zombie_2_coord, exit_coord
    movement_options = ("w", "a", "s", "d")

    # Call function to check adjacent cells
    adjacent_cells = check_adj(Grid, tuple(player_coord))
    # Extract just the positions from adjacent_cells
    adjacent_positions = [pos for pos, val in adjacent_cells]

    movement = input("Which direction would you like to move? (w, a, s, d): ")
    
    if movement in movement_options:
        # Store the original grid values before clearing
        zombie1_val = Grid[zombie_coord[0]][zombie_coord[1]]
        zombie2_val = Grid[zombie_2_coord[0]][zombie_2_coord[1]]
        player_val = Grid[player_coord[0]][player_coord[1]]
        
        # First clear zombie from the grid
        if zombie1_val == Fore.RED + "Z" + Fore.RESET:
            Grid[zombie_coord[0]][zombie_coord[1]] = " "
        if zombie2_val == Fore.RED + "Z" + Fore.RESET:
            Grid[zombie_2_coord[0]][zombie_2_coord[1]] = " "
        
        # Clear player from the grid
        if player_val == Fore.BLUE + "X" + Fore.RESET:
            Grid[player_coord[0]][player_coord[1]] = " "
        
        # Move player if valid
        original_player_pos = player_coord.copy()
        moved = False
        
        if movement == "w" and (player_coord[0] - 1, player_coord[1]) in adjacent_positions and Grid[player_coord[0] - 1][player_coord[1]] != "1":
            player_coord[0] -= 1
            moved = True
        elif movement == "s" and (player_coord[0] + 1, player_coord[1]) in adjacent_positions and Grid[player_coord[0] + 1][player_coord[1]] != "1":
            player_coord[0] += 1
            moved = True
        elif movement == "a" and (player_coord[0], player_coord[1] - 1) in adjacent_positions and Grid[player_coord[0]][player_coord[1] - 1] != "1":
            player_coord[1] -= 1
            moved = True
        elif movement == "d" and (player_coord[0], player_coord[1] + 1) in adjacent_positions and Grid[player_coord[0]][player_coord[1] + 1] != "1":
            player_coord[1] += 1
            moved = True
        else:
            print("You can't go there!")
            player_coord = original_player_pos
            return False
        
        # Check if player reached the exit
        if player_coord[0] == exit_coord[0] and player_coord[1] == exit_coord[1]:
            os.system("clear")
            print_grid(Grid)
            print(Fore.GREEN + "Congratulations! You've reached the exit and escaped the zombies!" + Fore.RESET)
            exit()
        
        # Only move zombies if the player moved
        if moved:
            if zombie_2_coord[0] == len(Grid) - 1:
                zombie_2_coord[0] = 0
            else:
                zombie_2_coord[0] += 1
                
            if zombie_coord[1] == len(Grid[0]) - 1:
                zombie_coord[1] = 0
            else:
                zombie_coord[1] += 1
        
        os.system("clear")
        return True
    return False
def instruction():
    # Print instructions at the start
    print(Fore.CYAN + "Welcome to Zombie Escape!" + Fore.RESET)
    print(Fore.CYAN + "You are the blue 'X'. Avoid the red 'Z' zombies and reach the green 'E' exit." + Fore.RESET)
    print(Fore.CYAN + "Zombies can see in straight lines - avoid their sight (red dots)!" + Fore.RESET)
    print(Fore.CYAN + "Use W, A, S, D to move." + Fore.RESET)
    print(Fore.CYAN + "Press Enter to start..." + Fore.RESET)
    input()
    os.system("clear")


instruction()
while True:
    # Clear all sight markers before updating
    clear_all_sight_markers(Grid)
    
    # Make sure exit stays on the grid (in case it was overwritten)
    Grid[exit_coord[0]][exit_coord[1]] = Fore.GREEN + "E" + Fore.RESET
    
    # Place entities on the grid
    Grid[player_coord[0]][player_coord[1]] = Fore.BLUE + "X" + Fore.RESET
    Grid[zombie_coord[0]][zombie_coord[1]] = Fore.RED + "Z" + Fore.RESET
    Grid[zombie_2_coord[0]][zombie_2_coord[1]] = Fore.RED + "Z" + Fore.RESET
    
    # Update zombie sight AFTER placing zombies but BEFORE printing
    zombie_sight(zombie_coord, Grid)
    zombie_sight(zombie_2_coord, Grid)
    
    # Print the grid
    print_grid(Grid)
    
    # Handle movement
    if not movement():
        print("Please enter a valid movement command.")