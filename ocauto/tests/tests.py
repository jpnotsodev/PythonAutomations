import sys
import os
import unittest

sys.path.append(r"C:\Users\john.delmundo\Desktop\PythonAutomations\ocauto")

from main import _get_year_and_month_before
from main import _read_file
from main import _row_to_list
import pyodbc

class TestAppFunctions(unittest.TestCase):

    _test_file = "test_file.txt"
    _test_dir_conf = {
        
    }
    _test_db_conn = pyodbc.connect(
        "DRIVER=%(driver)s; SERVER=%(server)s; DATABASE=%(db)s; UID=%(uid)s; PWD=%(pwd)s;" % (
            {
                "driver": "ODBC Driver 17 for SQL Server",
                "server": "172.16.0.109",
                "db": "PRD",
                "uid": "dba",
                "pwd": "misdbadmin01",
            }
        )
    )
    _test_script = """SELECT 1 as [Col1], 2 as [Col2], 3 as [Col3]"""
    
    def test_get_year_and_month_before_func(self):
        self.assertEqual(_get_year_and_month_before(), "202302")

    def test_read_file_func(self):
        file = open(self._test_file, "w")
        file.write("For testing purposes only.")
        file.close()
        self.assertEqual(_read_file(self._test_file), "For testing purposes only.")

    def test_row_to_list_func(self):
        cursor = self._test_db_conn.cursor()
        cursor.execute(self._test_script)
        self.assertEqual(_row_to_list(cursor), [[1, 2, 3]])

    def test_row_to_list_func_with_include_header_to_true(self):
        cursor = self._test_db_conn.cursor()
        cursor.execute(self._test_script)
        self.assertEqual(_row_to_list(
            cursor,
            include_headers=True), 
            [["Col1", "Col2", "Col3"], [1, 2, 3]]
        )

if __name__ == "__main__":
    unittest.main(verbosity=2)