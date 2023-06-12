
class Component:

    def __init__(self, man, kind, id):
    
        self.man = man
        self.kind = kind
        self.id = id

class Meter(Component):

    def __init__(self, man, kind, range, id):
    
        super().__init__(man, kind, id)
        self.range = range
    
lib = {
    
    "ct": Meter("SOLAX", "CT", None, "ct"),
    "dtsu": Meter("CHINT", "DTSU666", None, "dtsu"),
    "essl": "ALFEN EVE Single S-Line",
    "espl": "ALFEN EVE Single Pro-Line",
       
}
