import os
from datetime import date, datetime
from collections.abc import Sequence
import pyodbc
import openpyxl

def _generate_date(from_year: int, from_month: int):
    
    _DATE_FORMAT = "%Y%m"
    fy = None
    fm = None

    if isinstance(from_year, int):
        if from_year > 0 and \
                from_year < 9999:
            fy = from_year
        else:
            raise ValueError("Invalid range for year")
    else:
        raise TypeError("")
    
    if isinstance(from_month, int):
        if from_month > 0 and \
                from_month <= 12:
            fm = from_month
        else:
            raise ValueError("Invalid range for month")
    else:
        raise TypeError("You entered an invalid value for month")
    
    today = date.today()
    y_diff = today.year - fy + 1

    dd = today.year + 1
    d = []
    for x in range(y_diff):
        dd = dd - 1
        d.append(dd)
        curr_val = dd
        dd = curr_val

    d.sort()
    for g in d:
        for i in range(fm, 13):
            y = date.today().year
            m = date.today().month
            if i == m and \
                    g == y:
                break
            yield datetime(year=g, month=i, day=1).strftime(_DATE_FORMAT)
        fm = 1

def _create_paths(*args):
    """Creates a path from a given list of items
    First element being the root directory"""

    if not isinstance(args, Sequence):
        raise Exception
    path = [p for p in args]
    path = "\\".join(path[0])
    return path

# print(_create_paths(("DataCenter", "Inventory", "2023", "12")))
# try:
#     for i in range(16):
#         try:
#             os.makedirs(os.path.join(os.path.dirname(__file__),
#                  _create_paths(("DataCenter", "Inventory", "2021", str(i)))))
#         except:
#             pass
# except:
#     pass

# try:
#     for i in range(16):
#         try:
#             os.makedirs(os.path.join(os.path.dirname(__file__),
#                  _create_paths(("DataCenter", "Inventory", "2022", str(i)))))
#         except:
#             pass
# except:
#     pass

# try:
#     for i in range(16):
#         try:
#             os.makedirs(os.path.join(os.path.dirname(__file__),
#                  _create_paths(("DataCenter", "Inventory", "2023", str(i)))))
#         except:
#             pass
# except:
#     pass

def _create_dirs():
    if not os.path.exists(SubFolders.ROOT):
        os.mkdir(SubFolders.ROOT)
    
    os.chdir(SubFolders.ROOT)
    
    for key, val in SubFolders.__dict__.items():
        if not "__" in key and \
                not key == "ROOT":
            if not os.path.exists(val):
                os.mkdir(val)
            os.chdir(val)
            print(os.getcwd())
            dates = _generate_date(2021, 12)
            it = iter(dates)
            # for d in dates:
            while True:
                try:
                    n = next(it)
                    dirs = [dir for dir in os.listdir(val)]
                    year, month = n[0:4], n[4:]
                    print(year, month)
                    if year not in dirs:
                        os.mkdir(year)
                    os.chdir(year)
                    print(os.getcwd())
                    if not os.path.exists(month):
                        os.mkdir(month)
                    os.chdir(val)
                except:
                    break

