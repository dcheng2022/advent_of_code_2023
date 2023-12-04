def get_id(game):
    id_and_colon = game.split()[1]
    id = id_and_colon.split(':')[0]

    return int(id)


def get_rounds(game):
    parsed_rounds = []
    rounds_str = game.split(':')[1]
    rounds_str_split = [r.strip() for r in rounds_str.split(';')]
    
    for round in rounds_str_split:
        round_dict = {}
        num_color_pairs = [c.strip() for c in round.split(',')]
        
        for nc_pair in num_color_pairs:
            num_str, color = nc_pair.split()
            number = int(num_str)
            round_dict[color] = number

        parsed_rounds.append(round_dict)

    return parsed_rounds


def is_valid_round(round, cubes):
    COLORS = set(['red', 'blue', 'green'])

    for color in COLORS:
        if color in round and round[color] > cubes[color]: return False

    return True


def is_valid_game(game, cubes):
    rounds = get_rounds(game)

    for round in rounds:
        if not is_valid_round(round, cubes): return False

    return True


def sum_possible_ids(games, cubes):
    games = games.split('\n')

    return sum([get_id(game) for game in games if is_valid_game(game, cubes)])

    
def get_min_cube_counts(game):
    COLORS = set(['red', 'blue', 'green'])
    rounds = get_rounds(game)
    min_cube_counts = {c:0 for c in COLORS}

    for round in rounds:
        for color in COLORS:
            if not color in round:
                continue
            elif min_cube_counts[color] == None:
                min_cube_counts[color] = round[color]
            else:
                min_cube_counts[color] = max(min_cube_counts[color], round[color])

    return min_cube_counts


def get_power(game):
    power = 1

    for c in get_min_cube_counts(game).values():     
        power *= c

    return power


def sum_min_cubes_powers(games):
    games = games.split('\n')

    return sum([get_power(game) for game in games])


if __name__ == '__main__':
    games1 = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
    Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
    Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
    Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""
    cubes1 = {'red': 12, 'green': 13, 'blue': 14}

    assert(sum_possible_ids(games1, cubes1) == 8)
    assert(sum_min_cubes_powers(games1) == 2286) 

