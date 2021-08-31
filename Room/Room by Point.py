import clr
clr.AddReference('RhinoInside.Revit')
clr.AddReference('RevitAPI') 

from System import Enum

import RhinoInside
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML
from RhinoInside.Revit import Revit
from Autodesk.Revit import DB

clr.ImportExtensions(RhinoInside.Revit.Convert.Geometry)
from Rhino.Geometry import Point2d

# access the active document object
doc = Revit.ActiveDBDocument

def show_warning(msg):
    ghenv.Component.AddRuntimeMessage(RML.Warning, msg)

def show_error(msg):
    ghenv.Component.AddRuntimeMessage(RML.Error, msg)

def show_remark(msg):
    ghenv.Component.AddRuntimeMessage(RML.Remark, msg)

Rooms = []

if len(Points) == 1:
    Points = [Points]

with DB.Transaction(doc, "Create Rooms by Points") as t:
    t.Start()
    try:
        for point in Points:
            room = doc.Create.NewRoom(Level, Point2d(point).ToUV())
            Rooms.append(room)
        t.Commit()
    except Exception as txn_err:
        show_error(str(txn_err))
        t.RollBack()
