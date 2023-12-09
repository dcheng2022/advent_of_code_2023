from inputs.day6 import test2
from functools import reduce
from math import floor, ceil

def parse(races_and_records):
    races_str, records_str = races_and_records.split('\n')
    races = [int(time) for time in races_str.split()[1:]]
    records = [int(dist) for dist in records_str.split()[1:]]

    return [(races[i], records[i])for i in range(len(races))]


def parse_as_one(race_and_record):
    race_str, record_str = race_and_record.split('\n')
    race_time = int(''.join(race_str.split()[1:]))
    record_dist = int(''.join(record_str.split()[1:]))

    return (race_time, record_dist)


def get_button_times(race_time, record_dist):
    discriminant = race_time ** 2 - 4 * record_dist
    
    root1 = (race_time - discriminant ** 0.5) / 2
    root2 = (race_time + discriminant ** 0.5) / 2

    return [root1, root2]


def get_ways_to_win(race_and_record):
    """
        button_time = x
        0 <= x <+ race_time
        distance = (race_time - button_time) * buttom_time
        distance = (race_time * x - x^2)
        distance' = race_time - 2 * x
        
        solve for x of record_distance
        -x^2 + race_time * x - record_distance = 0
        x = -race_time +/- sqrt(race_time ** 2 - 4 * record_distance) / -2

        e.g. record_distance = 9, race_time = 7
        x = -7 +/- sqrt(49 - 36) / -2
        x = -7 +/- sqrt(13) / -2
        x = 7 +/- sqrt(13) / 2
        sqrt(13) ~ 3.5 (in practice we will use actual value)

        number of integers in range (1.75, 5.25) is the answer
        so in this case (2, 3, 4, 5) => 4
    """

    race_time, record_dist = race_and_record
    lower_btn_time, higher_btn_time = get_button_times(race_time, record_dist)
    
    return ceil(higher_btn_time) - floor(lower_btn_time) - 1
   
        
def product_of_ways_to_win(races_and_records):
    races_and_records = parse(races_and_records)
    ways_to_win_races = [get_ways_to_win(race_and_record) for race_and_record in races_and_records]

    return reduce(lambda x, y: x * y, ways_to_win_races)


def get_ways_to_win_as_one(race_and_record):
    race_and_record = parse_as_one(race_and_record)
    ways_to_win_race = get_ways_to_win(race_and_record)

    return ways_to_win_race


if __name__ == '__main__':
    test1 = """Time:      7  15   30
    Distance:  9  40  200"""

    assert(product_of_ways_to_win(test1) == 288)
    assert(get_ways_to_win_as_one(test1) == 71503)

    print(get_ways_to_win_as_one(test2))
