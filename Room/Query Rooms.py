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

Names, Numbers, WallFinishes, FloorFinishes, CeilingFinishes = [], [], [], [], []

Rooms = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Rooms).WhereElementIsNotElementType().ToElements()

for room in Rooms:
    room_name = room.LookupParameter("Name").AsValueString()
    room_number = room.LookupParameter("Number").AsValueString()
    room_wfinish = room.LookupParameter("Wall Finish").AsValueString()
    room_ffinish = room.LookupParameter("Floor Finish").AsValueString()
    room_cfinish = room.LookupParameter("Ceiling Finish").AsValueString()
    Names.append(room_name)
    Numbers.append(room_number)
    WallFinishes.append(room_wfinish)
    FloorFinishes.append(room_ffinish)
    CeilingFinishes.append(room_cfinish)
