#This definition checks whether if the family instance is flipped or not
# and gives the list of elements that are flipped and a Boolean list for filtering in detail.

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

Bools = []
IsMirrored = []
NotMirrored = []

Elements = Elements if isinstance(Elements, list) else [Elements]

for element in Elements:
    if element.Mirrored == True:
        Bools.append(True)
        IsMirrored.append(element)
    else:
        Bools.append(False)
        NotMirrored.append(element)
