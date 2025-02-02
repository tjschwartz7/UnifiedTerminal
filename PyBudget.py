import pandas as pd
import PyRamseyPlanning as PRP



if __name__ == "__main__":

    while True:
        print("Choose one of the options from below:")
        print("1. Quit")
        print("2. See Baby Steps budget")
        
        try:
            choice = int(input("Selection: "))

            if choice == 1:
                break
            elif choice == 2:
                PRP.viewPlan()
                
            
        except Exception as e:
            print(f"Invalid selection: {e}") 


