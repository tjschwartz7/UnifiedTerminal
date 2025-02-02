import pandas as pd
from datetime import datetime
import PyExpense as PE
import PyAccount as PA
import PyRevenue as PR
import PyGlobals as PG
import PyTableUtils as PTU


def newTransaction():
    insertedRow = PE.insertNewRow()
    if insertedRow.loc[0, 'PaymentMethod'] == 'Credit':
        PA.updateCreditBalance(insertedRow.loc[0, 'Amount'])
    else:
        PA.updateDebitBalance(insertedRow.loc[0, 'Amount']*-1) #Negative because its a cost

def newEarnings():
    insertedRow = PE.insertNewRow()
    newEarnings = insertedRow.loc[0, 'Amount']
    PA.updateDebitBalance(newEarnings)

def query():
    while True:
        try:
            print("\nEnter your choice from the options below:")
            print("1. Quit\n2. Account\n3. Expense\n4. Revenue")
            choice = int(input())

            if choice == 1:
                print("Exiting...")
                break
            elif choice == 2:
                PA.query()
            elif choice == 3:
                PE.query()
            elif choice == 4:
                PR.query()
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
                PTU.genericUpdateValue(PG.getAccountPath(), PG.getAccountSheet())

            elif choice == 3:
                year = datetime.now().year
                PTU.genericUpdateValue(PG.getExpensePath(year=year), PG.getExpenseSheet())
            elif choice == 4:
                year = datetime.now().year
                PTU.genericUpdateValue(PG.getRevenuePath(year=year), PG.getRevenueSheet())
            else:
                print("Invalid choice. Please try again.")
        except Exception as e:
            print(f"Error: {e}. Please try again.")

def deleteTableRow():
    while True:
        try:
            print("\nEnter your choice from the options below:")
            print("1. Go back\n2. Account\n3. Expense\n4. Revenue")
            choice = int(input())

            if choice == 1:
                print("Exiting...")
                break
            elif choice == 2:
                PTU.genericDeleteRow(PG.getAccountPath(), PG.getAccountSheet())

            elif choice == 3:
                year = datetime.now().year
                PTU.genericDeleteRow(PG.getExpensePath(year=year), PG.getExpenseSheet())
            elif choice == 4:
                year = datetime.now().year
                PTU.genericDeleteRow(PG.getRevenuePath(year=year), PG.getRevenueSheet())
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
                PA.alterBalanceOnTwoAccounts(PE.costInput())

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
    

