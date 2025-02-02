import pandas as pd
from datetime import datetime
import PyQuery as PQ
import PyCategoryInputs as CI
import PyGlobals as PG
import PyTableUtils as PTU

ACCOUNT_CATEGORY_INPUT = CI.CategoryInput("Categories/accounts.txt")
BANK_CATEGORY_INPUT = CI.CategoryInput("Categories/banks.txt")
LIABILITY_CATEGORY_INPUT = CI.CategoryInput("Categories/liability.txt")
ACCOUNT_COLUMNS = ["AccountName","AccountType", "BankName" ,"AccountBalance", "InterestRate", "IsLiquid"]

def getAccountTable():
    return PTU.createOrLoadTable(PG.getAccountPath(), PG.getAccountSheet(), cols=ACCOUNT_COLUMNS)

def bankInput():
    return BANK_CATEGORY_INPUT.get_category()

def accountInput():
    return ACCOUNT_CATEGORY_INPUT.get_category()

def liabilityInput():
    return LIABILITY_CATEGORY_INPUT.get_category()

def interestRateInput():
    while True:
        try:
            newInterestRate = float(input("Enter the interest rate %(0-100.0): "))
            return newInterestRate
        except Exception as e:
            print(f"Error: {e}. Please try again.")

def updateInterestRate():
    # Handle income sheet
    accountTable = getAccountTable()
    while True:
        try:
            print("Select which account you'd like to update:")
            print(accountTable)
            
            choice = int(input("Enter the number of your chosen column: "))
            if 0 <= choice < len(accountTable):
                
                try:
                    newInterestRate = float(input("Enter the new interest rate: "))
                    accountTable.loc[choice, 'InterestRate'] = newInterestRate
                except:
                    print("Invalid selection.")
                break
            else:
                print("Invalid choice. Please select a valid column number.")
        except Exception as e:
            print(f"Error: {e}. Please try again.")
    accountTable.to_excel(PG.getAccountPath(), sheet_name=PG.getAccountSheet(), engine="openpyxl", index=False)

def updateCreditBalance(transactionCost):
    # Handle income sheet
    accountTable = getAccountTable()
    creditAccounts = accountTable[accountTable['AccountType'] == 'Credit']
    while True:
        try:
            print("Select which account you'd like to update:")
            print(creditAccounts)
            
            choice = int(input("Enter the number of your chosen column: "))
                
            try:
                newBalance = creditAccounts.loc[choice, 'AccountBalance'] + transactionCost
                accountTable.loc[choice, 'AccountBalance'] = newBalance
                break
            except:
                print("Invalid selection.")
        except Exception as e:
            print(f"Error: {e}. Please try again.")
    accountTable.to_excel(PG.getAccountPath(), sheet_name=PG.getAccountSheet(), engine="openpyxl", index=False)

def updateDebitBalance(transactionCost):
    accountTable = getAccountTable()
    
    debitAccounts = accountTable[accountTable['AccountType'] == 'Debit']
    while True:
        try:
            print("Select which account you'd like to update:")
            print(debitAccounts)
            
            choice = int(input("Enter the number of your chosen column: "))
            newBalance = debitAccounts.loc[choice, 'AccountBalance'] + transactionCost
            accountTable.loc[choice, 'AccountBalance'] = newBalance
            break
        except Exception as e:
            print(f"Error: {e}. Please try again.")
    accountTable.to_excel(PG.getAccountPath(), sheet_name=PG.getAccountSheet(), engine="openpyxl", index=False)

def updateAccountBalance():
    accountTable = getAccountTable()
    while True:
        try:
            print("Select which account you'd like to update:")
            print(accountTable)
            
            choice = int(input("Enter the number of your chosen column: "))
            if 0 <= choice < len(accountTable):
                
                try:
                    newBalance = float(input("Enter the new account balance: "))
                    accountTable.loc[choice, 'AccountBalance'] = newBalance
                    break
                except:
                    print("Invalid selection.")
            else:
                print("Invalid choice. Please select a valid column number.")
        except Exception as e:
            print(f"Error: {e}. Please try again.")
    accountTable.to_excel(PG.getAccountPath(), sheet_name=PG.getAccountSheet(), engine="openpyxl", index=False)

