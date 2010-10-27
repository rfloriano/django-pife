from baralho import Pack, Card

class Player(object):
    def __init__(self):
        self.cards = Pack([])

    def play(self):
        """ Need to implement on extends """
        raise NotImplementedError

    def show_cards(self):
        i = 1
        for card in self.cards:
            print i, card
            i += 1
        return

    def get_card(self, card):
        self.cards.get_card(card)

class Human(Player):
    def __repr__(self):
        return "Human"

#    def play(self, garbage, pack):
#        self.show_cards()
#        if garbage:
#            print "Garbage -> %s" % (garbage)
#            choice = raw_input("Digite 'g' para pegar do lixo ou 'c' para comprar do bolo")
#            if choice == "c":
#                card = pack.next_card()
#                print "Gotted -> %s" % (card)
#            elif choice == "g":
#                card = garbage
#        else:
#            card = pack.next_card()
#            print "Gotted -> %s" % (card)
#            choice = raw_input("Digite 'c' para comprar outra do bolo ou 'f' para ficar com esta: ")
#            if choice == "c":
#                card = pack.next_card()
#                print "Gotted -> %s" % (card)
#        #TODO: resolver bug - validar raw_input
#        self.cards.get_card(card)
#        card = self.cards[self.discart()]
#        self.cards.remove(card)
#        return card

    def play(self, garbage, pack):
        card = pack.next_card()
        self.cards.get_card(card)
        return self.discart(self.cards[0])

    def get_card(self, card):
        self.cards.get_card(card)

    def discart(self, card):
        for c in self.cards:
            if c.id() == card.id():
                card = c
                break
        return self.cards.discart(card)

#    def discart(self):
#        card = int(raw_input("Digite a carta: "))
#        return card - 1

class Computer(Player):
    def __repr__(self):
        return "Computer"

    def check(self, exclude, set_cards):
        result = True
        for i in exclude:
            if i.intersection(set_cards):
                result = False
                break
        return result

    def brain(self, garbage, pack):
        pos = 0
        self.get_card(garbage)
        exclude = []
        for card in self.cards:
            rate_seq = self.has_sequence(card)
            rate_value = self.has_same_value(card)
            if rate_seq == 20:
                cards = self.get_seq_group(card)
                cards.append(card)
                set_cards = set(cards)
                if not set_cards in exclude and self.check(exclude, set_cards):
                    exclude.append(set_cards)
            else:
                if rate_value == 20:
                    cards = self.get_same_group(card)
                    cards.append(card)
                    set_cards = set(cards)
                    if not set_cards in exclude and self.check(exclude, set_cards):
                        exclude.append(set_cards)
            self.cards[pos].rate = rate_value + rate_seq
            pos += 1
        print "lixo ", garbage, garbage.rate
        rates = self.cards.get_rates()
        index = rates.index(min(rates))
        rate = rates[index]
        if rate < garbage.rate and garbage.rate > 0 and garbage != self.cards[index]:
            print "pegou lixo ", garbage, garbage.rate
        else:
            garbage = self.discart(garbage)
            c = pack.next_card()
            self.get_card(c)

            pos = 0
            exclude = []
            for card in self.cards:
                rate_seq = self.has_sequence(card)
                rate_value = self.has_same_value(card)
                if rate_seq == 20:
                    cards = self.get_seq_group(card)
                    cards.append(card)
                    set_cards = set(cards)
                    if not set_cards in exclude and self.check(exclude, set_cards):
                        exclude.append(set_cards)
                else:
                    if rate_value == 20:
                        cards = self.get_same_group(card)
                        cards.append(card)
                        set_cards = set(cards)
                        if not set_cards in exclude and self.check(exclude, set_cards):
                            exclude.append(set_cards)
                self.cards[pos].rate = rate_value + rate_seq
                pos += 1
            print "comprou ", c, c.rate
            rates = self.cards.get_rates()
            index = rates.index(min(rates))
        discarted = self.discart(self.cards[index])
        rates = self.cards.get_rates()
        index = rates.index(min(rates))
        print 'min ---> ', self.cards[index], self.cards[index].rate
        if len(exclude) == 3:
            print "Computador ganhou"
            return exclude
        return discarted

    def discart(self, card):
        return self.cards.discart(card)

    def get_seq_group(self, card):
        sequence = lambda x: [x-1, x, x+1]
        same_suit = lambda card, card2: card.suit == card2.suit
        seq = sequence(card._value)

        c = self.cards.has_card(seq[0])
        d = self.cards.has_card(seq[2])

        result = []
        if not c is None and same_suit(card, c):
            result.append(c)
        if not c is None and same_suit(card, d):
            result.append(d)
        return result

    def has_sequence(self, card):
        sequence = lambda x: [x-1, x, x+1]
        print card
        same_suit = lambda card, card2: card.suit == card2.suit

        seq = sequence(card._value)

        c = self.cards.has_card(seq[0])
        d = self.cards.has_card(seq[2])

        rate = 0
        if not c is None and not d is None and same_suit(card, c) and same_suit(card, d):
            rate = 20
        elif not c is None and same_suit(card, c):
            rate = 10
        elif not d is None and same_suit(card, d):
            rate = 10
        return rate

    def get_same_group(self, card, exclude=None):
        not_same_suit = lambda card, card2: card.suit != card2.suit
        result = []
        for c in self.cards:
            if not c is card and not c is exclude and c._value == card._value and not_same_suit(c, card):
                result.append(c)
        return result

    def has_same_value(self, card):
        not_same_suit = lambda card, card2: card.suit != card2.suit
        rate = 0
        for c in self.cards:
            if not c is card:
                if c._value == card._value and not_same_suit(c, card):
                    rate += 10
                if (c._value == card._value and not not_same_suit(c, card)):
                    rate -= 20
        return rate

    def count(self, card):
        i = 0
        for c in self.cards:
            if c._value == card._value:
                i += 1
        return i

    def play(self, garbage, pack, verbose=True):
        if verbose:
            self.show_cards()
        card = self.brain(garbage, pack)
        return card

