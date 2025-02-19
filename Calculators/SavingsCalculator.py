

def inputLowBoundInterestRate():
    lowBoundInterest = 0
    while True:
        try:
            lowBoundInterest = int(input("Enter the low bound interest rate you're expecting (0<x<100): "))
            break
        except:
            print("Invalid input. Please try again.")
    return lowBoundInterest

def inputHighBoundInterestRate():
    highBoundInterest = 0
    while True:
        try:
            highBoundInterest = int(input("Enter the high bound interest rate you're expecting (0<x<100): "))
            break
        except:
            print("Invalid input. Please try again.")
    return highBoundInterest

def inputMonthlyIncome():
    income = 0
    while True:
        try:
            income = float(input("Enter your monthly income: "))
            break
        except:
            print("Invalid input. Please try again.")
    return income

def inputMonthlyExpenses():
    expenses = 0
    while True:
        try:
            expenses = float(input("Enter your monthly expenses: "))
            break
        except:
            print("Invalid input. Please try again.")
    return expenses

def inputMonthlySavings():
    monthlySavings = 0
    while True:
        try:
            monthlySavings = float(input("Enter your monthly savings: "))
            break
        except:
            print("Invalid input. Please try again.")
    return monthlySavings   

def inputCurrentSavings():
    currentSavings = 0
    while True:
        try:
            currentSavings = float(input("Enter your current savings balance: "))
            break
        except:
            print("Invalid input. Please try again.")
    return currentSavings   

def inputYearsToSave():
    numberYears = 0
    while True:
        try:
            numberYears = int(input("Enter the number of years you will be saving: "))
            break
        except:
            print("Invalid input. Please try again.")
    return numberYears   



if __name__  == '__main__':
    P = inputCurrentSavings()
    monthlyIncome = inputMonthlyIncome()
    lowBoundInterestRate = inputLowBoundInterestRate()
    highBoundInterestRate = inputHighBoundInterestRate()
    n = 12
    t = inputYearsToSave()

    percentagesSaved = {.15, .25, .35, .4, .5, .6}
    for savingsRate in percentagesSaved:
        monthlySavings = monthlyIncome * savingsRate
        print(f"\nAmount saved in {t} years assuming %{savingsRate} savings rate (${monthlySavings}): ")
        for r in range(lowBoundInterestRate, highBoundInterestRate+1, 1):
            newBalance = P
            for i in range(0, n*t, 1):
                
                newBalance = (newBalance+monthlySavings) * (1 + ((r/100) / n))
            print(f"With %{r} interest: {newBalance}")

    input()