# try:
#     conx = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};SERVER=172.16.0.109;DATABASE=PRD;UID=dba;PWD=misdbadmin01")
#     cursor = conx.cursor()
#     # for d in _generate_date(2022, 1):
#     res = cursor.execute("""SELECT
# prd.EKPO.BUKRS AS [Company Code],
# prd.EKPO.EBELN AS [Purchase Order No],
# CAST(prd.EKKO.AEDAT AS DATE) AS [Purchase Order Date],
# [Document Type] = (SELECT 
#                         BATXT 
#                     FROM
#                         prd.T161T
#                     WHERE
#                         BSART = prd.EKKO.BSART
#                         AND MANDT = '888'
#                         AND SPRAS = 'E'),
# CONVERT(BIGINT, prd.EKKO.LIFNR) AS [Vendor Code],
# prd.LFA1.NAME1 + 
#     NAME2 + 
#         NAME3 + 
#             NAME4 AS [Vendor Name],
# prd.EKPO.NETPR AS [Unit Cost under GR Currency],
# CONVERT(INT, prd.EKPO.MENGE) AS [GR Qty],
# prd.EKPO.MATNR AS [Material No],
# prd.EKPO.NETWR AS [Amount in FOREX],
# [Storage Location] = (SELECT 
#                         LGOBE
#                     FROM
#                         prd.T001L
#                     WHERE
#                         WERKS = prd.EKPO.WERKS
#                         AND LGORT = prd.EKPO.LGORT
#                         AND MANDT = '888'),
# EKBE.WAERS AS [Currency],
# [Exchange Rate] = CASE WHEN EKBE.WAERS ='PHP' THEN 1 
#                     ELSE (SELECT 
#                             UKURS
#                         FROM
#                             prd.ZPR_TCURR_HIST
#                         WHERE
#                             FCURR = EKBE.WAERS
#                             AND DATE_ADDED = EKBE.BUDAT) END,
# [Amount in PHP] = CASE WHEN EKBE.WAERS ='PHP' THEN CONVERT(DECIMAL(10, 2), (prd.EKPO.MENGE * prd.EKPO.NETPR) * 1)
#                     ELSE (SELECT 
#                             CONVERT(DECIMAL(10, 2), (prd.EKPO.MENGE * prd.EKPO.NETPR) * UKURS)
#                         FROM
#                             prd.ZPR_TCURR_HIST
#                         WHERE
#                             FCURR = EKBE.WAERS
#                             AND DATE_ADDED = EKBE.BUDAT) END,
# EKBE.EBELP AS [Line No],
# EKBE.BELNR AS [GR Doc No],
# CAST(EKBE.BUDAT AS DATE) AS [GR Date]
# FROM
# -- Purchasing Document Header
# prd.EKPO
#     JOIN
#         -- Purchasing Document Item
#         prd.EKKO
#     ON
#         prd.EKPO.EBELN = prd.EKKO.EBELN
#         AND prd.EKPO.MANDT = prd.EKPO.MANDT
#     JOIN
#         -- Vendor Master List
#         prd.LFA1
#     ON
#         prd.LFA1.LIFNR = prd.EKKO.LIFNR
#         AND prd.LFA1.MANDT = prd.EKPO.MANDT
#     JOIN
#         -- History per Purchasing Document
#         (SELECT 
#             *
#         FROM
#             prd.EKBE
#         WHERE				
#             prd.EKBE.ELIKZ = 'X' -- Delivery Completed Indicator
#             AND prd.EKBE.MANDT = '888') EKBE
#         --SELECT * FROM
#         --prd.EKPO WHERE EBELN = '4500028733'
#     ON
#         prd.EKPO.EBELN = EKBE.EBELN
#         AND prd.EKKO.MANDT = EKBE.MANDT
#         AND prd.EKPO.EBELP = EKBE.EBELP
# WHERE
# prd.EKPO.MANDT = '888'
# --AND prd.EKPO.ELIKZ = 'X' -- Delivery Completed Indicator
# AND prd.EKPO.WEPOS = 'X' -- Goods Receipt Indicator
# AND (NOT prd.EKPO.LOEKZ = 'L' -- Deletion Indicator
#     OR prd.EKPO.LOEKZ = '')
# AND LEFT(EKBE.BUDAT, 4) = ? -- Indicates that the 
# AND prd.EKPO.RETPO <> 'X'
# AND LEFT(prd.EKPO.EBELN, 2) NOT IN ('79', '55', '45')""", "2021")
#     col_head = [desc[0] for desc in res.description]
#     # print(col_head)
#     wb = openpyxl.Workbook()
#     # wb1 = openpyxl.Workbook()
#     ws = wb.active
#     # ws1 = wb1.active
#     ws.title = "Sheet"
#     # ws1.title = "SALES_CL" + "202208"
#     ws.append(col_head)
#     # ws1.append(col_head)
#     # print(row)
#     for row in res:
#         # if row[0] == "1000":
#         row = tuple(row)
#         ws.append(row)
#         # elif row[0] == "4000":
#         #     row = tuple(row)
#             # ws1.append(row)
#     # ws.append(row)
#     ws.auto_filter.ref = ws.dimensions
#     # ws1.auto_filter.ref = ws1.dimensions
#     wb.save("DataCenter/GR/GR_{}.xlsx".format("2021"))
#     # wb1.save("DataCenter/SALES/CELOG/SALES_CL_{}.xlsx".format(d))
# except Exception as e:
#     print(e)

# _create_folders()
today = datetime(year=2029, month=3, day=1).strftime("%Y%m")
# dates = _generate_date(2020, 12)
# for d in dates:
#     print(d)