class Manager(object):
    players = []
    _turn = -1
    _num_players = 0
    _garbage = None
    _flipped = None

    def __init__(self):
        self.cards = Pack()
        self.cards.shuffle()
        self.players = Human(), Computer()
        self._num_players = len(self.players)
        self.distribute()

    def distribute(self):
        for i in xrange(9):
            for player in self.players:
                player.cards.get_card(self.cards.next_card())

    def turn(self):
        self._turn += 1
        if self._turn < self._num_players:
            return self.players[self._turn]
        self._turn = 0
        return self.players[self._turn]

    def game(self):
        winner = None
        while self.cards:
            player = self.turn()
            self._garbage = player.play(self._garbage, self.cards)
            if isinstance(self._garbage, list):
                winner = self.players[1] # computador
                break
        return winner

    def next_card(self):
        if self._flipped is None:
            self._flipped = self.cards.next_card()
        return self._flipped

    def has_sequence(self, cards):
        cards = Pack(cards)
        cardlist = cards.get_values()
        x = min(cardlist)
        sequence = lambda x: [x, x+1, x+2]
        if cardlist == sequence(x):
            return True
        return False

    def has_same_value(self, cards):
        cards = Pack(cards)
        valuelist = cards.get_values()
        if valuelist[1] == valuelist[0] and valuelist[2] == valuelist[0]:
            return True
        return False

    def has_same_suit(self, cards):
        cards = Pack(cards)
        suitlist = cards.get_suits()
        if suitlist[1] == suitlist[0] and suitlist[2] == suitlist[0]:
            return True
        elif suitlist[1] != suitlist[0] and suitlist[2] != suitlist[0] and suitlist[2] != suitlist[1]:
            return False
        return None

    def meta_group(self, cards):
        ordened = cards.sort_by_value()
        if len(ordened) == 3:
            if (self.has_sequence(ordened) and self.has_same_suit(ordened) == True) or \
               (self.has_same_value(ordened) and self.has_same_suit(ordened) == False):
                return True
        return False

    def meta(self, cards_groups):
        cards = []
        for group in cards_groups:
            data = []
            for card in group:
                if card:
                    data.append(Card(card))
                else:
                    data.append(None)
            cards.append(Pack(data))
        if len(cards) == 3:
            is_valid = True
            for group in cards:
                if not self.meta_group(group):
                    is_valid = False
                    break
                continue
            return is_valid
        return False

