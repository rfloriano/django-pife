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

    def brain(self, garbage, pack):
        pos = 0
        self.get_card(garbage)
        for card in self.cards:
            seq = self.has_sequence(card) + self.has_same_value(card)
            self.cards[pos].rate = seq
            pos += 1
        print "lixo ", garbage, garbage.rate
        rates = self.cards.get_rates()
        index = rates.index(min(rates))
        rate = rates[index]
        if rate < garbage.rate and garbage.rate > 0 and garbage != self.cards[index]:
#            pass
            print "pegou lixo ", garbage, garbage.rate
        else:
            garbage = self.discart(garbage)
            c = pack.next_card()
            self.get_card(c)
            pos = 0
            for card in self.cards:
                seq = self.has_sequence(card) + self.has_same_value(card)
                self.cards[pos].rate = seq
                pos += 1
            print "comprou ", c, c.rate
            rates = self.cards.get_rates()
            index = rates.index(min(rates))
        discarted = self.discart(self.cards[index])
        rates = self.cards.get_rates()
        index = rates.index(min(rates))
        print 'min ---> ', self.cards[index], self.cards[index].rate
        if self.cards[index].rate >= 2:
            cards = Pack(self.cards.sort_by_rate())
            groups = []
            for card in cards:
                groups.append(set(self.win_game(card)))
            new_groups = []
            for i in groups:
                if i and not i in new_groups:
                    new_groups.append(i)
            v_groups = []
            ls = []
            win_groups = list(new_groups)
            a = []
            exclude = []
            for groupa in win_groups:
                for groupb in win_groups:
                    if groupb != groupa and groupb in new_groups and not groupb in exclude and not len(groupa.intersection(groupb)) == 0:
                        print "----", groupb
                        new_groups.remove(groupb)
                exclude.append(groupa)
            l = win_groups
            o = exclude
            p = []
            for i in l:
                for j in o:
                    if not j in l:
                        p.append(j)
            #TODO: Implementar funcionalidade de aprendizado - salvar vitorias do jogador e utiliza-las como novos estados meta
            #TODO: Verificar a possibilidade de utilizar busca em amplitude
            if len(p)>=3 or self.cards[index].rate >= 2:
                print "ganhou"
                print "------", self.cards
                return self.cards
        return discarted

    def discart(self, card):
        return self.cards.discart(card)

    def win_game(self, card):
        sequence = lambda x: ([x, x+1, x+2], [x, x-1, x-2], [x, x-1, x+1])
        same_suit = lambda card, card2: card.suit == card2.suit

        group = []
        for seq in sequence(card._value):
            rate = 0
            c1 = self.cards.has_card(seq[1])
            if c1 and same_suit(card, c1):
                rate += 1
            c2 = self.cards.has_card(seq[2])
            if c2 and same_suit(card, c2):
                rate += 1
            if rate == 2:
                group = [card, c1, c2]
                break
        if group:
            return group
        not_same_suit = lambda card, card2: card.suit != card2.suit
        rate = 0
        tmp_cards = [card]
        for c in self.cards:
            if c != card:
                if c._value == card._value and not_same_suit(c, card):
                    tmp_cards.append(c)
                    if len(tmp_cards) == 3:
                        group = tmp_cards
                        break
        return group

    def has_sequence(self, card):
        sequence = lambda x: [x, x+1, x+2]
        same_suit = lambda card, card2: card.suit == card2.suit

        myseq = sequence(card._value)
        c = self.cards.has_card(myseq[1])
        rate = 0
        if c and same_suit(card, c):
            rate += 1
        c = self.cards.has_card(myseq[2])
        if c and same_suit(card, c):
            rate += 1
        reverse = lambda x: [x, x-1, x-2]
        myseq = reverse(card._value)
        c = self.cards.has_card(myseq[1])
        if c and same_suit(card, c):
            rate += 1
        c = self.cards.has_card(myseq[2])
        if c and same_suit(card, c):
            rate += 1
        return rate

    def has_same_value(self, card):
        not_same_suit = lambda card, card2: card.suit != card2.suit
        rate = 0
        for c in self.cards:
            if c != card:
                if c._value == card._value and not_same_suit(c, card):
                    rate += 1
                if c._value == card._value and not not_same_suit(c, card):
                    rate -= 10
        return rate

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

