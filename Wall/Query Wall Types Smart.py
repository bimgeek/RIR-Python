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

WallTypeCollector = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Walls).WhereElementIsElementType().ToElements()
WallTypes = []

if WallSystemFamily == 0:
    for wall in WallTypeCollector:
        if wall.Kind == DB.WallKind.Basic:
            WallTypes.append(wall)

elif WallSystemFamily == 1:
    for wall in WallTypeCollector:
        if wall.Kind == DB.WallKind.Curtain:
            WallTypes.append(wall)

elif WallSystemFamily == 2:
    for wall in WallTypeCollector:
        WallTypes = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_StackedWalls).WhereElementIsElementType().ToElements()

else:
    WallTypes = WallTypeCollector
