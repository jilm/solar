from . import base
import re

class Breaker(base.Breaker):
    
    """ Jistič od NOARKU. """

    def __init__(self, curr_nom, poles=1, char="B", n = False, obj = ""):
    
        super().__init__(curr_nom, poles, char)
        self.obj = obj
        self.n = n
        
    def __str__(self):
    
        return "{} {} {}".format(self.descr(), self.man(), self.kind())

    def man(self):
        return "NOARK"
        
    def kind(self):
        flag = "N" if self.n else ""
        return "Ex9BH {0.poles}P{1} {0.char}{0.curr_nom:.0f}".format(self, flag)
        
    def descr(self):
        return "Jistič"


class Contactor(base.Contactor):
    
    """ Stykač nebo relé od NOARKU """

    def __init__(self, curr_nom, no, nc):
    
        self.curr_nom = curr_nom
        self.no = no
        self.nc = nc
        
    def __str__(self):
    
        return "{} {} {}".format(self.descr(), self.man(), self.kind())

    def man(self):
        return "NOARK"
        
    def kind(self):
        return "Ex9CH{0.curr_nom:.0f} {0.no}{0.nc} 230V 50/60Hz".format(self)
        
    def descr(self):
        return "Stykač"

def parse(text, obj = ""):

    if text.startswith("Ex9BH"):

        pattern = re.compile(r"""Ex9BH\s(?P<poles>[1-4])P(?P<n>N?)\s(?P<char>[BCD])(?P<curr>\d\d?)""", re.X)
        m = re.search(pattern, text)
        if m:
            poles = int(m["poles"])
            n = m["n"] == "N"
            char = m["char"]
            curr = float(m["curr"])
            return Breaker(curr, poles, char, n, obj)

    elif text.startswith("Ex9CH20"):

        pass

    elif text.startswith("Ex9CH"):

        pattern = re.compile(r"""EX9CH
            (?P<curr>\d\d)\s
            (?P<no>\d)
            (?P<nc>\d)
            230V""", re.X)
        m = re.search(pattern, text)
        if m:
            pass

lib = list([
             
    parse(kind, obj) for obj, kind in [

# jednopolové jističe
             
    ("100270", "Ex9BH 1P B1"),
    ("100271", "Ex9BH 1P B2"),
    ("100272", "Ex9BH 1P B3"),
    ("100273", "Ex9BH 1P B4"),
    ("100274", "Ex9BH 1P B6"),
    ("100275", "Ex9BH 1P B8"),
    ("100276", "Ex9BH 1P B10"),
    ("100277", "Ex9BH 1P B13"),
    ("100278", "Ex9BH 1P B15"),
    ("100279", "Ex9BH 1P B20"),
    ("100280", "Ex9BH 1P B25"),
    ("100281", "Ex9BH 1P B32"),
    ("100282", "Ex9BH 1P B40"),
    ("100283", "Ex9BH 1P B50"),
    ("100284", "Ex9BH 1P B63"),
             
    ("100285", "Ex9BH 1PN B1"),
    ("100286", "Ex9BH 1PN B2"),
    ("100287", "Ex9BH 1PN B3"),
    ("100288", "Ex9BH 1PN B4"),
    ("100289", "Ex9BH 1PN B6"),
    ("100290", "Ex9BH 1PN B8"),
    ("100291", "Ex9BH 1PN B10"),
    ("100292", "Ex9BH 1PN B13"),
    ("100293", "Ex9BH 1PN B16"),
    ("100294", "Ex9BH 1PN B20"),
    ("100295", "Ex9BH 1PN B25"),
    ("100296", "Ex9BH 1PN B32"),
    ("100297", "Ex9BH 1PN B40"),
    ("100298", "Ex9BH 1PN B50"),
    ("100299", "Ex9BH 1PN B63"),

# dvoupolové

    ("100300", "Ex9BH 2P B1"),
    ("100301", "Ex9BH 2P B2"),
    ("100302", "Ex9BH 2P B3"),
    ("100303", "Ex9BH 2P B4"),
    ("100304", "Ex9BH 2P B6"),
    ("100305", "Ex9BH 2P B8"),
    ("100306", "Ex9BH 2P B10"),
    ("100307", "Ex9BH 2P B13"),
    ("100308", "Ex9BH 2P B16"),
    ("100309", "Ex9BH 2P B20"),
    ("100310", "Ex9BH 2P B25"),
    ("100311", "Ex9BH 2P B32"),
    ("100312", "Ex9BH 2P B40"),
    ("100313", "Ex9BH 2P B50"),
    ("100314", "Ex9BH 2P B63"),
    
# třípolové jističe

    ("100315", "Ex9BH 3P B1"),
    ("100316", "Ex9BH 3P B2"),
    ("100317", "Ex9BH 3P B3"),
    ("100318", "Ex9BH 3P B4"),
    ("100319", "Ex9BH 3P B6"),
    ("100320", "Ex9BH 3P B8"),
    ("100321", "Ex9BH 3P B10"),
    ("100322", "Ex9BH 3P B13"),
    ("100323", "Ex9BH 3P B16"),
    ("100324", "Ex9BH 3P B20"),
    ("100325", "Ex9BH 3P B25"),
    ("100326", "Ex9BH 3P B32"),
    ("100327", "Ex9BH 3P B40"),
    ("100328", "Ex9BH 3P B50"),
    ("100329", "Ex9BH 3P B63"),

# čtyřpolové jističe

    ("100345", "Ex9BH 4P B1"),
    ("100346", "Ex9BH 4P B2"),
    ("100347", "Ex9BH 4P B3"),
    ("100348", "Ex9BH 4P B4"),
    ("100349", "Ex9BH 4P B6"),
    ("100350", "Ex9BH 4P B8"),
    ("100351", "Ex9BH 4P B10"),
    ("100352", "Ex9BH 4P B13"),
    ("100353", "Ex9BH 4P B16"),
    ("100354", "Ex9BH 4P B20"),
    ("100355", "Ex9BH 4P B25"),
    ("100356", "Ex9BH 4P B32"),
    ("100357", "Ex9BH 4P B40"),
    ("100358", "Ex9BH 4P B50"),
    ("100359", "Ex9BH 4P B63"),

# Jednomodulové stykače

    ("107017", "Ex9CH25 02 230V 50/60Hz"),
    ("107320", "Ex9CH25 20 230V 50/60Hz"),
    ("107322", "Ex9CH25 11 230V 50/60Hz"),


]])

def get_breaker(breaker):

    return Breaker(breaker.curr_nom, breaker.poles, breaker.char)

