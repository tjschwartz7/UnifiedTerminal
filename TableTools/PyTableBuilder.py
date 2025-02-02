import pandas as pd
from datetime import datetime

if __name__ == "__main__":

    while True:
        print("Choose one of the options from below:")
        print("1. Quit")
        
        try:
            choice = int(input("Selection: "))

            if choice == 1:
                
                break
            
        except Exception as e:
            print(f"Invalid selection: {e}") 


