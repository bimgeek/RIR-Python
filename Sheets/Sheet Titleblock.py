#This definition will grab the titleblock from the given sheet.

import clr
clr.AddReference('System.Core')
clr.AddReference('RhinoInside.Revit')
clr.AddReference('RevitAPI') 
clr.AddReference('RevitAPIUI')

from System import Enum

import rhinoscriptsyntax as rs
import Rhino
import RhinoInside
import Grasshopper
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML
from RhinoInside.Revit import Revit, Convert
from Autodesk.Revit import DB

# access the active document object
doc = Revit.ActiveDBDocument

def show_warning(msg):
    ghenv.Component.AddRuntimeMessage(RML.Warning, msg)

def show_error(msg):
    ghenv.Component.AddRuntimeMessage(RML.Error, msg)

def show_remark(msg):
    ghenv.Component.AddRuntimeMessage(RML.Remark, msg)

Sheet = Sheet if isinstance(Sheet, list) else [Sheet]

TitleBlock = []

for sheet in Sheet:
    if isinstance(sheet, DB.ViewSheet):
        titleblock = DB.FilteredElementCollector(doc, sheet.Id).OfCategory(DB.BuiltInCategory.OST_TitleBlocks).ToElements()[0]
        TitleBlock.append(titleblock)
