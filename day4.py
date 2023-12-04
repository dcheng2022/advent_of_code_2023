def parse_card(card):
    numbers_str = card.split(':')[1]
    winning_nums_str, card_nums_str = numbers_str.split('|')

    winning_nums = set([int(n) for n in winning_nums_str.split()])
    card_nums = [int(n) for n in card_nums_str.split()]

    return (winning_nums, card_nums)


def get_card_points(card):
    winning_nums, card_nums = parse_card(card)
    card_points = 0

    for c_num in card_nums:
        if not c_num in winning_nums: continue

        if card_points == 0:
            card_points = 1
        else:
            card_points *= 2

    return card_points


def get_num_cards_won(card):
    winning_nums, card_nums = parse_card(card)
    num_cards_won = len([n for n in card_nums if n in winning_nums])

    return num_cards_won


def get_card_num(card):
    card_num_str = card.split(':')[0].split()[-1]
    card_num = int(card_num_str)

    return card_num


def get_card_nums_and_wins(cards):
    winnings = {get_card_num(card):get_num_cards_won(card) for card in cards}

    return winnings

"""
def get_total_num_cards(cards):
    cards = [c.strip() for c in cards.split('\n')]
    total_num_cards = len(cards)

    card_nums_and_wins = get_card_nums_and_wins(cards)
    card_num_queue = [get_card_num(card) for card in cards]

    while card_num_queue:
        card_num = card_num_queue.pop(0)
        num_cards_won = card_nums_and_wins[card_num]
        total_num_cards += num_cards_won

        for won_card_num in range(card_num + 1, card_num + num_cards_won + 1):
            card_num_queue.append(won_card_num)

    return total_num_cards
"""

def get_total_num_cards(cards):
    cards = [c.strip() for c in cards.split('\n')]
    total_num_cards = len(cards)

    card_nums_and_wins = get_card_nums_and_wins(cards)
    dp = [0 for i in range(len(cards))]

    for i in range(len(cards) - 2, -1, -1):
        num_cards_won = card_nums_and_wins[i + 1]
        dp[i] += num_cards_won

        for j in range(1, num_cards_won + 1):
            dp[i] += dp[i + j]
 
    total_num_cards += sum(dp)

    return total_num_cards

    
def get_total_points(cards):
    cards = [c.strip() for c in cards.split('\n')]

    return sum([get_card_points(c) for c in cards])


