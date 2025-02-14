import subprocess
import os
import glob
import PyPageEditor as PGE
dir = "Pages/"

def delete_files():
    print('1. Quit')
    pages = glob.glob(f"{dir}*.txt")
    index = 2
    for page in pages:
        print(f'{index}. {page}')

    try:
        choice = int(input("Selection: "))
        
        if choice == 1:
            return
        
        page = pages[choice - 2]
        PGE.delete_file(os.path.abspath(page))
    except Exception as e:
        print(f"Invalid selection: {e}")

def edit_files():
    print('1. Quit')
    pages = glob.glob(f"{dir}*.txt")
    index = 2
    for page in pages:
        print(f'{index}. {page}')

    try:
        choice = int(input("Selection: "))
        
        if choice == 1:
            return
        
        page = pages[choice - 2]
        PGE.edit(os.path.abspath(page))
    except Exception as e:
        print(f"Invalid selection: {e}") 

if __name__ == "__main__":
    os.chdir('Notes/')
    while True:
        
        print("Choose one of the options from below:")
        print("1. Quit")
        print('2. New page')
        print('3. Edit page')
        print('4. Delete page')
        try:
            choice = int(input("Selection: "))
            if choice == 1:
                break
            elif choice == 2:
                page_name = input("New page name: ")
                PGE.create_empty_file(f'{dir}{page_name}')
            elif choice == 3:
                edit_files()
            elif choice == 4:
                delete_files()
        except Exception as e:
            print(f"Invalid selection: {e}") 