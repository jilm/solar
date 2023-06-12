from . import tex

def calc_temp_impact(value, temp, coef):
    temp_min, temp_nom, temp_max = temp
    val_min = value * ( 1 + coef * (temp_min - temp_nom) / 100.0)
    val_nom = value
    val_max = value * ( 1 + coef * (temp_max - temp_nom) / 100.0)
    return val_min, val_nom, val_max

pvs = {
    
    "ks550" : {

        "man" : "CanadianSolar",
        "type" : "HiKu6 Mono PERC 550W",
        "pmax-nom" : 550.0,
        "uoc-temp-coef": -0.26,
        "isc-temp-coef": 0.050,
        "pmax-temp-coef": -0.34,
        "dim" : (2261.0, 1134.0, 30.0),
        "weight" : 27.6,
        "isc-nom" : 14.0,
        "uoc-nom" : 49.6,
        "ump" : 41.7,
        "imp" : 13.2,
        "ef" : 21.5,
        "ip" : "IP68",
        "temp": (-40, 25, 85),
        "src": ""

    },

    "sp400": {
    
        "man" : "SUNPRO",
        "type" : "SP400W-108M10",
        "pmax-nom" : 400.0,
        "uoc-temp-coef": -0.25,
        "isc-temp-coef": 0.050,
        "pmax-temp-coef": -0.35,
        "dim" : (1724.0, 1134.0, 30.0),
        "weight" : 21.5,
        "isc-nom" : 13.76,
        "uoc-nom" : 36.94,
        "ump" : 30.83,
        "imp" : 12.94,
        "ef" : 20.46,
        "ip" : "IP68",
        "temp": (-40, 25, 85),
        "src": ""
    },
       
    "sp450": {
       
        "man": "SUNPRO",
        "type": "SP450-144M6",
        "pmax-nom": 450,
        "dim": (1048, 2108, 40),
        "weight": 24.2,
        "isc-nom": 11.56,
        "uoc-nom": 49.8,
        "ump": 41.0,
        "imp": 10.98,
        "ef": 20.37,
        "ip": "IP68",
        "uoc-temp-coef": -0.26,
        "isc-temp-coef": 0.049,
        "pmax-temp-coef": -0.34,
        "temp": (-40, 25, 85),
        "src": ""

    },
    
    "ts450": {
       
        "man": "Talesun",
        "type": "TP6L72M-450W",
        "pmax-nom": 450,
        "dim": (1038, 2094, 40),
        "weight": 23.5,
        "isc-nom": 11.54,
        "uoc-nom": 49.6,
        "ump": 40.9,
        "imp": 11.01,
        "ef": 20.7,
        "ip": "IP68",
        "uoc-temp-coef": -0.26,
        "isc-temp-coef": 0.043,
        "pmax-temp-coef": -0.36,
        "temp": (-40, 25, 85),
        "src": ""

    },
    
    "lo450": {
       
        "man": "LONGi",
        "type": "LR4-72HPH-450M",
        "pmax-nom": 450,
        "dim": (1038, 2094, 35),
        "weight": 23.5,
        "isc-nom": 11.60,
        "uoc-nom": 49.3,
        "ump": 41.5,
        "imp": 10.85,
        "ef": 20.7,
        "ip": "IP68",
        "uoc-temp-coef": -0.27,
        "isc-temp-coef": 0.048,
        "pmax-temp-coef": -0.35,
        "temp": (-40, 25, 85),
        "src": ""

    },
}

def get(key):
    
    """ Vrací parametry solárního panelu nebo None pokud takový
    panel """

    if key in pvs:
        return pvs[key]
    else:
        return None
        

invs = {

    
    "solax x3-hybrid-8.0" : {
        
        "dc-in-a" : "solax x3-hybrid-8.0-D dc-in A",
        "dc-in-b" : "solax x3-hybrid-8.0-D dc-in B",
        
    },
}

metas = {
    "pmax" : ("Maximální výkon", "Wp", "{:_.1f}"),
    "isc"  : ("Zkratový proud", "A", "{:.1f}"),
    "uoc"  : ("Napětí naprázdno ", "V", "{}"),
    "ump"  : ("Napětí při max. výkonu", "V", "{}"),
    "imp"  : ("Proud při max. výkonu", "A", "{}"),
    "uoc-temp-coef" : ("Teplotní koeficient Uoc", "%/K", "{}"),
    "isc-temp-coef" : ("Teplotní koeficient Isc", "%/K", "{}"),
    "pmax-temp-coef" : ("Teplotní koeficient Pmax", "%/K", "{}"),
    "temp" : ("Teplotní rozsah", "degC", "{}"),
}

