# -*- coding: utf-8 -*-
import os
import sys
__cad_path__ = 'D:\\Program Files\\FreeCAD 0.20\\bin'
sys.path.append(__cad_path__)
from cadquery import assembly, Assembly, importers


def change_extension(file_path, new_extension):
    file_name, old_extension = os.path.splitext(file_path)
    new_file_name = file_name + new_extension
    new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)

    return new_file_path


def main():
    file_path = r'D:\Projects\PythonProjects\igs2stl\assets\_lately(1).step'
    assembly.exportGLTF(assy=Assembly(importers.importStep(file_path)), path=change_extension(file_path, '.gltf'))


if __name__ == '__main__':
    main()
