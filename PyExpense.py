import pandas as pd
import openpyxl
from datetime import datetime
import os
import glob

import PyFunctionUtils as PFU
import CategoryInputs as CI

dir = "./"
expenseFiles = glob.glob("Raw/*_Expense.xlsx")

EXPENSE_COLUMNS = ["Amount", "Date", "Category", "Method", "RatioType", "Description"]
EXPENSE_CATEGORY_INPUT = CI.CategoryInput('Categories/expenseCategories.txt')
LIABILITY_INPUT = CI.CategoryInput("Categories/liability.txt")
RATIO_CATEGORY_INPUT = CI.CategoryInput("Categories/ratioTypes.txt")

EXPENSE_SHEET_NAME = "Expense"


def costInput():
    print("Enter the expense amount.")
    while True:
        try:
            amount = float(input())
            return amount
        except ValueError:
            print("Invalid amount given. Please try again.")



def expenseCategoryInput():
    return EXPENSE_CATEGORY_INPUT.get_category()
    

def paymentMethodInput():
    return LIABILITY_INPUT.get_category()

def ratioTypeInput():
    return RATIO_CATEGORY_INPUT.get_category()

def descriptionInput():
    return input("Enter a description of this expense (Optional): ")

def insertNewRow():
    income = costInput()
    exp_cat = expenseCategoryInput()
    date = PFU.date_input()
    paymentMethod = paymentMethodInput()
    ratioType = ratioTypeInput()
    description = descriptionInput()
    # Handle income sheet
    expenseTable = pd.DataFrame()
    try:
        expenseTable = pd.read_excel(f"Raw/{date.year}_Expense.xlsx", engine="openpyxl", sheet_name=EXPENSE_SHEET_NAME)
    except:
        expenseTable = pd.DataFrame(columns=EXPENSE_COLUMNS)
    new_row = pd.DataFrame({
        'Amount': [income],
        'Date': [date],
        'Category': [exp_cat],
        'PaymentMethod': [paymentMethod],
        'RatioType': [ratioType],
        'Description' : [description]
    })
    expenseTable = pd.concat([expenseTable, new_row], ignore_index=True)
    expenseTable.to_excel(f"Raw/{date.year}_Expense.xlsx", sheet_name=EXPENSE_SHEET_NAME, engine="openpyxl", index=False)
    return new_row


def query():
    expenseDF = pd.DataFrame()
    for excelFile in expenseFiles:
        yearDF = pd.read_excel(excelFile, engine="openpyxl", sheet_name=EXPENSE_SHEET_NAME)
        expenseDF = pd.concat([expenseDF, yearDF], ignore_index=True)

    while True:
        print("Choose one of the options from below:")
        print("1. Quit")
        print("2. Query")
        print("3. Monthly Report")
        print("4. View table")
        try:
            choice = int(input("Selection: "))
            if choice == 1:
                break
            elif choice == 2:
                while True:
                    query = input("Enter a query (or exit to quit): ")
                    if query == 'exit':
                        break
                    else:
                        print(expenseDF.query(query))
            elif choice == 3:
                expenseDF['Date'] = pd.to_datetime(expenseDF['Date'])
                while True:
                    try:
                        year = datetime.now().year
                        month = datetime.now().month
                        months = [
                                "January", "February", "March", "April", "May", "June", 
                                "July", "August", "September", "October", "November", "December"
                            ]
                        choice = int(input("Enter the number of months you'd like to see (0 to quit): "))
                        if choice == 0: 
                            break

                        #This needs initialized beforehand
                        period_report = pd.DataFrame(columns=["Amount", "Date", "Category", "PaymentMethod", "RatioType", "Description"])

                        for i in range(0, choice):
                            
                            print(months[month-1])
                            print("-------------")
                            result = expenseDF[(expenseDF["Date"].dt.year == year) & (expenseDF["Date"].dt.month == month)]
                            period_report = pd.concat([period_report, result], ignore_index=True)
                            print(result.sort_values(by='Date', ascending=True))
                            month = month - 1
                            if month == 0:
                                month = 12
                                year = year - 1

                        print(f"Total spending over period: {period_report['Amount'].sum()}")

                        #These are series objects of key-value timestamps. Don't worry about it.
                        start_date = pd.to_datetime(expenseDF['Date'].dt.to_period('M').dt.start_time[1])
                        end_date = pd.to_datetime(expenseDF['Date'].dt.to_period('M').dt.end_time[1])
                        all_dates = pd.date_range(start=start_date, end=end_date)
                        print(f"Average spending per day: {period_report.groupby('Date')['Amount'].sum().reindex(all_dates, fill_value=0).mean()}\n")
                        
                        # Group by category and sum the expenses
                        category_expenses = period_report.groupby('Category')['Amount'].sum().sort_values(ascending=False)
                        print(f"Category Spending")
                        print("-------------")
                        print(category_expenses)

                    except Exception as e:
                        print(f"Invalid selection: {e}")
            elif choice == 4:
                print(expenseDF)
        except Exception as e:
            print("Invalid selection.")

def menu():
    while True:
        try:
            print("\nEnter your choice from the options below:")
            print("1. Quit\n2. Query\n3. Enter new expense report")
            choice = int(input())

            if choice == 1:
                print("Exiting...")
                break
            elif choice == 2:
                query()
            elif choice == 3:
                insertNewRow()
            else:
                print("Invalid choice. Please try again.")
        except Exception as e:
            print(f"Error: {e}. Please try again.")

if __name__ == "__main__":
    menu()