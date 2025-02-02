import pandas as pd
from datetime import datetime
import glob

DIR = "./"
TRANSACTION_FILES = glob.glob("Raw/*_Expense.xlsx")

CUR_YEAR = datetime.now().year
CUR_MONTH = datetime.now().month
BUDGET_PATH = f"Raw/{CUR_YEAR}{CUR_MONTH}_MonthlyPlan.xlsx"
TRANSACTION_PATH = f"Raw/{CUR_YEAR}_Expense.xlsx"
ACCOUNT_PATH = "Raw/Account.xlsx"
INCOME_PATH = "Raw/Income.xlsx"
EXPENSE_PATH = "Raw/Expense.xlsx"


def getTotalLiquidity(): 
    accounts = pd.read_excel(ACCOUNT_PATH, engine="openpyxl", sheet_name="Account")

    assets = accounts[accounts['AccountType'] == 'Debit']
    liquidity = assets[assets['IsLiquid']]['AccountBalance'].sum()
    return liquidity

def getTotalIlliquidity():
    accounts = pd.read_excel(ACCOUNT_PATH, engine="openpyxl", sheet_name="Account")

    assets = accounts[accounts['AccountType'] == 'Debit']
    illiquidity = assets[assets['IsLiquid'] == False]['AccountBalance'].sum()
    return illiquidity

def getDebtTable():
    accounts = pd.read_excel(ACCOUNT_PATH, engine="openpyxl", sheet_name="Account")

    debt = accounts[(accounts['AccountType'] == 'Credit')]
    return debt

def getNonMortgageDebtTable():
    debt = getDebtTable()
    nonMortgageDebtTable =  debt[(debt['AccountName'] != 'Mortgage')]
    return nonMortgageDebtTable


def getAssetsTable():
    accounts = pd.read_excel(ACCOUNT_PATH, engine="openpyxl", sheet_name="Account")

    assets = accounts[accounts['AccountType'] == 'Debit']
    return assets

def getAssetsByLiquidityTable():
    debitAssets = getAssetsTable()
    assetsGroupedByLiquidity = debitAssets.groupby('IsLiquid')['AccountBalance'].sum()
    return assetsGroupedByLiquidity

def getNonMortgageDebt():
    debt = getDebtTable()
    nonMortgageDebt = debt[(debt['AccountName'] != 'Mortgage')]['AccountBalance'].sum()
    return nonMortgageDebt

def getMortgage():
    debt = getDebtTable()
    mortgage = debt[(debt['AccountName'] == 'Mortgage')]['AccountBalance'].sum()
    return mortgage

def calculateMonthlyIncome():
    
    income = pd.read_excel(INCOME_PATH, engine="openpyxl", sheet_name="Income")

    incomeByFrequency = income.groupby("IncomeFrequency")['IncomeAmount'].sum()
    monthlyIncome = 0
    try:
        sum = incomeByFrequency.loc['Weekly'] * 4
        monthlyIncome = monthlyIncome + sum
    except:
        ...

    try:
        sum = incomeByFrequency.loc['Bi-Weekly'] * 2
        monthlyIncome = monthlyIncome + sum
    except:
        ...

    try:
        sum = incomeByFrequency.loc['Monthly']
        monthlyIncome = monthlyIncome + sum
    except:
        ...

    try:
        sum = incomeByFrequency.loc['Annual'] / 12.0
        monthlyIncome = monthlyIncome + sum
    except:
        ...

    return monthlyIncome


def calculateMonthlyExpense():
    expense = pd.read_excel(EXPENSE_PATH, engine="openpyxl", sheet_name="Expense")

    expenseByFrequency = expense.groupby("ExpenseFrequency")['ExpenseAmount'].sum()
    monthlyExpense = 0
    try:
        sum = expenseByFrequency.loc['Weekly'] * 4
        monthlyExpense = monthlyExpense + sum
    except:
        ...

    try:
        sum = expenseByFrequency.loc['Bi-Weekly'] * 2
        monthlyExpense = monthlyExpense + sum
    except:
        ...

    try:
        sum = expenseByFrequency.loc['Monthly']
        monthlyExpense = monthlyExpense + sum
    except:
        ...

    try:
        sum = expenseByFrequency.loc['Annual'] / 12.0
        monthlyExpense = monthlyExpense + sum
    except:
        ...

    return monthlyExpense

def getSavingsAccountsTable():
    accounts = pd.read_excel(ACCOUNT_PATH, engine="openpyxl", sheet_name="Account")
    savingsAccounts = accounts[accounts['AccountName'] == 'Savings']
    return savingsAccounts

def getTotalAssets():
    savingsAccounts = getSavingsAccountsTable()
    currentSavings = savingsAccounts['AccountBalance'].sum()
    return currentSavings

def getExpenseIncomeTable():
    accountTable = pd.read_excel(ACCOUNT_PATH, engine="openpyxl", sheet_name="Account")
    expenseIncomeTable = accountTable.groupby('AccountType')['AccountBalance'].sum()
    return expenseIncomeTable

def getSpendByCategory():
    transactionTable = pd.read_excel(TRANSACTION_PATH, engine="openpyxl", sheet_name="Transaction")
    spendByCategoryTable = transactionTable.groupby('TransactionCategory')['TransactionAmount']
    return spendByCategoryTable

def getPostExpenseTotal():
    totalExpenses = calculateMonthlyExpense()
    totalIncome = calculateMonthlyIncome()
    return totalIncome - totalExpenses

def getBabyStepsBudgetActualSpend():
    budget = pd.read_excel(BUDGET_PATH, engine="openpyxl", sheet_name="Budget")
    actualSpend = budget[budget['RatioType'] == 'Debt']['ActualCost'].sum()
    return actualSpend