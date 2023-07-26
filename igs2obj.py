# -*- coding: utf-8 -*-
import sys
import os

__cad_paths__ = [
    r'D:\Program Files\FreeCAD 0.20\bin',
    r'D:\Program Files\FreeCAD 0.20\bin\Lib\site-packages'
]
for __cad_path__ in __cad_paths__:
    sys.path.append(__cad_path__)

import FreeCAD as App
import Part
import importOBJ
from tkinter import filedialog


def main():
    folder = filedialog.askdirectory()
    # first we check for filenames that contain .stp, .step, .igs or .iges
    cadfiles = []
    for f in os.listdir(folder):
        for ext in [".igs", ".iges"]:
            if f.lower().endswith(ext):
                cadfiles.append((folder + os.sep + f, ext))
                break

    if not cadfiles:
        print("No step or iges files found in the given folder")
        sys.exit()

    for f, ext in cadfiles:
        Part.insert(f, 'model')
        new_file = change_extension(f, '.obj')
        objs = []
        for obj in App.ActiveDocument.Objects:
            objs.append(App.getDocument('model').getObject(obj.Name))
        importOBJ.export(objs, new_file)
    print("finished")


def change_extension(file_path, new_extension):
    file_name, old_extension = os.path.splitext(file_path)
    new_file_name = file_name + new_extension
    new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)

    return new_file_path


if __name__ == '__main__':
    main()
