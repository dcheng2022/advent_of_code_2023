def get_num_and_y_loc(char_row, j):
    ptr_go_left = j
    ptr_go_right = j

    while ptr_go_left > 0 and char_row[ptr_go_left - 1].isdigit(): 
        ptr_go_left -= 1

    while ptr_go_right < len(char_row) - 1 and char_row[ptr_go_right + 1].isdigit():
        ptr_go_right += 1

    return (int(char_row[ptr_go_left:ptr_go_right + 1]), ptr_go_left)


def get_adjacent_nums(schematic_rows, sym_loc):
    num_locs = set()
    nums = []
    sym_i, sym_j = sym_loc
    
    checks = {
            'left': (0, -1),
            'right': (0, 1),
            'up': (-1, 0),
            'down': (1, 0),
            'upleft': (-1, -1),
            'upright': (-1, 1),
            'downleft': (1, -1),
            'downright': (1, 1)
            }
    
    for x_delta, y_delta in checks.values():
        changed_i = sym_i + x_delta
        changed_j = sym_j + y_delta

        if changed_i < 0 or changed_i > len(schematic_rows) - 1: continue
        if changed_j < 0 or changed_j > len(schematic_rows[0]) - 1: continue

        element = schematic_rows[changed_i][changed_j]
        
        if not element.isdigit(): continue
 
        num, num_loc_y = get_num_and_y_loc(schematic_rows[changed_i], changed_j)
        num_loc = (changed_i, num_loc_y)

        if num_loc in num_locs: continue

        num_locs.add(num_loc)
        nums.append(num)

    return nums
        

def get_symbol_locs(schematic_rows):
    symbol_locs = []

    for (i, char_row) in enumerate(schematic_rows):
        for (j, char) in enumerate(char_row):
            if char.isdigit() or char == '.': continue
            
            symbol_locs.append((i, j))
    
    return symbol_locs


def get_potential_gear_locs(schematic_rows):
    potential_gear_locs = []

    for (i, char_row) in enumerate(schematic_rows):
        for (j, char) in enumerate(char_row):
            if char != '*': continue

            potential_gear_locs.append((i, j))
    
    return potential_gear_locs


def get_part_nums(schematic_rows):
    symbol_locs = get_symbol_locs(schematic_rows)
    part_nums = []

    for sym_loc in symbol_locs:
        part_nums.extend(get_adjacent_nums(schematic_rows, sym_loc))

    return part_nums


def sum_part_nums(schematic):
    schematic_rows = [s.strip() for s in schematic.split('\n')]

    return sum(get_part_nums(schematic_rows))


def get_gear_ratio(gear_adj_nums):
    return gear_adj_nums[0] * gear_adj_nums[1]


def get_gear_ratios(schematic_rows):
    potential_gear_locs = get_potential_gear_locs(schematic_rows)
    potential_gears_adj_nums = [get_adjacent_nums(schematic_rows, gear_loc) for gear_loc in potential_gear_locs]
    gears_adj_nums = [adj_nums for adj_nums in potential_gears_adj_nums if len(adj_nums) == 2]
    
    return [get_gear_ratio(gear_adj_nums) for gear_adj_nums in gears_adj_nums]


def sum_gear_ratios(schematic):
    schematic_rows = [s.strip() for s in schematic.split('\n')]
    
    return sum(get_gear_ratios(schematic_rows))
    
if __name__ == '__main__':
    test1 = """467..114..
    ...*......
    ..35..633.
    ......#...
    617*......
    .....+.58.
    ..592.....
    ......755.
    ...$.*....
    .664.598.."""

    assert(sum_part_nums(test1) == 4361)
    assert(sum_gear_ratios(test1) == 467835)

