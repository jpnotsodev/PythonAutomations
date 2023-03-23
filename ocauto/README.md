# OwnCloud Report Automation

A python program that is written for the sole purpose of automating the process of:

- Extraction of data from the database
- Creating spreadsheets
- Making a copy of the report files into ownCloud remote client

All this in just a single run of a program.

---

### Table of Contents

- [Pre-requisites](#pre-requisites)
- [Setting up your program](#setting-up-your-program)
  - [Clone the repository](#clone-the-repository)
  - [Activate virtual environment](#activate-virtual-environment)
  - [Install required packages](#install-required-packages)
- [Adding new report](#adding-new-report)
  - [Add ownCloud directory mapping](#add-owncloud-directory-mapping)
  - [Create the required sql script that will generate the report for your new directory mapping](#create-the-required-sql-script-that-will-generate-the-report-for-your-new-directory-mapping)
  - [Run the program](#run-the-program)
- [Running tests](#running-tests)
- [Limitations](#limitations)

---

### Pre-requisites

- ownCloud Desktop App/Client ([_download here_](https://owncloud.com/desktop-app/))
- Latest version of python ([_download here_](https://www.python.org/))

> **Note:** In order for this program to actually work, you must install/setup your ownCloud Desktop App first. Make sure that you are already logged in using authorized credentials.

### Setting up your program

#### Clone the repository <small> (You can skip this part if you already have a copy of this to your local system) </small>

```bash
> cd <to your preferred target location>
> git clone 'https://github.com/jpdelmundo223/PythonAutomations.git'
```

#### Activate virtual environment

```bash
> cd PythonAutomations\ocauto
> venv\Scripts\active
```

#### Install required packages

```bash
> pip install -r requirements.txt
```

### Adding new report

To add a report, you must first specify the location (identical to what your ownCloud remote client has e.g. `DataCenter\Balances`) where the report file will be stored at, create a script that will be responsible for fetching data from your database, and so on.

You can do all that by going to `config.py`:

#### Add ownCloud directory mapping

```python
dirs = {
    ...
    "OC_MAPPED_DIRS": {
        ...
        # Add new mapping below
        "<DIR_MAPPER_NAME>": Path(r"<path_to_report_dir>"), # Add this line here, together with the existing mappings
```

##### Sample:

```python
"BALANCES": Path(r"DataCenter\Balances")
```

#### Create the required sql script that will generate the report for your new directory mapping

#### Sample SQL script:

```sql
SELECT
    *
FROM
    dbo.Balances
```

Now, save it to folder `scripts\` and name it as `balances.sql`

> **Note:** Your mapper name and the name of the script file must be of the same name (just like what we did in previous examples). That is because each time you add a new directory mapping, the program will look for any file (inside `scripts\` folder) that matches the name of the mapping you've just created. Failing to do so will cause the program to stop/terminate.

#### Run the program

```bash
> python ocauto\main.py
```

### Running tests

Running test cases are important as it will ensure you that the program would work as intended.

You can run tests by running the ff. code against your command line interface:

```bash
> python tests\tests.py
```

### Limitations
