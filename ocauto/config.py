from pathlib import Path
import os

class ConfigException(BaseException):
    pass

class MissingConfigError(ConfigException):
    pass

SCRIPTS_DIR = "scripts"

# A dictionary object, which contains mapping 
dirs = {
    "LOCAL_ROOT": Path(r"DataCenter"),
    "OC_ROOT_DIR": Path(r"C:\Users\john.delmundo\ownCloud - john.delmundo@data.cebookshop.com\DataCenter"),
    "OC_MAPPED_DIRS": {
        "SALES_CE": Path(r"Sales\5 Year Sales\CE"),
        "SALES_CL": Path(r"Sales\5 Year Sales\CELogic"),
        "GR": Path(r"Purchases\Receipts\5 Years GR Data"),
        "PO": Path(r"Purchases\Outstanding"),
        "OMS": Path(r"Orders\5 Years OMS Data"),
        "MATLIST_CE": Path(r"Material List"),
        "MATLIS_CL": Path(r"Material List"),
        "INVENTORY_ASOF": Path(r"Inventory"),
        "INVENTORY_MONTHLY": Path(r"Inventory\Monthly Invty"),
        # Add new report path mapping below
    },
    "SCRIPTS_DIR": Path(r"scripts")
}

# A dictionary object for database configuration
database = {
    "DEFAULT": {
        "DRIVER": "ODBC Driver 17 for SQL Server",
        "SERVER": "172.16.0.109",
        "DATABASE": "PRD",
        "UID": "dba",
        "PWD": "misdbadmin01",
        "TrustCertificate": "Yes"
    },
}

LOCAL_ROOT_DIR = dirs.get("LOCAL_ROOT", None)
OC_MAPPED_DIRS = dirs.get("OC_MAPPED_DIRS", None)

if not LOCAL_ROOT_DIR is None:
    if not LOCAL_ROOT_DIR == "" \
        and not isinstance(LOCAL_ROOT_DIR, str):
        try:
            LOCAL_ROOT_DIR.mkdir()
        except:
            pass
    else:
        raise TypeError(
            "'%s' must be of type 'Path', not 'str'." % "LOCAL_ROOT_DIR"
        )
else:
    raise MissingConfigError(
        "'%s' is missing from your configuration file." % "LOCAL_ROOT_DIR"
    )

if not OC_MAPPED_DIRS is None:
    for key, val in OC_MAPPED_DIRS.items():
        if not isinstance(val, str):
            path = Path(LOCAL_ROOT_DIR / val)
            if not path.exists():
                os.makedirs(path)
        else:
            raise TypeError(
                "'%s' must be of type 'Path', not 'str'." % key
            )
else:
    raise MissingConfigError(
        "'%s' is missing from your configuration file." % "OC_SUBDIRS"
    )