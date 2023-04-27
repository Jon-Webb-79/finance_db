# Import necessary packages here
# import pytest
import os
import sqlite3
import sys
from io import StringIO

from finance_db.database import create_database

# - If a package and a module within the package is to be imported
#   uncomment the following lines where dir is the directory containing
#   the source files.  These lines should go above the module imports
# import sys
# import os
# sys.path.insert(1, os.path.abspath(dir))
# ==========================================================================================
# ==========================================================================================
# File:    test.py
# Date:    April 26, 2023
# Author:  Jonathan A. Webb
# Purpose: Describe the types of testing to occur in this file.
# Instruction: This code can be run in hte following ways
#              - pytest # runs all functions beginnning with the word test in the
#                         directory
#              - pytest file_name.py # Runs all functions in file_name beginning
#                                      with the word test
#              - pytest file_name.py::test_func_name # Runs only the function
#                                                      titled test_func_name in
#                                                      the file_name.py file
#              - pytest -s # Runs tests and displays when a specific file
#                            has completed testing, and what functions failed.
#                            Also displays print statments
#              - pytest -v # Displays test results on a function by function
#              - pytest -p no:warnings # Runs tests and does not display warning
#                          messages
#              - pytest -s -v -p no:warnings # Displays relevant information and
#                                supports debugging
#              - pytest -s -p no:warnings # Run for record
# ==========================================================================================
# ==========================================================================================
# Insert Code here


def test_no_database():
    """
    This function tests the create_database function to ensure it fails properly
    if a user attempts to create a database with a name of an already existing
    database in that directory
    """
    # create a test database using create_database function
    file_name = "../data/test/duplicate_database"
    full_name = file_name + ".db"
    # create a test database using create_database function
    create_database(file_name)

    # redirect stderr to a buffer to capture warning messages
    old_stderr = sys.stderr
    sys.stderr = StringIO()

    # attempt to create the same database again
    create_database(file_name)

    msg = f"Database '{full_name}' already exists. Choose a different file name."
    # check that a warning message was printed to stderr
    warning_message = sys.stderr.getvalue()
    assert warning_message == msg

    # restore original stderr and delete the test database file
    sys.stderr = old_stderr

    # Delete filename if it exists
    if os.path.exists(file_name + ".db"):
        os.remove(file_name + ".db")


# ------------------------------------------------------------------------------------------


def test_create_database():
    """
    This function tests the create_database function to ensure it correctly
    creates a database.  This function ensures that the database is created, and
    that the database contains the correct schema
    """
    # create a test database using create_database function
    file_name = "../data/test/test_database"
    create_database(file_name)

    # connect to the test database
    conn = sqlite3.connect(file_name + ".db")

    # create a cursor object
    c = conn.cursor()

    # get a list of all tables in the database
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()

    # verify that the database has two tables: expenses and sales
    assert len(tables) == 2
    assert ("expenses",) in tables
    assert ("sales",) in tables

    # verify the schema of the expenses table
    c.execute("PRAGMA table_info(expenses)")
    columns = c.fetchall()
    expected_columns = [
        (0, "id", "INTEGER", 0, None, 1),
        (1, "date", "DATE", 1, None, 0),
        (2, "time", "TIME", 1, None, 0),
        (3, "expense_value", "REAL", 1, None, 0),
        (4, "company", "TEXT", 1, None, 0),
        (5, "description", "TEXT", 1, None, 0),
        (6, "modified_date", "DATE", 1, "CURRENT_DATE", 0),
        (7, "modified_time", "TIME", 1, "CURRENT_TIME", 0),
    ]
    assert columns == expected_columns

    # verify the schema of the sales table
    c.execute("PRAGMA table_info(sales)")
    columns = c.fetchall()
    expected_columns = [
        (0, "id", "INTEGER", 0, None, 1),
        (1, "date", "DATE", 1, None, 0),
        (2, "time", "TIME", 1, None, 0),
        (3, "first_name", "TEXT", 1, None, 0),
        (4, "last_name", "TEXT", 1, None, 0),
        (5, "email_address", "TEXT", 1, None, 0),
        (6, "phone_number", "TEXT", 0, None, 0),
        (7, "product_id", "INTEGER", 1, None, 0),
        (8, "modified_date", "DATE", 1, "CURRENT_DATE", 0),
        (9, "modified_time", "TIME", 1, "CURRENT_TIME", 0),
    ]
    assert columns == expected_columns

    # close the database connection
    conn.close()

    # Delete database if it exists
    if os.path.exists(file_name + ".db"):
        os.remove(file_name + ".db")


# ==========================================================================================
# ==========================================================================================
# eof
