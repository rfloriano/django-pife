# take a random hand of cards where each card is identified by
# string 'rank suit' and sort by rank and suit

def cards_str2tup(cards):
    """
    convert each card 'rank suit' string to a (suit, rank) tuple
    where rank is an integer number
    """
    cards_tup = []
    for card in cards:
        rank, suit = card.split()
        cards_tup.append((suit, int(rank)))
    return cards_tup

def cards_tup2str(cards_tup):
    """
    convert each card (suit, rank) tuple to a 'rank suit' string
    """
    cards = []
    space = ' '
    for tup in cards_tup:
        suit, rank = tup
        s = str(rank) + space + suit
        cards.append(s)
    return cards

# assume random hand of five cards
hand = ['4 c', '2 s', '12 h', '8 s', '6 s']

# this will sort looking at rank number as a string
hand.sort()
print hand  # oops  ['12 h', '2 s', '4 c', '6 s', '8 s']

# to sort properly convert to a list of (suit, int(rank)) tuples
# by default:
# suit, the first item in each tuple will be primary sort criteria
# rank, the second item in each tuple will be secondary sort criteria
cards_tup = cards_str2tup(hand)
cards_tup.sort()

# suits are in order and each suit's rank is in order too
print cards_tup  # [('c', 4), ('h', 12), ('s', 2), ('s', 6), ('s', 8)]

# convert the properly sorted list of tuples to a list of strings
cards = cards_tup2str(cards_tup)

print cards  # ['4 c', '12 h', '2 s', '6 s', '8 s']

