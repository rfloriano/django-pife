#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

from random import shuffle
from operator import attrgetter
import os#, pygame,math
#from pygame.locals import *
import unicodedata

class Card(object):
    _letters = {"A":1, "J":11, "Q":12, "K": 13}
    _suits = {"copas": "h", "ouro": "d", "paus": "c", "espada": "s"}
    _path = "images/cards/"
    _backImage = _path + "b.gif"

    def __init__(self, *args, **kwargs): #value, suit, color):
        if len(args) == 1: #instance by id
            id = unicodedata.normalize('NFKD', args[0]).encode('ascii','ignore')
            color = "preto" if id[-1] == "p" else "vermelho"
            suit = id[-2]
            suit = self._suits.values().index(suit)
            suit = self._suits.keys()[suit]
            value = id[:-2]
        else:
            value = args[0]
            suit = args[1]
            color = args[2]
        self.symbol = value
        self.value = value
        self.suit_symbol = suit
        self.suit = suit
        self.color = color

    def frontImage(self):
        suit = self._suits[self.suit_symbol]
        img = "%(symbol)s%(suit)s.gif" % {"symbol": self.symbol, "suit": self.suit}
        return self._path + img.lower()

    def backImage(self):
        return self._backImage

    def _set_value(self, value):
        try:
            self._value = int(value)
        except:
            self._value = self._letters[value.upper()]

    def _get_value(self):
        return self._value

    value = property(_get_value, _set_value)

    def _set_suit(self, suit):
        self._suit = self._suits[suit]

    def _get_suit(self):
        return self._suit

    suit = property(_get_suit, _set_suit)

    def __repr__(self):
        return repr("<%s de %s - %s>" % (self.symbol, self.suit_symbol, self.color))

    def id(self):
        suit = self._suits[self.suit_symbol]
        color = self.color[0]
        img = "%(symbol)s%(suit)s%(color)s" % {"symbol": self.symbol, "suit": self.suit, "color":color}
        return img.lower()

    def flip(self):
        if self.side==1:
            self.side = 0
            self.img = self.bimg
        else:
            self.side = 1
            self.img = self.fimg

    def backSide(self):
        self.side = 0
        self.img = self.bimg

    def frontSide(self):
        self.side = 1
        self.img = self.fimg

    def setSide(self,side):
        if side:
            self.img = self.fimg
        else:
            self.img = self.bimg
        self.side = side

    def move(self,dx,dy):
        self.rect.x += dx
        self.rect.y += dy
        if self.child:
            self.child.move(dx,dy)

    def draw(self,surface):
        surface.blit(self.img,self.rect.topleft)

class Pack(object):
    colors = "vermelho preto".split()
    suits = "paus ouro espada copas".split()
    values = "A 2 3 4 5 6 7 8 9 10 J Q K".split()

    def __init__(self, cards=None):
        if cards is None:
            self.cards = [ Card	(v,s,c) for c in self.colors for s in self.suits for v in self.values ]
        else:
            self.cards = cards

    def __len__(self):
        return len(self.cards)

    def __getitem__(self, pos):
        return self.cards[pos]

    def __repr__(self):
        for card in self.cards:
            print card
        return ""

    def resort(self, ordering):
        print self.cards

    def sort_by_value(self):
        return sorted(self.cards, key=lambda card: card.value)

    def sort_by_suit(self):
        return sorted(self.cards, key=lambda card: card.suit)

    def sort_by_rate(self):
        return sorted(self.cards, key=lambda card: card.rate)

    def get_values(self):
        return [ card.value for card in self.cards ]

    def get_suits(self):
        return [ card.suit for card in self.cards ]

    def get_rates(self):
        rates = []
        for card in self.cards:
            if hasattr(card, 'rate'):
                rates.append(card.rate)
            else:
                rates.append(0)
        return rates

    def has_card(self, card):
        card2 = None
        for c in self.cards:
            if c.value == card:
                card2 = c
                break
        return card2

    def shuffle(self):
        shuffle(self.cards)

    def next_card(self):
        if self.cards:
            return self.cards.pop()
        return None

    def get_card(self, card):
        self.cards.append(card)

    def discart(self, card):
        index = self.cards.index(card)
        card = self.cards[index]
        self.cards.remove(card)
        return card

