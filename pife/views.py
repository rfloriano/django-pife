# Django imports
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
# Projects imports
from utils.pife import Manager
from pife import restart

def renderGame(request):
    debug = request.GET.get("debug", False)
    m = restart()
    playerCards = m.players[0].cards
    response = render_to_response("base.html", locals(), context_instance=RequestContext(request))
    try:
        debug = eval(debug)
    except:
        if debug == "0" or not debug or debug == "false":
            debug = False
        else:
            debug = True
    response.set_cookie('debug', debug)
    return response

