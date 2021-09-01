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

if EL01 and EL02:
    with DB.Transaction(doc, "Join Two Sets of Geometry") as t:
        t.Start()
        try:
            for el01, el02 in zip(EL01, EL02):
                DB.JoinGeometryUtils.JoinGeometry(doc, el01, el02)
            t.Commit()
        except Exception as txn_err:
            # if any errors happen while changing the document, an exception is thrown
            # make sure to print the exception message for debugging
            show_error(str(txn_err))
            # and rollback the changes made before error
            t.RollBack()
