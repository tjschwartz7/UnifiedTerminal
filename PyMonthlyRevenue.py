import pandas as pd
import openpyxl
from datetime import datetime
import CategoryInputs as CI
import PyFunctionUtils as PFU

MONTHLY_REVENUE_PATH = "Raw/MonthlyRevenue.xlsx"
MONTHLY_REVENUE_SHEET_NAME = "MonthlyRevenue"
FREQUENCY_INPUT = CI.CategoryInput("Categories/frequencies.txt")
INCOME_CATEGORY_INPUT = CI.CategoryInput("Categories/revenueCategories.txt")

def revenueInput():
    print("What is the post-tax amount on revenue?")
    while True:
        try:
            revenue = float(input())
            return revenue
        except ValueError:
            print("Invalid amount given. Please try again.")

def revenueFrequencyInput():
    return FREQUENCY_INPUT.get_category()

def revenueSourceInput():
    return INCOME_CATEGORY_INPUT.get_category()


def insertNewRow():
    # Handle revenue sheet
    try:
        revenueSheet = pd.read_excel(MONTHLY_REVENUE_PATH, engine="openpyxl", sheet_name=MONTHLY_REVENUE_SHEET_NAME)
    except:
        revenueSheet = pd.DataFrame(columns=["Amount", "Frequency", "Source", "State"])
    revenue = revenueInput()
    in_freq = revenueFrequencyInput()
    in_src = revenueSourceInput()
    state = PFU.select_state()
    new_row = pd.DataFrame({
        'Amount': [revenue],
        'Frequency': [in_freq],
        'Source': [in_src],
        'State': [state]
    })
    revenueSheet = pd.concat([revenueSheet, new_row], ignore_index=True)
    revenueSheet.to_excel(MONTHLY_REVENUE_PATH, sheet_name=MONTHLY_REVENUE_SHEET_NAME, engine="openpyxl", index=False)

def query():

    # Handle revenue sheet
    try:
        revenueSheet = pd.read_excel(MONTHLY_REVENUE_PATH, engine="openpyxl", sheet_name=MONTHLY_REVENUE_SHEET_NAME)
    except:
        revenueSheet = pd.DataFrame(columns=["Amount", "Frequency", "Source", "State"])
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
                        print(revenueSheet.query(query))
            elif choice == 3:
                print("Revenue by frequency")
                print("-------------")
                print(revenueSheet.groupby("Frequency")['Amount'].sum())
            elif choice == 4:
                print(revenueSheet)
        except:
            print("Invalid selection.")
            break

def menu():
    while True:
        try:
            print("\nEnter your choice from the options below:")
            print("1. Quit\n2. View data\n3. Enter new revenue statement")
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
    