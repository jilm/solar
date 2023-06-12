#
#     .ooooo.  oooo d8b ooo. .oo.  .oo.    .ooooo.  
#    d88' `88b `888""8P `888P"Y88bP"Y88b  d88' `88b 
#    888   888  888      888   888   888  888ooo888 
#    888   888  888      888   888   888  888    .o 
#    `Y8bod8P' d888b    o888o o888o o888o `Y8bod8P' 
#
#

import re

# Hustota mědi

rho_cu = 8960.0    # [kg/m3]

# Číselníky
code00 = ["H"]
code01 = ["01", "03", "05", "07"]
code02 = ["B", "G", "J", "M", "N", "N2", "N4", "N8", "Q", "Q4", "R", "S", "T", "T6", "V", "V2", "V4", "V5", "Z", "Z1", "Z2"]
code03 = ["C", "C4"]
code04 = []
code05 = ["H", "H2", "H6"]
code06 = code02
code07 = ["-", "-A"]
code08 = ["D", "E", "F", "H", "K", "R", "U", "Y"]


#    Materiál izolace
izolace = [
    "pvc",
    "xple",
    "epr",
]

#    Materiál vodiče
vodic = [
    "cu"
    "al"
]

#    Referenční způsoby uložení kabeláže dle čsn ...
ulozeni_keys = [
    "A1",
    "A2",
    "B1",
    "B2",
    "C",
    "D1",
    "D2",
]

# Tabulka 52.1 - Nejvyšší pracovní teploty pro různé druhy izolací:
table52_1 = {
    "pvc" : 70,
    "xlpe": 90,
    "epr" : 90,
}

class HWire:

    def __init__(self, voltage, ins1, sheath, ins2, special, structure, core, core_type, core_nr, color, cs):
    
        self.voltage = voltage
        self.ins1 = ins1
        self.sheath = sheath
        self.ins2 = ins2
        self.special = special
        self.structure = structure
        self.core = core
        self.core_type = core_type
        self.core_nr = core_nr
        self.color = color
        self.cs = cs

    def __str__(self):
    
        sheath = "" if self.sheath is None else self.sheath
        insulating2 = "" if self.ins2 is None else self.ins2
        special = "" if self.special is None else self.special
        structure = "" if self.structure is None else self.structure
        core = "" if self.core is None else self.core
        core_nr = "" if self.core_nr <= 1 else str(self.core_nr)
        return "H{0.voltage}{0.ins1}{1}{2}{3}{4}-{5}{0.core_type} {6}{0.color}{0.cs}".format(self, sheath, insulating2, special, structure, core, core_nr)
        
    def curr_max(self, ulozeni):
    
        assert ulozeni in ulozeni_keys, "Neznámý způsob uložení {}".format(ulozeni)
    
def parse_h(text):

    pattern = re.compile("""
        H
        (?P<voltage>(?:01)|(?:03)|(?:05)|(?:07))
        (?P<insulating1>B|G|J|M|N|(?:N2)|(?:N4)|(?:N8)|Q|(?:Q4)|R|S|T|(?:T6)|V|(?:V2)|(?:V3)|(?:V4)|(?:V5)|Z|(?:Z1)|(?:Z2))
        (?P<sheath>C|(?:C4))?
        (?P<insulating2>B|G|J|M|N|(?:N2)|(?:N4)|(?:N8)|Q|(?:Q4)|R|S|T|(?:T6)|V|(?:V2)|(?:V3)|(?:V4)|(?:V5)|Z|(?:Z1)|(?:Z2))?
        (?P<special>(?:D3)|(?:D5))?
        (?P<structure>H|(?:H2)|(?:H6)|(?:H7)|(?:H8))?
        \-
        (?P<core>A)?
        (?P<core_type>[DEFHKRUY])
        \s
        (?P<core_nr>[2-9])?
        (?P<color>[XG])
        (?P<cs>(?:0\\,5)|(?:0\\,75)|(?:1\\,5)|(?:2\\,5)|4|6|(?:10)|(?:16))
        """, re.X)
    m = re.search(pattern, text)
    if m:
        voltage = m["voltage"]
        insulating1 = m["insulating1"]
        try:
            sheath = m["sheath"]
        except:
            sheath = None
        insulating2 = m["insulating2"]
        try:
            special = m["special"]
        except:
            special = None
        try:
            structure = m["structure"]
        except:
            structure = None
        try:
            core = m["core"]
        except:
            core = "C"
        core_type = m["core_type"]
        try:
            core_nr = int(m["core_nr"])
        except:
            core_nr = 1
        color = m["color"]
        cs = m["cs"]
        return HWire(voltage, insulating1, sheath, insulating2, special, structure, core, core_type, core_nr, color, cs)
    else:
        return None

