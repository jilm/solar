
from . import tools
from . import batery
from . import base
from . import load
from . import fve
from . import tex
from . import pv
from . import dxf4tikz
from . import checklist
from .project import schemas
from jinja2 import Environment, PackageLoader, select_autoescape, BaseLoader
import re

def make_title(document):

    env = Environment(

        loader=PackageLoader(
            package_name="solar",
            package_path="template"
        ),
        autoescape=select_autoescape()
    )

    template = env.get_template("TextTitle.tex.jinja")
    print(template.render(document=document))

def load_project():

    """ Načte objednávku ze souboru order v aktuálním adresáři,
    zpracuje je ji do objektu project a vrátí ho. """
    
    order_proc2 = load.process_history()
    project = load.Project(iter(order_proc2))
    return project
    
def component_list(project):

    """ Na základě načteného projektu sestaví a vrátí seznam
    komponent. """
    
    components = [
    
    ]
    
def meta(project, schema_name="-"):

    """ Sestaví metadata pro daný project a vrací ho. """
    
    env = Environment(

        loader=PackageLoader(
            package_name="solar",
            package_path="template"
        ),
        autoescape=select_autoescape()
    )

    meta_temp = env.get_template("meta.tex.jinja")
    output = meta_temp.render(project=project, schema_name=schema_name)
    return output

def schema_legend(legend):

    template = tools.get_template("legend.tex.jinja")
    output = template.render(legend=legend)
    return output

def head():
    
    env = Environment(

        loader=PackageLoader(
            package_name="solar",
            package_path="template"
        ),
        autoescape=select_autoescape()
    )

    temp = env.get_template("head.tex.jinja")
    return temp.render()

def tz_content(project):

    env = Environment(

        loader=PackageLoader(
            package_name="solar",
            package_path="template"
        ),
        autoescape=select_autoescape()
    )
    canvas = pv.Canvas()
    pv.paint_param_table(project.pv, canvas)
    project.pv["param-table"] = canvas.result

    tz_temp = env.get_template("tz.tex.jinja")
    if project.bat:
        tz_batery = batery.tz(project.bat_type)
    else:
        tz_batery = ""
    output = tz_temp.render(project=project, tz_batery = tz_batery)
    
    return output
    
def tz():

    project = load_project()
    content = tz_content(project)
    doc_meta = meta(project, schema_name="")
    sch = ""
    for i, s in enumerate(schemas):
        if s.predicate(project):
            sch += schema(s, project, i)
    
    env = Environment(

        loader=PackageLoader(
            package_name="solar",
            package_path="template"
        ),
        autoescape=select_autoescape()
    )
    temp = env.get_template("tex.jinja")
    output = temp.render(content = content, schemas = sch, meta = doc_meta)
    print(output)

def make_attributes(attributes, labels):

    return [ (labels[key][2], attributes[key], labels[key][1]) for key in attributes ]

def project():

    """ Makro, které sestaví projektovou dokumentaci."""
    
    order_raw = solar.load.order()
    order = base.Order(order_raw)
    for q in order.get_requirements():
        print(q)
    
def params_table(comp):

    for val, key in comp.get_params():
        if key in tex.param_meta:
            desc_en, unit, form, desc_cz = tex.param_meta[key]
        else:
            desc_en, unit, form, desc_cz = fve.param_meta[key]
        yield tex.form_table_row((val, desc_en, unit, form, desc_cz))

def schema(schema, project, page_no):
    
    """ Vytvoří a vrátí schema """

    result = schema_legend(schema.get_legend(project))
    for l in schema.layers:
        if l.predicate(project):
            result += dxf4tikz.make_layer(l)
    template = tools.get_template("schema.tex.jinja")
    output = template.render(content = result, title = schema.title, project = project, page_no = page_no)
    return output

def jps():

    """ Vytvoří a vrátí jednopolové schéma. """
    
    project = load_project()
    doc_meta = meta(project, schema_name="Jednopolové schéma")
    doc_head = head()
    doc_tail = "\\bye"
    sch = schemas[0]
    print(doc_meta + doc_head + schema(sch, project, 1) + doc_tail)
    
def check():

    project = load_project()
    template = tools.get_template("checklist.tex.jinja")
    naradi = set([t for step in checklist.lib for t in step.tools])
    material = set([m for step in checklist.lib for m in step.material])
    output = template.render(lib = checklist.lib, tools = naradi)
    print(output)
