from datetime import datetime

def getAccountPath():
    return "Raw/Account.xlsx"

def getAccountSheet():
    return "Account"

def getExpensePath(year=datetime.now().year):
    return f"Raw/{year}_Expense.xlsx"

def getExpenseSheet():
    return "Expense"

def getRevenuePath(year=datetime.now().year):
    return f"Raw/{year}_Revenue.xlsx"

def getRevenueSheet():
    return "Revenue"

def getMonthlyRevenuePath():
    return "Raw/MonthlyRevenue.xlsx"

def getMonthlyRevenueSheet():
    return "MonthlyRevenue"

def getMonthlyExpensePath():
    return "Raw/MonthlyExpense.xlsx"

def getMonthlyExpenseSheet():
    return "MonthlyExpense"

def getBudgetPath(month=datetime.now().month, year=datetime.now().year):
    return f"Raw/{year}{month:02d}_Budget.xlsx"

def getBudgetSheet():
    return "Budget"

