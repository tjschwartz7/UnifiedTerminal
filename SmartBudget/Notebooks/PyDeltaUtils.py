
import pandas as pd
from deltalake.writer import write_deltalake
from deltalake import DeltaTable


#Assumed that the dataframe is formatted properly!
def writeToDeltaTable(dataframe, deltaFilePath, conditionForMerge):
    dt = DeltaTable(deltaFilePath)
    
    # Convert new data to Delta Lake compatible format
    # This is a simplification; make sure your new data is in the same format as Delta tables (e.g., PyArrow, etc.)
    new_data_delta = DeltaTable.from_pandas(dataframe)

    


    write_deltalake(deltaFilePath, dataframe, mode="overwrite")

def deltaToDataframe(deltaFilePath):
    dt = DeltaTable(deltaFilePath)
    return dt.to_pandas()