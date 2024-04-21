import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import tkinter as tk
import numpy as np
import openmesh as om
import FreeCAD as App
from FreeCAD import Gui

def get_input():
    global window, size_var, color_var
    window = tk.Tk()
    window.geometry("%dx%d+%d+%d" % (400, 200, (window.winfo_screenwidth() - 400) / 2, (window.winfo_screenheight() - 200) / 2))
    # Size选项
    size_frame = tk.LabelFrame(window, text="请输入顶点大小（推荐20；输入0则不显示点）")
    size_frame.pack(fill="both", expand="yes")
    size_var = tk.StringVar(window)
    size_var.set("0")
    size_entry = tk.Entry(size_frame, textvariable=size_var)
    size_entry.pack()
    # Color选项
    color_frame = tk.LabelFrame(window, text="请选择面是否着色")
    color_frame.pack(fill="both", expand="yes")
    color_var = tk.StringVar(window)
    color_var.set("否")
    color_option = tk.OptionMenu(color_frame, color_var, "否", "是")
    color_option.pack()
    # Transparency选项
    transparency_frame = tk.LabelFrame(window, text="请输入面的透明度([0,1]的浮点数，0为全透明，1为不透明)")
    transparency_frame.pack(fill="both", expand="yes")
    transparency_var = tk.StringVar(window)
    transparency_var.set("1")
    transparency_entry = tk.Entry(transparency_frame, textvariable=transparency_var)
    transparency_entry.pack()
    
    button = tk.Button(window, text="确定", command=lambda:[window.destroy()])
    button.pack()
    window.mainloop()
    return int(size_var.get()) , 1 if color_var.get()=="否" else 0.5, float(transparency_var.get())



def show(mesh):
    vertices = np.array(mesh.points())
    faces = np.array([[v.idx() for v in mesh.fv(f)] for f in mesh.faces()])
    size,color,transparency = get_input()
    polys = [vertices[face] for face in faces]
    fig = plt.figure()
    ax = fig.add_subplot(111, projection = '3d')
    ax.add_collection3d(Poly3DCollection(polys, edgecolors='k', linewidths=1, facecolors = (color, color, color, transparency)))
    ax.auto_scale_xyz(vertices[:,0], vertices[:,1], vertices[:,2])
    ax.scatter(vertices[:,0], vertices[:,1], vertices[:,2], s = size, c='r')
    ax.axis('off')
    def on_scroll(event):
        scale_factor = 0.9 if event.button == 'up' else 1.1
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        zlim = ax.get_zlim()
        ax.set_xlim([x * scale_factor for x in xlim])
        ax.set_ylim([y * scale_factor for y in ylim])
        ax.set_zlim([z * scale_factor for z in zlim])
    fig.canvas.mpl_connect('scroll_event', on_scroll)
    return
