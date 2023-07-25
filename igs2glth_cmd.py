# -*- coding: utf-8 -*-
import sys, os
__cad_path__ = 'D:\\Program Files\\FreeCAD 0.20\\bin'
__env__ = os.environ.copy()

__path__ = __env__ .get("PATH", "")
__path__ = __cad_path__ + os.pathsep + __path__
__env__ ["PATH"] = __path__

os.environ.update(__env__)

import subprocess
from tkinter import filedialog

def main():
    folder=filedialog.askdirectory()
    cadfiles = []
    for f in os.listdir(folder):
        for ext in [".igs", ".iges"]:
            if f.lower().endswith(ext):
                cadfiles.append((folder+os.sep+f,ext))
                break

    if not cadfiles:
        print ("No step or iges files found in the given folder")
        sys.exit()

    for f, ext in cadfiles:
        stl = change_extension(f, '.gltf')
        print(f'正在处理{f}-->{stl}')
        command = f'FreeCADCmd -h'
        subprocess.call(command, shell=True)
    print("finished")

def change_extension(file_path, new_extension):
    file_name, old_extension = os.path.splitext(file_path)
    new_file_name = file_name + new_extension
    new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)
    
    return new_file_path

main()
