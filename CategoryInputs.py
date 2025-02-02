
class CategoryInput:
    def __init__(self, categoryFile):
        self.categoryFile = categoryFile

    def get_category(self, newCategoriesAllowed=False):
        # Open the file in read mode
    
        while True:
            #This is superior windows code
            #os.system("cls")
            categories = []
            with open(self.categoryFile, 'r') as file:
                # Read lines into a list, removing the newline character
                categories = file.read().splitlines()

            if newCategoriesAllowed:
                print("\nSelect a category by number (0 to enter a new category):")
            else:
                print("\nSelect a category by number:")
            for i, lines in enumerate(categories, start=1):
                print(f"{i}. {lines}")
            try:
                choice = int(input())
                if choice == 0 and newCategoriesAllowed:
                    newCategory = input("Enter the new category: ")
                    with open(self.categoryFile, 'a') as file:
                        file.write(f"\n{newCategory}")
                elif 1 <= choice <= len(categories):
                    return categories[choice - 1]
                else:
                    print("Invalid option given. Please try again.")
            except ValueError as ve:
                print(f"Invalid option given. Please try again: {ve}")

