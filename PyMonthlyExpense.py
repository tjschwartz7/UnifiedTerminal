import pandas as pd
from datetime import datetime
import CategoryInputs as CI

EXPENSE_CATEGORY_INPUT = CI.CategoryInput("Categories/expenseCategories.txt")
FREQUENCY_INPUT = CI.CategoryInput("Categories/frequencies.txt")
LIABILITY_CATEGORY_INPUT = CI.CategoryInput("Categories/liability.txt")
MONTHLY_EXPENSE_PATH = "Raw/MonthlyExpense.xlsx"
MONTHLY_EXPENSE_SHEET_NAME = "MonthlyExpense"
MONTHLY_EXPENSE_COLUMNS = ["Amount", "Frequency","Category", "Method", "Description"]

def expenseInput():
    print("Enter the expense amount.")
    while True:
        try:
            amount = float(input())
            return amount
        except ValueError:
            print("Invalid amount given. Please try again.")

def expenseFrequencyInput():
    return FREQUENCY_INPUT.get_category()


def expenseCategoryInput():
    return EXPENSE_CATEGORY_INPUT.get_category()
    

def paymentMethodInput():
    return LIABILITY_CATEGORY_INPUT.get_category()

def descriptionInput():
    return input("Enter a description of this expense (Optional): ")

def insertNewRow():
    # Handle income sheet
    try:
        expenseSheet = pd.read_excel(MONTHLY_EXPENSE_PATH, engine="openpyxl", sheet_name=MONTHLY_EXPENSE_SHEET_NAME)
    except:
        expenseSheet = pd.DataFrame(columns=MONTHLY_EXPENSE_COLUMNS)
    income = expenseInput()
    exp_freq = expenseFrequencyInput()
    exp_cat = expenseCategoryInput()
    paymentMethod = paymentMethodInput()
    description = descriptionInput()
    new_row = pd.DataFrame({
        'Amount': [income],
        'Frequency': [exp_freq],
        'Category': [exp_cat],
        'PaymentMethod': [paymentMethod],
        'Description' : [description]
    })
    expenseSheet = pd.concat([expenseSheet, new_row], ignore_index=True)
    expenseSheet.to_excel(MONTHLY_EXPENSE_PATH, sheet_name=MONTHLY_EXPENSE_SHEET_NAME, engine="openpyxl", index=False)

def query():
    # Handle income sheet
    try:
        expenseSheet = pd.read_excel(MONTHLY_EXPENSE_PATH, engine="openpyxl", sheet_name=MONTHLY_EXPENSE_SHEET_NAME)
    except:
        expenseSheet = pd.DataFrame(columns=MONTHLY_EXPENSE_COLUMNS)
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
                        print(expenseSheet.query(query))
            elif choice == 3:
                frequencyExpenses = expenseSheet.groupby('Frequency')['Amount'].sum()
                print(f"Expenses by frequency")
                print("-------------")
                print(frequencyExpenses)
                
                # Group by category and sum the expenses
                category_expenses = expenseSheet.groupby('Category')['Amount'].sum().sort_values(ascending=False)
                print(f"Category Spending")
                print("-------------")
                print(category_expenses)
                input()
            elif choice == 4:
                print(expenseSheet)

        except Exception as e:
            print(f"Invalid selection: {e}")

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
    

    