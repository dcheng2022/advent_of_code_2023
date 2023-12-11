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


""" def is_all_z(names):
    for name in names:
        if not name.endswith('Z'): return False
    
    return True """


def get_cycle_start_and_len(instructions, network, location_name):
    steps_taken = 0
    steps_to_z = {}
    num_instructions = len(instructions)

    while True:


def get_simul_steps_to_zzz(instructions, network):
    instructions = [0 if char == 'L' else 1 for char in instructions]
    location_names = get_names_ending_a(list(network.keys()))
    all_cycle_starts_and_lens = [get_cycle_start_and_len(instructions, network, loc_name) for loc_name in location_names]
    latest_start = max(all_cycle_starts_and_lens, key=lambda x: x[0])[0]
    all_steps_before_cycle = [get_steps_to_zzz_before(instructions, network, loc_name, latest_start) for loc_name in location_names]
    acyclic_result = get_simul_steps_taken(all_steps_before_cycle)

    if acyclic_result: return acyclic_result

    all_steps_to_first_zzz = [get_first_zzz_after(instructions, network, loc_name, latest_start) for loc_name in location_names]

    return reduce(lambda x, y: x * y, all_steps_to_first_zzz)


""" def get_simul_steps_to_zzz_par(instructions, network, location_name, idx, start, interval):
    steps_taken = start
    steps_to_z = []

    while steps_taken < start + interval:
        for inst in instructions:
            location_name = network[location_name][inst]
            steps_taken += 1

            if location_name.endswith('Z'): steps_to_z.append(steps_taken)

    return (idx, steps_to_z, location_name) """


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
        if lst[0] == max_num: continue

        while lst != [] and lst[0] < max_num:
            lst.pop(0)

    return 0 


def get_simul_steps_taken(steps_list):
    while not 0 in [len(l) for l in steps_list]:
        steps_taken = steps_list[0][0]
        in_progress = False

        for lst in steps_list[1:]:
            if lst[0] == steps_taken: continue

            remove_fewer_steps(steps_list)

            in_progress = True

            break

        if not in_progress: return steps_taken
        
    return None 
      

""" def update_steps_list_and_loc(steps_list, location_names, payload):
    idx, steps_to_z, new_loc = payload

    print(f'update loc from {location_names[idx]} to {new_loc}')
    print(f'extending {steps_list[idx]} with {steps_to_z}') 

    steps_list[idx].extend(steps_to_z)
    location_names[idx] = new_loc

    return 0 """


""" def run_test_simul_par(test, interval=10000):
    instructions, network = parse(test)
    instructions = [0 if char == 'L' else 1 for char in instructions]
    location_names = get_names_ending_a(list(network.keys()))
    num_locations = len(location_names)
    pool = Pool(processes=num_locations)
    steps_list = [[] for i in range(num_locations)]
    start = 0

    print(f'starting with {num_locations} processes...')
    print(f'steps_list initialized with {len(steps_list)} lists...')

    while True:
        for i in range(num_locations):
            location_name = location_names[i]

            pool.apply_async(
                get_simul_steps_to_zzz_par, 
                args=(instructions, network, location_name, i, start, interval), 
                callback=(lambda x: update_steps_list_and_loc(steps_list, location_names, x))
            )

        if 0 in [len(l) for l in steps_list]:
            sleep(1)
            
            continue

        simul_total_steps = get_simul_steps_taken(steps_list)

        if simul_total_steps != None: 
            pool.terminate()
            pool.join()

            return simul_total_steps
        else:
            start += interval """


if __name__ == '__main__':
    test1 = """LLR

    AAA = (BBB, BBB)
    BBB = (AAA, ZZZ)
    ZZZ = (ZZZ, ZZZ)"""

    assert(get_total_steps(test1) == 6)
    assert(get_simul_total_steps(test1) == 6)
    # assert(run_test_simul_par(test1, interval=100000) == 6)

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
    
    print(get_simul_total_steps(test2))
