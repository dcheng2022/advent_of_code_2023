from inputs.day5 import test2
from multiprocessing import Pool
import time

def parse_map_range(range_str):
    range_nums = [int(num_str) for num_str in range_str.split()]

    return range_nums


def parse_maps(maps):
    map_names_and_ranges = {}
    maps = maps[1:]

    for map_str in maps:
        map_str = map_str.split(':')
        map_name = map_str[0].split()[0]
        map_ranges_str = map_str[1].split('\n')[1:]
        map_ranges = [parse_map_range(range_str) for range_str in map_ranges_str]
        map_names_and_ranges[map_name] = map_ranges

    return map_names_and_ranges


""" def get_actual_seeds(maps):
    seeds_str = maps[0].split()[1:]
    seeds = set()

    for i in range(0, len(seeds_str) - 1, 2):
        range_start = int(seeds_str[i])
        range_len = int(seeds_str[i + 1])

        for i in range(range_len):
            seeds.add(range_start + i)

    return seeds """


def get_seed_ranges(maps):
    seeds_str = maps[0].split()[1:]
    seed_ranges = []

    for i in range(0, len(seeds_str) - 1, 2):
        range_start = int(seeds_str[i])
        range_len = int(seeds_str[i + 1])
        range_end = range_start + range_len - 1

        seed_ranges.append((range_start, range_end))

    return seed_ranges


def get_seeds(maps):
    seeds_str = maps[0].split()[1:]

    return [int(seed_str) for seed_str in seeds_str]


def get_mapped_num(num, ranges):
    for map_range in ranges:
        dst_range_start, src_range_start, range_len = map_range
        src_range_end = src_range_start + range_len

        if num >= src_range_start and num < src_range_end:
            offset = num - src_range_start

            return dst_range_start + offset

#        for i in range(range_len):
#            if num == src_range_start + i: return dst_range_start + i

    return num


def get_reverse_mapped_num(num, ranges):
    for map_range in ranges:
        src_range_start, dst_range_start, range_len = map_range
        src_range_end = src_range_start + range_len

        if num >= src_range_start and num < src_range_end:
            offset = num - src_range_start

            return dst_range_start + offset

    return num


def get_potential_seed_num(map_names_and_ranges, location):
    reverse_mapped_num = location

    for (map_name, map_ranges) in list(map_names_and_ranges.items())[::-1]:
        reverse_mapped_num = get_reverse_mapped_num(reverse_mapped_num, map_ranges)

    return reverse_mapped_num


def is_seed(seed_ranges, num):
    for seed_range in seed_ranges:
        range_start, range_end = seed_range

        if num >= range_start and num <= range_end: return True

    return False


def get_location(map_names_and_ranges, seed):
    mapped_num = seed

    for (map_name, map_ranges) in map_names_and_ranges.items():
        mapped_num = get_mapped_num(mapped_num, map_ranges)

    return mapped_num


def get_lowest_location(maps):
    maps = maps.split('\n\n')
    seeds = get_seeds(maps)
    map_names_and_ranges = parse_maps(maps)
    seed_locations = [get_location(map_names_and_ranges, seed) for seed in seeds]

    return min(seed_locations)


def get_actual_lowest_location_bu(maps):
    maps = maps.split('\n\n')
    seed_ranges = get_seed_ranges(maps)
    map_names_and_ranges = parse_maps(maps)
    lowest_location = 0

    while True:
        potential_seed_num = get_potential_seed_num(map_names_and_ranges, lowest_location)

        if is_seed(seed_ranges, potential_seed_num): break

        lowest_location += 1

    return lowest_location


def get_actual_lowest_location_bu_par(maps, start, increment):
    maps = maps.split('\n\n')
    seed_ranges = get_seed_ranges(maps)
    map_names_and_ranges = parse_maps(maps)
    lowest_location = start

    while True:
        potential_seed_num = get_potential_seed_num(map_names_and_ranges, lowest_location)

        if is_seed(seed_ranges, potential_seed_num): break

        lowest_location += increment

    return lowest_location


def get_actual_lowest_location_td_par(maps, seed_range):
    map_names_and_ranges = parse_maps(maps)
    lowest_location = get_location(map_names_and_ranges, seed_range[0])

    for seed in seed_range[1:]:
        lowest_location = min(lowest_location, get_location(map_names_and_ranges, seed))

    return lowest_location


def get_largest_range(ranges):
    largest_range = ranges[0]
    largest_diff = ranges[0][1] - ranges[0][0]

    for range in ranges[1:]:
        range_start, range_end = range
        range_diff = range_end - range_start

        if range_diff > largest_diff:
            largest_diff = range_diff
            largest_range = range

    return largest_range


def expand_to_n_ranges(ranges, n):
    while len(ranges) < n:
        range = get_largest_range(ranges)
        range_start, range_end = range
        range_mid = (range_start + range_end) // 2

        ranges.remove(range)
        ranges.append((range_start, range_mid))
        ranges.append((range_mid + 1, range_end))

    return ranges


if __name__ == '__main__':
    test1 = """seeds: 79 14 55 13

    seed-to-soil map:
    50 98 2
    52 50 48

    soil-to-fertilizer map:
    0 15 37
    37 52 2
    39 0 15

    fertilizer-to-water map:
    49 53 8
    0 11 42
    42 0 7
    57 7 4

    water-to-light map:
    88 18 7
    18 25 70

    light-to-temperature map:
    45 77 23
    81 45 19
    68 64 13

    temperature-to-humidity map:
    0 69 1
    1 0 69

    humidity-to-location map:
    60 56 37
    56 93 4"""

    start = time.time()
    assert(get_lowest_location(test1) == 35)
    end = time.time()

    print(f'lowest_loc took {end-start} seconds')

    start = time.time()
    assert(get_actual_lowest_location_bu(test1) == 46)
    end = time.time()

    print(f'act_lowest_loc took {end-start} seconds')

    start = time.time()
    print(get_lowest_location(test2))
    end = time.time()

    print(f'lowest_loc took {end-start} seconds')

    def run_test_with_n_processes_bottom_up(test, n):
        results = []
        pool = Pool(processes=n)

        start = time.time()

        for i in range(n):
            pool.apply_async(get_actual_lowest_location_bu_par, args=(test, i, n), callback=(lambda x: results.append(x)))

        pool.close()
        pool.join()

        end = time.time()

        print(min(results))
        print(f'act_lowest_loc_bu with {n} processes took {end-start} seconds')

        return 0


    def run_test_with_n_min_processes_top_down(test, min_n):
        results = []
        maps = test.split('\n\n')
        seed_ranges = get_seed_ranges(maps)
        seed_ranges = expand_to_n_ranges(seed_ranges, min_n) if len(seed_ranges) < min_n else seed_ranges
        seed_ranges = [range(seed_range[0], seed_range[1] + 1) for seed_range in seed_ranges]

        pool = Pool(processes=max(min_n, len(seed_ranges)))

        start = time.time()

        for i in range(len(seed_ranges)):
            pool.apply_async(get_actual_lowest_location_td_par, args=(maps, seed_ranges[i]), callback=(lambda x: results.append(x)))

        pool.close()
        pool.join()

        end = time.time()

        print(min(results))
        print(f'act_lowest_loc_td with {len(seed_ranges)} processes took {end-start} seconds')

        return 0


    run_test_with_n_processes_bottom_up(test1, 1)
    run_test_with_n_processes_bottom_up(test2, 20)

    # run_test_with_n_min_processes_top_down(test1, 2)
    # run_test_with_n_min_processes_top_down(test2, 20)
