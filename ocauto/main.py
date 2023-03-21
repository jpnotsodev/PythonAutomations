import owncloud
from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.styles import Color
from openpyxl.styles import Alignment
from openpyxl.styles import PatternFill
import pyodbc
from collections.abc import MutableMapping

import os
import datetime
import time
import shutil
from pathlib import Path
from enum import Enum
import logging

logging.basicConfig(level = logging.DEBUG)
logger = logging.getLogger()

class BaseException(Exception):
    pass

class InvalidFileExtensionError(BaseException):
    pass

SCRIPTS_DIR = "scripts"
LOCAL_ROOT_DIR = "DataCenter"

# Container for ownCloud directory mapping(s)
oc_dirs_mapping = dict()

# Mappings
oc_dirs_mapping["root"] = "C:\\Users\\john.delmundo\\ownCloud - john.delmundo@data.cebookshop.com\\DataCenter"
oc_dirs_mapping["sales_ce"] = "Sales\\5 Year Sales\\CE"
oc_dirs_mapping["sales_cl"] = "Sales\\5 Year Sales\\CELogic"
oc_dirs_mapping["gr"] = "Purchases\\Receipts\\5 Years GR Data"
# oc_dirs_mapping["po"] = "Purchases\\Outstanding"
oc_dirs_mapping["orders"] = "Orders\\5 Years OMS Data"
oc_dirs_mapping["matlist_ce"] = "Material List"
oc_dirs_mapping["matlist_cl"] = "Material List"
oc_dirs_mapping["inventory_asof"] = "Inventory\\"
oc_dirs_mapping["inventory_monthly"] = "Inventory\\Monthly Invty"

# Local directory mappings(s)
local_dirs_mapping = dict()

# Mappings
local_dirs_mapping["root"] = "DataCenter"
local_dirs_mapping["sales_ce"] = "Sales\\5 Year Sales\\CE"
local_dirs_mapping["sales_cl"] = "Sales\\5 Year Sales\\CELogic"
local_dirs_mapping["gr"] = "Purchases\\Receipts\\5 Years GR Data"
# local_dirs_mapping["po"] = "Purchases\\Outstanding"
local_dirs_mapping["orders"] = "Orders\\5 Years OMS Data"
local_dirs_mapping["matlist_ce"] = "Material List"
local_dirs_mapping["matlist_cl"] = "Material List"
local_dirs_mapping["inventory_asof"] = "Inventory\\"
local_dirs_mapping["inventory_monthly"] = "Inventory\\Monthly Invty"

# Normalizes the root paths
if not oc_dirs_mapping["root"].endswith("\\"):
    oc_dirs_mapping["root"] += "\\"

if not LOCAL_ROOT_DIR.endswith("\\"):
    local_dirs_mapping["root"] += "\\"

# Creates a directory called 'scripts' (if it doesn't exists already) within 
# your project directory. This is the location where you are going to put all
# your sql script(s) that will later be used by this program for generating custom reports
if not Path(SCRIPTS_DIR).is_dir():
    Path(SCRIPTS_DIR).mkdir()

def generate_report_from_script(script: str, param: str=None):
    """This function generates a structured data (list) from a given
    sql script. This uses the python module 'pyodbc' to connect to your
    database, and perform querying tasks.
    """

    # Builds a pyodbc connection object
    conn = pyodbc.connect(
        "DRIVER={%s}; SERVER=%s; DATABASE=%s; UID=%s; PWD=%s;" 
            % ("ODBC Driver 17 for SQL Server", "172.16.0.109", "PRD", "dba", "misdbadmin01"),
        autocommit=False
    )

    # Creates a cursor
    cursor = conn.cursor()

    # This checks whether the passed sql script is parameterized or not
    if param is not None:
        result = cursor.execute(script, param)
    else:
        result = cursor.execute(script)

    # Get column names
    col_names = [c[0] for c in result.description]

    # Get row data
    rows = [list(row) for row in result]

    # Merge column name(s) with row data
    data = list([col_names])
    for row in rows:
        data.append(row)

    return data

