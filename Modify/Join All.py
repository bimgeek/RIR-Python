# This definition joins all elements with each other.(Even not intersecting elements.)
#Since it is really heavy in terms of performance, not recommended to be used in large models.
#This definition takes two lists of geometry. Joins corresponding elements with each other.
#This definition works best when used with Intersects Element/Brep Filter.

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

EL01 = EL01 if isinstance(EL01, list) else [EL01]
EL02 = EL02 if isinstance(EL02, list) else [EL02]

if EL01 and EL02:
    with DB.Transaction(doc, "Join Two Sets of Geometry") as t:
        t.Start()
        try:
            for el01 in EL01:
                for el02 in EL02:
                    DB.JoinGeometryUtils.JoinGeometry(doc, el01, el02)
            t.Commit()
        except Exception as txn_err:
            # if any errors happen while changing the document, an exception is thrown
            # make sure to print the exception message for debugging
            show_error(str(txn_err))
            # and rollback the changes made before error
            t.RollBack()

