import pandas as pd
import os
from datetime import datetime
import PyConfig as PC
import PyQuery as PQ

EMERGENCY_SAVINGS_BUFFER = PC.getEmergencySavingsBuffer()
EMERGENCY_SAVINGS_MONTHS = PC.getEmergencySavingMonths()
SUGGESTED_RENT_PERCENTAGE = PC.getEmergencyRentPercentage()
SUGGESTED_SAVINGS_PER_MONTH = PC.getEmergencySavingsPerMonth()
DEBUG = True

CUR_YEAR = datetime.now().year
CUR_MONTH = datetime.now().month
BUDGET_PATH = f"Raw/{CUR_YEAR}{CUR_MONTH}_MonthlyPlan.xlsx"
ACCOUNT_PATH = "Raw/Account.xlsx"
INCOME_PATH = "Raw/MonthlyRevenue.xlsx"


def getCurrentBabyStep(): 
    #Step 1
    #-Build up EMERGENCY_SAVINGS_BUFFER emergency savings
    #Step 2
    #-Pay off ALL debt (excluding mortgage right now) from smallest to largest balance
    #Step 3
    #-Save 3-6 months of expenses for emergency fund
    #Step 4
    #-Save 15 percent:
    #--Max Match 401K 
    #--Max Roth
    #--Remainder goes into Traditional 401k
    #Step 5
    #-Save for childrens college fund
    #Step 6
    #-Pay off mortgage
    #Step 7
    #-Build wealth with intentionality
    liquidity = PQ.getTotalLiquidity()
    nonMortgageDebt = PQ.getNonMortgageDebt()
    mortgage = PQ.getMortgage()
    currentStep = 1
    #The first step is to figure out how much emergency savings the user has
    if liquidity >= EMERGENCY_SAVINGS_BUFFER:
        currentStep = 2
        if nonMortgageDebt < 100:
            currentStep = 3
            if liquidity >= SUGGESTED_SAVINGS_PER_MONTH * EMERGENCY_SAVINGS_MONTHS:
                currentStep = 6
                if mortgage == 0:
                    currentStep = 7

    return currentStep


def insertRow(ratioType, percentMonthlyIncome):
    monthlyIncome = PQ.calculateMonthlyIncome()
    transactions = pd.read_excel(f"{CUR_YEAR}_Transaction.xlsx", engine="openpyxl", sheet_name="Transaction")

    currentMonthSpending = transactions[(transactions["TransactionDate"].dt.year == CUR_YEAR) & (transactions["TransactionDate"].dt.month == CUR_MONTH)]

    # Handle income sheet
    try:
        budget = pd.read_excel(BUDGET_PATH, engine="openpyxl", sheet_name="Budget")
    except:
        budget = pd.DataFrame(columns=["RatioType","PercentageMonthlyIncome", "BudgetedCost" ,"ActualCost", "Difference", "Month"])
    actualCost = currentMonthSpending[currentMonthSpending['RatioType'] == ratioType]['TransactionAmount'].sum()
    budgetCost = monthlyIncome*percentMonthlyIncome
    months = [
        "January", "February", "March", "April", "May", "June", 
        "July", "August", "September", "October", "November", "December"
    ]
    new_row = pd.DataFrame({
    'RatioType': [ratioType],
    'PercentageMonthlyIncome': [percentMonthlyIncome],
    'BudgetedCost': [budgetCost],
    'ActualCost': [actualCost],
    'Difference' : [budgetCost - actualCost],
    'Month':[months[CUR_MONTH-1]]
    })
    budget = pd.concat([budget, new_row], ignore_index=True)
    budget.to_excel(BUDGET_PATH, sheet_name="Budget", engine="openpyxl", index=False)

