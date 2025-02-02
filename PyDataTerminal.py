import pandas as pd
import openpyxl
import subprocess
from datetime import datetime
import os

if __name__ == "__main__":

    while True:
        print("Choose one of the options from below:")
        print("1. Quit")
        print("2. Monthly")
        print("3. Accounts")
        print("4. Budgeting")
        print("5. Create backup")
        
        try:
            choice = int(input("Selection: "))

            if choice == 1:
                print("Thanks for using PyBudget! :)")
                break
            elif choice == 2:
                cmd = ["python", "PyMonthly.py"]
                subprocess.run(cmd, check=True)
            elif choice == 3:
                cmd = ["python", "PyAccounting.py"]
                subprocess.run(cmd, check=True)
            elif choice == 4:
                cmd = ["python", "PyBudget.py"]
                subprocess.run(cmd, check=True)
            elif choice == 5:
                cmd = ["python", "PyBackup.py"]
                subprocess.run(cmd, check=True)
            
        except Exception as e:
            print(f"Invalid selection: {e}") 


