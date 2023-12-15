import random

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

def place_ship(board, ship_size):
    while True:
        try:
            print_board(board)
            print(f"Place a ship of size {ship_size}")
            coords = input("Enter the coordinates (e.g., A1 A2 A3 A4 A5): ").split()
            ship_coordinates = [convert_coordinates(coord) for coord in coords]

            for x, y in ship_coordinates:
                if board[x][y] != '.':
                    raise ValueError("Invalid placement. Ships cannot overlap.")
            
            for x, y in ship_coordinates:
                board[x][y] = 'O'

            break
        except (ValueError, IndexError):
            print("Invalid input. Try again.")

def random_place_ship(board, ship_size):
    while True:
        x = random.randint(0, 9)
        y = random.randint(0, 9)
        orientation = random.choice(['h', 'v'])

        try:
            if orientation == 'h':
                for i in range(ship_size):
                    if board[x][y + i] != '.':
                        raise ValueError
                for i in range(ship_size):
                    board[x][y + i] = 'O'
            elif orientation == 'v':
                for i in range(ship_size):
                    if board[x + i][y] != '.':
                        raise ValueError
                for i in range(ship_size):
                    board[x + i][y] = 'O'

            break
        except ValueError:
            continue

def player_turn(board):
    while True:
        try:
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
            print("Congratulations! You won!")
            break

        computer_turn(player_board)
        if is_winner(player_board):
            print("Sorry, you lost. Better luck next time!")
            break

if __name__ == "__main__":
    battleship_game()
