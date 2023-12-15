import random


def create_board(size):
    """Create a square game board of the given size."""
    return [['.' for _ in range(size)] for _ in range(size)]


def print_board(board, show_ships=False):
    """Print the game board with letters for columns and numbers for rows."""
    size = len(board)
    print("  " + " ".join(chr(ord('A') + i) for i in range(size)))
    for i, row in enumerate(board):
        print(f"{i} {' '.join(row if show_ships else '.' for row in row)}")
    print()


def is_valid_placement(board, ship_cells):
    """Check if the ship can be placed on the board without overlapping or going outside."""
    size = len(board)

    for cell in ship_cells:
        row, col = cell
        if not (0 <= row < size and 0 <= col < size and board[row][col] == '.'):
            return False

    return True


def place_ship_manually(board, ship_size):
    """Allow the player to manually place a ship on the board."""
    print_board(board, show_ships=True)

    try:
        coordinates = input(f"Enter the coordinates for the ship (e.g., 'A1 A2' or 'C3 D3 E3'): ").upper().split()
        ship_cells = []

        for coord in coordinates:
            if len(coord) >= 2:
                col, row_str = coord[:-1], coord[-1]
                row = int(row_str)
                col_num = ord(col) - ord('A')

                ship_cells.append((row, col_num))

        if len(ship_cells) != ship_size:
            print(f"Invalid number of coordinates. Please enter {ship_size} coordinates.")
            return place_ship_manually(board, ship_size)

        if not all(0 <= row < len(board) and 0 <= col < len(board) for row, col in ship_cells):
            print("Invalid coordinates. Ensure that all coordinates are within the board.")
            return place_ship_manually(board, ship_size)

        if not is_valid_placement(board, ship_cells):
            print("Invalid placement. Ensure that the ship does not overlap with other ships.")
            return place_ship_manually(board, ship_size)

        # Place the ship on the board
        for row, col in ship_cells:
            board[row][col] = 'B'

        return ship_cells
    except ValueError:
        print("Invalid input. Please enter valid coordinates.")
        return place_ship_manually(board, ship_size)


def get_player_ship_manually(size):
    """Allow the player to place a ship on the board manually."""
    print_board(create_board(size), show_ships=True)
    try:
        ship_size = int(input("Enter the size of the ship: "))
        if 1 <= ship_size <= size:
            ship_cells = place_ship_manually(create_board(size), ship_size)
            return ship_cells
        else:
            print(f"Invalid ship size. Please enter a size between 1 and {size}.")
            return get_player_ship_manually(size)
    except ValueError:
        print("Invalid input. Please enter a valid ship size.")
        return get_player_ship_manually(size)


def get_player_guess(size):
    """Get the player's guess for row and column within the board size."""
    try:
        coordinates = input(f"Enter the coordinates (e.g., 'A1' or 'B2'): ").upper()
        if len(coordinates) == 2:
            col, row_str = coordinates[0], coordinates[1]
            row = int(row_str)
            col_num = ord(col) - ord('A')

            if 0 <= row < size and 0 <= col_num < size:
                return (row, col_num)
            else:
                print(f"Invalid input. Row must be between 0 and {size - 1}, and column must be between A and {chr(ord('A') + size - 1)}.")
                return get_player_guess(size)
        else:
            print("Invalid input. Please enter valid coordinates.")
            return get_player_guess(size)
    except ValueError:
        print("Invalid input. Please enter valid coordinates.")
        return get_player_guess(size)


def update_board_on_hit(board, cell, ships):
    """Update the game board when a ship is hit."""
    row, col = cell

    for ship_cells in ships:
        if cell in ship_cells:
            ship_cells.remove(cell)  # Mark the hit cell on the ship

            if not ship_cells:  # The entire ship has been sunk
                for r, c in ship_cells:
                    board[r][c] = 'S'
            else:
                board[row][col] = 'H'  # Mark the hit cell on the board

            return True

    return False


def update_board_on_miss(board, cell):
    """Update the game board when a shot is a miss."""
    row, col = cell
    board[row][col] = 'M'


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
    player_ships = []
    computer_ships = []
    for _ in range(num_ships):
        player_ship = get_player_ship_manually(size)
        computer_ship = place_ship_manually(computer_board, len(player_ship))
        player_ships.append(player_ship)
        computer_ships.append(computer_ship)

    # Number of turns allowed
    turns = size * num_ships  # Adjust the number of turns based on the board size and number of ships

    while turns > 0:
        print_board(player_board, show_ships=True)
        print("Computer's Board:")
        print_board(computer_board)

        # Player's turn to guess
        player_guess = get_player_guess(size)
        player_row, player_col = player_guess

        # Check if the player's guess hits a ship
        player_hit = update_board_on_hit(computer_board, player_guess, computer_ships)

        if player_hit:
            print("Hit! You sunk part of the computer's fleet!")
        else:
            update_board_on_miss(computer_board, player_guess)
            print("Missed! Your turn is over.")

        turns -= 1
        print(f"You have {turns} turns left.")

        # Check for victory
        if all(not ship for ship in computer_ships):
            print("Congratulations! You've sunk all of the computer's fleet.")
            break

        # Computer's turn to guess
        computer_guess = (random.randint(0, size - 1), random.randint(0, size - 1))
        computer_row, computer_col = computer_guess

        # Check if the computer's guess hits a ship
        computer_hit = update_board_on_hit(player_board, computer_guess, player_ships)

        if computer_hit:
            print("Oh no! The computer hit part of your fleet!")
        else:
            update_board_on_miss(player_board, computer_guess)
            print("Computer missed! It's your turn again.")

        turns -= 1
        print(f"You have {turns} turns left.")

        # Check for victory
        if all(not ship for ship in player_ships):
            print("Oh no! The computer has sunk all of your fleet.")
            break

    print("Game over.")
    print("Your Board:")
    print_board(player_board, show_ships=True)
    print("Player's fleet:")
    print(player_ships)
    print("Computer's Board:")
    print_board(computer_board)
    print("Computer's fleet:")
    print(computer_ships)


if __name__ == "__main__":
    play_battleship()
