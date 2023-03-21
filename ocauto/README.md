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

### Step 1: Add mappings for the ownCLoud target report location

```python
oc_dirs_mapping = dict()
...
...
# Add a new line here
oc_dirs_mapping[<report_name>] = "<ownCloud_target_path>"
```

### Sample:

```python
oc_dirs_mapping["balances"] = "Reports\\Balances\\"
```

### Step 2: Create the script (SQL) file you will be using to extract the data needed for your new report, and save it inside the `scripts` folder

### Sample SQL script:

```sql
SELECT * FROM dbo.Balances
```

> **Note:** You can pass parameter to a script by placing a `= ?` placeholder, instead of the actual value.

Now save your script to folder `scripts` and name it `balances.sql`

> **Note:** The name of the directory mapping and the name of the script file should be the same (always), just like what we did from the above examples. And that is because each time you add a new location/directory mapping, the program will look for any script file that matches the name of the mapping you created.