def viewPlan():
    currentStep = getCurrentBabyStep()
    loadSheet()

    # Handle income sheet
    try:
        budget = pd.read_excel(BUDGET_PATH, engine="openpyxl", sheet_name="Budget")
    except:
        budget = pd.DataFrame(columns=["RatioType","PercentageMonthlyIncome", "BudgetedCost" ,"ActualCost", "Difference", "Month"])

    #windows superiority
    os.system("cls")
    print(f"Step {currentStep} of budget plan")
    print(budget)

    currentLiquidity = PQ.getTotalLiquidity()

    print()
    if currentStep == 1:
        print(f"Current / Goal: (${currentLiquidity} / ${EMERGENCY_SAVINGS_BUFFER})")
        print(f"{currentLiquidity / EMERGENCY_SAVINGS_BUFFER} % Saved")
    elif currentStep == 2:
        actualSpend = PQ.getBabyStepsBudgetActualSpend()
        nonMortgageDebtTable = PQ.getNonMortgageDebtTable()
        nonMortgageDebt = PQ.getNonMortgageDebt()
        print(f"At your current rate of ${actualSpend} in debt payments per month,")
        if actualSpend == 0:
            print(f"you will never reach step three (zero non-mortgage debt)).")
        else:
            numMonths = nonMortgageDebt / actualSpend
            print(f"you will reach step three (zero non-mortgage debt) in {numMonths} months.")

        print("\nThe next loan you should pay off is: ")
        print(nonMortgageDebtTable[nonMortgageDebtTable['AccountBalance'] == nonMortgageDebtTable['AccountBalance'].min()])
        
    elif currentStep == 3:
        print(f"Current / Goal: (${currentLiquidity} / ${SUGGESTED_SAVINGS_PER_MONTH * EMERGENCY_SAVINGS_MONTHS})")
        print(f"{currentLiquidity / SUGGESTED_SAVINGS_PER_MONTH * EMERGENCY_SAVINGS_MONTHS} % Saved")

    print()
    overBudget = budget['Difference'].sum()
    if overBudget < 0:
        print(f"You are ${overBudget} over your budget.")
    else:
        print(f"You are ${overBudget} under your budget.")

    print()
    availableCashForSavings = PQ.getPostExpenseTotal()
    print(f"The total amount available (per month) after all of your expenses is ${availableCashForSavings}")

    bufferBetweenEmergencyBuffer = currentLiquidity - EMERGENCY_SAVINGS_BUFFER
    print(f"Your current liquidity: ${currentLiquidity}")
    print(f"Your emergency savings buffer: ${EMERGENCY_SAVINGS_BUFFER}")
    print(f"Difference: ${bufferBetweenEmergencyBuffer}")
    input()

def loadSheet():
    budget = pd.DataFrame(columns=["RatioType","PercentageMonthlyIncome", "BudgetedCost" ,"ActualCost", "Difference", "Month"])
    budget.to_excel(BUDGET_PATH, sheet_name="Budget", engine="openpyxl", index=False)
    currentStep = getCurrentBabyStep()
    
    if currentStep == 1 or currentStep == 3:
        insertRow("Needs", .8)
        insertRow("Debt", 0.0)
        insertRow("Mortgage", .15)
        insertRow("Wants", .05)
    elif currentStep == 2:
        insertRow("Needs", .3)
        insertRow("Debt", .5)
        insertRow("Mortgage", .15)
        insertRow("Wants", .05)
    elif currentStep == 6:
        insertRow("Needs", .4)
        insertRow("Debt", 0.0)
        insertRow("Mortgage", .4)
        insertRow("Wants", .2)
    elif currentStep == 7:
        insertRow("Needs", .5)
        insertRow("Debt", 0.0)
        insertRow("Mortgage", 0.0)
        insertRow("Wants", .5)

def menu():
    loadSheet()
    while True:
        print("Choose one of the options from below:")
        print("1. Quit")
        print("2. View automated plan")
        try:
            choice = int(input())

            if choice == 1:
                print("Exiting...")
                break
            elif choice == 2:
                viewPlan()
            else:
                print("Invalid choice. Please try again.")
        except Exception as e:
            print(f"Error: {e}. Please try again.")

if __name__ == "__main__":
    menu()
    


        

