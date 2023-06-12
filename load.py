import re
import functools
from . import meta
from . import pv as pvlib
from . import invert
from . import base
from . import dxf4tikz
from . import project
from . import batery
from . import library
from . import component

""" Funkce pro získávání perzistentních dat. """

class Project:

    def __init__(self, order):
    
        # defaultní parametry projektu
        self.author = "Ing. Jiří Lidinský"
        self.approved_by = "Sanjay Maggu"
        self.checked_by = "Vladimír Vaněk"
        self.revision = 0
        self.bat = False
        self.watt = False
        self.wall = False
        self.bkp = False
        self.pv_nr = 0          # Celkový počet solárních panelů
        self.s1a_nr = 0         # Počet panelů prvního stringu
        #self.s2_nr = 0         # Počet panelů druhého stringu
        self.er_access = "?"
        self.er_fc = 25.0
        self.descr = ""
        self.dc_trasa = ""
        self.components = {
        
            "-FC1": component.get("4xB20"),
            "-FC2": component.get("4xB16"),
            "-FC3": component.get("3xB2"),
            "-FC4": component.get("B2"),
            #"-QA1": component.get("stykač 40A 4xNO")
        }
        
        self.schemas = [] #project.schemas
        
        for lno, key, val in order:

            if key == "id":
                self.id = val
                
            # použité panely typ
            elif key == "pv":
                self.pv = pvlib.pvs[val]
                project.components["-GC"] = "Solární panely: {} {}".format(self.pv["man"], self.pv["type"])
            
            # Celkový počet použitých panelů
            elif key == "pv-nr":
                self.pv_nr = int(val)

            # Střídač
            elif key == "-TA":
                self.invert = invert.get(val)
                project.components["-TA"] = "Měnič: {} {}".format(self.invert.man(), self.invert.kind())
            #assert "invert" in order, "Není zadán typ střídače"
            
            # DC rozváděč
            
            # Stringy
            elif key == "s1a-nr":
                self.s1a_nr = int(val)
            elif key == "s1a-elev":
                self.s1a_elev = float(val)
            elif key == "s1a-azimuth":
                self.s1a_azimuth = float(val)
            
            elif key == "s2-nr":
                self.s2_nr = int(val)
            elif key == "s2-elev":
                self.s2_elev = float(val)
            elif key == "s2-azimuth":
                self.s2_azimuth = float(val)
                    
            # AC Rozváděč
            
            # On-Grid kabeláž
            
            # ER rozváděč
            
            elif key == "er-access":
                self.er_access = val
            elif key == "hdo":
                self.hdo = val == "yes"
            elif key == "hdo-fc":
                self.hdo_fc = float(val)
            
            elif key == "consume":
                self.consume = float(val)

            # Off-Grid kabeláž
            
            elif key == "name":
                self.name = val
            elif key == "address1":
                self.address1 = val
            elif key == "address2":
                self.address2 = val

            # baterie
            elif key == "bat":
                self.bat = True
                self.bat_type = val
                self.bat_capacity = batery.lib[val]["capacity"]
                
            # wattrouter
            elif key == "watt":
                self.watt = True
                #self.schemas[0].coord.append((3, 15))
            
            # wallbox
            elif key == "wall":
                self.wall = True
                project.components["=WALL-TA"] = library.lib[val]
            
            # historie revizí
            elif key == "history":
                self.history = sorted(val, key = lambda x: x[1].date)
                
            elif key == "hdr-pozice":
                self.hdr_position = val
                
            elif key == "fve-pozice":
                self.fve_position = val
                
            elif key == "tuv-objem":
                self.tuv_cont = float(val)
                
            elif key == "er-fc":
                self.er_fc = float(val)
                
            elif key == "deksoft2":
                self.deksoft2 = float(val)
                
            elif key == "deksoft3":
                self.deksoft3 = float(val)
                
            elif key == "deksoft5":
                self.deksoft5 = float(val)
            
            elif key == "bkp":
                self.bkp = True
                
            elif key == "descr":
                self.descr = val
                
            elif key == "scope":
                self.scope = val
            
            elif key == "dc-trasa":
                self.dc_trasa = "DC trasa: " + val + "."

            else:
                #print("Nwznámý klíč {}".format(key))
                pass
            
        self.pv_p_sum = self.pv["pmax-nom"] * self.pv_nr
        self.string_nr = 0
        if self.s1a_nr > 0:
            self.string_nr += 1
        if self.s2_nr > 0:
            self.string_nr += 1
        self.revision = self.get_revison()
        self.inv_param_tab = invert.param_tab(self.invert)
        #for i in range(7):
        #    self.schema.append(dxf4tikz.make(i))
        

        if "deksoft2" in dir(self) and "deksoft3" in dir(self) and "deksoft5" in dir(self):
            self.deksoft = [
                self.deksoft2 + self.deksoft5,
                self.deksoft2,
                self.deksoft3,
                self.deksoft2 + self.deksoft3,
                self.deksoft5,
                self.deksoft2 / (self.deksoft2 + self.deksoft3),
                self.deksoft2 / (self.deksoft2 + self.deksoft5)
            ]
            

    def string_param_table(self, canvas):
    
        canvas.append_table_begin()
        canvas.append_rowdelimred()
        canvas.append_3value("temp", self.pv["temp"])
        canvas.append_rowdelim()
        canvas.append_value("pv-nr", self.s1a_nr)
        canvas.append_rowdelim()
        canvas.append_value("azimuth", self.s1a_azimuth)
        canvas.append_rowdelim()
        canvas.append_value("elevation", self.s1a_elev)
        canvas.append_rowdelim()
        canvas.append_3value("pmax", [self.s1a_nr * p for p in self.pv["pmax"]])
        canvas.append_rowdelim()
        canvas.append_3value("uoc", [self.s1a_nr * u for u in self.pv["uoc"]])
        canvas.append_rowdelim()
        canvas.append_3value("isc", self.pv["isc"])
        canvas.append_rowdelimred()
        canvas.append_table_end("tbl:string", "Parametry stringu.")

    def get_revison(self):
    
        indices = "abcdefghijklmnopqrstuvwxyz"
        return indices[len(self.history) - 1]
        
    def get_issue_date(self):
    
        """ Vrací datum poslední revize v historii """
        
        return self.history[-1][1].date