if __name__ == '__main__':
    test1 = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
    Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
    Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
    Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
    Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
    Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""

    assert(get_total_points(test1) == 13)
    assert(get_total_num_cards(test1) == 30)

    test2 = """Card   1: 73 92 13 35 18 96 37 72 76 39 | 82 14 66 57 25 98 49 28  3 95 81 85 31 30 16 79  7 12 55 19 97 45  9 58  2
    Card   2: 41 93 82 81 96 56 46 13 44 79 | 13 28 47 49 46 94 84 87 96 45 41 79 35 43 31 34 81 82 64 93  8 56  9 44 55
    Card   3: 22 26 55 46 94 88  3 17 91 95 | 95 97 44 25 46 91 17 20 43 94 22 34 62 73 31 55 60 79 88 90  3 80 33 89 26
    Card   4: 78 32 27 65 64 28 43 81 50 93 | 95 37 77 46 29 55 98 88 94 72 53 80 43 41  7 63 92 33 32 66  2 35 31 24 65
    Card   5: 74 21 96 20 45 88 18 10 53 73 | 80 87 86 81 28 11 77 16 70 44  8 22 72 85 27 35 42 36 84 37 59  9 41 56  3
    Card   6: 70 48 93 10 63 97 20 77 72 42 | 19  7 12  1 47 31 72 88 36 82 69 17 29 62 22  8 32 86 52 76 96 41 51 55 44
    Card   7: 79 43 87 42  8 74 51 69  3 44 | 30 27 19 42 99 28 68 43  5 36 54 24 92 97 34 44 96  2 50 82 35 69 25 45 18
    Card   8: 11 39 32 62 93 41 75 94 23 29 | 40 31 95 41 17 21 81 90 34 13  4  5 48 24 20 80 50 26 27 43 54 61  8 73 89
    Card   9: 75 99 39 45 32 35 55 87 76 21 | 34 14 80  3 93 46 71 78 23 22 87 82 42 49 76 94 10 51 44 58 11  4 91 26 43
    Card  10: 34 53  9 36 52 30 70 60 65 96 | 85 31 29 41  4 88 63 93  9 52 11 37 23 61 51 71 97 26 70 15 38 72 94 64 95
    Card  11: 41 92 42 94 63 89 85 25 86 98 |  3 20 70 74 93 34 21 82 37 55  9 79 85 41 14 99  2 92 90 26 40 57 67 89 31
    Card  12: 50 37 85 46 56 44  2 42 60 66 | 69 78 30 59 71 87  6 51  9 81 75 45 24 16 31 61 44 96 41 86 23 17 42 27 40
    Card  13: 24 46 50 29 89 77 49 25 53 65 | 63 66 43 86 11  9 40 70 38 79 78 27 12 20 84 42 67 73 22  8 68 35  6  4 69
    Card  14: 72 68  9 78 90 40 55 37 16 52 | 27 98 76 63 58 70  8 44 48 90  6 92  3 20 96 88 59 31 95 15 45 47 30 65 64
    Card  15: 15 28 38 87 24 61 26 13 18 94 | 63 56 51 29 17 47 21 62 19 14 69 32 60 41 11 10 54 89  7 35 71 16 96 20 27
    Card  16: 11 24 42 76 99 12 45 94 33 10 | 36 94 72 31 12 28 24 18 11 99 61 33 79 10 53 35 76 42 43 22 78 27 62 59 45
    Card  17: 72 40 35 28 16 51  2 89 83 39 | 68 79 67 15 77 35 12 34 57 16 10 75 72 39 89 60 27 29 19 17 32 45 37 38 14
    Card  18: 13 68 25 92 79 95 67 87 50  7 | 29 23  1 59 91 51 17 80 12 84 27 66 69 61 39 16 34 44 54 37  4 11  9 45 14
    Card  19: 62 14 80 15 40 69 26 65 83 32 | 72 18 66 83 59 48 65 50 37 93 80 14 67 60 40 68 32 69 27 85 30 31 62 15 26
    Card  20:  4 20 48 56 11 13  8 83 98 96 | 87 25  5 99 19  3 51 79 36 35 39 43 45 63 80 40 20 75 24 64 54 98 95 68 72
    Card  21: 13 67 19 78 79 47 49 69  8  9 | 44  9 47 62 50 78 19 76  8 57 77 13 39 11 43 67 49 18 79 94 69 55 58  7 70
    Card  22: 21 39  6 99 81 57 22 53 95 90 | 80 46 74 15 69 72 14 16 87 10 99 20 45 81  6 27 51 21 40 89 90 95 65 57 50
    Card  23: 27 36 95 10 68 52 30 43 51 70 | 62 52 51 95 68 25 11 30 65 10 55 49 27 81 34 37 63 43  9 56 96 70  1 36 58
    Card  24: 31 57 94  2 78 82 63 27 97 70 | 97 58 46 37 70  2 98 57 11 29 36 94 51 90 56 27 13 31 39 28 60 71 96 78 26
    Card  25: 96 13 61 89 70 80 93 57  9 28 | 13 27 29 50  9 94 59 80 16  7 40 89 91  3 60 75 17 18 36 86 15 28 26 61 57
    Card  26: 53 96 15 97 36 13 31 22 19 35 | 61 55  1 92 93 65 19 41 52  3 85 24 22 78 13 70 66 54 31 95 71 96 58 97 35
    Card  27: 56 75 28 85 82 52 58 59 13 33 |  2 31 12 10 81 94  9 80  5 95 43 55 83 60 66 79 61 58 49 34 29 57 99 92 88
    Card  28:  4 21 19 94 95 47 92 52 78 73 | 72 96 85  7 26 44 56 86 49  6 63 35  1 66  4 70 13 40 71 17 62  8 69 76 32
    Card  29: 44 13 92 57 70 83 96 63  6 76 | 51 30 71 38 42 76 77 99 10 64 26 81 21 50 89 59 31  8 79 83 85  2  5 75 44
    Card  30: 59 26 61 78 20  5 11 32 87 23 | 97 41 35 31 27 80 83 51 42  2 17 48 69  6 37 62 43 29 18 73  8 95 82 79 45
    Card  31: 80 30 36 54  1 81 95 16 45 62 | 99 73 91 43 93 23  4 51 71 30 84 28 80 63 46 53 49 55 74 31 25  2 52  3 21
    Card  32: 10  9  5 18 68 47 81  1 93 65 | 55 80 77 33 50 94 56  9 58 22 86 31 51  2 88 44 98 99 26 21  3 30 20 52 93
    Card  33: 16 48 32  5  1 96 11  2 14 46 | 80 10 79 87 19  5 71 72 30 29 93 13 39 67  8 49 22 48 76 28 52 23 58 38 81
    Card  34: 70 24 23 27 67 55 95 96 80 92 | 54  5 42 37 93 49 10  7 74 80 50 34 78 40  2 28 39 52  3 83 62 21 91 71 73
    Card  35: 70 96 75 73 29 58 88 16 77 71 | 68 42 64 11 65 63  5 79 38 52 34 41 86 35 25 44 48 93 20 60 78  4 90 80 21
    Card  36: 17 59 71 39 41 83 86 51  4 23 | 88 96 35 17 91 16 34 26 27 92 75 97 46 78 39 80 32 60 70  9 81 28 50 95 18
    Card  37: 52 75  8 64 39 42 10 34 71 73 | 62 34 29 80 46 64  2 42 81 45 55 44 17 33 66 26 12 50 52  8 94  4 43 85 48
    Card  38: 61 74 68 26 97 31 86 96 41 98 | 95 56 70 49  3 86 21  8 90 39 96 26 30 16 46 31 97 89 61 68 53 41 98 54 74
    Card  39:  3 18 75 56 73 41 43 82 34 33 | 70 26 42 78  6 56 90 41 17 75 18 47 82 32 13 60 81 39  5 52 54 55 12 48 98
    Card  40: 96 25 22 84 95 72 50 40 90 69 | 48 91 77 78 16 17 55 26  1 28 14 31 23 79 51 24 82 97 62 47 13 93 12  4 20
    Card  41: 71 54 24 39  7 51 95 46 90 17 | 96 44 64 69  8 62 97 39 48  2 76 71 37 84 90 54 95 81 46 63  7 51 50 24 47
    Card  42: 48 94 44 43 57 58 55  7 17 11 |  2 12 84 40 96 57 73 17 55 94 43 87 90 95 35 21 11 42 34 26 25 10 74 60 41
    Card  43: 75  8 12 87 36 35 33 62 11 39 | 25 73 71 64 46 99 60 57 15 24 80 10 74 67 12 23 63 69 56 55 20 53  1 52 81
    Card  44: 66 71 25 56  8 65 96 38 68 41 | 41 33 18 60 66 72 37 87 59 94 56 96  5  7 17 21 14 25 93 39 74 79 46 71 11
    Card  45: 27  8 93 49 24 48 23 78 98 51 | 71 37 96 47 74 21  9 40 12 45 49 70 84 76 58 53 50 91 34 85 13  7  5 29 55
    Card  46: 84 42 44 27 98 64 19 28 93 74 | 17 15  4 47 75 52 73 90 89 57 55 36 80 81 54 71 88 53  1 56 21 32 66 91 38
    Card  47: 53 21  4 28 65 58 49 98 10 23 | 25 20 19 64 10 67 15 78 80  7 83 13 35 38 75 86 33 28 98 27 73 70 59 79 14
    Card  48: 37 12  5 10 95 45 70 11 72 97 | 16 89 35 32 24 78 71 91 14 52  9 63 53 36 17  8 82 97 69 27 26 12 81 67 43
    Card  49: 54  4 71 83 72 50 95 78 35 36 | 46 87 98 18 36 72 74 75 66 70 69 16 21 58 90 33 93 68 41 59  7 23 92  5 11
    Card  50: 70 93 33 38 27 36 61 55 74 94 | 40 20 58 70 78 12 14 31 95 29 19 65 81 17 90 16 45 51 13 97 72 63 53 41 88
    Card  51: 27 14 41  6 24 48 96 66 43 18 | 11  1 81 92  8 29 26 13 35 73  3 78 93 52 98 77 60 99 62 79 22 54  9 21 30
    Card  52:  1 28 54 70 24 22 50 37 63 87 | 22 11 71 87 50 25 24 70 37 14 95 28 40 80  3 54 63 58 82  1 34 41 13 10 75
    Card  53: 33 96 53 80 60  6 35 77 32 83 | 35  5 43 67 32 80 18 79 58 91 28 96 23 53  6 83 77 86 71 50 21 33 60 30 24
    Card  54: 45 76 84  5 12  3 44  2 81 59 |  6 76 63 81 16  2 12  3 87 44 21 24 45 19 59 84  5 17 68 80 66 36 15 99 31
    Card  55:  5 67 46 50 68 64 14 94 11  4 | 45 34 62 53 97 65 37 27 68 36 22 44 20 60 75 77 89 55 33  9 13 28 63 31 47
    Card  56: 51 96 40 33 39 81 74 60 62 65 | 70 90 69 76 32 62 40 65 56 80 28 33 74 81 82 94 60 12 49  7 39 96  8 63 51
    Card  57: 24 71 51 97 23 89 41 46  6 56 | 62 52 20  4 67 24 38  5 92 50 11 63 59 17 55 83 98 21 48 87 97 32 23 53 66
    Card  58: 63 72 78 10 64 46 65 54 95  9 |  8 77  4 58 32 82 42 49 97 47 40  2 87 24  9 94 63 61 17 27 56 55 12 75 39
    Card  59: 62 67 17 58 45 46 91 94 81 93 | 46 40 52 26 74 81 17 41 82 61 12 50 35 97 62 94 28 58 38 45 92 63 67 93 91
    Card  60: 81 21 13 88 69  2 49 17 59 51 | 64  4 59 28 95 21  2 17 49 88 48 13 82 51 18 65 54 81 42 10 22 69 32 85 60
    Card  61: 50 51 58 20 22 31 61 89 84  7 |  1 68 27 88 52 39 13 23  2  3 42  5 55 29 77 38 44 95 63 34 46 75  4 60 16
    Card  62: 62 84 76 41 71 86 25 15 55 42 | 71 32 35 76 42 41 84 15  1 43 30 88 48 86 25 70 98 62 93  3 13 46 77 97 50
    Card  63: 34 20  1 29  7 61 31 97 81 85 | 26  8 78  2 29 61 23 59 60  7 10 86 12 64  1 87 24 56 58 30 19 53 36 81 34
    Card  64:  3 82 28 70 49 95  9 52 45 38 | 27 28 65 81 57 15 29 71 32 60 48 52  4 73 38 72 67 10 88  7  3  5 78 91 18
    Card  65: 85 74 52 87 60 24 82 72 67 93 | 72  4 87 52 86 48 39 67 18 15 99 41 78 38 60 84 36 75 79 23  2 42 54 16 69
    Card  66: 33 54 78 76 24 29 62 20  2 98 | 76 98 51 99 75  2 30 83 33 72 28  3 29 62 20 84 54 61 59 94  1 16 63 24 78
    Card  67: 59 78 56 63 44 35 10 94 13  4 | 46 63 56  1 94 86 55 80 20 28 50 67  4 53  6 59 13 58 93 10 22 19 84 12  8
    Card  68: 87 12 41  7 75 43 62 68 63 81 |  4 95 20 24 91 37 70 56 67 49 90 82  6 21 59 30 71 64 41 65 58 96  8 25 13
    Card  69: 89 39  8 86 62 97 53 84 72 74 | 11 48 25 89 72 59  7 85 15 19 65 80 54  1 21 38 29 30 40 58 56 49  3 83 52
    Card  70: 75 49 73 78 29 12 47 36 24 88 | 92 84 50 75 12 34 73 28 97 86 29 56 78  8 69 47 17 44 32 68 81 15 16 26 37
    Card  71: 44 41 24 40 59 85 74 36  4 92 | 33 48 32 49 78 34 35 29 45 93 36 37 18 98 16 17 58 69 40 61 66 94 60 59 75
    Card  72:  9 21 83 27  2 23 99  7  6 59 | 73 74 81 25 65 33 29 14 27 44 24 63 49 43 12 37 69 79 36 54 52 82 55 78 94
    Card  73: 71 70  3 47 31 76 78 72 86 98 | 95 20 70 33 45 89 85 29 52 88 42 90  6 80 25 58 79 13 48 67 41 49 24 27 39
    Card  74: 22 39 58 70 56 59  3 98 61 97 | 13 84 72 47 11 52  4 35 46 49  5 24 62 43  9 40 63 16 99 93 33 83 30 91 14
    Card  75: 29 48 85 95 64 61 35 99 15 46 | 98 97  9 76  5 14 74 87 38 75 82 54  4 63 20 53 79 40 62 96  2 85 31 36 80
    Card  76: 70 94  3  1 46 48 87  5 16 74 | 52 14 22  6 24 65  4  8 42 36 66 43  9 45 93 69 51 57 19 44 81 98 77 35 79
    Card  77: 77  8 29 21 11 31 93 74 72 71 | 67  8 43 72 62 40 11 77 71 29 61 92 74 12 52 37 78 93 56 31 14 21 63 39 35
    Card  78: 66 48  5  4 63 54 91 74 76 77 | 48 54 36 95 11 61 76 52 46 65 18 67 66 63 62 19  5 74 77 64  4 42  9 91 55
    Card  79: 57 19 65 23 69 74 28 97 89 41 | 89 15 41 99 58 53  8 17 23 81 28 94 43 57  1 46 71 38 87  6 49 59 80 85 75
    Card  80: 64 39 19 41 14  6 91  8 61 46 | 66 94 39 82 43 92 33  8 30  1 40 55 18 95  6 86  7 80 91 65 97  9 12 61  2
    Card  81: 26 28 44 29 78 30 14 68 22 40 | 38  8 25 72 51 31 16 71 45 37 87 23 85 64  7  6 34 44 90  9 13 15 82 49 32
    Card  82: 47 26  6 33 32  1 37 42 96 29 | 68 20 10 56  6 27 13 22 83 15 41 37 24 79 52 93 80 94 45 92 50 46  2 78 42
    Card  83: 33 32 63  1 19 69 29  3 64 10 | 69 43  8 32  9 67 40 23 64 20 96 27  1 42 11 19  3 10 63 33 22 29 55  6 49
    Card  84: 25 47 44 53 22 60 77 89 37 67 | 99 48 44 53 60  6  9  8 22 70 37 96 50 47 25 89 11 49 67 90 29 32 77 40 66
    Card  85: 30 60 57 86 93 88 18 27 48 82 | 94 10 57 86 59 88 48 52 78 29 20 41 82 77 90 87 64  6 60 81 44 51  2 68 45
    Card  86:  8 29 97 92 91 69 48 82 51 67 | 40 81 10 97 57 94  7 65 84 17 96 38  5 76 98 55 39 34 88 27 12 18  3 26  9
    Card  87: 29 21 65 98 26 23 40 94 90 51 | 42 53 95 94 62 75 86 55 29 49 92 21 87 37 56 40 13 68 65 23 26 98 38 31 69
    Card  88: 30 79 14 43 73 41 36 83 19 17 |  3 73 70 55 99 34 90 38 26  5 85 22 81 97 66 16 24 88  2 33 21 63 96 58 41
    Card  89: 81 41 29 97 76 57 30 79 25 52 | 76 37 89 90 38 17 87 46  7 93 99 54 41 62 79 43 82 95 70 61 29 58 48 12 60
    Card  90: 26 94 39 29 48 22 16 98 66 64 | 52 66 61 50 45 64 80 27  5 14 68 13 58 37  7 26 39 82 16 72 33  8 48 99 88
    Card  91: 87 17 19 24 64  7 45 28 36 23 | 54 16 64 83 48 49 61 31 95 66 92 15 85 41  3 82 63 67 55 57  9 68 18 32 43
    Card  92: 48 41  8 81 26 60 65 73  1 88 | 39 65 51 63 69 88 25 41  3 13 66 98 18 31 73 71 86 12 10 96  6 93 20  9 82
    Card  93: 79  2 21 93 97 59 62 43 83 73 | 26  9 28 84 47 46 44  2 83  5 13 95  7  4 36 35 11 10 72 82 90 65 73 98 87
    Card  94: 74 86 50 28 11  2 94 47 54 77 |  1 69 35 40 22 19 16 61 66 68 28 56 29 85 10 51 83  7 50 59 92 71  9 86 67
    Card  95: 96 12 56 26 91 15 64 61 82 40 | 52 14 50 70 93 83 54 42 84 19 43 80 82 25 73  3 44 45 81  5 87 41  8 16 78
    Card  96: 80 38  2 91 44 92 19 43 10 64 | 11 45 21 28 31 71 23 88 93 62 17 27  7 78 33 32 54 84  5 72 15 52 63 68 91
    Card  97: 32 54 71 38  5 89 28 47 75 42 | 98 34 57 25  9 80 37 71 61 62 94  6 65 13 92 84 11  2 72 90 17 67  4  1 46
    Card  98: 39 57  6 68 64 91 90 51 78 10 | 56 30  1 12 62 44 21 69 53 65 84 32 96 25 94 92 38 60 14 47 77 13 71 93 20
    Card  99:  6 89 48 77 90 57 21 72 87 73 | 39 48 45 73 87 79 14 25 57 72 66 89 31 30 77 50 74  6 34 36 21 23 90 10 49
    Card 100: 33 40 16 54 58 60 30 47 22  6 | 31 47 30 76 48 67 33 68 22 57 54  5 16  6 58 43  3 64 55 15 40 60 77 13  4
    Card 101: 19 52 71 42 34 73 35 89 62 46 |  9 73 26 49 72 14 19 46 99 32  4 88 84 10 87 17 27 89 30 98 40  7 75 78 90
    Card 102:  2 79  8 73 25 16 82 47 20 52 | 71 88 82 79  2 51 52  3 54 20 56 19 69 10 97 66 45 28 36 39 47 61 40 13 42
    Card 103: 77 28 11 32 36 23 39 88 76 51 | 26 36 99 55 25 19 31 42 18 66 39 11 59 46  4 74 23 71 77 16 84 58 28 32 53
    Card 104: 22 90 17 19 96 62 98 55 41 49 | 90 91 74 23 98 84 77 31 81 16 41 67 49 55 56 86 22 24 73 52 99 62 93 32 34
    Card 105: 41 91  2  4 18 81 52 93 89 87 |  3 47  6 77 60 24 97 26 70 19 37 36 51 82 48 21 31 99 73 88 59 15 46 35 32
    Card 106: 48 54 60 39 80 50 13 61 43 51 | 24 66 90 38 10 74 28 29 89 16  5 25  2 54 15 34 70  7 44 47 14 48 69 78 13
    Card 107: 10 20 81 62 85 75  4 49 58  1 | 32 89 48 79 90 96 15 59 36 14 49 55 38 34 30 11 62 28 53 72 17 77 41 80 66
    Card 108: 79 94 49 89 78 71 20  7 48 56 | 11 53 35 90 22 29  4 71 48 94 70  8 72 78 27 45  7 21 49 16 55 56 73 42 81
    Card 109: 32 73 98 31  4 46 57 11 40 88 | 36 40 89 47 18 87 98 48 45 84 21  1 80 33 67 32 64 28 61  3 51 10 86 97 62
    Card 110: 45 51 97 87 23 48 19 50 63 55 | 19 20 15 22 27 24 38 93 55 54 98 23 28 97 82 59 73 11  8  1 18 64 50 63 48
    Card 111: 38  1 49 22 26 96  3 88 24 70 | 79 58 20 74 70 80 55 68 35 77 88  3 24 40 87 53 50 47 38 54 82 26 49  7  2
    Card 112: 79 90  9 20 94 36 88 31 48 42 | 25 68 69 52 24 98 76 63 97 41 67 94 61 90 32 87 18 13 75 38 84 60 64 86 89
    Card 113:  7 32  6 52 76 72 39 24 46 79 | 67 19 31 94 50 26 66 11 45 80 86 68 88 22 65  3 99 12 90 79 38 14  4 73 54
    Card 114: 80 54  9  2 58 26 44 63 15 21 |  5 60 76 47 87 33 89 23  4 55 17 42 62 46 97 48 90 91 95 82 34 64 30 19 31
    Card 115: 51 34 88 42 20 98 75 79 39 48 | 76 94 13 58 12 66 50 72  2 89 68 21 96 25 10 45 30  7 99 15 46 59 90  9 53
    Card 116: 43 32 82 89  9 63 78 57 55 77 | 19 47 23 27 70 22 18 52 28 93 36 76 80 65 21  8 67 20 84  9 12 90 92 97  5
    Card 117: 71 50 45 29 32 75 10 96 82 43 | 96 46 83 47 10 11 16 39 36  3 89  9 67  5 72 53  2 27 19  7  8 24 61 37  4
    Card 118: 37 44 20 31 43 47 13 46 51 39 |  8 70  7 66 48 50 18 82 84 96 73 12  6 97 62 75 17 49 26 22  4 24 54 94 61
    Card 119: 36 75 46 25 47 69 95  8 94 81 | 48 91 62 11 99 10  9  7 26 15  1 79 54 45 49 27 53 78 64 65 33 31 59 17  5
    Card 120: 37 96 65 31 64 95  9 55 92 29 | 71 62 77 18 86 52 33 19  8 93 30 74 17 84 59 11 69  4 41 67 76 10 66 43 38
    Card 121: 39 99 21 22 11 13 61 72 49 29 | 98 79 29 42 27 73 12 40 96 13 88 45 14 18  4 36 99 80 11 22 49 23 67 21 72
    Card 122: 74 88 60 36 94 18 99 55 70 16 | 91 77 18  6 93 84 97 68 45 13 63 94 14 21 31 10 65 16 61 54 70 51 30 46 36
    Card 123: 67 91 97 35 11  3  8 69 81 15 | 14 45 66 15  8 29 69 24 68 67 10 59 35 18 17 53 11  3 91 12 43 72 97 81 89
    Card 124: 64 61 94 18 21 17 42 80 86 43 | 25 83 69 59 57 51 87 38 91 54 56 46  4 75 99 90 73 37 20 86 49 98 21 58 81
    Card 125: 51 79 20 71 43 42 46 36 77  7 | 55 46 22 24 76 86 34 95 73 36 98 63 49 43 54 28 58 10 26 62 79 97 39 60 32
    Card 126: 44 51 42 27  1 84 56 38 18 91 | 27 67  1 51 42 44 19 18 73 84 16 12 56 24 91 21 97 47 99 88 90 25  6 38 65
    Card 127: 85 92 63  8 17 51 43 61 52 78 | 37 81 65 43 88 97 17 79 46 51 39 23 44 78 95  2 28 49 32 85 63 84 61  8 92
    Card 128: 36 40  7 30 79 76  4 37 97 27 | 97 29 30 58 84 71  4 98 78 27  6 76 43 22 37 40 36 32  7 23 70 92 53 79 48
    Card 129: 98 81 33 49 20 93 32 82 39 48 | 39 65  7 78 52 87 79 53 33 60 63 81 71 93 55 92 12 30 82 32 38 27 90 95 84
    Card 130: 29 59 99 28 65 42 80 87 19 85 | 87 65 59 82 28 29 64 99 79 33  9 31 19 75 53  1 20 42 97 39 72 80  8 85 63
    Card 131: 88 58 37  3 66 87 67 60 84  5 | 84 86 40 82 37 16 34 55 54 70 80 65 22 77 31 48 78 11 68 18 12 52 69 17 32
    Card 132: 50 23 57 31 27  1 25  2 38 21 | 52 61 75 38 15 71 90 50 76 66 22 39 99 68 13 37 78 18 87 43 63 40 53 84  2
    Card 133:  3 59 60 91 93 68 65 45 86 20 | 13 32 74  8 90 68 58 94 67 38 93 97 75  2 71 20 31 37 59 30 39 44 28 34 64
    Card 134: 42  6 64 28 96 55 43 58 24 40 | 36 99 10 79  2  9 42 61 84 58 35  7 77 38 85 21 64 32 78  6 96 74 89 40 55
    Card 135: 38 15 49 59 73 40 13 60 41 25 | 46 80  2 60 42 59 51 57 56 27 40 62 76 37 84 16 89 18 25 73  5 22 45 70 81
    Card 136: 18 17 68 43 77 76 91 13  4 79 | 11 67 10 73 23 71  8 46 87 79  5 51 58 47 62 66 24 29 55 82 93 20 80 32 42
    Card 137: 60 51 99 79 67 59 66 40 25 87 | 44 53 76  5 77 75 65 90  9 41 55 22 60 23 71 30  1 86 88 15 54 66 59 13 68
    Card 138: 78 65 89 48 62 88  3 12 87 99 | 11 19 39 38 69 81 12 75 17 52 26 56 29 77 91 23 93 53 50 66 15 16 85 80 71
    Card 139: 34 12 48 47 25 98 32 37 21 54 | 13 62 79 43 90 72 47 11 20 82 38 29 69 10 66 35  1 84  7 52 27 42 46 91 58
    Card 140: 61 27 68 51  7 58 43 89 26 59 |  2 17 44 87 36 15  6 35 57 29 62 13 56 81 40 19 53  9 85  5 10 46 64 86 88
    Card 141: 40 28  9 81 37 43 18 77 83 23 | 13 59  2 31 52 30 47  6 42 89 70 69 86 92 19 93 58 49 36  8 29 99 60 63 67
    Card 142: 25  6 69  2 14 44 13 93 89 95 | 13 33 76  2 14 68 95 25 18 23 44 43 89  6 93 11  4 24  9 45 38 69 36 15 17
    Card 143:  3 87 14 59  7  5 69 35 20 17 |  5 16 21 69 38 50 64 97 72 30 53 77 73 13 33 55 79 70  4 10 95 59  3 41 42
    Card 144: 94 63 13 51 62 72 33  9 64 22 | 11 90 13 28 47 56 10  4 93 30  7 70 33 69 62 36 72 96 24 22 71 63 52 86 73
    Card 145: 76  1 41 88 97 18 10 11 52 20 | 18 11 41  1 71 52 12 94 74 44 58 70 69 73 79 97 20 45 59 76 78 88  4 10 64
    Card 146: 93  1 18 44 21 66 28 60 98  9 | 13 42 18 46 28 23 96 16 12 55 70 53 98 56 64 50 15 61 25 72 24 35  8 43 97
    Card 147: 67 27 79 43  7 74 11 15 64 75 | 17 57 90  7 41 36 93 29 62 14 77  5 38 33 68 70 32 13 23  6 25 30 55 45  9
    Card 148: 59 62 37  5 52 53 43 29 98  2 | 33 62 93 52 29 68 43 23 11 35 87 14 76 53 59 77  4 89 48 13  2 15 49 72 99
    Card 149: 38 74 24 93 50 21 19 65 95  5 | 93 82 57 95 67 11  9 55  5 74 46  2 96 19 21 92 56 14 38 33 77 58 32 43 37
    Card 150:  8 99 26 38 47 48 96 20 82 92 | 80 46 13 97 66 22 40 36 85 73 63 32  1 70 49 60 90 88 43  2 48  5 76 34 50
    Card 151: 41 69 32 12  5 72  3 29  2 79 | 28 41 11 64 69 71  3 87 45 40  5 15 50 95 90 53 19 55 26 98 82 12  6 77 14
    Card 152: 96 20 94 19  7 68 24 56 88 97 | 54 70 63 84 26 73 35 24 39 99  6 79 44 20 64 12 38 87  1 43 46 42 11 60  8
    Card 153: 60  9 99 62 93 22 16 11 34 28 | 57 43 38 98 82 89 20 58 71 40 79 53 86  1 69  4 27 19 36 85 83 33 59 90 96
    Card 154: 45 75 27 11 76 24  1  4 21 99 | 96 51 54 55 78 69 24 31 77 18 92 17 89 86  3 11 19 15 88 64 49 47 68 36 14
    Card 155: 97 56 99 89 82  6 17 15 52 29 | 23 26 85 70 13 47 72  1 51 64 90 44 53 45 42 77 88 32 74 25 58 68 37 21 79
    Card 156: 28 78 54 72 36 25 84 47 87 30 | 75 49 44  5 83 48 16 17 82 33 60 15 12 94 41 66 23 51 43 39  6 55 34 77 32
    Card 157: 44 74 36 93 15 96 25 12 19 40 | 84 44 54 96 80 48 59 79 78 55 42 27 11 69 76 19 93  2 35 83 77 43 40 85 99
    Card 158: 74 73 99 41 17 45 92 80 21 85 | 85 51 97 91 69 81 74 73 88 80 28 14  6 95 99 92 50 29 17  5 77 89 76 21 41
    Card 159:  7  2 83 33 51 95 96 18 75 52 | 52 96 21 27 47 98 51 83 29 77 75 53  2 64  7 33 57 82 50 14 95 34 79 44 18
    Card 160: 46 54  7 84 37 42 60  9 47 10 | 84 34  9 85 24 29 80  8 88 10  1 46 43 59 47 76 81 26 68 60 30 42  7 56 37
    Card 161: 18 88 61 65 90 29  1 20 22 25 | 25 84 28  2 45 61 39 71 35 32 16 18 65  1 29 23 49  5 22 83 78 24 20 88 90
    Card 162: 78 93 50 17 75 29 69 31 65 85 | 31 18 45 12 28 85 65 69 81 15 32 64 22 40 33 23 50 17 29 97  7 37 63 93 78
    Card 163: 66 47 30 99 34 45 60 82 72 43 | 73 98 29 36 35 54 49 61 17  1 52 95 81 56 31 27 15 96 24 20 32 33 65 55 82
    Card 164: 45 23 93 75 49  1  3 12 36 67 | 77 79 15 82 12 93 49 23 45 31  8 62 66 75 32 48  6 30 78 67 64  3 36  1 94
    Card 165: 75 62 57 30 69 52 35 84 17 32 |  9 17 46 33 69 29 35 34 84 55 57 83 56 70 10  7 30 75 27 99 52 62 32 47 77
    Card 166:  2 79 15 96 51 77 38 98 36 74 |  1 54 12 73 39 75 87 24 49 74 43 53 56 16 34 99 26 30 50 40 86 94 35 66 65
    Card 167: 41 77  3 17 78 56 92 33 87 52 | 98 37 44 68 43 53 76 13 74 59 49 71 66 90 54 82 46  5 95 16 15 62 96 58 25
    Card 168: 23 61 30 69 41 58 21 49 97 16 | 26 74 24 40 58 30 20 38 34 87 72 46 15 77 50  2 57  1 75 81 84 70 23 69 11
    Card 169:  9 17 32 25  1 65 22 46  8 99 | 84 19 66 27 28 15 34 90 42  2 43 87 78  6 81 46 24 13 63  3 48 20 86 70 73
    Card 170: 32 86 96 77 56 40 66 46 89  2 | 87  1 50 91 59 96 29 70 92 93 33 10 20 45 12 60 63 21 14 54 36 80 56 19 75
    Card 171: 70 36 51 80  5 24 40 87 72 30 | 30 52 71 81 84 97 22 95 72 53 46 55 44 51 24 19 98 63 73 56  6 80 90 59 77
    Card 172: 97 74 79 52 85 56 40  2 30 54 | 66 40 49 94 16 47 57 85 24 45 53 63 51 74 69 38 46 90 50 91 75 97 28 31 62
    Card 173: 72 49 45 75 23 20 90 50 48 94 | 38 34 28 33 91 65 87 19 37 30  9 18 64 14 53 70 49 39 90 79 88 51 12 57 48
    Card 174: 48 39 78 41 80 49 43 87 61 22 | 68 39 65 84 67 79 10 29 78 81 36 73 62  6 44 72 27  1 19 66 93  4 16 46 50
    Card 175: 96 91 10 82 43 98 30 65  3 83 | 49 77 40 78 70 23 52 34 16  2 64 72 69 61 15 33 79 32 39 74  7 92 24 46 36
    Card 176: 29 21 33 68 60 35 11 99 82 61 | 81 13 97 71 32 40 23 36 59 53 66 54 62 47 89 93 44 33 87 55 26 18 31 64 67
    Card 177: 97 45 62 55 76 34 66 54 14 68 | 94 42 28 30 32 58 33 48 46 80  7 15 92 98 95 81 90 17 71 24 26 16 39 13 93
    Card 178: 99 45 47 89  4 17 36 14 86 96 | 40 33 56 89 17 93 94 45 75  4  5 99 37 36 47 98 70 44 86 65 14 73 96  8 22
    Card 179: 30 63  6 25  4 85 41 17 83 11 | 44 92 25 71 95 61 50 11 27  4  6 30  9 85 63 67 87 13 17 83 18 53 41 10 52
    Card 180: 70 89 32 66 15 30 76  8 42 36 | 36 16 89 13 45 42 31 77 76 30 71 27  8 95 98 32 35 14 66 70 26 85 72 33 15
    Card 181: 74 81 12 28 22 21 14 54  3  5 | 32 59 69 67 15 35 42 12 34 11  5 71 79  2 73 14 55 87 56 65 28 17 30 99  9
    Card 182: 79 41 90 19 21 15 66  2 55 59 |  2 93 34 65 67 63 72 79 15  5 59 14 55 95 70 83 90 21 68 66 19  7 41 92  3
    Card 183:  6  8 44 39 74 78 10  2 61 59 |  6 61 75 44 62 92 77 29  8 39 78 20 73 18 68  4 60 66 74 59 49  3  2  5 10
    Card 184: 68 32 10 82 15 95 56 89 28 42 | 25 56 28 73  6 11 43 37 95  2 70 18 19 90 45 89 26 42 10 32  7 98 82 15 68
    Card 185: 66 74 17  3 71 21 51 28 14 48 | 80 34 77 37 45 74 84 20 44 14 31 66 51 48 17 86 12 43 71 56 35 13  4 93 27
    Card 186: 79 33 25 28 86 18 57  7 76 40 | 26 16 59 99 31 62 77 21 23 70  7 25 35 49 81 18 72 45 65 58 86 51 88 80 76
    Card 187:  1  2 73 43 13 64 69 21  3 46 | 65 37 53 92 82 13 12 28  3 58 71 46 64  1 56 19 98 21 73 43 60  2 57 29 69
    Card 188: 85 77 35 15 22 67 79 18 66 99 | 42 46 93 19 28  4 89 32 95 75 11 57  6 40 39 30 22 43 41 24  8 78 58 69 48
    Card 189: 13 48  6 61 55 38 75 96 76 42 | 42 32 61 81 55 13 26 41  9 77 70 68 56 35 58 89 20 75  6 72 91 38 90 93 96
    Card 190: 19 78 50 35 32 14 45 70 16 77 | 32 92 71 86 75 77  9  8 19 68 16  6 67 33 15 78 43 57 55 85 69 35 73 50 14
    Card 191: 71 62  7 72 70  4 89 95 94 59 | 36 94 40  6 71 59 45 28 90 12 89 95 16 85 83 88  4 48 72 62 76  7 13 70 11
    Card 192: 52 15 61 83 18 67 29 75 34 36 |  8 65 43 93 67 53 88 83 52 75 81 37 49 29  6 39 76 91 92 36 19 98 50 41 33
    Card 193: 78 94  7 48 25 16 91 38 13  5 | 22 77 76 84 17 40 41 36 93 56 50 35 64 59 23 95 89 49 61 30 42 85 37 92 44
    Card 194: 66 92 16 37 42 62 86 76 98 36 | 46 60 34 31 79 40 11 19 16 74 75 36 71 43 13  2 90 76 50 29 85 55 54 10 35
    Card 195: 66 23 45 62 30 95 38  5 97 39 | 96 65 37 89 95 73 69 75 25 45 51 22 62  7 33 13 94 78 34 35 36 56 55 70 24
    Card 196: 15 45 70 41 97 27 80 64 25 28 | 88 93 65 83 36 16 35 92  6 71 82 24 17 64 66 33 37 69 78 60 56 49 91 19 61
    Card 197: 46 35  2 60 75 99  6 42 47 21 | 91 93 70  8 46  6 35 50 55 72 71 64 47 82 39 94 25 67 41 60 86 83 87 90  7
    Card 198: 71 62 73 96 79 63 41 17 56 68 | 95 77 16 70 29 68 66 63 98 80 20 18 31 34 52  5 42 22 49  6 25 38 51 75 50
    Card 199: 70 84 46 98 44 45 16 36 29 99 | 78 21 92 77 32 91 22 90 76 74 42 55 51 69 94 64 26 65 41 97 10 34 15 35  9
    Card 200: 96 60 87 21 80 48 44 69  3 49 |  2 65 66 94 55 62 72 52 86 15 30 71 45 82 49 47 81 33 14 42  4  1 51 75 34
    Card 201: 55 53 33 19  1 70 17 61  2 72 | 62  6 30 86 45 71 46 33 15 90 73 37 18 12 68 87 89 49  8 60 52 22 51 25 74
    Card 202:  5 47 96 53 54 14 77 29 12  3 | 26 71 91 86 59 70 78  8 83 92 35 64  9 79 84 34 36 93 90 40 16 44 51  6  4"""

    print(get_total_num_cards(test2))