def liquidityInput():
    while True:
        try:
            isNotLiquid = int(input("Is this account liquid? (0) Yes or (1) No: "))
            if isNotLiquid == 0:
                return "TRUE"
            elif isNotLiquid == 1:
                return "FALSE"
            else:
                print("Invalid selection.")
        except:
            print("Invalid selection: ")


def alterBalanceOnTwoAccounts(transactionCost):
    accountTable = getAccountTable()

    debitAccounts = accountTable[accountTable['AccountType'] == 'Debit']
    while True:
        try:
            print("Select which account the money is coming from:")
            print(debitAccounts)
            
            choice = int(input("Enter the number of your chosen column: "))
            try:
                currentBalance = accountTable.loc[choice, 'AccountBalance']
                accountTable.loc[choice, 'AccountBalance'] = currentBalance - transactionCost
                break
            except:
                print("Invalid selection.")
        except Exception as e:
            print(f"Error: {e}. Please try again.")   

    while True:
        try:
            print("Select which account the money is going into:")
            print(accountTable)
            
            choice = int(input("Enter the number of your chosen column: "))

            try:
                currentBalance = accountTable.loc[choice, 'AccountBalance']
                if accountTable.loc[choice, 'AccountType'] == 'Credit':
                    #Credit payments LOWER the balance...
                    accountTable.loc[choice, 'AccountBalance'] = currentBalance - transactionCost
                else:
                    #Debit payments INCREASE the balance
                    accountTable.loc[choice, 'AccountBalance'] = currentBalance + transactionCost
                break
            except:
                print("Invalid selection.")
        except Exception as e:
            print(f"Error: {e}. Please try again.")
    accountTable.to_excel(PG.getAccountPath(), sheet_name=PG.getAccountSheet(), engine="openpyxl", index=False)

def insertNewRow():
    accountTable = getAccountTable()
    accountName = accountInput()
    accountType = liabilityInput()
    bankName = bankInput()
    interestRate =interestRateInput()
    isLiquid = liquidityInput()
    accountBalance = 0.0
    new_row = pd.DataFrame({
        'AccountName': [accountName],
        'AccountType': [accountType],
        'BankName': [bankName],
        'AccountBalance': [accountBalance],
        'InterestRate': [interestRate],
        'IsLiquid': [isLiquid]
    })
    accountTable = pd.concat([accountTable, new_row], ignore_index=True)
    accountTable.to_excel(PG.getAccountPath(), sheet_name=PG.getAccountSheet(), engine="openpyxl", index=False)

def query():
    accountTable = getAccountTable()
    while True:
        print("Choose one of the options from below:")
        print("1. Quit")
        print("2. Query")
        print("3. Detailed Report")
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
                        print(accountTable.query(query))
            elif choice == 3:
                # Group by AccountType and sum AccountBalance
                print("Income vs. Expense")
                print("-------------")
                total_balances = PQ.getExpenseIncomeTable()
                print(total_balances)

                print("Assets")
                print("-------------")
                assets = PQ.getAssetsByLiquidityTable()
                # Loop through the results for a clean display
                for is_liquid, total in assets.items():
                    status = "Liquid Assets" if is_liquid else "Non-Liquid Assets"
                    print(f"{status}: ${total:,.2f}")
               
                input()
            elif choice == 4:
                print(accountTable)
        except:
            print("Invalid selection.")
            break


def menu():

    print("This menu is debug only.")
    while True:
        try:
            print("\nEnter your choice from the options below:")
            print("1. Quit\n2. View data\n3. Update balance\n4. Update interest rate\n5. Create new account\n6. View all accounts")
            print("7. Update credit balance\n8. Update debit balance")
            choice = int(input())

            if choice == 1:
                print("Exiting...")
                break
            elif choice == 2:
                query()
            elif choice == 3:
                updateAccountBalance()
            elif choice == 4:
                updateInterestRate()
            elif choice == 5:
                insertNewRow()
            elif choice == 6:
                accountTable = getAccountTable()
                print(accountTable)
            elif choice == 7:
                updateCreditBalance(0)
            elif choice == 8:
                updateDebitBalance(0)
            else:
                print("Invalid choice. Please try again.")
        except Exception as e:
            print(f"Error: {e}. Please try again.")

if __name__ == "__main__":
    menu()