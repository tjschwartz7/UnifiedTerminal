import pandas as pd
import openpyxl
from datetime import datetime
import glob
import PyFunctionUtils as PFU
import PyCategoryInputs as CI
import PyGlobals as PG
import PyTableUtils as PTU

dir = "./"
revenueFiles = glob.glob("Raw/*_Revenue.xlsx")

REVENUE_CATEGORY_INPUT = CI.CategoryInput("Categories/revenueCategories.txt")
REVENUE_COLUMNS = ["Amount", "Date", "Source", "State"]

def revenueInput():
    print("What was the post-tax amount on earnings?")
    while True:
        try:
            revenue = float(input())
            return revenue
        except ValueError:
            print("Invalid amount given. Please try again.")


def revenueSourceInput():
    REVENUE_CATEGORY_INPUT.get_category()


def insertNewRow():
    revenue = revenueInput()
    date = PFU.date_input()
    in_src = revenueSourceInput()
    state = PFU.select_state()
    revenueSheet = PTU.createOrLoadTable(PG.getRevenuePath(year=date.year), PG.getRevenueSheet(), cols=REVENUE_COLUMNS)
    new_row = pd.DataFrame({
        'Amount': [revenue],
        'Date': [date],
        'Source': [in_src],
        'State': [state]
    })
    revenueSheet = pd.concat([revenueSheet, new_row], ignore_index=True)
    revenueSheet.to_excel(PG.getRevenuePath(year=date.year), sheet_name=PG.getRevenueSheet(), engine="openpyxl", index=False)
    return new_row

def query():
    revenueDF = pd.DataFrame()
    for excelFile in revenueFiles:
        yearDF = pd.read_excel(excelFile, engine="openpyxl", sheet_name=PG.getRevenueSheet())
        revenueDF = pd.concat([revenueDF, yearDF], ignore_index=True)
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
                        print(revenueDF.query(query))
            elif choice == 3:
                revenueDF['Date'] = pd.to_datetime(revenueDF['Date'])
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
                        period_report = pd.DataFrame(columns=REVENUE_COLUMNS)

                        for i in range(0, choice):
                            
                            print(months[month-1])
                            print("-------------")
                            result = revenueDF[(revenueDF["Date"].dt.year == year) & (revenueDF["Date"].dt.month == month)]
                            period_report = pd.concat([period_report, result], ignore_index=True)
                            print(result.sort_values(by='Date', ascending=True))
                            month = month - 1
                            if month == 0:
                                month = 12
                                year = year - 1

                        print(f"Total revenue over period: {period_report['Amount'].sum()}")
                        #These are series objects of key-value timestamps. Don't worry about it.
                        start_date = pd.to_datetime(revenueDF['Date'].dt.to_period('M').dt.start_time[1])
                        end_date = pd.to_datetime(revenueDF['Date'].dt.to_period('M').dt.end_time[1])
                        all_dates = pd.date_range(start=start_date, end=end_date)
                        print(f"Average revenue per day: {period_report.groupby('Date')['Amount'].sum().reindex(all_dates, fill_value=0).mean()}\n")
                        
                        # Group by category and sum the expenses
                        source_revenue = period_report.groupby('Source')['Amount'].sum().sort_values(ascending=False)
                        print(f"Revenue by Source")
                        print("-------------")
                        print(source_revenue)
                    except Exception as e:
                        print(f"Invalid selection: {e}")
            elif choice == 4:
                print(revenueDF)
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

    