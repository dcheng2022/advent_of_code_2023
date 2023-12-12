from inputs.day9 import test2
from functools import reduce

def parse(histories):
    histories = histories.split('\n')
    histories_int = []

    for h in histories:
        history_int = [int(n) for n in h.split()]

        histories_int.append(history_int)

    return histories_int


def all_equal(diff):
    start = diff[0]

    for i in range(1, len(diff)):
        if diff[i] != start: return False

    return True


def get_diffs(history):
    diffs = [history]
    queue = [history]

    while queue:
        history = queue.pop(0)
        diff = [history[i + 1] - history[i] for i in range(0, len(history) - 1)]

        diffs.append(diff)
        queue.append(diff)

        if all_equal(diff): return diffs


def get_extrapolation(history):
    diffs = get_diffs(history)

    return reduce(lambda x, y: x + y, [d[-1] for d in diffs])


def get_neg_extrapolation(history):
    diffs = get_diffs(history)
    
    sum_even_diffs = reduce(lambda x, y: x + y, [diffs[i][0] for i in range(0, len(diffs), 2)])
    sum_odd_diffs = reduce(lambda x, y: x + y, [diffs[i][0] for i in range(1, len(diffs), 2)])

    return sum_even_diffs - sum_odd_diffs


def get_sum_extrapolations(histories):
    histories = parse(histories)
    extrapolations = [get_extrapolation(h) for h in histories]

    return reduce(lambda x, y: x + y, extrapolations)


def get_sum_neg_extrapolations(histories):
    histories = parse(histories)
    neg_extrapolations = [get_neg_extrapolation(h) for h in histories]

    return reduce(lambda x, y: x + y, neg_extrapolations)


if __name__ == '__main__':
    test1 = """0 3 6 9 12 15
    1 3 6 10 15 21
    10 13 16 21 30 45"""

    assert(get_sum_extrapolations(test1) == 114)
    assert(get_sum_neg_extrapolations(test1) == 2)

    print(get_sum_neg_extrapolations(test2))
