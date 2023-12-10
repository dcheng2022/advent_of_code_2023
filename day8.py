from inputs.day8 import test2
from time import sleep
from multiprocessing import Pool, Manager

def parse(inst_and_network):
    inst_and_network = inst_and_network.split('\n')

    instructions = inst_and_network[0]
    network_strs = inst_and_network[2:]
    network_strs = [network_str.split() for network_str in network_strs]
    network_dict = {network[0]: (network[2][1:4], network[3][:3]) for network in network_strs}

    return (instructions, network_dict)


def get_names_ending_a(names):
    return [n for n in names if n.endswith('A')]


def is_all_z(names):
    for name in names:
        if not name.endswith('Z'): return False
    
    return True


def get_simul_steps_to_zzz(instructions, network):
    steps_taken = 0
    instructions = [0 if char == 'L' else 1 for char in instructions]
    location_names = get_names_ending_a(list(network.keys()))

    while not is_all_z(location_names):
        for inst in instructions:
            location_names = [network[loc_n][inst] for loc_n in location_names]
            steps_taken += 1

    return steps_taken


def get_simul_steps_to_zzz_par(instructions, network, location_name, steps_list, idx):
    steps_taken = 0
    instructions = [0 if char == 'L' else 1 for char in instructions]

    while True:
        for inst in instructions:
            location_name = network[location_name][inst]
            steps_taken += 1

            if location_name.endswith('Z'): steps_list[idx].append(steps_taken)


def get_steps_to_zzz(instructions, network):
    steps_taken = 0
    instructions = [0 if char == 'L' else 1 for char in instructions]
    location_name = 'AAA'

    while True:
        for inst in instructions:
            location_name = network[location_name][inst]
            steps_taken += 1

            if location_name == 'ZZZ': return steps_taken


def get_total_steps(inst_and_network):
    instructions, network = parse(inst_and_network)

    return get_steps_to_zzz(instructions, network)


def get_simul_total_steps(inst_and_network):
    instructions, network = parse(inst_and_network)

    return get_simul_steps_to_zzz(instructions, network)


def remove_fewer_steps(steps_list):
    max_num = max(steps_list, key=lambda x: x[0])[0]

    for (idx, lst) in enumerate(steps_list):
        if lst[0] == max_num:
            continue
        else:
            lst.pop(0)

    return 0


def watch_steps_list(pool, steps_list):
    steps_taken = None

    # Wait for lists to populate
    sleep(1)

    while True:
        print([len(l) for l in steps_list])
        steps_taken = steps_list[0][0]
        not_done = False

        for lst in steps_list[1:]:
            if lst[0] == steps_taken: continue

            remove_fewer_steps(steps_list)

            not_done = True

            break

        if not_done: continue

        print(f'steps: {steps_taken}')

        pool.terminate()
        break

    pool.join()

    return steps_taken 
      

def run_test_simul_par(test):
    instructions, network = parse(test)
    location_names = get_names_ending_a(list(network.keys()))
    num_locations = len(location_names)
    pool = Pool(processes=num_locations)
    manager = Manager()
    steps_list = manager.list([manager.list() for i in range(num_locations)])

    print(f'starting with {num_locations} processes...')
    print(f'steps_list initialized with {len(steps_list)} lists...')

    for i in range(num_locations):
        location_name = location_names[i]

        pool.apply_async(get_simul_steps_to_zzz_par, args=(instructions, network, location_name, steps_list, i))

    simul_total_steps = watch_steps_list(pool, steps_list)

    return simul_total_steps


if __name__ == '__main__':
    test1 = """LLR

    AAA = (BBB, BBB)
    BBB = (AAA, ZZZ)
    ZZZ = (ZZZ, ZZZ)"""

    assert(get_total_steps(test1) == 6)
    assert(get_simul_total_steps(test1) == 6)
    assert(run_test_simul_par(test1) == 6)

    test3 = """LR

    11A = (11B, XXX)
    11B = (XXX, 11Z)
    11Z = (11B, XXX)
    22A = (22B, XXX)
    22B = (22C, 22C)
    22C = (22Z, 22Z)
    22Z = (22B, 22B)
    XXX = (XXX, XXX)"""

    assert(get_simul_total_steps(test3) == 6)
    assert(run_test_simul_par(test3) == 6)
    
    print(run_test_simul_par(test2))
    