def to_spreadsheet(data: list[list|tuple]|tuple[list|tuple], local_path: str, filename: str, extension: str="xlsx"):
    """This function will create a spreadsheet based on the given first positional 
    argument 'data'. The argument 'data' accepts list/tuple sequence types only.

    params::\n
    data - the data to be converted into a spreadsheet.
    local_path - the path where the generated spreadsheet will be stored at.
    filename - the filename of your spreadsheet.
    extension - the file extension to be used (if isn't specified, defaults to xlsx)

    returns::\n
    file - a string representation of the spreadsheet file location.
    """

    # Verifies if the provided file extension is a valid spreadsheet extention.
    allowed_extensions = ["xls", "xlsx"]
    if extension not in allowed_extensions:
        raise InvalidFileExtensionError("'%s' is an invalid spreadsheet extension." % extension)

    wb = Workbook()
    ws = wb.active
    ws.title = "Sheet"

    for row in data:
        ws.append(row)

    # Apply custom cell formatting/styling 
    for row in ws.iter_rows(max_row=1):
        for cell in row:
            cell.font = Font(
                size=11,
                bold=True
            )
            cell.alignment = Alignment(
                horizontal="center",
                vertical="center"
            )

    # This produces the alternating rows background color/shade effect for
    # each row in the spreadsheet
    rowcount = 1
    for row in ws.iter_rows(min_row=2):
        rowcount += 1
        if rowcount % 2 == 0:
            for cell in row:
                cell.fill = PatternFill(
                    fill_type="solid",
                    fgColor="F0F0F0"
                )
        else:
            for cell in row:
                cell.fill = PatternFill(
                    fill_type="solid",
                    fgColor="00FFFFFF"
                )

    # Freeze column headers
    ws.freeze_panes = ws["A2"]
    # Apply filtering
    ws.auto_filter.ref = ws.dimensions

    # Checks whether the given local_path, where the spreadsheet will be saved, exists. 
    # If not, creates the path accordingly.
    if not os.path.isdir(local_path):
        try:
            os.makedirs(local_path)
        except Exception as exc:
            raise exc

    # Normalize the filename
    if not filename.endswith("."):
        filename += "."

    filename = local_path + "/" + filename + extension

    try:
        wb.save(filename)
    except Exception as exc:
        raise exc

    file = filename
    return file

def copy_local_file_to_oc(source_file_path: str, destination_file_path: str):
    try:
        shutil.copy(source_file_path, destination_file_path)
    except Exception as exc:
        raise exc

def _get_formatted_date():
    """Transforms the date into 'YYYYMM' format
    to conform the date format to query filtering
    
    params: None
    returns: Formatted Date (YYYYMM)
    """

    _DATE_FORMAT = "%Y%m"

    f_date = None
    date = datetime.date.today()
    m = date.month - 1
    if isinstance(m, int) and m > 0 and m < 12: 
        f_date = date.replace(month=m)
    elif m < 1:
        m = 12
        y = date.year - 1
        f_date = date.replace(year=y, month=m)
    res = datetime.datetime.strftime(f_date, _DATE_FORMAT)
    return res

def main():
    root = local_dirs_mapping["root"]
    if not os.path.isdir(root):
        os.mkdir(root)

    for _, path in local_dirs_mapping.items():
        if not path == "root":
            root_p = Path(root)
            subdir_p = Path(path)
            path = Path(root_p / subdir_p)
            if not path.is_dir():
                try:
                    os.makedirs(path)
                except:
                    pass

    scripts_path = Path(Sc)
    for path in scripts_path.iterdir():
        if path.is_dir():
            raise Exception("Scripts folder must contain script files only.")

    script_files = [str(os.path.basename(file)).removesuffix(".sql").lower() for file in Path(SCRIPTS_DIR).glob("*.sql")]

    for k in oc_dirs_mapping:
        if k.lower() not in script_files and k != "root":
            raise FileNotFoundError("Script for key/mapping '%s' not found." % (k))
        if k != "root":
            try:
                file_handle = open("%s\%s" % (SCRIPTS_DIR, k + ".sql"))
                script = file_handle.read()
                if "= ?" in script:
                    data = generate_report_from_script(script, _get_formatted_date())
                else:
                    data = generate_report_from_script(script)
                spreadsheet = to_spreadsheet(
                    data=data, 
                    local_path=LOCAL_ROOT_DIR + oc_dirs_mapping[k], # Points to local directory
                    filename=k.upper(),
                    extension="xlsx"
                )
                copy_local_file_to_oc(
                    destination_file_path=oc_dirs_mapping["root"] + oc_dirs_mapping[k], 
                    source_file_path=spreadsheet
                )
            except Exception as exc:
                raise exc
            finally:
                file_handle.close()

if __name__ == "__main__":
    main()