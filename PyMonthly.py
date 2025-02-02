import pandas as pd
import PyMonthlyExpense as PE
import PyMonthlyRevenue as PI
import PyTableUtils as PTU
import subprocess

MONTHLY_EXPENSE_SHEET_NAME = "MonthlyExpense"
MONTHLY_REVENUE_SHEET_NAME = "MonthlyRevenue"

MONTHLY_EXPENSE_PATH = "Raw/MonthlyExpense.xlsx"
MONTHLY_REVENUE_PATH = "Raw/MonthlyRevenue.xlsx"

def updateTableValue():
    while True:
        try:
            print("\nEnter your choice from the options below:")
            print("1. Go back\n2. Expense\n3. Income")
            choice = int(input())

            if choice == 1:
                print("Exiting...")
                break
            elif choice == 2:
                PTU.genericUpdateValue(MONTHLY_EXPENSE_PATH, MONTHLY_EXPENSE_SHEET_NAME)
            elif choice == 3:
                PTU.genericUpdateValue(MONTHLY_REVENUE_PATH, MONTHLY_REVENUE_SHEET_NAME)
            else:
                print("Invalid choice. Please try again.")
        except Exception as e:
            print(f"Error: {e}. Please try again.")

def deleteTableRow():
    while True:
        try:
            print("\nEnter your choice from the options below:")
            print("1. Go back\n2. Expense\n3. Income")
            choice = int(input())

            if choice == 1:
                print("Exiting...")
                break
            elif choice == 2:
                PTU.genericDeleteRow(MONTHLY_EXPENSE_PATH, MONTHLY_EXPENSE_SHEET_NAME)
            elif choice == 3:
                PTU.genericDeleteRow(MONTHLY_REVENUE_PATH, MONTHLY_REVENUE_SHEET_NAME)
            else:
                print("Invalid choice. Please try again.")
        except Exception as e:
            print(f"Error: {e}. Please try again.")


def editTable():
    while True:
        try:
            print("\nEnter your choice from the options below:")
            print("1. Go back\n2. Update\n3. Delete")
            choice = int(input())

            if choice == 1:
                print("Exiting...")
                break
            elif choice == 2:
                updateTableValue()
            elif choice == 3:
                deleteTableRow()
            else:
                print("Invalid choice. Please try again.")
        except Exception as e:
            print(f"Error: {e}. Please try again.")


def query():
    while True:
        try:
            print("\nEnter your choice from the options below:")
            print("1. Quit\n2. Income\n3. Expense")
            choice = int(input())

            if choice == 1:
                print("Exiting...")
                break
            elif choice == 2:
                PI.query()
            elif choice == 3:
                PE.query()
            else:
                print("Invalid choice. Please try again.")
        except Exception as e:
            print(f"Error: {e}. Please try again.")


def menu():
    while True:
        try:
            print("\nEnter your choice from the options below:")
            print("1. Quit\n2. Income\n3. Expense\n4. Edit table")
            choice = int(input())

            if choice == 1:
                print("Exiting...")
                break
            elif choice == 2:
                cmd = ["python", "PyIncome.py"]
                subprocess.run(cmd, check=True)
            elif choice == 3:
                cmd = ["python", "PyExpense.py"]
                subprocess.run(cmd, check=True)
            elif choice == 4:
                editTable()
            else:
                print("Invalid choice. Please try again.")
        except Exception as e:
            print(f"Error: {e}. Please try again.")


if __name__ == "__main__":
    menu()
    
