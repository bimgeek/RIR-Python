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

from System.Collections.Generic import List

# access the active document object
doc = Revit.ActiveDBDocument

# a few utility methods
def show_warning(msg):
    ghenv.Component.AddRuntimeMessage(RML.Warning, msg)

def show_error(msg):
    ghenv.Component.AddRuntimeMessage(RML.Error, msg)

def show_remark(msg):
    ghenv.Component.AddRuntimeMessage(RML.Remark, msg)

#import treehelp library when working with DataTrees.
import ghpythonlib.treehelpers as th

#This is for converting single items to list so we can loop through it.
#IN = IN if isinstance(IN, list) else [list]

# write your code here
"""
with DB.Transaction(doc, "Give it a descriptive name") as t:
    t.Start()
    try:
        
        t.Commit()
    except Exception as txn_err:
        show_error(str(txn_err))
        t.RollBack()
"""

#Output list of ceilings.
Ceilings = []

#Ceiling Types as a List
Types = []

#Room Boundary count (just in case when we want to apply a single type to all rooms.)
BoundaryBranchCount = Boundary.BranchCount

#Converting data trees to nested lists.
Boundary = th.tree_to_list(Boundary)
Type = th.tree_to_list(Type)

#Making sure length of Type and Boundary inputs are same.
if len(Type) == 1:
    for i in range(BoundaryBranchCount):
        Types.append(Type)
elif BoundaryBranchCount == 0:
    show_warning("This component expects a boundary.")
elif len(Type) != len(Boundary):
    show_warning("Boundary and Type inputs do not contain same amount of elements.")
else:
    Types = Type

with DB.Transaction(doc, "Create Ceilings") as t:
    t.Start()
    try:
        for b, ty in zip(Boundary, Types):
            CurveLoop = List[DB.CurveLoop]()
        #Then Loop through each polyline/curve and append the to the CurveLoop list.
        #Do not forget to convert them to Revit equivalents.
            for c in b:
                CurveLoop.Add(c.ToCurveLoop())
            ceiling = DB.Ceiling.Create(doc, CurveLoop, ty.Id, Level.Id)
            Ceilings.append(ceiling)
        t.Commit()
    except Exception as txn_err:
        show_error(str(txn_err))
        t.RollBack()
