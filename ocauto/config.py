from pathlib import Path

class ConfigException(BaseException):
    pass

class MissingConfigError(ConfigException):
    pass

# Mapping configuration for ownCloud
dirs = {
    "LOCAL_ROOT_DIR": Path(r"DataCenter"),
    "OC_ROOT_DIR": Path(r"C:\Users\john.delmundo\ownCloud - john.delmundo@data.cebookshop.com\DataCenter"),
    "OC_MAPPED_DIRS": {
        "SALES_CE": Path(r"Sales\5 Year Sales\CE"),
        "SALES_CL": Path(r"Sales\5 Year Sales\CELogic"),
        "GR": Path(r"Purchases\Receipts\5 Years GR Data"),
        # "PO": Path(r"Purchases\Outstanding"),
        "OMS": Path(r"Orders\5 Years OMS Data"),
        "MATLIST_CE": Path(r"Material List"),
        "MATLIST_CL": Path(r"Material List"),
        "INVENTORY_ASOF": Path(r"Inventory"),
        "INVENTORY_MONTHLY": Path(r"Inventory\Monthly Invty"),
        # Add new mapping below
        "ARCC": Path(r"Accounting\ARCC"),
    },
    "SCRIPTS_DIR": Path(r"scripts"),
}

# Database configuration
database = {
    "DRIVER": "your-driver-version",
    "SERVER": "your-server-name",
    "DATABASE": "your-database-name",
    "UID": "your-database-username",
    "PWD": "your-database-password",
    "TrustCertificate": "Yes"
}