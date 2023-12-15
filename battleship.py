import os
import random

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_board(board):
    print("   1 2 3 4 5 6 7 8 9 10")
    print("  ---------------------")
    for i, row in enumerate(board):
        print(f"{chr(65 + i)} | {' '.join(row)}")

def convert_coordinates(coord):
    # Convert user input like 'A1' to row and column indices
    row = ord(coord[0].upper()) - 65
    col = int(coord[1:]) - 1
    return row, col

def validate_ship_placement(board, ship_coordinates):
    for x, y in ship_coordinates:
        if board[x][y] != '.':
            return False

    x_values, y_values = zip(*ship_coordinates)
    if len(set(x_values)) == 1 or len(set(y_values)) == 1:
        return True
    return False

def place_ship(board, ship_size):
    while True:
        try:
            clear_screen()
            print_board(board)
            print(f"Place a ship of size {ship_size}")
            start_coord = input("Enter the starting coordinates (e.g., A1): ")
            end_coord = input("Enter the ending coordinates (e.g., A5): ")

            start_x, start_y = convert_coordinates(start_coord)
            end_x, end_y = convert_coordinates(end_coord)

            ship_coordinates = []
            if start_x == end_x:
                # Place horizontally
                ship_coordinates = [(start_x, start_y + i) for i in range(ship_size)]
            elif start_y == end_y:
                # Place vertically
                ship_coordinates = [(start_x + i, start_y) for i in range(ship_size)]
            else:
                raise ValueError("Invalid placement. Ships cannot be placed diagonally.")

            if validate_ship_placement(board, ship_coordinates):
                for x, y in ship_coordinates:
                    board[x][y] = 'O'
                break
            else:
                raise ValueError("Invalid placement. Ships cannot overlap or be diagonal.")
        except (ValueError, IndexError):
            print("Invalid input. Try again.")

def random_place_ship(board, ship_size):
    while True:
        x = random.randint(0, 9)
        y = random.randint(0, 9)
        orientation = random.choice(['h', 'v'])

        try:
            if orientation == 'h' and y + ship_size <= 10:
                for i in range(ship_size):
                    if board[x][y + i] != '.':
                        raise ValueError
                for i in range(ship_size):
                    board[x][y + i] = 'O'
            elif orientation == 'v' and x + ship_size <= 10:
                for i in range(ship_size):
                    if board[x + i][y] != '.':
                        raise ValueError
                for i in range(ship_size):
                    board[x + i][y] = 'O'
            else:
                raise ValueError
            break
        except ValueError:
            continue

def player_turn(board):
    while True:
        try:
            clear_screen()
            print_board(board)
            coord = input("Enter the coordinates to attack (e.g., A1): ")
            x, y = convert_coordinates(coord)

            if board[x][y] == '.':
                print("Miss!")
                board[x][y] = 'X'
            elif board[x][y] == 'O':
                print("Hit!")
                board[x][y] = '*'
            else:
                print("Invalid move. Try again.")
                continue

            break
        except (ValueError, IndexError):
            print("Invalid input. Try again.")

def computer_turn(board):
    while True:
        x = random.randint(0, 9)
        y = random.randint(0, 9)

        if board[x][y] == '.':
            print(f"Computer missed at {chr(65 + x)}{y + 1}!")
            board[x][y] = 'X'
        elif board[x][y] == 'O':
            print(f"Computer hit at {chr(65 + x)}{y + 1}!")
            board[x][y] = '*'
        else:
            continue

        break

def is_winner(board):
    return all(all(cell != 'O' for cell in row) for row in board)

def battleship_game():
    player_board = [['.' for _ in range(10)] for _ in range(10)]
    computer_board = [['.' for _ in range(10)] for _ in range(10)]

    player_ships = [5, 4, 3, 3, 2]
    computer_ships = [5, 4, 3, 3, 2]

    for ship in player_ships:
        place_ship(player_board, ship)

    for ship in computer_ships:
        random_place_ship(computer_board, ship)

    while True:
        player_turn(computer_board)
        if is_winner(computer_board):
            clear_screen()
            print("Congratulations! You won!")
            break

        computer_turn(player_board)
        if is_winner(player_board):
            clear_screen()
            print("Sorry, you lost. Better luck next time!")
            break

if __name__ == "__main__":
    battleship_game()