def order2_tokens():

    """ Načte soubor ve tvaru key: value. Komentáře, následující
    za znakem # jsou ignorovány. Navíc, value může být delší než
    jeden řádek. Funkce vrací tzv. tokeny, tedy trojice:
    (line-no, token-type, token). """
    
    with open("order", "r") as f:
        for no, line in enumerate(f):
            # Odstraň komentáře
            if "#" in line:
                line_cl, comment = line.split("#", 1)
            else:
                line_cl = line
            # rozděl na key: val
            if ":" in line_cl:
                token_l, token_r = line_cl.split(":", 1)
                key = token_l.strip()
                val = token_r.strip()
                if len(key) > 0:
                    yield (no, "key", key)
                if len(val) > 0:
                    yield (no, "val", val)
            else:
                val = line_cl.strip()
                if len(val) > 0:
                    yield (no, "val", val)

def order2_group_val():

    """ Sdruží více po sobě jdoucích val tokenů do jedinného. """
    
    last_tt = ""
    val = ""
    val_lno = 0
    for lno, tt, tv in order2_tokens():
        if tt == "key":
            if last_tt == "val":
                yield (val_lno, "val", val)
                val = ""
            yield (lno, tt, tv)
        else:
            if last_tt == "val":
                val += " " + tv
            else:
                val = tv
                val_lno = lno
        last_tt = tt
    yield(val_lno, last_tt, val)
    
def order2_group():

    """ Sgrupuje po sobě jdoucí key, value do jednoho tokenu """
    
    ki = iter(order2_group_val())
    try:
        while True:
            kno, _, key = next(ki)
            vno, _, val = next(ki)
            yield (kno, key, val)
    except:
        pass

def order():

    """ Načtení parametrů objednávky FVE ze souboru, který
    má tvar: <key>: <value>. Odstraní se komentáře, následují-
    cí za znakem #. Vynechají se prázdné řádky. Ostatní se
    vrací jako trojice (line-no, key, val). """
    
    with open("order", "r") as f:
        for no, line in enumerate(f):
            if "#" in line:
                token, comment = line.split("#", 1)
            else:
                token = line
            if ":" in token:
                key, val = token.split(":", 2)
                yield (no, key.strip(), val.strip())

@functools.total_ordering
class Date:

    def __init__(self, day, month, year):
        
        self.day = day
        self.month = month
        self.year = year
        
    def __hash__(self):
    
        return (self.year - 1973) * 366 + self.month * 31 + self.day
        
    def __eq__(self, other):
    
        if isinstance(other, Date):
            return self.year == other.year and self.month == other.month and self.day == other.day
        else:
            return NotImplemented
            
    def __lt__(self, other):
    
        if not isinstance(other, Date):
            return NotImplemented
        elif self.year < other.year:
            return True
        elif self.year > other.year:
            return False
        elif self.month < other.month:
            return True
        elif self.month > other.month:
            return False
        elif self.day < other.day:
            return True
        elif self.day > other.day:
            return False
        else:
            return False
    
    def __str__(self):

        return "{}.{}.{}".format(self.day, self.month, self.year)
    

def parse_date(text):
    
    patt = re.compile(
        r"""(?P<day>[1-3]?[0-9])        # den
        \.\s?                           # oddělovač
        (?P<month>(1[0-2])|([1-9]))     # měsíc
        \.\s?                           # oddělovač
        (?P<year>20[0-9]{2})            # rok
        (?P<message>.*$)
        """
        , re.X)
    m = re.search(patt, text)
    if m:
        return Date(int(m["day"]), int(m["month"]), int(m["year"])), m["message"]
    else:
        return None, None

def process_dates():
    
    """ Z dat které vrací order, vezme jen ty, které v
    klíči obsahují slovo date, v části value najde datum
    a udělá z něj integer, který se dá porovnat. """

    for no, key, val in order2_group():
        if "date" in key:
            date, message = parse_date(val)
            hr = base.HistoryRec(date, message)
            if date is None:
                print("Not a date: ")
            else:
                yield(no, key, hr)
        else:
            yield (no, key, val)

def process_history():

    history = []
    for no, key, val in process_dates():
        if key == "ch-date":
            history.append((key, val))
        elif key == "jps-date":
            val.message = "Jednopolové schéma"
            history.append((key, val))
            yield no, key, val
        elif "date" in key:
            history.append((key, val))
            yield (no, key, val)
        else:
            yield (no, key, val)
    yield (-1, "history", history)
        

def load_pv_string(prefix, order, pv):

    pv_string = pvlib.PVString(pv)
    for key, val in order.items():
        if key.startswith(prefix):
            pre, suf = key.split("-", 1)
            if suf == "nr":
                pv_string.nr = int(val)
            elif suf == "azimuth":
                pv_string.azimuth = float(val)
            elif suf == "elevation":
                pv_string.elevation = float(val)
    return pv_string