class PVString:

    def __init__(self, pv):
        
        self.pv = pv
        
    def paint_pt(self, canvas):
        canvas.append_table_begin()
        canvas.append_rowdelimred()
        canvas.append_3value("temp", self.pv["temp"])
        canvas.append_rowdelim()
        canvas.append_value("pv-nr", self.nr)
        canvas.append_rowdelim()
        canvas.append_value("azimuth", self.azimuth)
        canvas.append_rowdelim()
        canvas.append_value("elevation", self.elevation)
        canvas.append_rowdelim()
        canvas.append_3value("pmax", [self.nr * p for p in self.pv["pmax"]])
        canvas.append_rowdelim()
        canvas.append_3value("uoc", [self.nr * u for u in self.pv["uoc"]])
        canvas.append_rowdelim()
        canvas.append_3value("isc", self.pv["isc"])
        canvas.append_rowdelimred()
        canvas.append_table_end("tbl:string", "Parametry stringu.")

class Canvas:
    
    def __init__(self):
        self.result = ""
    
    def append(self, text):
        self.out(text)

    def append_value(self, key, value):
        label, unit, format = tex.metas[key]
        str_value = tex.num_escape(format.format(value))
        self.out("\\valuerow{{{0}}}{{{1}}}{{{2}}}".format(label, str_value, unit))

    def append_3value(self, key, values):
        label, unit, format = tex.metas[key]
        str_values = [ tex.num_escape(format.format(v)) for v in values ]
        self.out("\\valuerowthree{{{0}}}{{{1[0]}}}{{{1[1]}}}{{{1[2]}}}{{{2}}}".format(label, str_values, unit))
        
    def append_rowdelim(self):
        self.out("\\rowdelim")
        
    def append_rowdelimred(self):
        self.out("\\rowdelimred")
        
    def append_table_begin(self):
        self.out("\\tblbegin")
        
    def append_table_end(self, label, caption):
        self.out("\\tblend{{{}}}{{{}}}".format(label, caption))
        
    def open(self):
        pass
        
    def close(self):
        self.out(tex.document_end)
        
    def document_begin(self, title, project):
        self.out(tex.identification.format(project))
        self.out(tex.document_begin)
        
    def document_end(self):
        pass
        
    def append_title_page(self, doc_name, metas):
    
        self.out("""
            \\nopagenumbers
            \\tit{{{}}}
            \\hrule
            \\vskip 12pt
            \\hfil{\\typosize[14/16]\\it Fotovoltaická elektrárna }\\par
            \\vskip 48pt
        
            \\typosize[12/16]
            \\vfill
            \\titlebox
            \\eject
        """.format(doc_name))
        
    def out(self, text):
    
        self.result += text
    

def paint_string_pt(project, canvas):

    canvas.append_3value("temp", project.pv["temp"])
    canvas.append_value("pv-nr", project.s1a_nr)


def paint_param_table(pv, canvas):
    
    keys = [ "imp", "ump", "uoc-temp-coef", "isc-temp-coef", "pmax-temp-coef", "dim", "weight", "ip", "ef" ]
    canvas.append_rowdelimred()
    canvas.append_3value("temp", pv["temp"])
    canvas.append_rowdelim()
    canvas.append_3value("pmax", pv["pmax"])
    canvas.append_rowdelim()
    canvas.append_3value("isc", pv["isc"])
    canvas.append_rowdelim()
    canvas.append_3value("uoc", pv["uoc"])
    canvas.append_rowdelim()
 
    for key in keys:
        canvas.append_value(key, pv[key])
        canvas.append_rowdelim()
        
for key, pv in pvs.items():
    temp = pv["temp"]
    pv["pmax"] = calc_temp_impact(pv["pmax-nom"], temp, pv["pmax-temp-coef"])
    pv["isc"] = calc_temp_impact(pv["isc-nom"], temp, pv["isc-temp-coef"])
    pv["uoc"] = calc_temp_impact(pv["uoc-nom"], temp, pv["uoc-temp-coef"])

class Wire:

    def __init__(self, label):

        self.curr_nom = None
        self.cores = None
        self.type = None
        self.len = None
        self.label = label
        self.end = (None, None)
        self.cs = None

    def set_type(self, type):
    
        if type in ("CYA", "CYKY", "CYSY"):
            self.type = type
            
