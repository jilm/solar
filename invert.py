class Invert:

    def __init__(self, power):
        self.power = power
        pass
    
    def man(self):
        return "SOLAX"
        
    def kind(self):
        return "X3-HYBRID-{}.0-D".format(self.power)
        
    def descr(self):
        return "Střídač"
    
    def __str__(self):
        return "{} {} {}".format(self.descr(), self.man(), self.kind())

    def get_params(self):
        return lib[self.power]

def proc_category(x):

    return "\n\\rowdelim\n".join([
        metas[key](val)
            for key, val in x.items()
                if key in metas
    ])
    
def proc_category_plus(x, title):

    return "\\wholerow{\\bf{}" + title + "\\hfill}\n\\rowdelim\n" + proc_category(x) + "\n\\rowdelim"

metas = {

    "dc-in-a" : lambda x: proc_category_plus(x, "DC vstup A"),

    "dc-in-b" : lambda x: proc_category_plus(x, "DC vstup B"),
    
    "ac-out" : lambda x: proc_category_plus(x, "AC výstup"),

    "ac-in" : lambda x: proc_category_plus(x, "AC vstup"),
    
    "batt" : lambda x: proc_category_plus(x, "Baterie"),

    "eps-out" : lambda x: proc_category_plus(x, "Eps výstup"),

    "p-max" : lambda x: "\\valuerow{{Max. výkon $P_{{MAX}}$:}}{{ {:.0f} }}{{W}}".format(x),
    "j-max" : lambda x: "\\valuerow{{Max. zdánlivý výkon $J_{{MAX}}$:}}{{ {:.0f} }}{{VA}}".format(x),
    "p-nom" : lambda x: "\\valuerow{{Nom. výkon $P_{{NOM}}$:}}{{ {:.0f} }}{{W}}".format(x),
    "u-max" : lambda x: "\\valuerow{{Max. napětí $U_{{MAX}}$:}}{{ {:.0f} }}{{V}}".format(x),
    "u-nom" : lambda x: "\\valuerow{{Nom. napětí $U_{{NOM}}$:}}{{ {:.0f} }}{{V}}".format(x),
    "i-max" : lambda x: "\\valuerow{{Max. proud $I_{{MAX}}$:}}{{ {:.1f} }}{{A}}".format(x),
    "isc-max" : lambda x: "\\valuerow{{Max. zkratový proud $I_{{SC,MAX}}$:}}{{ {:.1f} }}{{A}}".format(x),
    "u-start" : lambda x: "\\valuerow{{Startovací napětí $U_{{START}}$:}}{{{:.1f}}}{{V}}".format(x),
    "i-char-max" : lambda x: "\\valuerow{{Nabíjecí proud maximální:}}{{{:.1f}}}{{A}}".format(x),
    "i-disch-max" : lambda x: "\\valuerow{{Vybíjecí proud maximální:}}{{{:.1f}}}{{A}}".format(x),

}


lib = {

    8 : {
        
        "man" : "SOLAX",
        "type" : "X3-HYBRID-8.0-D",
        
        "dc-in-a" : {
            "p-max" : 7000.0,
            "u-max" : 1000.0,
            "u-nom" : 640.0,
            "i-max" : 26.0,
            "isc-max" : 30.0,
            "u-range-mppt" : (180.0, 950.0),
            "u-start" : 200.0,
        },
        
        "dc-in-b" : {
            "p-max" : 5000.0,
            "u_max" : 1000.0,
            "u_nom" : 640.0,
            "i-max" : 14.0,
            "isc-max" : 16.0,
            "u-range-mppt" : (180.0, 950.0),
            "u-start" : 200.0,
        },
        
        "ac-out": {
            "p-nom" : 8000.0,
            "j-max" : 8800.0,
            "i-max" : 12.9,
            "cos-phi" : 1.0,
            "thdi" : 3.0
        },
        
        "ac-in" : {
            "p-nom" : 16000.0,
            "i-max" : 25.8,
        },
        
        "batt" : {
            "i-char-max" : 30.0,
            "i-disch-max" : 30.0,
        },
        
        "eps-out" : {
            "p-nom" : 8000.0,
            "i-nom" : 11.6,
            "p-max" : 120000.0,
        },
        
    },

    10 : {
        
        "man" : "SOLAX",
        "type" : "X3-HYBRID-10.0-D",
        
        "dc-in-a" : {
            "p-max" : 9000.0,
            "u-max" : 1000.0,
            "u-nom" : 640.0,
            "i-max" : 26.0,
            "isc-max" : 30.0,
            "u-range-mppt" : (180.0, 950.0),
            "u-start" : 200.0,
        },
        
        "dc-in-b" : {
            "p-max" : 6000.0,
            "u_max" : 1000.0,
            "u_nom" : 640.0,
            "i-max" : 14.0,
            "isc-max" : 16.0,
            "u-range-mppt" : (180.0, 950.0),
            "u-start" : 200.0,
        },
        
        "ac-out": {
            "p-nom" : 10000.0,
            "j-max" : 11000.0,
            "i-max" : 16.1,
            "cos-phi" : 1.0,
            "thdi" : 3.0
        },
        
        "ac-in" : {
            "p-nom" : 20000.0,
            "i-max" : 32.0,
        },
        
        "batt" : {
            "i-char-max" : 30.0,
            "i-disch-max" : 30.0,
        },
        
        "eps-out" : {
            "p-nom" : 10000.0,
            "i-nom" : 14.5,
            "p-max" : 150000.0,
        },
        
    },


}

library = [
    Invert(8),
    Invert(10),
]

def get(key):
    
    for inv in library:
        if key == "{} {}".format(inv.man(), inv.kind()):
            return inv

def param_tab(inv):

    return "\n".join([ metas[key](val)
        for key, val in inv.get_params().items()
            if key in metas
    ])
