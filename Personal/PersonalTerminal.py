import subprocess
import os

def run_notebooks():
    try:
        cmd = ["python", "Notebooks/PySourceCreator.py"]
        subprocess.run(cmd, check=True)
    except Exception as e:
        print(f"Error: {e}")

prepend = 'Enriched/'
files = ['Boundaries', 'Emotions', 'FeelingTracker', 'Goals', 'Likes', 'Needs', 'Parts']


def file_functions(file):
    print('1. Quit')
    print('2. Insert')
    try:
        choice = int(input("Selection: "))
        
        if choice == 1:
            return

        choice = choice - 2
        file = files[choice]
        file_functions(prepend + file + '/' + file + '.parquet')

        
    except Exception as e:
        print(f"Invalid selection: {e}") 

def alter_table():
    i = 2
    for file in files:
        print(f"{i}. {file}")
        i = i + 1
    
    try:
        choice = int(input("Selection: "))
        
        if choice == 1:
            return

        choice = choice - 2
        file = files[choice]
        file_functions(prepend + file + '/' + file + '.parquet')
    except Exception as e:
        print(f"Invalid selection: {e}") 

if __name__ == "__main__":
    os.chdir('Personal/')
    run_notebooks()

    while True:
        
        print("Choose one of the options from below:")
        print("1. Quit")
        print('2. Alter table')
        print('3. Insert new goal')

        try:
            choice = int(input("Selection: "))
            
            if choice == 1:
                break
            elif choice == 2:
                alter_table()
            
            

        except Exception as e:
            print(f"Invalid selection: {e}") 
        

            




