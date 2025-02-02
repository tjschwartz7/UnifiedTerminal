import pandas as pd
from datetime import datetime
import PyGlobals as PG

DIR = "./"
CUR_YEAR = datetime.now().year
CUR_MONTH = datetime.now().month


def getTotalLiquidity(): 
    accounts = pd.read_excel(PG.getAccountPath(), engine="openpyxl", sheet_name=PG.getAccountSheet())

    assets = accounts[accounts['AccountType'] == 'Debit']
    liquidity = assets[assets['IsLiquid']]['AccountBalance'].sum()
    return liquidity

def getTotalIlliquidity():
    accounts = pd.read_excel(PG.getAccountPath(), engine="openpyxl", sheet_name=PG.getAccountSheet())

    assets = accounts[accounts['AccountType'] == 'Debit']
    illiquidity = assets[assets['IsLiquid'] == False]['AccountBalance'].sum()
    return illiquidity

def getDebtTable():
    accounts = pd.read_excel(PG.getAccountPath(), engine="openpyxl", sheet_name=PG.getAccountSheet())

    debt = accounts[(accounts['AccountType'] == 'Credit')]
    return debt

def getNonMortgageDebtTable():
    debt = getDebtTable()
    nonMortgageDebtTable =  debt[(debt['AccountName'] != 'Mortgage')]
    return nonMortgageDebtTable


def getAssetsTable():
    accounts = pd.read_excel(PG.getAccountPath(), engine="openpyxl", sheet_name=PG.getAccountSheet())

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
    
    income = pd.read_excel(PG.getMonthlyRevenuePath(), engine="openpyxl", sheet_name=PG.getMonthlyRevenueSheet())

    incomeByFrequency = income.groupby("Frequency")['Amount'].sum()
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
    expense = pd.read_excel(PG.getMonthlyExpensePath(), engine="openpyxl", sheet_name=PG.getMonthlyExpenseSheet())

    expenseByFrequency = expense.groupby("Frequency")['Amount'].sum()
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
    accounts = pd.read_excel(PG.getAccountPath(), engine="openpyxl", sheet_name=PG.getAccountSheet())
    savingsAccounts = accounts[accounts['AccountName'] == 'Savings']
    return savingsAccounts

def getTotalAssets():
    savingsAccounts = getSavingsAccountsTable()
    currentSavings = savingsAccounts['AccountBalance'].sum()
    return currentSavings

def getExpenseIncomeTable():
    accountTable = pd.read_excel(PG.getAccountPath(), engine="openpyxl", sheet_name=PG.getAccountSheet())
    expenseIncomeTable = accountTable.groupby('AccountType')['AccountBalance'].sum()
    return expenseIncomeTable

def getSpendByCategory():
    transactionTable = pd.read_excel(PG.getExpensePath(), engine="openpyxl", sheet_name=PG.getExpenseSheet())
    spendByCategoryTable = transactionTable.groupby('Category')['Amount']
    return spendByCategoryTable

def getPostExpenseTotal():
    totalExpenses = calculateMonthlyExpense()
    totalIncome = calculateMonthlyIncome()
    return totalIncome - totalExpenses

def getBabyStepsBudgetActualSpend():
    budget = pd.read_excel(PG.getBudgetPath(), engine="openpyxl", sheet_name=PG.getBudgetSheet())
    actualSpend = budget[budget['RatioType'] == 'Debt']['ActualCost'].sum()
    return actualSpend