#
# Tabulka B52.2
# dva zatížené vodiče, izolace je PVC
#
#   1/ průřez vodiče [mm2]
#   2/ materiál vodiče
#   3/ způsob uložení
#   4/ dovolený proud [A]
#

tableB52_2 = [
              
    (1.5, "cu", "A1", 14.5),
    (1.5, "cu", "A2", 14.0),
    (1.5, "cu", "B1", 17.5),
    (1.5, "cu", "B2", 16.5),
    (1.5, "cu", "C",  19.5),
    (1.5, "cu", "D1", 22.0),
    (1.5, "cu", "D2", 22.0),
    
    (2.5, "cu", "A1", 19.5),
    (2.5, "cu", "A2", 18.0),
    (2.5, "cu", "B1", 24.0),
    (2.5, "cu", "B2", 23.0),
    (2.5, "cu", "C",  27.0),
    (2.5, "cu", "D1", 29.0),
    (2.5, "cu", "D2", 28.0),
              
    (4.0, "cu", "A1", 26.0),
    (4.0, "cu", "A2", 25.0),
    (4.0, "cu", "B1", 32.0),
    (4.0, "cu", "B2", 30.0),
    (4.0, "cu", "C",  36.0),
    (4.0, "cu", "D1", 37.0),
    (4.0, "cu", "D2", 38.0),
              
    (6.0, "cu", "A1", 34.0),
    (6.0, "cu", "A2", 32.0),
    (6.0, "cu", "B1", 41.0),
    (6.0, "cu", "B2", 38.0),
    (6.0, "cu", "C",  46.0),
    (6.0, "cu", "D1", 46.0),
    (6.0, "cu", "D2", 48.0),
              
]

#
# Tabulka B52.4
# tři zatížené vodiče, izolace je PVC
#
#   1/ průřez vodiče [mm2]
#   2/ materiál vodiče
#   3/ způsob uložení
#   4/ dovolený proud [A]
#

tableB52_4 = [
              
    (1.5, "cu", "A1", 13.5),
    (1.5, "cu", "A2", 13.0),
    (1.5, "cu", "B1", 15.5),
    (1.5, "cu", "B2", 15.0),
    (1.5, "cu", "C",  17.5),
    (1.5, "cu", "D1", 18.0),
    (1.5, "cu", "D2", 19.0),
    
    (2.5, "cu", "A1", 18.0),
    (2.5, "cu", "A2", 17.5),
    (2.5, "cu", "B1", 21.0),
    (2.5, "cu", "B2", 20.0),
    (2.5, "cu", "C",  24.0),
    (2.5, "cu", "D1", 24.0),
    (2.5, "cu", "D2", 24.0),
              
    (4.0, "cu", "A1", 24.0),
    (4.0, "cu", "A2", 23.0),
    (4.0, "cu", "B1", 28.0),
    (4.0, "cu", "B2", 27.0),
    (4.0, "cu", "C",  32.0),
    (4.0, "cu", "D1", 30.0),
    (4.0, "cu", "D2", 33.0),
              
    (6.0, "cu", "A1", 31.0),
    (6.0, "cu", "A2", 29.0),
    (6.0, "cu", "B1", 36.0),
    (6.0, "cu", "B2", 34.0),
    (6.0, "cu", "C",  41.0),
    (6.0, "cu", "D1", 38.0),
    (6.0, "cu", "D2", 41.0),
              
]

