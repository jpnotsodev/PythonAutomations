import owncloud
import pyodbc
from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.styles import Color
from openpyxl.styles import Alignment
from openpyxl.styles import PatternFill

import os
import re
import datetime
import time
import shutil
from pathlib import Path

from utils.logger import logger
from exceptions.exceptions import ScriptNotFoundError
from exceptions.exceptions import InvalidFileExtensionError
from exceptions.exceptions import TooManyParametersError

SCRIPTS_DIR = "scripts"
LOCAL_ROOT_DIR = "DataCenter"
OC_ROOT_DIR = "C:\\Users\\john.delmundo\\ownCloud - john.delmundo@data.cebookshop.com\\DataCenter"

# Container for ownCloud directory mapping(s)
oc_dirs_mapping = dict()

# Mappings
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
if not OC_ROOT_DIR.endswith("\\"):
    OC_ROOT_DIR += "\\"

if not LOCAL_ROOT_DIR.endswith("\\"):
    LOCAL_ROOT_DIR += "\\"

# Creates a directory called 'scripts' (if it doesn't exists already) within 
# your project directory. This is the location where you are going to put all
# your sql script(s) that will later be used by this program for generating custom reports

if not Path(SCRIPTS_DIR).is_dir():
    logger.info("Creating {} directory..."
        .format(SCRIPTS_DIR + "\\")
    )
    Path(SCRIPTS_DIR).mkdir()
    logger.info("{} directory created successfully..."
        .format(SCRIPTS_DIR + "\\")
    )

def generate_report_from_script(script: str, param: str=None):
    """This function generates a structured data (list) from a given
    sql script. This uses the python module 'pyodbc' to connect to your
    database, and perform querying tasks.
    """

    # Builds a pyodbc connection object
    logger.info("Connecting to '{database}', under instance name '{servername}'..."
        .format(database="PRD",
            servername="172.16.0.109"
        )
    )
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
    logger.info("Extracting table columns...")
    col_names = [c[0] for c in result.description]
    logger.info("Done...")

    # Get row data
    logger.info("Extracting table rows...")
    rows = [list(row) for row in result]
    logger.info("Done...")

    # Merge column name(s) with row data
    logger.info("Sanitizing report data...")
    data = list([col_names])
    for row in rows:
        data.append(row)
    logger.info("Done...")

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
    logger.info("Validating provided file extension...")
    allowed_extensions = ["xls", "xlsx"]
    if extension not in allowed_extensions:
        raise InvalidFileExtensionError("Valid file extensions are (xls, xlsx), used '{}' instead.".format(extension))

    logger.info("Creating new workbook...")
    wb = Workbook()
    ws = wb.active
    ws.title = "Sheet"

    for row in data:
        ws.append(row)

    # Apply custom cell formatting/styling 
    logger.info("Applying styles...")
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
    logger.info("Done...")

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
        logger.info("Saving file '{}' to '{}'..."
            .format(os.path.basename(filename),
                os.path.dirname(filename)
            )
        )
        wb.save(filename)
        logger.info("Done...")
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
    root = LOCAL_ROOT_DIR
    if not os.path.exists(root):
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

    scripts_path = Path(SCRIPTS_DIR)
    for path in scripts_path.iterdir():
        if path.is_dir():
            raise Exception("Scripts folder must contain script files only.")

    script_files = [str(os.path.basename(file)).removesuffix(".sql").lower() for file in Path(SCRIPTS_DIR).glob("*.sql")]

    for k in oc_dirs_mapping:
        if k.lower() not in script_files and k != "root":
            raise ScriptNotFoundError("Script for key/mapping '%s' not found." % (k))
        if k != "root":
            try:
                file_handle = open("%s\%s" % (SCRIPTS_DIR, k + ".sql"))
                script = file_handle.read()
                if re.search("= +\?", script):
                    param_count = len(re.findall("= +\?", script))
                    if param_count > 1:
                        raise TooManyParametersError("The function only supports %s parameter at a time, but '%s' has %s."
                            % (
                                1,
                                os.path.join(SCRIPTS_DIR, k + ".sql"),
                                param_count
                            )
                        )
                    data = generate_report_from_script(script, _get_formatted_date())
                else:
                    data = generate_report_from_script(script)
                spreadsheet = to_spreadsheet(
                    data=data, 
                    local_path=LOCAL_ROOT_DIR + oc_dirs_mapping[k], # Points to local directory
                    filename=k.upper(),
                    extension="xlsx"
                )
                logger.info("Copying '{}' from '{}' to '{}'..."
                    .format(os.path.basename(spreadsheet),
                        os.path.dirname(spreadsheet),
                        os.path.dirname(OC_ROOT_DIR + oc_dirs_mapping[k])
                    )
                )
                # copy_local_file_to_oc(
                #     destination_file_path=oc_dirs_mapping["root"] + oc_dirs_mapping[k], 
                #     source_file_path=spreadsheet
                # )
                logger.info("Done...")
            except Exception as exc:
                raise exc
            finally:
                file_handle.close()

if __name__ == "__main__":
    main()