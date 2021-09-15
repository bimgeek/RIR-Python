__author__ = "mbgoker"
__version__ = "2021.09.09"

import clr
clr.AddReference('System.Core')
clr.AddReference('RhinoInside.Revit')
clr.AddReference('RevitAPI') 
clr.AddReference('RevitAPIUI')

from System import Enum, Action

import rhinoscriptsyntax as rs
import Rhino
import RhinoInside
import Grasshopper
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML
from RhinoInside.Revit import Revit, Convert
# add extensions methods as well
# this allows calling .ToXXX() convertor methods on Revit objects
clr.ImportExtensions(Convert.Geometry)
from Autodesk.Revit import DB
from Rhino.Geometry import Point2d

# access the active document object
doc = Revit.ActiveDBDocument

# a few utility methods
def show_warning(msg):
    ghenv.Component.AddRuntimeMessage(RML.Warning, msg)

def show_error(msg):
    ghenv.Component.AddRuntimeMessage(RML.Error, msg)

def show_remark(msg):
    ghenv.Component.AddRuntimeMessage(RML.Remark, msg)

#This is for converting single items to list so we can loop through it.
Point = Point if isinstance(Point, list) else [Point]
Room = []

with DB.Transaction(doc, "Add Rooms by Point and Level") as t:
    t.Start()
    try:
        for point in Point:
            room = doc.Create.NewRoom(Level, Point2d(point).ToUV())
            Room.append(room)
        t.Commit()
    except Exception as txn_err:
        show_error(str(txn_err))
        t.RollBack()
