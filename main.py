def generate_ships(count: int):
    ship_list = [generate_ship()]
    for i in range(count - 1):
        ship_list.append(add_ship(ship_list))
    return ship_list

def add_ship(ships: List[List[tuple(int, int)]]):
    while True:
        new_ship = generate_ship()
        if is_ship_overlapping(new_ship, ships) is False:
            break
    return new_ship

def generate_ship():
    vertical = randint(0, 1)
    if vertical == 1:
        ship = _generate_vertical_ship()
    else:
        ship = _generate_horizontal_ship()
    return ship

def is_ship_overlapping(ship: List[tuple(int, int)], ships: List[List[tuple(int, int)]]):
    for coord in ship:
        for other_ship in ships:
            if is_coordinate_in_ship(coord, other_ship) is True:
                return True
    return False

def is_coordinate_in_ship(coordinate: tuple(int, int), ship: List[tuple(int, int)]):
    for ship_coord in ship:
        if coordinate[0] == ship_coord[0] and coordinate[1] == ship_coord[1]:
            return True
    return False

def _generate_vertical_ship():
    TOP_EDGE = 0
    y = randint(0, 4)
    x = randint(0, 4)
    if y == TOP_EDGE:
        y_new = y + 1
    else:
        y_new = y - 1
    return [(x, y), (x, y_new)]

def _generate_horizontal_ship():
    RIGHT_EDGE = 4
    x = randint(0, 4)
    y = randint(0, 4)
    if x == RIGHT_EDGE:
        x_new = x - 1
    else:
        x_new = x + 1
    return [(x, y), (x_new, y)]

def move_coordinates_right(coordinates: tuple(int, int)):
    x = coordinates[0]
    y = coordinates[1]
    new_x = x + 1
    if x >= 4:
        new_x = 0
    return (new_x, y)

def move_coordinates_down(coordinates: tuple(int, int)):
    x = coordinates[0]
    y = coordinates[1]
    new_y = y + 1
    if y >= 4:
        new_y = 0
    return (x, new_y)

def update_coordinate_led(cursor: tuple(int, int), coordinates: tuple(int, int)):
    hide_coordinate_led(cursor)
    show_coordinate_led(coordinates)

def show_ship(ship: List[tuple(int, int)]):
    for coordinate in ship:
        show_coordinate_led(coordinate)

def hide_ship(ship: List[List[number]]):
    for coordinate2 in ship:
        hide_coordinate_led(coordinate2)

def hide_coordinate_led(coordinate: List[number]):
    led.unplot(coordinate[0], coordinate[1])

def show_coordinate_led(coordinate: List[number]):
    led.plot(coordinate[0], coordinate[1])

def make_guess(cursor: tuple(int, int), ships: List[List[tuple(int, int)]]):
    for ship in ships:
        guess = _make_guess(cursor, ship)
        if is_guess_a_hit(guess) is True:
            return guess
    return guess

def _make_guess(cursor: tuple(int, int), ship: List[tuple(int, int)]):
    is_hit = 0
    if is_coordinate_in_ship(cursor, ship):
        hit()
        is_hit = 1
    return [cursor[0], cursor[1], is_hit]

def is_guess_a_hit(guess: List[number]):
    HIT_INDEX = 2
    if guess[HIT_INDEX] == 1:
        return True
    return False

def hit():
    game.add_score(1)
    basic.clear_screen()

def show_guesses(guess_list: List[List[number]]):
    for guess in guess_list:
        if is_guess_a_hit(guess) is True:
            _show_hit(guess)
        else:
            _show_guess(guess)

def _show_hit(guess):
    show_coordinate_led((guess[0], guess[1]))

def _show_guess(guess: List[number]):
    coordinate = (guess[0], guess[1])
    show_coordinate_led(coordinate)
    led.plot_brightness(guess[0], guess[1], 100)

def is_gameover(guesses: List[List[number]], max_guesses: int, win_threshold: int):
    hit_count = _get_guess_hit_count(guesses)
    if hit_count >= win_threshold:
        return True
    elif guesses.length >= max_guesses:
        return True
    return False

def _get_guess_hit_count(guesses: List[List[number]]):
    hits = _get_guess_hits(guesses)
    return hits.length

def _get_guess_hits(guesses: List[List[number]]):
    hits: List[List[number]] = []
    for guess in guesses:
        if is_guess_a_hit(guess) is True:
            hits.append(guess)
    return hits

def display_game_board(cursor: tuple(int, int), guesses: List[List[number]]):
    show_coordinate_led(cursor)
    show_guesses(guesses)
    pause(500)
    hide_coordinate_led(cursor)
    show_guesses(guesses)
    pause(500)

# Reduce number to increase difficulty
# Increase number to reduce difficulty
GUESS_COUNT = 15

SHIP_COUNT = 2
CURSOR = (0, 0)
SHIPS = generate_ships(SHIP_COUNT)
WIN_THRESHOLD = SHIP_COUNT * 2
GUESSES: List[List[number]] = []

def on_button_pressed_a():
    new_coords = move_coordinates_down(CURSOR)
    update_coordinate_led(CURSOR, new_coords)
    CURSOR[1] = new_coords[1]
input.on_button_pressed(Button.A, on_button_pressed_a)

def on_button_pressed_b():
    new_coords = move_coordinates_right(CURSOR)
    update_coordinate_led(CURSOR, new_coords)
    CURSOR[0] = new_coords[0]
input.on_button_pressed(Button.B, on_button_pressed_b)

def on_button_pressed_ab():
    guess = make_guess(CURSOR, SHIPS)
    GUESSES.append(guess)
input.on_button_pressed(Button.AB, on_button_pressed_ab)

while not game.is_game_over():
    display_game_board(CURSOR, GUESSES)
    game_over = is_gameover(GUESSES, GUESS_COUNT, WIN_THRESHOLD)
    if game_over:
        score = GUESS_COUNT - GUESSES.length
        game.set_score(score)
        game.game_over()

