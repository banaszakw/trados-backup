# -*- coding: utf-8 -*-

# Version: 2017-11-10 13:42

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
        return False
    else:
        print(errmsg['is_pso'])
        return True


def ispath_02():
    if os.path.isdir(path_02):
        return False
    else:
        print(errmsg['is_dir_02'])
        return True


def isfile_01():
    if os.path.isfile(filepath_01):
        return False
    else:
        print(errmsg['in_01'])
        return True


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
    precheck = [check_input(), isdir_pso(), ispath_02(), isfile_01(), isfile_02()]
    if any(precheck):
        input(errmsg['final'])
    else:
        try:
            shutil.move(input_filepath, filepath_02)
            print("Uruchamiam copy()")
            shutil.copy2(filepath_01, input_path)
        except (OSError, FileNotFoundError):
            tb = sys.exc_info()[-1]
            fname = get_excep_caller(tb)
            print(errmsg[fname])
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
        'input':     r"Problem z plikiem wejsciowym",
        'in_01':     r"W \01 nie ma pliku",
        'in_02':     r"W \02 juz jest plik",
        'is_pso':    r"Nie ma katalogu \_PSO",
        'is_dir_02': r"Nie ma katalogu \02",
        'shutil.copy2(filepath_01, input_path)':
            r"Nie skopiowano pliku z \01 do glownego katalogu",
        'shutil.move(input_filepath, filepath_02)':
            r"Nie przeniesiono pliku z głownego katalogu do \02",
        'final':
            r"Niepowodzenie!" + "\n" + "Nacisnij <Enter>, zeby zakonczyc..."
    }
    main()
