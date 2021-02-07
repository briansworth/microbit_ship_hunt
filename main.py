def generate_ship():
    vertical = randint(0, 1)
    if vertical == 1:
        ship = _generate_vertical_ship()
    else:
        ship = _generate_horizontal_ship()
    return ship

def _generate_horizontal_ship():
    LEFT_EDGE = 0
    x = randint(0, 4)
    y = randint(0, 4)
    if x == LEFT_EDGE:
        x_new = x + 1
    else:
        x_new = x - 1
    return [[x, y], [x_new, y]]

def _generate_vertical_ship():
    TOP_EDGE = 0
    y = randint(0, 4)
    x = randint(0, 4)
    if y == TOP_EDGE:
        y_new = y + 1
    else:
        y_new = y - 1
    return [[x, y], [x, y_new]]

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

def make_guess(cursor: tuple(int, int), ship: List[tuple(int, int)]):
    is_hit = 0
    if is_coordinate_in_ship(cursor, ship):
        hit()
        is_hit = 1
    return [cursor[0], cursor[1], is_hit]

def is_coordinate_in_ship(coordinate: tuple(int, int), ship: List[tuple(int, int)]):
    for ship_coord in ship:
        if coordinate[0] == ship_coord[0] and coordinate[1] == ship_coord[1]:
            return True
    return False

def hit():
    game.add_score(1)
    basic.clear_screen()

def show_guesses(guess_list: List[List[number]]):
    HIT_INDEX = 2
    for guess in guess_list:
        if guess[HIT_INDEX] == 1:
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
    HIT_INDEX = 2
    hit_count = 0
    for guess in guesses:
        if guess[HIT_INDEX] == 1:
            hit_count += 1
    if hit_count >= win_threshold:
        return True
    elif guesses.length >= max_guesses:
        return True
    return False


# Reduce number to increase difficulty
# Increase number to reduce difficulty
GUESS_COUNT = 15

CURSOR = (0, 0)
SHIP = generate_ship()
WIN_THRESHOLD = SHIP.length
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
    guess = make_guess(CURSOR, SHIP)
    GUESSES.append(guess)
input.on_button_pressed(Button.AB, on_button_pressed_ab)

while not game.is_game_over():
    show_coordinate_led(CURSOR)
    pause(500)
    hide_coordinate_led(CURSOR)
    show_guesses(GUESSES)
    pause(500)

    game_over = is_gameover(GUESSES, GUESS_COUNT, WIN_THRESHOLD)
    if game_over:
        score = GUESS_COUNT - GUESSES.length
        game.set_score(score)
        game.game_over()