class Wire:

    def __init__(self, cores, cores_load, cs, core_material="cu", izol_material="pvc"):
    
        """ cores: celkový počet vodičů v jednom kabelu
            cores_load: celkový počet zatížených vodičů
            cs: průřez vodičů [mm2]
            core_material: materiál vodičů
            izol_material: materiál izolace """

        self.cores = cores
        self.cores_load = cores_load
        self.cs = cs
        self.core_material = core_material
        self.izol_material = izol_material

    def __eq__(self, other):

        if isinstance(other, Wire):
            return self.cores == other.cores and self.cs == other.cs

    @property
    def kind(self):
        return str(self)

    @property
    def manufact(self):
        return "Sonepar"
        
    def __str__(self):
    
        return "H{0.un}{0.izol}{0.kov}{0.izol_out}"
        
class CYKY(Wire):
                                                      
    def __init__(self, cores, cs, diameter=None, mass=None, bending_radius=None, resistence = 0.0, ccc_air = 0, ccc_ground = 0):
        super().__init__(cores, cores-1, cs, "cu", "pvc")
                                                   
    def __str__(self):
        return "1-CYKY-J {}x{}".format(self.cores, self.cs)
       
class H05VVF(Wire):

    def __init__(self, cores, cs, diameter=None, mass=None, bending_radius=None, resistence=0.0, ccc_air=0.0):
        super().__init__(cores, cores-1, cs, "cu", "pvc")
        
    def __str__(self):
        return "H05VV-F {}x{}".format(self.cores, self.cs)

#
# Kabely typu CYKY - informace čerpány z webu výrobce kabelů NKT
#
# počet žil kabelu (cores) [-]
# průřez žil (cross-section) [mm^2]
# diameter - vnější průměr celého kabelu [mm]
# mass - váha kabelu / metr [kg / km]
# bench radius - min. poloměr ohnutí kabelu [mm]
# činný odpor při 20 st. C (resistance) [ohm / km]
# zatižitelnost na vzduchu (current carrying capacity) [A]
# zatižitelnost v zemi [A]
#

