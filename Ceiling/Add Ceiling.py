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
from System.Collections.Generic import List

# access the active document object
doc = Revit.ActiveDBDocument

def show_warning(msg):
    ghenv.Component.AddRuntimeMessage(RML.Warning, msg)

def show_error(msg):
    ghenv.Component.AddRuntimeMessage(RML.Error, msg)

def show_remark(msg):
    ghenv.Component.AddRuntimeMessage(RML.Remark, msg)

#Output list of ceilings
Ceilings = []

#Converting data tree to a list of lists-
BoundaryList = []

#Counting how many branch does the data tree have.
BranchCount = Boundary.BranchCount

#Looping data tree and appending elements to the newly created list.
for i in range(BranchCount):
    BoundaryList.append(Boundary.Branch(i))

#Making sure that Types is a list input containing the same amount of elements as BoundaryList.
Types = []

if len(Type) == 1:
    for i in range(len(BoundaryList)):
        Types.append(Type[0])

elif Boundary.BranchCount == 0:
    show_remark("This component expects a boundary.")

elif len(Type) != len(BoundaryList):
    show_warning("Boundary and Type inputs do not contain same amount of elements.")

else:
    Types = Type

with DB.Transaction(doc, "Create Ceilings") as t:
    t.Start()
        #First, loop through each branch and create a curve loop. This curveloop will be the boundary of our floor.
        #This curveloop will create the ceiling with opening.
    for b, ty in zip(BoundaryList, Types):
        CurveLoop = List[DB.CurveLoop]()
        #Then Loop through each polyline/curve and append the to the CurveLoop list.
        #Do not forget to convert them to Revit equivalents.
        for c in b:
            CurveLoop.Add(c.ToCurveLoop())
        ceiling = DB.Ceiling.Create(doc, CurveLoop, ty.Id, Level.Id)
        Ceilings.append(ceiling)
    t.Commit()
