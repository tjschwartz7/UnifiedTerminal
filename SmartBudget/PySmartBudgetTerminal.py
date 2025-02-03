import pandas as pd
import openpyxl
import subprocess
from datetime import datetime
import os

def run_notebooks():
    try:
        cmd = ["python", "Notebooks/PyCiti.py"]
        subprocess.run(cmd, check=True)

        cmd = ["python", "Notebooks/PyFidelity.py"]
        subprocess.run(cmd, check=True)

        cmd = ["python", "Notebooks/PyMarcus.py"]
        subprocess.run(cmd, check=True)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    os.chdir('SmartBudget/')
    run_notebooks()

    while True:
        
        print("Choose one of the options from below:")
        print("1. Quit")
        
        try:
            choice = int(input("Selection: "))

            if choice == 1:
                print("Thanks for using PyBudget! :)")
                break

            
        except Exception as e:
            print(f"Invalid selection: {e}") 


