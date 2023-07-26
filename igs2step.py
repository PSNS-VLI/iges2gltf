# -*- coding: utf-8 -*-
import sys, os
__cad_path__ = 'D:\\Program Files\\FreeCAD 0.20\\bin'
sys.path.append(__cad_path__)

import FreeCAD as App
import Part
from tkinter import filedialog

def main():
    folder=filedialog.askdirectory()
    # first we check for filenames that contain .stp, .step, .igs or .iges
    cadfiles = []
    for f in os.listdir(folder):
        for ext in [".stp", ".step", ".igs", ".iges"]:
            if f.lower().endswith(ext):
                cadfiles.append((folder+os.sep+f,ext))
                break

    if not cadfiles:
        print ("No step or iges files found in the given folder")
        sys.exit()

    for f, ext in cadfiles:
        s = Part.insert(f, 'model')
        stl = change_extension(f, '.step')
        objs = []
        for obj in App.ActiveDocument.Objects:
            objs.append(App.getDocument('model').getObject(obj.Name))
        Part.export(objs, stl)
    print("finished")

def change_extension(file_path, new_extension):
    file_name, old_extension = os.path.splitext(file_path)
    new_file_name = file_name + new_extension
    new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)
    
    return new_file_path

main()
