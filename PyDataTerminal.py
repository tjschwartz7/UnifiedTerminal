import pandas as pd
import openpyxl
import subprocess
from datetime import datetime
import os

if __name__ == "__main__":

    while True:
        
        print("Choose one of the options from below:")
        print("1. Quit")
        print("2. Budget Terminal")
        
        try:
            choice = int(input("Selection: "))

            if choice == 1:
                print("Thanks for using PyBudget! :)")
                break
            elif choice == 2:
                cmd = ["python", "Budget/PyBudgetTerminal.py"]
                subprocess.run(cmd, check=True)
                os.chdir('../')

            
        except Exception as e:
            print(f"Invalid selection: {e}") 


