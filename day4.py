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

