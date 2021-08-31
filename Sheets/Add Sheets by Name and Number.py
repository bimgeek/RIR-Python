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

Sheets = []

with DB.Transaction(doc, "<Create Sheets>") as t:
    t.Start()
    if SheetNames and SheetNumbers:
        try:
            for i in range(len(SheetNames)):
                sheet = DB.ViewSheet.Create(doc, TitleBlock.Id)
                sheet.Name = SheetNames[i]
                sheet.SheetNumber = SheetNumbers[i]
                Sheets.append(sheet)
            t.Commit()
        except Exception as txn_err:
            show_error(str(txn_err))
            t.RollBack()
    else:
        Sheets.append("Lütfen tüm inputları bağlayınız.")
