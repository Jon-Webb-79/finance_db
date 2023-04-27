# Import necessary packages here

# - If a package and a module within the package is to be imported
#   uncomment the following lines where dir is the directory containing
#   the source files.  These lines should go above the module imports
import datetime
import os
import sqlite3
import sys

# ==========================================================================================
# ==========================================================================================

# File:    main.py
# Date:    April 26, 2023
# Author:  Jonathan A. Webb
# Purpose: This file contains functions that will create a database, add, subtract, and
#          modify data in the database
# ==========================================================================================
# ==========================================================================================
# Insert Code here


def create_database(file_name: str) -> None:
    """
    :param file_name: The name of the database to be created without a .db file
                      extension

    This function will create a SQLite table for expenses and another table
    for sales.  The tables have the following schema.

    Expenses Table:

    +---------------+------------------+--------------------------------------+
    | Column        | Data Type        | Description                          |
    +===============+==================+======================================+
    | id            | INTEGER PRIMARY  | Unique identifier for the expense    |
    |               | KEY              |                                      |
    +---------------+------------------+--------------------------------------+
    | date          | DATE NOT NULL    | Date of the expense                  |
    +---------------+------------------+--------------------------------------+
    | time          | TIME NOT NULL    | Time of the expense                  |
    +---------------+------------------+--------------------------------------+
    | expense_type  | TEXT NOT NULL    | type of expense, only allows entires |
    |               |                  | of 'credit' or 'debit'               |
    +---------------+------------------+--------------------------------------+
    | expense_value | REAL NOT NULL    | Value of the expense                 |
    +---------------+------------------+--------------------------------------+
    | company       | TEXT NOT NULL    | Company associated with the expense  |
    +---------------+------------------+--------------------------------------+
    | description   | TEXT NOT NULL    | Description of the expense           |
    +---------------+------------------+--------------------------------------+
    | modified_date | DATE NOT NULL    | Date when the expense was last       |
    |               |                  | modified. (default: current date)    |
    +---------------+------------------+--------------------------------------+
    | modified_time | TIME NOT NULL    | Time when the expense was last       |
    |               |                  | modified. (default: current time)    |
    +---------------+------------------+--------------------------------------+

    Sales Table:

    +---------------+------------------+---------------------------------------+
    | Column        | Data Type        | Description                           |
    +===============+==================+=======================================+
    | id            | INTEGER PRIMARY  | Unique identifier for the sale        |
    |               | KEY              |                                       |
    +---------------+------------------+---------------------------------------+
    | date          | DATE NOT NULL    | Date of the sale                      |
    +---------------+------------------+---------------------------------------+
    | time          | TIME NOT NULL    | Time of the sale                      |
    +---------------+------------------+---------------------------------------+
    | first_name    | TEXT NOT NULL    | First name of the customer            |
    +---------------+------------------+---------------------------------------+
    | last_name     | TEXT NOT NULL    | Last name of the customer             |
    +---------------+------------------+---------------------------------------+
    | email_address | TEXT NOT NULL    | Email address of the customer         |
    +---------------+------------------+---------------------------------------+
    | phone_number  | TEXT             | Phone number of the customer          |
    |               |                  | (optional)                            |
    +---------------+------------------+---------------------------------------+
    | product_id    | INTEGER NOT NULL | Unique identifier for the product     |
    +---------------+------------------+---------------------------------------+
    | modified_date | DATE NOT NULL    | Date when the sale was last modified. |
    |               |                  | (default: current date)               |
    +---------------+------------------+---------------------------------------+
    | modified_time | TIME NOT NULL    | Time when the sale was last modified. |
    |               |                  | (default: current time)               |
    +---------------+------------------+---------------------------------------+

    The modified_date and modified_time fields are automatically updated
    to the current date and time whenever a row is inserted or updated.
    """
    # append .db extension to file name
    file_name = file_name + ".db"

    # check if database already exists
    if os.path.exists(file_name):
        msg = f"Database '{file_name}' already exists. Choose a different file name."
        sys.stderr.write(msg)
        return

    # create a new database file and connect to it
    conn = sqlite3.connect(file_name)
    c = conn.cursor()

    # create the expenses table
    c.execute(
        """CREATE TABLE expenses
                (id INTEGER PRIMARY KEY,
                 date DATE NOT NULL,
                 time TIME NOT NULL,
                 expense_type TEXT NOT NULL CHECK(expense_type IN('credit', 'debit')),
                 expense_value REAL NOT NULL,
                 company TEXT NOT NULL,
                 description TEXT NOT NULL,
                 modified_date DATE NOT NULL DEFAULT CURRENT_DATE,
                 modified_time TIME NOT NULL DEFAULT CURRENT_TIME)"""
    )

    # create the sales table
    c.execute(
        """CREATE TABLE sales
                (id INTEGER PRIMARY KEY,
                 date DATE NOT NULL,
                 time TIME NOT NULL,
                 first_name TEXT NOT NULL,
                 last_name TEXT NOT NULL,
                 email_address TEXT NOT NULL,
                 phone_number TEXT,
                 product_id INTEGER NOT NULL,
                 modified_date DATE NOT NULL DEFAULT CURRENT_DATE,
                 modified_time TIME NOT NULL DEFAULT CURRENT_TIME)"""
    )

    # commit the changes and close the connection
    conn.commit()
    conn.close()

    sys.stdout.write(f"Database file '{file_name}' created successfully.")


# ------------------------------------------------------------------------------------------


def add_expense(
    file_name: str, expense_value: float, company: str, description: str
) -> None:
    """
    Adds a new expense to the expenses table in the specified SQLite database
    file, with the specified expense value, company, and description. The date,
    time, modified date, and modified time are automatically entered based on
    the current computer time.

    :param file_name: The name of the SQLite database file to add the expense to
    :param expense_value: The value of the expense to add
    :param company: The name of the company associated with the expense
    :param description: A description of the expense
    """
    # Open a connection to the database
    conn = sqlite3.connect(file_name)

    # Get the current date and time
    current_date = datetime.date.today()
    current_time = datetime.datetime.now().time()

    # Insert the new expense into the expenses table
    query = "INSERT INTO expenses (date, time, expense_value, company, description, "
    insert_query = query + " modified_date, modified_time) VALUES (?, ?, ?, ?, ?, ?, ?)"
    values = (
        current_date,
        current_time,
        expense_value,
        company,
        description,
        current_date,
        current_time,
    )
    conn.execute(insert_query, values)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


# ==========================================================================================
# ==========================================================================================
# eof
