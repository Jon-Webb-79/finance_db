# Import necessary packages here
import os
import sqlite3
import sys
from io import StringIO

import pytest

from finance_db.database import add_expense, create_database, update_expense_type

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

    msg = f"Database '{full_name}' already exists. Choose a different file name.\n"
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
    file_name = "../data/test/duplicate_database"
    create_database(file_name)
    file_name += ".db"

    conn = sqlite3.connect(file_name)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    assert len(tables) == 2  # two tables should be created

    cursor.execute("SELECT * FROM expenses")
    expenses_columns = [description[0] for description in cursor.description]
    assert "id" in expenses_columns
    assert "date" in expenses_columns
    assert "time" in expenses_columns
    assert "expense_type" in expenses_columns
    assert "expense_value" in expenses_columns
    assert "company" in expenses_columns
    assert "description" in expenses_columns
    assert "modified_date" in expenses_columns
    assert "modified_time" in expenses_columns

    cursor.execute("SELECT * FROM sales")
    sales_columns = [description[0] for description in cursor.description]
    assert "id" in sales_columns
    assert "date" in sales_columns
    assert "time" in sales_columns
    assert "first_name" in sales_columns
    assert "last_name" in sales_columns
    assert "email_address" in sales_columns
    assert "phone_number" in sales_columns
    assert "product_id" in sales_columns
    assert "modified_date" in sales_columns
    assert "modified_time" in sales_columns

    # clean up
    conn.close()
    if os.path.exists("../data/test/test_database1.db"):
        os.remove("../data/test/test_database1.db")


# ------------------------------------------------------------------------------------------


def test_add_expense_with_invalid_expense_type():
    """
    This function tests the add_expense function to ensure it fails nicely and incorrect
    expense_type is entered
    """
    # Create a test database
    create_database("../data/test/test_database1")
    # Try to add an expense with an invalid expense type
    with pytest.raises(ValueError):
        add_expense(
            "../data/test/test_database1.db",
            "Invalid expense type",
            100.0,
            "Test Company",
            "Test description",
        )
    if os.path.exists("../data/test/test_database1.db"):
        os.remove("../data/test/test_database1.db")


# ------------------------------------------------------------------------------------------


def test_add_expense_no_database(capfd):
    """
    This function tests the add_expense function to ensure it fails properly if there
    is not database to add data to
    """
    file_name = "../data/test/no_database.db"
    add_expense(file_name, "debit", 100.0, "Test_Company", "Test Description")
    # Check that the error message was printed to stderr

    _, err = capfd.readouterr()
    expected_error_message = f"Database '{file_name}' does not exist."
    assert err == expected_error_message


# ------------------------------------------------------------------------------------------


def test_add_expense():
    """
    This function tests the add_expense function to ensure it properly enters
    a row to the expense table
    """
    # Create a test database
    file_name = "../data/test/test_database3"
    create_database(file_name)
    file_name += ".db"

    # Add a debit expense to the database
    expense_type = "debit"
    expense_value = 50.0
    company = "Test Company 1"
    description = "Test description 1"
    add_expense(file_name, expense_type, expense_value, company, description)

    # open the database and verify the expense was added
    conn = sqlite3.connect(file_name)
    c = conn.cursor()
    c.execute("SELECT * FROM expenses WHERE company='Test Company 1'")
    expense = c.fetchall()
    assert expense[0][3] == "debit"
    assert expense[0][4] == 50.0
    assert expense[0][5] == "Test Company 1"
    assert expense[0][6] == "Test description 1"
    # Delete the test database
    conn.close()

    # Delete the test database
    if os.path.exists(file_name):
        os.remove(file_name)


# ------------------------------------------------------------------------------------------


def test_update_expense_type():
    """
    This function tests the update_expense_type function to ensure it properly enters
    a row to the expense table
    """
    # Create a test database
    file_name = "../data/test/test_database4"
    create_database(file_name)
    file_name += ".db"

    # Add a debit expense to the database
    expense_type = "debit"
    expense_value = 50.0
    company = "Test Company 1"
    description = "Test description 1"
    add_expense(file_name, expense_type, expense_value, company, description)
    update_expense_type(file_name, 1, "credit")

    # open the database and verify the expense was added
    conn = sqlite3.connect(file_name)
    c = conn.cursor()
    c.execute("SELECT * FROM expenses WHERE company='Test Company 1'")
    expense = c.fetchall()
    assert expense[0][3] == "credit"
    assert expense[0][4] == 50.0
    assert expense[0][5] == "Test Company 1"
    assert expense[0][6] == "Test description 1"
    # Delete the test database
    conn.close()

    # Delete the test database
    if os.path.exists(file_name):
        os.remove(file_name)


# ==========================================================================================
# ==========================================================================================
# eof
