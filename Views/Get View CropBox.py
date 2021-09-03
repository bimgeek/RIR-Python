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

View = View if isinstance(View, list) else [View]

CropBoxCurve = []
Active = []
Visible = []

for v in View:
    Active.append(v.CropBoxActive)
    Visible.append(v.CropBoxVisible)
    crop = v.GetCropRegionShapeManager().GetCropShape()
    if len(crop)>0:
        CropBoxCurve.append(crop[0].ToCurve())
    else:
        CropBoxCurve.append(None)
