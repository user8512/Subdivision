import Loop
import Catmull_Clark
import sqrt3
import ShowMesh
import tkinter as tk
from tkinter import filedialog
import openmesh as om
import FreeCAD as App
from FreeCAD import Gui
import Mesh
import os
from datetime import datetime

current_mesh = None

class ImportFileCommandClass:
    
    def GetResources(self):
        return {
            "MenuText": App.Qt.translate("Import_from_file", "Import from file.."),
            "ToolTip": App.Qt.translate("Import_from_file", "Import a mesh from a file\n")
        }
    
    def Activated(self):
        global current_mesh
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(title = "请选择输入文件")
        root.destroy()
        current_mesh = om.read_polymesh(file_path)
        return

    def IsActive(self):
        return True
    
class ImportSelectionCommandClass:
    
    def GetResources(self):
        return {
            "MenuText": App.Qt.translate("Import_from_selection", "Import from selection"),
            "ToolTip": App.Qt.translate("Import_from_selection", "Import selected mesh\n")
        }
    
    def Activated(self):
        global current_mesh
        mesh = Gui.Selection.getSelection()
        Mesh.export(mesh, r'./temp.off')
        current_mesh = om.read_polymesh(r'./temp.off')
        os.remove(r'./temp.off')
        return

    def IsActive(self):
        if len(Gui.Selection.getSelection()) != 1:
            return False
        obj = Gui.Selection.getSelection()[0]
        if not (obj.isDerivedFrom("Mesh::Feature")):
            return False
        return True


class ShowCurrentMeshCommandClass:
    
    def GetResources(self):
        return {
            "MenuText": App.Qt.translate("Show_current_mesh", "Show current mesh"),
            "ToolTip": App.Qt.translate("Show_current_mesh", "Show current mesh in a matplotlib window\n")
        }
    
    def Activated(self):
        ShowMesh.show(current_mesh)
        return

    def IsActive(self):
        if current_mesh != None:
            return True
        else:
            return False
        
class ExportMeshCommandClass:
    
    def GetResources(self):
        return {
            "MenuText": App.Qt.translate("Export_file", "Export mesh.."),
            "ToolTip": App.Qt.translate("Export_file", "Export current mesh to path\n")
        }
    
    def Activated(self):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.asksaveasfile(title="请选择输出文件路径", filetypes=[('All Files' , '*')], defaultextension='.obj')
        om.write_mesh(file_path.name, current_mesh)
        return

    def IsActive(self):
        if current_mesh != None:
            return True
        else:
            return False

class LoopSubdivisionCommandClass:
    
    def GetResources(self):
        return {
            "MenuText": App.Qt.translate("Loop_subdivision", "Loop subdivision"),
            "ToolTip": App.Qt.translate("Loop_subdivision", "Create a subdivided mesh from a mesh\n")
        }
    
    def Activated(self):
        global current_mesh
        om.write_mesh(r'./temp.off', current_mesh)
        current_mesh = om.read_trimesh(r'./temp.off')
        start_time = datetime.now()
        current_mesh = Loop.mesh_subdivision(current_mesh)
        end_time = datetime.now()
        print("Loop细分完成，用时: ", end_time - start_time)
        os.remove(r'./temp.off')
        return

    def IsActive(self):
        if current_mesh != None:
            return True
        else:
            return False
    
class CatmullClarkSubdivisionCommandClass:
    
    def GetResources(self):
        return {
            "MenuText": App.Qt.translate("Catmull-Clark_subdivision", "Catmull-Clark subdivision"),
            "ToolTip": App.Qt.translate("Catmull-Clark_subdivision", "Create a subdivided mesh from a mesh\n")
        }
    
    def Activated(self):
        global current_mesh
        start_time = datetime.now()
        current_mesh = Catmull_Clark.mesh_subdivision(current_mesh)  
        end_time = datetime.now()
        print("Catmull-Clark细分完成，用时: ", end_time - start_time)
        return

    def IsActive(self):
        if current_mesh != None:
            return True
        else:
            return False
    
class Sqrt3SubdivisionCommandClass:
    
    def GetResources(self):
        return {
            "MenuText": App.Qt.translate("Sqrt3_subdivision", "Sqrt3 subdivision"),
            "ToolTip": App.Qt.translate("Sqrt3_subdivision", "Create a subdivided mesh from a mesh\n")
        }
    
    def Activated(self):
        global current_mesh
        om.write_mesh(r'./temp.off', current_mesh)
        current_mesh = om.read_trimesh(r'./temp.off')
        start_time = datetime.now()
        current_mesh = sqrt3.mesh_subdivision(current_mesh)
        end_time = datetime.now()
        print("√3细分完成，用时: ", end_time - start_time)
        os.remove(r'./temp.off')
        return

    def IsActive(self):
        if current_mesh != None:
            return True
        else:
            return False
        
Gui.addCommand("Import_from_file", ImportFileCommandClass())
Gui.addCommand("Import_from_selection", ImportSelectionCommandClass())
Gui.addCommand("Loop_subdivision", LoopSubdivisionCommandClass())
Gui.addCommand("Catmull-Clark_subdivision", CatmullClarkSubdivisionCommandClass())
Gui.addCommand("Sqrt3_subdivision", Sqrt3SubdivisionCommandClass())
Gui.addCommand("Show_current_mesh", ShowCurrentMeshCommandClass())
Gui.addCommand("Export_file", ExportMeshCommandClass())