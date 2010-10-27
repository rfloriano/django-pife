from django.template.loader import render_to_string
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template import RequestContext
from dajaxice.core import dajaxice_functions
from dajax.core import Dajax
from django.conf import settings

from pife import m
from utils.baralho import Card, Pack
from datetime import datetime

def next_card(request):
    dajax = Dajax()
    card = m.next_card()
    m.players[0].get_card(card) # usuario pegou a carta do bolo
#    print m.players[0].cards
    if not card is None:
        dajax.script("flipCard('%s', '%s'); init(); trash_can_get = false;" % (settings.MEDIA_URL+card.frontImage(), card.id()))
    else:
        dajax.script("alert('game over - draw game')")
    return dajax.json()

def get_card(request, card, trash):
    dajax = Dajax()
    if not trash == 'true':
        m._flipped = None
    #TODO: interagir com a biblioteca pife.py enquanto o baralho do jogador eh alterado
    return dajax.json()

def trash_card(request, card):
    dajax = Dajax()
    card = Card(card)
    print "trash ", card
    m._garbage = m.players[0].discart(card) # jogador discarta a carta
    #TODO: bloquear tela: baralho e lixeira enquanto computador
    m._garbage = m.players[1].play(m._garbage, m.cards)

    debug = eval(request.COOKIES["debug"])

    if debug:
        string = ""
        for i in m.players[1].cards:
            string += '<img class="ui-draggable draggable-card trash" src="%s" id="%s" name="%s"/>' % (settings.MEDIA_URL+i.frontImage(), i.id(), i.id())
        dajax.assign("#jogo-dele", "innerHTML", string);

    if isinstance(m._garbage, list):
        dajax.script("$('#jogo-dele').html('')");
        string = ""
        for i in m._garbage:
            for j in i:
                string += '<img class="ui-draggable draggable-card trash" src="%s" id="%s" name="%s"/>' % (settings.MEDIA_URL+j.frontImage(), j.id(), j.id())
        dajax.script("alert('computador ganhou')")
        dajax.assign("#jogo-dele", "innerHTML", string);
    else:
        dajax.script("toGarbageCard('%s', '%s'); init(); trash_can_get = true;" % (settings.MEDIA_URL+m._garbage.frontImage(), m._garbage.id()))
    return dajax.json()

def gotted_trash(request):
    dajax = Dajax()
    m.players[0].get_card(m._garbage) # usuario pegou carta da lixeira
    return dajax.json()

def check_game(request, group1, group2, group3):
    dajax = Dajax()
    result = m.meta([group1, group2, group3])
    dajax.script("alert('%s');" % result)
    return dajax.json()

def reorder(request, order):
    dajax = Dajax()
    return dajax.json()

dajaxice_functions.register(next_card)
dajaxice_functions.register(get_card)
dajaxice_functions.register(trash_card)
dajaxice_functions.register(check_game)
dajaxice_functions.register(gotted_trash)

