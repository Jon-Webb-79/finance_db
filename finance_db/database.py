# Import necessary packages here
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
        msg = f"Database '{file_name}' already exists. Choose a different file name.\n"
        sys.stderr.write(msg)
        return

    # create a new database file and connect to it
    try:
        conn = sqlite3.connect(file_name)
        c = conn.cursor()
    except sqlite3.Error as e:
        raise sqlite3.Error("Unable to connect to database)") from e

    # create the expenses table
    c.execute(
        """CREATE TABLE expenses
                (id INTEGER PRIMARY KEY,
                 date DATE NOT NULL DEFAULT CURRENT_DATE,
                 time TIME NOT NULL DEFAULT CURRENT_TIME,
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
                 date DATE NOT NULL DEFAULT CURRENT_DATE,
                 time TIME NOT NULL DEFAULT CURRENT_TIME,
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
    file_name: str,
    expense_type: str,
    expense_value: float,
    company: str,
    description: str,
) -> None:
    """
    Adds a new expense to the expenses table in the specified SQLite database
    file, with the specified expense value, company, and description. The date,
    time, modified date, and modified time are automatically entered based on
    the current computer time.

    :param file_name: The name of the SQLite database file to add the expense to
    :param expense_type: Must be either 'credit', or 'debit'. Case sensitive!
    :param expense_value: The value of the expense to add
    :param company: The name of the company associated with the expense
    :param description: A description of the expense
    :raises ValueError: If an invalid expense type is provided
    :raises sqlite3.Error: If there is an error inserting the expense into the
                           database
    """
    # Check that the expense type is valid
    if expense_type not in ["credit", "debit"]:
        raise ValueError("Invalid expense type. Must be either 'credit' or 'debit'.")

    if not os.path.exists(file_name):
        msg = f"Database '{file_name}' does not exist."
        sys.stderr.write(msg)
        return

    try:
        conn = sqlite3.connect(file_name)
        c = conn.cursor()
        c.execute(
            f"""INSERT INTO expenses (expense_type, expense_value,
                     company, description) VALUES ('{expense_type}',
                     {expense_value}, '{company}', '{description}')"""
        )
        conn.commit()
        sys.stdout.write(f"Data succesfully written to '{file_name}'")
    except sqlite3.Error as e:
        raise sqlite3.Error("Error inserting expense into database") from e

    # Close the database
    conn.close()


# ------------------------------------------------------------------------------------------


def update_expense_type(file_name: str, expense_id: int, expense_type: str) -> None:
    """
    Updates the expense_type column of an expense in the expenses table.

    :param file_name: The name of the database file to connect to.
    :param expense_id: The ID of the expense to update.
    :param expense_type: The new value to set for the expense_type column.
    """
    # Check that the expense type is valid
    if expense_type not in ["credit", "debit"]:
        raise ValueError("Invalid expense type. Must be either 'credit' or 'debit'.")

    if not os.path.exists(file_name):
        msg = f"Database '{file_name}' does not exist."
        sys.stderr.write(msg)
        return
    # open the database and update the expense
    conn = None
    try:
        conn = sqlite3.connect(file_name)
        c = conn.cursor()
        c.execute(
            f"UPDATE expenses SET expense_type='{expense_type}' WHERE id={expense_id}"
        )
        conn.commit()
        sys.stdout.write("Expense type updated successfully.\n")
    except sqlite3.Error as e:
        sys.stderr.write(f"Error updating expense type: {e}\n")
    finally:
        if conn:
            conn.close()


# ==========================================================================================
# ==========================================================================================
# eof
