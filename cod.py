import random

def create_grid():
    """Создаёт игровое поле 10x10, заполненное символом '.'"""
    return [['.' for _ in range(10)] for _ in range(10)]

def print_grid(grid):
    """Выводит игровое поле с обозначениями строк и столбцов."""
    print("  A B C D E F G H I J")
    for i, row in enumerate(grid):
        print(f"{i+1:<2}{' '.join(row)}")

def is_valid_placement(grid, row, col, length, direction):
    """Проверяет, можно ли разместить корабль в указанной позиции."""
    for i in range(length):
        r = row + (i if direction == 'v' else 0)
        c = col + (i if direction == 'h' else 0)
        if r >= 10 or c >= 10 or grid[r][c] != '.':
            return False
    return True

def place_ship(grid, length):
    """Размещает корабль заданной длины на игровом поле случайным образом."""
    placed = False
    while not placed:
        row, col = random.randint(0, 9), random.randint(0, 9)
        direction = random.choice(['h', 'v'])
        if is_valid_placement(grid, row, col, length, direction):
            for i in range(length):
                r = row + (i if direction == 'v' else 0)
                c = col + (i if direction == 'h' else 0)
                grid[r][c] = 'O'
            placed = True

def setup_ships(grid):
    """Размещает все корабли на игровом поле."""
    ships = {4: 1, 3: 2, 2: 3, 1: 4}  # Длины кораблей и их количество
    for length, count in ships.items():
        for _ in range(count):
            place_ship(grid, length)

def get_user_input():
    """Получает и проверяет пользовательский ввод для выстрела."""
    while True:
        shot = input("Введите выстрел (например, A1, J10): ").strip().upper()
        if len(shot) < 2 or len(shot) > 3:
            print("Неверный ввод. Попробуйте снова.")
            continue
        col, row = shot[0], shot[1:]
        if col not in 'ABCDEFGHIJ' or not row.isdigit() or not (1 <= int(row) <= 10):
            print("Неверный ввод. Попробуйте снова.")
            continue
        return int(row) - 1, ord(col) - ord('A')

def process_shot(grid, target_grid, row, col):
    """Обрабатывает выстрел пользователя и обновляет игровое поле."""
    if target_grid[row][col] == 'O':
        print("Попадание!")
        grid[row][col] = 'X'
        target_grid[row][col] = 'X'
        return True
    elif target_grid[row][col] == '.':
        print("Мимо.")
        grid[row][col] = '-'
        target_grid[row][col] = '-'
    else:
        print("Вы уже стреляли сюда.")
    return False

def check_victory(target_grid):
    """Проверяет, уничтожены ли все корабли."""
    for row in target_grid:
        if 'O' in row:
            return False
    return True

def save_game(target_grid, filename="battleship_save.txt"):
    """Сохраняет текущее состояние игры в файл."""
    with open(filename, 'w') as file:
        for row in target_grid:
            file.write(''.join(row) + '\n')
    print("Игра сохранена.")

def load_game(filename="battleship_save.txt"):
    """Загружает состояние игры из файла."""
    try:
        with open(filename, 'r') as file:
            return [list(line.strip()) for line in file.readlines()]
    except FileNotFoundError:
        print("Сохранённая игра не найдена.")
        return None

def main():
    """Главная функция для запуска игры."""
    player_grid = create_grid()
    target_grid = create_grid()
    setup_ships(target_grid)

    while True:
        print("\nВаше поле:")
        print_grid(player_grid)

        row, col = get_user_input()
        process_shot(player_grid, target_grid, row, col)

        if check_victory(target_grid):
            print("Поздравляем! Вы уничтожили все корабли.")
            break

        action = input("Хотите сохранить игру? (y/n): ").strip().lower()
        if action == 'y':
            save_game(target_grid)

if __name__ == "__main__":
    main()
