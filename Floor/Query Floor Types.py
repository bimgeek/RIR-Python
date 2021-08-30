import clr
clr.AddReference('RhinoInside.Revit')
clr.AddReference('RevitAPI') 

from RhinoInside.Revit import Revit
from Autodesk.Revit import DB

# access the active document object
doc = Revit.ActiveDBDocument

def show_warning(msg):
    ghenv.Component.AddRuntimeMessage(RML.Warning, msg)

def show_error(msg):
    ghenv.Component.AddRuntimeMessage(RML.Error, msg)

def show_remark(msg):
    ghenv.Component.AddRuntimeMessage(RML.Remark, msg)

#Query Ceiling Types
FloorTypes = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Floors).WhereElementIsElementType().ToElements()
