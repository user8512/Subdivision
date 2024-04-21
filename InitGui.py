# _TEMPLATE_ gui init module
# (c) 2001 Juergen Riegel LGPL
import FreeCAD
from FreeCAD import Gui
import SubdivisionCmd

class Subdivision_Workbench(Workbench):
    MenuText = "Subdivision"
    ToolTip = "Subdivision workbench"

    def Initialize(self):
        self.appendMenu(["Subdivision Menu","Import"], ["Import_from_file", "Import_from_selection"])
        self.appendMenu(["Subdivision Menu", "Subdivision"], ["Loop_subdivision", "Catmull-Clark_subdivision", "Sqrt3_subdivision"])
        self.appendMenu("Subdivision Menu", "Show_current_mesh")
        self.appendMenu("Subdivision Menu", "Export_file")

    def GetClassName(self):
        return "Gui::PythonWorkbench"

Gui.addWorkbench(Subdivision_Workbench())
