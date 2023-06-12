# Technická zpráva má tyto kapitoly:
#
#   1. Předmět (Scope)
#   2. Zadání, výchozí podmínky (Basis)
#   3. Podklady
#   4. Řešení,
#   5. BOZP
#   6. Environment
#

scope []

environment = """
    Stavba nemá negativní vliv na životní prostředí, nezpůsobuje hluk,
    vibrace, prach nebo ne\\-bez\\-peč\\-né zplodiny. Při realizaci stavby,
    při výměně baterií, při demontáži panelů musí být dodrženy platné
    požadavky na odpadové hospodářství, tzn. s odpady musí být naloženo
    v souladu s místní obecní vyhláškou.

    Dle zákona č. 7/2005Sb. je výrobce nebo dovozce povinen odebírat
    zpět použité baterie.
"""

bozp = """
    Pracovníci provádějící práce na elektrickém zařízení budou mít
    potřebnou kvalifikaci dle nařízení vlády č. 194/2022 Sb.,
    o~požadavcích na odbornou způsobilost k výkonu činnosti na
    elektrických zařízeních a na odbornou způsobilost v elektrotechnice.

    Před uvedením do provozu bude provedena výchozí revize.

    Rozváděče: ER, HDR, FVE-R budou opatřeny varovnými tabulkami:
    \\itembull Pozor! Elektrické zařízení, nehas vodou ani pěnovými přístroji.
    \\itembull Pozor! Zpětný proud.
    \\itembull Pozor! Pod napětím i při vypnutém jističi.
"""

scope = """
    Předmětěm projektu je dodávka a instalace fotovoltaické elektrárny
    kategorie A1 dle \\cite[rfg16]. Elektrárna je určena především
    k~pokrytí vlastní spotřeby domu. Elektrárna bude připojena a~provozována
    paralelně k distribuční rozvodné síti, viz \cite[ppds22]. Celkový
    instalovaný výkon vypočtený jako součet výkonů všech panelů je:
    __NUM__(__PVE_WP__)~Wp. Instalovaný výkon použitého střídače je:
    __NUM__(__INVERT_AC_OU_NOM_P__)~W

    Elektrárna se skládá z těchto hlavních komponent:
"""

def append_scope(scope):

    scope.append(scope)

def paint(canvas):
    
    # __TOC__
    # __ABBR__
    
    canvas.start_section("Předmět")
    canvas.text(scope)
    canvas.end_section()
    
    # __BASIS__
    # __DESCRIPTION__
    
    canvas.start_section("Podklady")
    canvas.text(\usebibtex{normy}{plain})
    canvas.end_section()
    
    # __SOURCES__
    # dnl __REQUIREMENTS__
    # __SOLUTION__
    # __BOZP__
    # __ENVIRONMENT__

    # dnl __VECTOR_BEGIN__
    # dnl esyscmd(`python3 ~/macro/solar/dxf4tikz.py --row 2 ~/template/solar/D.1.4.2+0+4.dxf')
    # dnl __VECTOR_END__
                
    canvas.start_section("Bezpečnost a ochrana zdraví při práci")
    canvas.text(bozp)
    canvas.end_section()
    
    canvas.start_section("Dopad na životní prostředí")
    canvas.text(environment)
    canvas.end_section()

    pass
