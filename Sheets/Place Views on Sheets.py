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

clr.ImportExtensions(RhinoInside.Revit.Convert.Geometry)

# access the active document object
doc = Revit.ActiveDBDocument

def show_warning(msg):
    ghenv.Component.AddRuntimeMessage(RML.Warning, msg)

def show_error(msg):
    ghenv.Component.AddRuntimeMessage(RML.Error, msg)

def show_remark(msg):
    ghenv.Component.AddRuntimeMessage(RML.Remark, msg)

Viewports = []

if len(Views) == 1:
    Views = [Views]
if len(Sheets) == 1:
    Sheets = [Sheets]

show_remark("Please make sure that Views and Sheets list have the same length.")

with DB.Transaction(doc, "Place Views on Sheets") as t:
    t.Start()
    for v, s in zip(Views, Sheets):
        check = DB.Viewport.CanAddViewToSheet(doc, s.Id, v.Id)
        if check:
            viewport = DB.Viewport.Create(doc, s.Id, v.Id, Point.ToXYZ())
            Viewports.append(viewport)
        else:
            Viewports.append(None)
    t.Commit()
