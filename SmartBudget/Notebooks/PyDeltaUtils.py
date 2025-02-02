
import pandas as pd
from deltalake.writer import write_deltalake
from deltalake import DeltaTable


#Assumed that the dataframe is formatted properly!
def writeToDeltaTable(dataframe, deltaFilePath, conditionForMerge):
    dt = DeltaTable(deltaFilePath)
    
    # Convert new data to Delta Lake compatible format
    # This is a simplification; make sure your new data is in the same format as Delta tables (e.g., PyArrow, etc.)
    new_data_delta = DeltaTable.from_pandas(dataframe)

    
    # Perform the merge operation
    delta_table1.alias("target").merge(
        delta_table2.alias("source"),
        "target.CRC32 = source.CRC32"  # Merge condition on CRC32 column
    ).whenMatchedUpdate(
        condition="target.CRC32 = source.CRC32",  # Update only if CRC32 matches
        set={
            "Debit": "source.Debit",
            "Credit": "source.Credit",
            "Description": "source.Description",
            "Date": "source.Date"
        }
    ).whenNotMatchedInsert(
        values={
            "Debit": "source.Debit",
            "Credit": "source.Credit",
            "Description": "source.Description",
            "Date": "source.Date",
            "CRC32": "source.CRC32"
        }
    ).execute()

    write_deltalake(deltaFilePath, dataframe, mode="overwrite")

def deltaToDataframe(deltaFilePath):
    dt = DeltaTable(deltaFilePath)
    return dt.to_pandas()