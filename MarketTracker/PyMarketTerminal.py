import pandas as pd
import openpyxl
import subprocess
from datetime import datetime
import os

def run_notebooks():
    try:
        cmd = ["python", "Notebooks/PySP.py"]
        subprocess.run(cmd, check=True)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    os.chdir('MarketTracker/')
    run_notebooks()

    while True:
        
        print("Choose one of the options from below:")
        print("1. Quit")
        
        try:
            choice = int(input("Selection: "))

            if choice == 1:
                break

            
        except Exception as e:
            print(f"Invalid selection: {e}") 


