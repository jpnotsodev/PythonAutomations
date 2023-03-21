# OwnCloud Report Automation

### Description

A python program that is written for the sole purpose of automating the process of:

- Extraction of data from the database
- Creating spreadsheets
- Making a copy of the report files into ownCloud remote client

All this in just a single run of a program.

### Pre-requisites

- ownCloud Desktop App/Client ([_download here_](https://owncloud.com/desktop-app/))
- Latest version of python ([_download here_](https://www.python.org/))

> **Note:** In order for this program to actually work, you must install/setup your ownCloud Desktop App first. Make sure that you are already logged in using authorized credentials.

## Setting up your program

### Step 1: Clone the repository

```bash
>> cd <to your preferred target location>
>> git clone 'https://github.com/jpdelmundo223/PythonAutomations.git'
```

### Step 2: Activate virtual environment

```bash
>> cd PythonAutomations\ocauto
>> venv\Scripts\active
```

### Step 3: Install required packages

```bash
>> pip install -r requirements.txt
```

## Adding new custom report

To add a report, you must first specify the location (in ownCloud) where the report file will be stored at, create a script that will be responsible for fetching data from your database and save it inside the `scripts` folder.

To do that, you must do some modification(s) to the `main.py` file.

#### Step 1: Add mappings for the ownCLoud target report location

```python
oc_dirs_mapping = dict()
...
...
# Add a new line here
oc_dirs_mapping[<report_name>] = "<ownCloud_target_path>"
```

#### Sample:

```python
oc_dirs_mapping["balances"] = "Reports\\Balances\\"
```

#### Step 2: Create the script (SQL) file you will be using to extract the data needed for your new report, and save it inside the `scripts` folder

#### Sample SQL script:

```sql
SELECT * FROM dbo.Balances
```

> _Note:_ You can pass parameter to a script by placing a `= ?` placeholder, instead of the actual value.
