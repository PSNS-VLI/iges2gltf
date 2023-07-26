# -*- coding: utf-8 -*-
import sys
import os
from cadquery import assembly, Assembly, importers


class FileType:
    COULD_TYPES = ('gltf', 'step', 'obj_alias_mesh', 'obj_wavefront', 'stl', 'dae')
    for _type in COULD_TYPES:
        exec(f'{_type.upper()} = "{_type}"')

    @staticmethod
    def change_extension(file_path, new_extension, prefix=''):
        file_name, old_extension = os.path.splitext(file_path)
        if prefix:
            file_name = file_name + '_' + str(prefix)
        new_file_name = file_name + new_extension
        new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)

        return new_file_path


class Param:
    CAD_PATH = 'cad_path'
    MODEL_PATH = 'model_path'
    OUTPUT_TYPE = 'output_type'

    REQUIRED_PARAMS = (CAD_PATH, MODEL_PATH, OUTPUT_TYPE)


def import_freecad(cad_bin_path):
    for _path in [cad_bin_path, os.path.join(cad_bin_path, r'Lib\site-packages')]:
        sys.path.append(_path)
    try:
        import FreeCAD as App
        import Part
        import Mesh
        import importOBJ
        import importDAE
        globals()['App'] = App
        globals()['Part'] = Part
        globals()['Mesh'] = Mesh
        globals()['importOBJ'] = importOBJ
        globals()['importDAE'] = importDAE
    except ImportError as e:
        print(f'CADPathError: CAD bin 文件夹路径错误!({e})')
        sys.exit()
    except Exception as e:
        print(f'UndefinedError: 未知错误({e})')
        sys.exit()
    print('MODULE IMPORTED SUCCESS')

def main():
    input_types = ('.igs', '.iges')
    output_types = FileType.COULD_TYPES
    required_params = Param.REQUIRED_PARAMS
    params = {}

    for arg in sys.argv[1:]:
        print(arg)
        k, v = arg.split('=')
        params[k] = v

    for param in required_params:
        if not params.get(param):
            print(f'KeyError: 缺少必要参数{param}')
            sys.exit()

    import_freecad(params.get(Param.CAD_PATH))
    try:
        model_path = params.get(Param.MODEL_PATH)
        output_type = params.get(Param.OUTPUT_TYPE)

        document_name = 'model'
        Part.insert(model_path, document_name)
        new_model_path = FileType.change_extension(model_path, f'.{output_type}')
        __objs__ = []
        for obj in App.ActiveDocument.Objects:
            __objs__.append(App.getDocument(document_name).getObject(obj.Name))
        if output_type == FileType.DAE:
            importDAE.export(__objs__, new_model_path)
        elif output_type == FileType.OBJ_ALIAS_MESH:
            new_model_path = FileType.change_extension(new_model_path, '.obj', prefix='mesh')
            Mesh.export(__objs__, new_model_path)
        elif output_type == FileType.OBJ_WAVEFRONT:
            new_model_path = FileType.change_extension(new_model_path, '.obj', prefix='wave')
            importOBJ.export(__objs__, new_model_path)
        elif output_type == FileType.STL:
            Mesh.export(__objs__, new_model_path)
        elif output_type == FileType.STEP:
            Part.export(__objs__, new_model_path)
        elif output_type == FileType.GLTF:
            tmp_path = FileType.change_extension(new_model_path, '.step')
            Part.export(__objs__, tmp_path)
            assembly.exportGLTF(assy=Assembly(importers.importStep(tmp_path)),
                                path=new_model_path)
        else:
            print(f'TypeError: 未知的转换类型{output_type}')
            sys.exit()

        print('CONVERT SUCCESS!')
        return new_model_path
    except Exception as e:
        print(f'ProgramError: 未知的主程序异常({e})')
        sys.exit()


if __name__ == '__main__':
    main()
