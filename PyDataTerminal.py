import pandas as pd
import openpyxl
import subprocess
from datetime import datetime
import os

if __name__ == "__main__":
    while True:
        
        print("Choose one of the options from below:")
        print("1. Quit")
        print("2. Manual Budget Terminal")
        print("3. Smart Budget Terminal")
        print("4. Market Tracker")
        print('5. Notetaking')
        print('6. Savings Calculator')
        
        try:
            choice = int(input("Selection: "))

            if choice == 1:
                print("Thanks for using PyBudget! :)")
                break
            elif choice == 2:
                cmd = ["python", "ManualBudget/PyManualBudgetTerminal.py"]
                subprocess.run(cmd, check=True)
            elif choice == 3:
                cmd = ["python", "SmartBudget/PySmartBudgetTerminal.py"]
                subprocess.run(cmd, check=True)
            elif choice == 4:
                cmd = ["python", "MarketTracker/PyMarketTerminal.py"]
                subprocess.run(cmd, check=True)
            elif choice == 5:
                cmd = ["python", "Notes/PyNotes.py"]
                subprocess.run(cmd, check=True)
            elif choice == 6:
                cmd = ["python", "Calculators/SavingsCalculator.py"]
                subprocess.run(cmd, check=True)
        except Exception as e:
            print(f"Invalid selection: {e}") 


