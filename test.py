import random

class Ship:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.coordinates = []

class Board:
    def __init__(self, rows=10, cols=10, default_value=0):
        self.rows = rows
        self.cols = cols
        self.grid = [[default_value for _ in range(cols)] for _ in range(rows)]

    def print_grid(self):
        for row_index in range(self.rows):
            for col_index in range(self.cols):
                value = self.grid[row_index][col_index]
                print(f"grid[{row_index}][{col_index}] = {value}")
    
    def can_place(self, row, col, size, direction):
        if direction == 'H':
            if col + size > self.cols:
                return False
            return all(self.grid[row][c] == '.' for c in range(col, col + size))
        else:  # 'V'
            if row + size > self.rows:
                return False
            return all(self.grid[r][col] == '.' for r in range(row, row + size))
        
    def place_ship(self, ship):
        while True:
            direction = random.choice(['H', 'V'])
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)

            if self.can_place(row, col, ship.size, direction):
                coords = []
                if direction == 'H':
                    for c in range(col, col + ship.size):
                        self.grid[row][c] = ship.name[0]
                        coords.append((row, c))
                else:
                    for r in range(row, row + ship.size):
                        self.grid[r][col] = ship.name[0]
                        coords.append((r, col))
                ship.coordinates = coords
                break


class Player:
    def __init__(self, name):
        self.name = name
        self.board = Board()
        self.ships = []
        self._init_ships()

    def _init_ships(self):
        ship_definitions = [
            ("Battleship", 1), ("Battleship", 1),
            ("Destroyer", 2), ("Destroyer", 2),
            ("Carrier", 3),
            ("Submarine", 4),
            ("Cruiser", 5)
        ]
        for name, size in ship_definitions:
            ship = Ship(name, size)
            self.board.place_ship(ship)
            self.ships.append(ship)

# Example usage
player = Player("Player1")
print(f"{player.name}'s Board:")
player.board.print_grid()