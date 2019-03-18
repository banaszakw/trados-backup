# -*- coding: utf-8 -*-

# Version: 2017-11-10 10:38

import os
import shutil
import sys
import traceback


def check_input():
    if os.path.isfile(input_filepath):
        return False
    else:
        print(errmsg['input'])
        return True


def isdir_pso():
    if os.path.isdir(dirpath_pso):
        print(errmsg['is_pso'])
        return True
    else:
        return False


def isfile_01():
    if os.path.isfile(filepath_01):
        print(errmsg['in_01'])
        return True
    else:
        return False


def isfile_02():
    if os.path.isfile(filepath_02):
        print(errmsg['in_02'])
        return True
    else:
        return False


def get_excep_caller(tb):
    stk = traceback.extract_tb(tb, 1)
    return stk[0][3]


def main():
    precheck = [check_input(), isdir_pso(), isfile_01(), isfile_02()]
    if any(precheck):
        input(errmsg['final'])
    else:
        try:
            os.makedirs(path_01)
            os.makedirs(path_02)
            shutil.copy2(input_filepath, filepath_01)
        except (OSError, FileNotFoundError):
            tb = sys.exc_info()[-1]
            fname = get_excep_caller(tb)
            print(errmsg[fname])
            if os.path.isdir(dirpath_pso):
                try:
                    shutil.rmtree(dirpath_pso)
                except (OSError, FileNotFoundError):
                    print(errmsg['shutil.rmtree(dirpath_pso)'])
            input(errmsg['final'])


if __name__ == "__main__":
    input_filepath = str(sys.argv[1])
    input_path, input_file = os.path.split(input_filepath)

    path_01 = os.path.join(input_path, "_PSO", "backup.sdlproj", "01")
    path_02 = os.path.join(input_path, "_PSO", "backup.sdlproj", "02")

    dirpath_pso = os.path.join(input_path, "_PSO")

    filepath_01 = os.path.join(path_01, input_file)
    filepath_02 = os.path.join(path_02, input_file)

    errmsg = {
        'input':  r"Problem z plikiem wejsciowym",
        'in_01':  r"W \01 juz jest plik",
        'in_02':  r"W \02 juz jest plik",
        'is_pso': r"Katalog \_PSO juz istnieje",
        'os.makedirs(path_01)': r"Nie udalo sie utworzyc katalogow w \_PSO",
        'os.makedirs(path_02)': r"Nie udalo sie utworzyc katalogow w \_PSO",
        'shutil.copy2(input_filepath, filepath_01)':
            r"Nie skopiowano pliku z glownego katalogu do \01",
        'shutil.rmtree(dirpath_pso)': r"Nie udalo sie usunac katalogow",
        'final':  r"Niepowodzenie. Nacisnij <Enter>, zeby zakonczyc..."
    }
    main()
