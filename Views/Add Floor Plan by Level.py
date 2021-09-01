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

Level = Level if isinstance(Level, list) else [Level]
View = []

ViewFamilyTypes = DB.FilteredElementCollector(doc).OfClass(DB.ViewFamilyType).ToElements()
FloorPlanType = []
for vft in ViewFamilyTypes:
    if vft.ViewFamily == DB.ViewFamily.FloorPlan:
        FloorPlanType.append(vft)

with DB.Transaction(doc, "Add Floor Plans by Level") as t:
    t.Start()
    for l in Level:
        v = DB.ViewPlan.Create(doc, FloorPlanType[0].Id, l.Id)
        View.append(v)
    t.Commit()
