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

CeilingPlans = []
ViewFamilyType = []

Levels = Levels if isinstance(Levels, list) else [Levels]

ViewTypes = DB.FilteredElementCollector(doc).OfClass(DB.ViewFamilyType).ToElements()
for viewtype in ViewTypes:
    if viewtype.ViewFamily == DB.ViewFamily.CeilingPlan:
        ViewFamilyType.append(viewtype)



with DB.Transaction(doc, "Create Ceiling Plans by Level") as t:
    t.Start()
    
    for l in Levels:
        c = DB.ViewPlan.Create(doc, ViewFamilyType[0].Id, l.Id)
        CeilingPlans.append(c)
    t.Commit()
