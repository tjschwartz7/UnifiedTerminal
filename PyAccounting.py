import pandas as pd
from datetime import datetime
import PyExpense as PT
import PyAccount as PA
import PyRevenue as PE
import PyTableUtils as PTU


def newTransaction():
    insertedRow = PT.insertNewRow()
    if insertedRow.loc[0, 'PaymentMethod'] == 'Credit':
        PA.updateCreditBalance(insertedRow.loc[0, 'Amount'])
    else:
        PA.updateDebitBalance(insertedRow.loc[0, 'Amount'])

def newEarnings():
    insertedRow = PE.insertNewRow()
    newEarnings = insertedRow.loc[0, 'Amount']
    PA.updateDebitBalance(newEarnings)

def query():
    while True:
        try:
            print("\nEnter your choice from the options below:")
            print("1. Quit\n2. Account\n3. Transaction\n4. Earnings")
            choice = int(input())

            if choice == 1:
                print("Exiting...")
                break
            elif choice == 2:
                PA.query()
            elif choice == 3:
                PT.query()
            elif choice == 4:
                PE.query()
            else:
                print("Invalid choice. Please try again.")
        except Exception as e:
            print(f"Error: {e}. Please try again.")

def updateTableValue():
    while True:
        try:
            print("\nEnter your choice from the options below:")
            print("1. Go back\n2. Account\n3. Transaction\n4. Earnings")
            choice = int(input())

            if choice == 1:
                print("Exiting...")
                break
            elif choice == 2:
                PTU.genericUpdateValue("Raw/Account.xlsx", "Account")

            elif choice == 3:
                year = datetime.now().year
                PTU.genericUpdateValue(f"Raw/{year}_Expense.xlsx", "Expense")
            elif choice == 4:
                year = datetime.now().year
                PTU.genericUpdateValue(f"Raw/{year}_Revenue.xlsx", "Revenue")
            else:
                print("Invalid choice. Please try again.")
        except Exception as e:
            print(f"Error: {e}. Please try again.")

def deleteTableRow():
    while True:
        try:
            print("\nEnter your choice from the options below:")
            print("1. Go back\n2. Account\n3. Transaction\n4. Earnings")
            choice = int(input())

            if choice == 1:
                print("Exiting...")
                break
            elif choice == 2:
                PTU.genericDeleteRow("Raw/Account.xlsx", "Account")

            elif choice == 3:
                year = datetime.now().year
                PTU.genericDeleteRow(f"Raw/{year}_Expense.xlsx", "Expense")
            elif choice == 4:
                year = datetime.now().year
                PTU.genericDeleteRow(f"Raw/{year}_Revenue.xlsx", "Revenue")
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

def menu():
    while True:
        try:
            print("\nEnter your choice from the options below:")
            print("1. Quit\n2. Move money between accounts\n3. New transaction\n4. New earnings")
            print("5. New account\n6. Query\n7. Edit table")
            choice = int(input())

            if choice == 1:
                print("Exiting...")
                break
            elif choice == 2:
                PA.alterBalanceOnTwoAccounts(PT.costInput())

            elif choice == 3:
                newTransaction()
            elif choice == 4:
                newEarnings()
            elif choice == 5:
                PA.insertNewRow()
            elif choice == 6:
                query()
            elif choice == 7:
                editTable()
            else:
                print("Invalid choice. Please try again.")
        except Exception as e:
            print(f"Error: {e}. Please try again.")

if __name__ == "__main__":
    menu()
    

