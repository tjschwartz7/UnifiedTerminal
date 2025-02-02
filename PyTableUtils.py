import pandas as pd


def convert_to_dtype(value, dtype):
    """
    Convert the input value to the target data type.
    
    Parameters:
        value (str): The user input as a string.
        dtype: The target data type (from pandas dtype).
        
    Returns:
        The converted value.
    """
    try:
        if pd.api.types.is_integer_dtype(dtype):
            return int(value)
        elif pd.api.types.is_float_dtype(dtype):
            return float(value)
        elif pd.api.types.is_bool_dtype(dtype):
            # Handle boolean inputs
            if value.lower() in ['true', 'yes', '1']:
                return True
            elif value.lower() in ['false', 'no', '0']:
                return False
            else:
                raise ValueError("Invalid boolean value.")
        elif pd.api.types.is_string_dtype(dtype):
            return str(value)
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            # Handle datetime inputs
            return pd.to_datetime(value)
        else:
            raise ValueError(f"Unsupported data type: {dtype}")
    except ValueError as e:
        raise ValueError(f"Failed to convert '{value}' to {dtype}: {e}")



def genericUpdateValue(path, sheetName, custom_prompt="Enter the new value:"):

    dataframe = pd.read_excel(path, engine="openpyxl", sheet_name=sheetName)
    try:
        print("Please select one of the following (col then row): ")
        while True:
            try:
                for index, col in enumerate(dataframe.columns):
                    print(f"{index}. {col}")
                col = int(input("Please select the column you want to update (negative number to exit): "))
                if col < 0: 
                    break
                colName = dataframe.columns[col]


                for index, row in dataframe.iterrows():
                    print(f"\nIndex: {index}. \n{row}")
                row = int(input("Please select the row you want to update (negative number to exit): "))
                if row < 0: 
                    break
                # Show the current value
                current_value = dataframe.at[row, colName]
                current_dtype = dataframe[colName].dtype



                # Get the new value from the user
                while True:
                    try:
                        new_value = input(f"Enter the new value (type: {current_dtype}): ")
                        converted_value = convert_to_dtype(new_value, current_dtype)
                        
                        break  # Exit the loop if conversion is successful
                    except ValueError as e:
                        print(f"Error: {e}. The passed value was invalid.") 
                        
                dataframe.loc[row, colName] = converted_value
                dataframe.to_excel(path, sheet_name=sheetName, engine="openpyxl", index=False)
                break

                

            except:
                print("Invalid selection. Please try again.")
    except Exception as e:
        print(f"Error: {e}")
    
def genericDeleteRow(path, sheetName):
    print("Please be very careful using this function to maintain consistency with the data.")
    print("Values are NOT checked for correctness in this function!")

    dataframe = pd.read_excel(path, engine="openpyxl", sheet_name=sheetName)
    try:
        print("Please select one of the following (col then row): ")
        while True:
            try:

                for index, row in dataframe.iterrows():
                    print(f"\nIndex: {index}. \n{row}")
                row = int(input("Please select the row you want to delete (negative number to exit): "))
                if row < 0: 
                    break
                dataframe.drop(index)
                break

                

            except:
                print("Invalid selection. Please try again.")
    except Exception as e:
        print(f"Error: {e}")

def createOrLoadTable(filepath, sheetname, cols=[]):
    try:
        table = pd.read_excel(filepath, engine="openpyxl", sheet_name=sheetname)
    except:
        # Handle no existing sheet case
        table = pd.DataFrame(columns=cols)
    return table

def createNewTable(cols=[]):
    return pd.DataFrame(columns=cols)

