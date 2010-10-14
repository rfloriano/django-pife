from utils.pife import Manager
m = Manager()

def restart():
    global m
    m = Manager()
    return m