lib = [

    *[CYKY(*w) for w in [

        [2, 1.5, 7.0, 80.0, 42.0, 12.531, 22, 34],
        [2, 2.5, 8.0, 118.0, 46.0, 7.519, 30, 45],
        [2, 4.0, 7.0, 159.0, 42.0, 4.699, 40, 59],
        [2, 6.0, 10.0, 210.0, 60.0, 3.133, 51, 73],
        [2, 10.0, 14.0, 394.0, 168.0, 1.88, 70, 98],
        #[2, 16.0, 16.0, 549.0, 192.0, ],
        [3, 1.5, 7.0, 97.0, 42.0, 12.531, 18.5, 28],
        [3, 2.5, 9.0, 142.0, 54.0, 7.519, 25, 36],
        [3, 4.0, 10.0, 201.0, 60.0, 4.699, 34, 48],
        [3, 6.0, 11.0, 270.0, 66.0, 3.133, 43, 61],
        [3, 10.0, 15.0, 486.0, 180.0, 1.88, 60, 81],
        #[3, 16.0, 17.0, 689.0, 204.0, ],
        [4, 1.5, 8.0, 120.0, 48.0, 12.531, 18.5, 28],
        [4, 2.5, 9.0, 176.0, 54.0, 7.519, 25, 36],
        [4, 4.0, 11.0, 249.0, 66.0, 4.699, 34, 48],
        [4, 6.0, 12.0, 338.0, 72.0, 3.133, 43, 61],
        [4, 10.0, 16.0, 598.0, 192.0, 1.88, 60, 81],
        #[4, 16.0, 18.0, 857.0, 216.0, ],
        [5, 1.5, 9.0, 141.0, 54.0, 12.531, 18.5, 28],
        [5, 2.5, 10.0, 212.0, 60.0, 7.519, 25, 36],
        [5, 4.0, 12.0, 305.0, 72.0, 4.699, 34, 48],
        [5, 6.0, 13.0, 414.0, 78.0, 3.133, 43, 61],
        [5, 10.0, 18.0, 742.0, 216.0, 1.88, 60, 81],
        #[5, 16.0, 20.0, 1077.0, 240.0, ],
        [7, 1.5, 10.0, 178.0, 60.0, 12.531, 18.5, 28],
        [7, 2.5, 11.0, 268.0, 66.0, 7.519, 25, 36],
        #[7, 4.0, 15.0, 403.0, 180.0],
        #[12, 1.5, 14.0, 312.0, 168.0],
        #[12, 2.5, 15.0, 453.0, 180.0],
        #[12, 4.0, 18.0, 673.0, 216.0],
        #[19, 1.5, 18.0, 482.0, 216.0],
        #[19, 2.5, 19.0, 709.0, 228.0],
        #[24, 1.5, 19.0, 595.0, 228.0],
        
    ]],
       
    # cores
    # cs
    # diametr
    # mass [kg/km]
    # max. odpor
    # zatižitelnost na vzduchu (current carrying capacity) [A]
       
    *[H05VVF(*w) for w in [
                           
        (2, 0.75, 7.2, 50.9, 26.0, 14.5),
        (3, 0.75, 7.6, 70.6, 26.0, 14.5),
        (4, 0.75, 8.3, 70.8, 26.0, 14.5),
        (5, 0.75, 9.3, 89.5, 26.0, 14.5),
         
        (2, 1.0, 7.5, 59.2, 19.5, 17.0),
        (3, 1.0, 8.0, 72.6, 19.5, 17.0),
        (4, 1.0, 9.0, 91.4, 19.5, 17.0),
        (5, 1.0, 9.8, 113.0, 19.5, 17.0),
         
        (2, 1.5, 8.6, 80.1, 13.3, 21.0),
        (3, 1.5, 9.4, 98.9, 13.3, 21.0),
        (4, 1.5, 10.5, 123.8, 13.3, 21.0),
        (5, 1.5, 11.6, 159.0, 13.3, 21.0),
         
        (2, 2.5, 10.6, 120.3, 7.98, 29.0),
        (3, 2.5, 11.4, 151.2, 7.98, 29.0),
        (4, 2.5, 12.5, 186.5, 7.98, 29.0),
        (5, 2.5, 13.9, 235.3, 7.98, 29.0),
        
        (2, 4.0, 12.1, 176.3, 4.95, 39.0),
        (3, 4.0, 13.1, 225.6, 4.95, 39.0),
        (4, 4.0, 14.3, 278.1, 4.95, 39.0),
        (5, 4.0, 16.1, 347.6, 4.95, 39.0),
                           
    ]],
    
    *[ parse_h(w) for w in [
                            
        "H03VV-F 2X0,5",
        "H03VV-F 2X0,75",
        "H03VV-F 3X0,5",
        "H03VV-F 3X0,75",
        "H03VV-F 4X0,5",
        "H03VV-F 4X0,75",
        "H03VV-F 5X4",
        "H03VV-F 5X6",
                            
    ] ]

]



#lib.extend([
#    SYKFY(*w) for w in [
#        (4,)
#        ]
#    ]
#        )

def filter_cores(cores, lib = lib):

    """ Pro kabel s daným počtem žil, vrací postupně dostupné
    kabely od nejmenších průřezů po největší. """

    for i in sorted(lib, key=lambda x: x.cs):
        if i.cores == cores:
            yield i


def filter_cs(cs, lib = lib):

    for i in lib:
        if i.cs == cs:
            yield i

def filter_curr(curr, lib = lib):
    pass

def parse_old(text):

    return None
    
def explain_h(wire_h):

    voltage_explain = {
        "01": "Jmenovité napětí 100/100V",
        "03": "Jmenovité napětí 300/300V",
        "05": "Jmenovité napětí 300/500V",
        "07": "Jmenovité napětí 450/750V",
    }
    
    insulating_explain = {
        "B": "ethylen-propylenová pryž",
        "G": "ethylen/vinylacetátový kopolymer",
        "J": "oplet ze skelného vlákna",
    }

    print("H: Harmonizovaný vodič.")
    print("{}: {}".format(wire_h.voltage, voltage_explain[wire_h.voltage]))
