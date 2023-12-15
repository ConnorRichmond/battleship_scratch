import random

def create_board(size):
    """Create a square game board of the given size."""
    return [['.' for _ in range(size)] for _ in range(size)]

def print_board(board, show_ships=False):
    """Print the game board with letters for columns and numbers for rows."""
    size = len(board)
    print("  " + " ".join(chr(ord('A') + i) for i in range(size)))
    for i, row in enumerate(board):
        print(f"{i + 1} {' '.join(row if show_ships else '.' for row in row)}")
    print()

def is_valid_placement(board, ship_cells):
    """Check if the ship can be placed on the board without overlapping or going outside."""
    size = len(board)

    for cell in ship_cells:
        row, col = cell
        if not (0 <= row < size and 0 <= col < size and board[row][col] == '.'):
            return False

    return True

def place_ship_randomly(board, ship_size):
    """Randomly place a ship on the board."""
    size = len(board)
    orientation = random.choice(["horizontal", "vertical"])

    if orientation == "horizontal":
        row = random.randint(0, size - 1)
        col = random.randint(0, size - ship_size)
        ship_cells = [(row, col + i) for i in range(ship_size)]
    else:  # vertical
        row = random.randint(0, size - ship_size)
        col = random.randint(0, size - 1)
        ship_cells = [(row + i, col) for i in range(ship_size)]

    return ship_cells

def get_player_ship_manually(size):
    """Allow the player to place a ship on the board manually."""
    print_board(create_board(size), show_ships=True)
    try:
        ship_size = int(input("Enter the size of the ship: "))
        if 1 <= ship_size <= size:
            ship_cells = []

            while len(ship_cells) < ship_size:
                coordinates = input(f"Enter the coordinates (e.g., 'A1 A2' or 'B3 C3 D3') for the ship cells: ").upper()
                coordinates_list = coordinates.split()

                if all(len(coord) == 2 and coord[0].isalpha() and coord[1].isdigit() for coord in coordinates_list):
                    for coord in coordinates_list:
                        col, row_str = coord[0], coord[1]
                        row = int(row_str) - 1  # Adjust row to start from 0
                        col_num = ord(col) - ord('A')
                        if 0 <= row < size and 0 <= col_num < size:
                            cell = (row, col_num)
                            if cell not in ship_cells:
                                ship_cells.append(cell)
                            else:
                                print(f"Invalid input. Cell {coord} already chosen.")
                        else:
                            print(f"Invalid input. Row must be between 1 and {size}, and column must be between A and {chr(ord('A') + size - 1)}.")
                else:
                    print("Invalid input. Please enter valid coordinates.")

            return ship_cells
        else:
            print(f"Invalid ship size. Please enter a size between 1 and {size}.")
            return get_player_ship_manually(size)
    except ValueError:
        print("Invalid input. Please enter a valid ship size.")
        return get_player_ship_manually(size)

def update_board_on_hit(board, guess, ships):
    """Update the board when there is a hit."""
    row, col = guess
    board[row][col] = 'H'  # Mark the cell as a hit

    for ship_cells in ships:
        if guess in ship_cells:
            ship_cells.remove(guess)
            if not ship_cells:  # If the ship is sunk
                for sunk_cell in ship_cells:  # Iterate over the sunk ship cells
                    row, col = sunk_cell
                    board[row][col] = 'S'  # Mark the cell as a part of a sunk ship
                return True  # It's a hit
    return False  # It's a miss

def update_board_on_miss(board, guess):
    """Update the board when there is a miss."""
    row, col = guess
    board[row][col] = 'M'  # Mark the cell as a miss

def get_player_guess(size):
    """Get the player's guess for row and column within the board size."""
    try:
        coordinates = input(f"Enter the coordinates (e.g., 'A1' or 'B2'): ").upper()
        if len(coordinates) == 2 and coordinates[0].isalpha() and coordinates[1].isdigit():
            col, row_str = coordinates[0], coordinates[1]
            row = int(row_str) - 1  # Adjust row to start from 0
            col_num = ord(col) - ord('A')

            if 0 <= row < size and 0 <= col_num < size:
                return (row, col_num)
            else:
                print(f"Invalid input. Row must be between 1 and {size}, and column must be between A and {chr(ord('A') + size - 1)}.")
                return get_player_guess(size)
        else:
            print("Invalid input. Please enter valid coordinates.")
            return get_player_guess(size)
    except ValueError:
        print("Invalid input. Please enter a valid row number.")
        return get_player_guess(size)

def player_turn(board, computer_ships):
    """Execute the player's turn."""
    guess = get_player_guess(len(board))

    if update_board_on_hit(board, guess, computer_ships):
        print(f"You hit the computer's fleet at {chr(ord('A') + guess[1])}{guess[0] + 1}!")
    else:
        print(f"You missed at {chr(ord('A') + guess[1])}{guess[0] + 1}.")

def computer_turn(player_ships, board):
    """Simulate the computer's turn."""
    guess = random.choice([(row, col) for row in range(len(board)) for col in range(len(board[0]))])

    if update_board_on_hit(board, guess, player_ships):
        print(f"The computer hit your fleet at {chr(ord('A') + guess[1])}{guess[0] + 1}!")
    else:
        print(f"The computer missed at {chr(ord('A') + guess[1])}{guess[0] + 1}.")

def play_battleship():
    print("Welcome to Battleship!")

    # Get the size of the game board from the user
    size = int(input("Enter the size of the game board (between 4 and 10): "))
    if not 4 <= size <= 10:
        print("Invalid size. Please enter a size between 4 and 10.")
        return

    # Get the number of ships from the user
    num_ships = int(input("Enter the number of ships to place (1 or more): "))
    if num_ships < 1:
        print("Invalid number of ships. Please enter 1 or more.")
        return

    # Create the game board for the player and the computer
    player_board = create_board(size)
    computer_board = create_board(size)

    # Place ships for the player and the computer
    player_ships = [get_player_ship_manually(size) for _ in range(num_ships)]
    computer_ships = [place_ship_randomly(computer_board, random.randint(1, size)) for _ in range(num_ships)]

    while any(ships for ships in player_ships) and any(ships for ships in computer_ships):
        print("\nPlayer's turn:")
        player_turn(player_board, computer_ships)
        print_board(player_board, show_ships=True)

        if not any(ships for ships in computer_ships):
            print("Congratulations! You've sunk all of the computer's fleet.")
            break

        print("\nComputer's turn:")
        computer_turn(player_ships, computer_board)
        print_board(computer_board)

        if not any(ships for ships in player_ships):
            print("Oh no! The computer has sunk all of your fleet.")
            break

if __name__ == "__main__":
    play_battleship()