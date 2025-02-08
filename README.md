# UDSQL - Database Management System

## Team Members

- *Luis Alejandro Morales – 20222020175*
- *Esteban Villalba Delgadillo - 20212020064*
- *Santiago Marin Paez - 20231020159*

## Project Information

**Professor:** *Engineer Carlos Andrés Sierra Virgüez*  
**Career:** *Systems Engineer*  

## Introduction

UDSQL is a simple Database Management System (DBMS) that allows CRUD (Create, Read, Update, Delete) operations on tables. It uses a custom file format (.udsql) to store data and a metadata file to manage table structures.

This project is part of **Workshop 3** in the **Database Foundations** course.

## Internal Architecture

The project is designed using files (separate modules) instead of a fully class-oriented structure. Each file has a specific responsibility, following a modular approach where each part of the system handles a particular function.

## Modules

* **create_table.py** - Table Creation

  Generates .udsql files in the `tables/` folder.

  Defines the column names for each table.

* **metadata_manager.py** - Metadata Management

  Saves the table structure in `metadata.pkl` using `pickle`.

* **UDCRUD.py** - CRUD Implementation with the UDSQL Class

  The `UDSQL` class encapsulates the operations on the .udsql files in the `tables/` folder.


## Installation

### Prerequisites

Make sure you have **Python 3** installed on your system.

### Clone the Repository

```bash
 git clone https://github.com/Inaryuta/Database_Foundations_Workshop-3.git
 cd Database_Foundations_Workshop-3
```

If you want to start with a completely new database, you will only need the following files:

- `Operations` folder
- `main.py`
- `create_table.py`
- `metadata_manager.py`

### Initial Setup

Run the following commands to generate the database structure:

```bash
python3 create_table.py
```

Then, run:

```bash
python3 metadata_manager.py
```

> **Note:** Depending on your operating system, you may need to use `py` or `python` instead of `python3`.

## Running the Program

To execute the program, open a terminal in the project directory and run:

```bash
python3 main.py
```

Once the program starts, you will see a menu with the following options:

1. **Insert Record**
2. **Update Record**
3. **Delete Record**
4. **Select Records**
5. **Exit**

### Available Operations

#### Insert Record

1. Select option `1` from the main menu.
2. Enter the name of the table where the record will be inserted.
3. Provide values for each field in the table.
4. A confirmation message will display the new record's code.

#### Update Record

1. Select option `2` from the main menu.
2. Enter the name of the table where the record will be updated.
3. Enter the record's code to be modified.
4. Enter the new values for each field.
5. A confirmation message will be displayed.

#### Delete Record

1. Select option `3` from the main menu.
2. Enter the name of the table from which the record will be deleted.
3. Enter the record's code to delete.
4. A confirmation message will be displayed.

#### Select Records

1. Select option `4` from the main menu.
2. Enter the name of the table to query.
3. Enter a `WHERE` clause to filter records (optional). If left blank, all records will be displayed.
4. The selected records will be shown in a tabular format.

#### Additional information in the UDSQL Database User Manual document
