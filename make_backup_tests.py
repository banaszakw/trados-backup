#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import make_backup
import io
import sys
import unittest.mock


class TestMakeBackup(unittest.TestCase):

    def setUp(self):
        s = r"Ala-ma-kota"
        make_backup.input_filepath = s
        make_backup.filepath_01 = s
        make_backup.filepath_02 = s
        make_backup.dirpath_pso = s
        make_backup.errmsg = {
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

    @unittest.mock.patch("sys.stdout", new_callable=io.StringIO)
    @unittest.mock.patch("os.path.isfile")
    def test_check_input(self, mock_isfile, mock_print):
        mock_isfile.return_value = True
        self.assertFalse(make_backup.check_input())
        mock_isfile.return_value = False
        self.assertTrue(make_backup.check_input())
        self.assertEqual(mock_print.getvalue(), make_backup.errmsg['input'] + '\n')

    @unittest.mock.patch("sys.stdout", new_callable=io.StringIO)
    @unittest.mock.patch("os.path.isfile")
    def test_check_isfile_01(self, mock_isfile, mock_print):
        mock_isfile.return_value = True
        self.assertTrue(make_backup.isfile_01())
        mock_isfile.return_value = False
        self.assertFalse(make_backup.isfile_01())
        self.assertEqual(mock_print.getvalue(), make_backup.errmsg['in_01'] + '\n')

    @unittest.mock.patch("sys.stdout", new_callable=io.StringIO)
    @unittest.mock.patch("os.path.isfile")
    def test_check_isfile_02(self, mock_isfile, mock_print):
        mock_isfile.return_value = True
        self.assertTrue(make_backup.isfile_02())
        mock_isfile.return_value = False
        self.assertFalse(make_backup.isfile_02())
        self.assertEqual(mock_print.getvalue(), make_backup.errmsg['in_02'] + '\n')

    @unittest.mock.patch("sys.stdout", new_callable=io.StringIO)
    @unittest.mock.patch("os.path.isdir")
    def test_isdir_pso(self, mock_isdir, mock_print):
        mock_isdir.return_value = True
        self.assertTrue(make_backup.isdir_pso())
        mock_isdir.return_value = False
        self.assertFalse(make_backup.isdir_pso())
        self.assertEqual(mock_print.getvalue(), make_backup.errmsg['is_pso'] + '\n')

    # def fake_copy2_tb(self):
    #     try:
    #         # shutil.copy2(input_filepath, filepath_01)
    #         print(mock_copy2.side_effect)
    #     except:
    #         return sys.exc_info()[-1]

    @unittest.mock.patch("shutil.copy2")
    @unittest.mock.patch("os.makedirs")
    @unittest.mock.patch("os.path.isdir")
    @unittest.mock.patch("shutil.rmtree")
    @unittest.mock.patch("sys.stdout", new_callable=io.StringIO)
    @unittest.mock.patch("builtins.input", return_value="y")  # wycisza input()
    @unittest.mock.patch.multiple("make_backup",
                                  check_input=unittest.mock.DEFAULT,
                                  isfile_01=unittest.mock.DEFAULT,
                                  isfile_02=unittest.mock.DEFAULT,
                                  isdir_pso=unittest.mock.DEFAULT)
    def test_main(self,
                  mock_input,
                  mock_stdout,
                  mock_rmtree,
                  mock_isdir,
                  mock_makedirs,
                  mock_copy2,
                  check_input, isfile_01, isfile_02, isdir_pso):

        assert "copy2" in repr(mock_copy2)
        assert "makedirs" in repr(mock_makedirs)
        assert "isdir" in repr(mock_isdir)
        assert "rmtree" in repr(mock_rmtree)
        assert "input" in repr(mock_input)
        assert "check_input" in repr(check_input)
        assert "isdir_pso" in repr(isdir_pso)

        check_input.return_value = False
        isfile_01.return_value = False
        isfile_02.return_value = False
        isdir_pso.return_value = False

        # scenariusz: nie da sie utworzyc katalogow path_01
        mock_makedirs.side_effect = [OSError, OSError, True, True, True, True]
        mock_isdir.return_value = False
        errmsg_list = r"Nie udalo sie utworzyc katalogow w \_PSO" + "\n"
        make_backup.path_01 = "path_01"
        make_backup.path_02 = "path_02"
        make_backup.main()
        mock_makedirs.assert_called_once_with(make_backup.path_01)  # os.makedirs() wykonany tylko z path_01
        mock_copy2.assert_not_called()  # shutil.copy2() 
        assert mock_makedirs.call_count == 1  # os.makedirs() dla path_02 nie powinno juz byc uruchomione
        assert mock_rmtree.call_count == 0
        self.assertRaises(OSError, mock_makedirs)
        # os.makedirs() wyrzuca wyjatek; liczy sie jako kolejne wywolanie
        # funkcji, wiec licznik call_count +1
        with open("out_01.txt", mode="w") as fw:
            fw.write(mock_stdout.getvalue())
        self.assertEqual(mock_stdout.getvalue(), errmsg_list)

        # scenariusz: utworzono katalogi path_01 i path_02, nie udalo sie
        # skopiowac, nie udalo sie usunac katalogow
        mock_makedirs.reset_mock()  # reset licznika
        mock_stdout.truncate(0)
        mock_stdout.seek(0)
        mock_isdir.return_value = True
        # mock_makedirs.side_effect = itertools.repeat(True)
        mock_copy2.side_effect = FileNotFoundError
        mock_rmtree.side_effect = [FileNotFoundError, FileNotFoundError, True]
        errmsg_list = r"Nie skopiowano pliku z glownego katalogu do \01" + "\n" + r"Nie udalo sie usunac katalogow" + "\n"
        make_backup.main()
        assert mock_rmtree.call_count == 1
        assert mock_makedirs.call_count == 2
        with open("out_02.txt", mode="w") as fw:
            fw.write(mock_stdout.getvalue())
        self.assertRaises(FileNotFoundError, mock_copy2)
        self.assertRaises(FileNotFoundError, mock_rmtree)
        # shutil.copy2() wyrzuca wyjatek; liczy sie jako kolejne wywolanie
        # funkcji, wiec licznik call_count +1
        self.assertEqual(mock_stdout.getvalue(), errmsg_list)
        self.assertEqual(mock_input(), "y")

        # scenariusz: utworzono katalogi path_01 i path_02, nie udalo sie
        # skopiowac, ale udalo sie usunac katalogi
        mock_makedirs.reset_mock()  # reset licznika
        mock_rmtree.reset_mock()
        mock_stdout.truncate(0)
        mock_stdout.seek(0)
        mock_isdir.return_value = True
        errmsg_list = r"Nie skopiowano pliku z glownego katalogu do \01" + "\n"
        make_backup.main()
        self.assertEqual(mock_stdout.getvalue(), errmsg_list)
        assert mock_makedirs.call_count == 2
        assert mock_rmtree.call_count == 1
        self.assertRaises(FileNotFoundError, mock_copy2)
        with open("out_03.txt", mode="w") as fw:
            fw.write(mock_stdout.getvalue())
        self.assertEqual(mock_input(), "y")


if __name__ == "__main__":
    # execute only if run as a script
    unittest.main()
    # unittest.main(buffer=True)
    # If set to true, sys.stdout and sys.stderr will be buffered in between
    # startTest() and stopTest() being called. Collected output will only be
    # echoed onto the real sys.stdout and sys.stderr if the test fails or
    # errors. Any output is also attached to the failure / error message.
