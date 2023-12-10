from inputs.day7 import test2
from functools import reduce

def parse(hands_and_bids):
    hands_and_bids = hands_and_bids.split('\n')
    hands_and_bids = [tuple(hand_and_bid.split()) for hand_and_bid in hands_and_bids]
    hands_and_bids = {hand_and_bid[0]: int(hand_and_bid[1]) for hand_and_bid in hands_and_bids}

    return hands_and_bids


def get_num_pairs(card_counts):
    num_pairs = 0
    counts = list(card_counts.values())

    while 2 in counts:
        counts.remove(2)

        num_pairs += 1

    return num_pairs


def get_hand_type_joker(hand):
    """
        Joker transformations...
        Four of a kind (6) => Five of a kind (7)
        Full house (5) => Four of a kind (6)
        Three of a kind (4) => Four of a kind (6)
        Two pair (3) => Full house (5)
        One pair (2) => Three of a kind (4)
        High card (1) => One pair (2)
    """
        
    if not 'J' in hand:
        jokerless_type = get_hand_type(hand)
    else:
        jokerless_hand = hand.replace('J', '')
        card_counts = {}

        for card in jokerless_hand:
            card_counts[card] = card_counts.get(card, 0) + 1
        
        num_cards_in_hand = len(jokerless_hand)
        num_unique_cards = len(card_counts)

        if num_unique_cards == num_cards_in_hand:
            jokerless_type = 1
        elif num_unique_cards == 1 and num_cards_in_hand == 4:
            jokerless_type = 6
        elif num_unique_cards == 1 and num_cards_in_hand == 3:
            jokerless_type = 4
        elif num_unique_cards == 2 and 3 in card_counts.values() and num_cards_in_hand == 4:
            jokerless_type = 4
        elif get_num_pairs(card_counts) == 2:
            jokerless_type = 3
        else:
            jokerless_type = 2

    while 'J' in hand:
        if jokerless_type in set([1, 5, 6]):
            jokerless_type += 1
        elif jokerless_type in set([2, 3, 4]):
            jokerless_type += 2
        else:
            return jokerless_type

        hand = hand.replace('J', '', 1)

    return jokerless_type


def get_hand_type(hand):
    """
        Five of a kind: 7
        Four of a kind: 6
        Full house: 5
        Three of a kind: 4
        Two pair: 3
        One pair: 2
        High card: 1
    """

    card_counts = {}

    for card in hand:
        card_counts[card] = card_counts.get(card, 0) + 1
    
    num_unique_cards = len(card_counts)

    if num_unique_cards == 1:
        return 7
    elif num_unique_cards == 2:
        if 4 in card_counts.values():
            return 6
        elif 3 in card_counts.values():
            return 5
    elif num_unique_cards == 5:
        return 1
    else:
        if 3 in card_counts.values():
            return 4
        elif get_num_pairs(card_counts) == 2:
            return 3
        else:
            return 2


def get_first_card_value(card, joker=False):
    face_values = {
        'A': 14,
        'K': 13,
        'Q': 12,
        'T': 10
    }

    if joker:
        face_values['J'] = 1
    else:
        face_values['J'] = 11

    if card.isdigit():
        return int(card)
    else:
        return face_values[card]

 
def get_sorted_hands_and_card_val(hands, card_idx, joker=False):
    hands_and_first_vals = {hand: get_first_card_value(hand[card_idx], joker) for hand in hands}
    sorted_hands_and_first_vals = sorted(hands_and_first_vals.items(), key=lambda x: x[1])

    return sorted_hands_and_first_vals


def resolve_ties_and_append(hands_ranked_asc, tied_hands, card_idx=0, joker=False):
    if len(tied_hands) == 1:
        hands_ranked_asc.extend(tied_hands)
    else:
        sorted_hands_and_first_vals = get_sorted_hands_and_card_val(tied_hands, card_idx, joker)
        num_hands = len(tied_hands)
        tied_hands = [sorted_hands_and_first_vals[0][0]]
        tied_val = sorted_hands_and_first_vals[0][1]
        hand_idx = 1

        while hand_idx < num_hands:
            hand, hand_val = sorted_hands_and_first_vals[hand_idx]

            if hand_val == tied_val:
                tied_hands.append(hand)
            else:
                resolve_ties_and_append(hands_ranked_asc, tied_hands, card_idx + 1, joker) 

                tied_hands = [hand]
                tied_val = hand_val

            hand_idx += 1

        if len(tied_hands) >= 1:
            resolve_ties_and_append(hands_ranked_asc, tied_hands, card_idx + 1, joker)
               
    return 0 


def resolve_ties_and_rank(sorted_hand_types, joker=False):
    hands_ranked_asc = []
    num_hands = len(sorted_hand_types)

    idx = 1
    tied_hands = [sorted_hand_types[0][0]]
    tied_type = sorted_hand_types[0][1]
    
    while idx < num_hands:
        hand, hand_type = sorted_hand_types[idx]

        if hand_type == tied_type:
            tied_hands.append(hand)
        else:
            resolve_ties_and_append(hands_ranked_asc, tied_hands, joker=joker)

            tied_hands = [hand]
            tied_type = hand_type

        idx += 1

    if tied_hands != []: resolve_ties_and_append(hands_ranked_asc, tied_hands, joker=joker)

    return hands_ranked_asc
    

def get_hands_in_rank_asc(hands, joker=False):
    """
        No two hands can have the same type (i.e. tie)
        and the hand that wins the tiebreaker receives
        a higher hand type (i.e. number)

        So we sort hand_types and capture ties, resolving
        them by giving the weakest hand the original number
        and other hands the original (number + 1/n * rank)
    """

    if joker:
        hand_types = {hand: get_hand_type_joker(hand) for hand in hands}
    else:
        hand_types = {hand: get_hand_type(hand) for hand in hands}
   
    sorted_hand_types = sorted(hand_types.items(), key=lambda x: x[1])
    hands_ranked_asc = resolve_ties_and_rank(sorted_hand_types, joker)

    return hands_ranked_asc


def get_winnings(hands_and_bids, hands_ranked_asc):
    winnings = []

    for (idx, hand) in enumerate(hands_ranked_asc):
        rank = idx + 1

        # print(f'rank: {rank} hand: {hand}')
        
        winnings.append(rank * hands_and_bids[hand])

    return winnings


def get_total_winnings(hands_and_bids, joker=False):
    """
        The index for any hand and bid is maintained
        in returns from function calls 
    """

    hands_and_bids = parse(hands_and_bids)
    hands = hands_and_bids.keys()
    hands_ranked_asc = get_hands_in_rank_asc(hands, joker) 
    winnings = get_winnings(hands_and_bids, hands_ranked_asc)

    return reduce(lambda x, y: x + y, winnings)


if __name__ == '__main__':
    test1 = """32T3K 765
    T55J5 684
    KK677 28
    KTJJT 220
    QQQJA 483"""

    assert(get_total_winnings(test1) == 6440)
    assert(get_total_winnings(test1, joker=True) == 5905)

    test3 = """322QJ 10
        11119 20
        39391 30"""

    assert(get_total_winnings(test3) == 130)
    assert(get_total_winnings(test3, joker=True) == 110)

    test4 = """1111A 10
    1111J 20
    1111Q 30"""

    assert(get_total_winnings(test4) == 110)
    assert(get_total_winnings(test4, joker=True) == 110)

    print(get_total_winnings(test2, joker=True))
