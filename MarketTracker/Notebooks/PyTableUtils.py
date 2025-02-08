import PyHashUtils as PHU
import os
import pandas as pd

def addCrcHash(pd_dataframe):
    # Apply the function to each row to create the new CRC32 column
    pd_dataframe['CRC32'] = pd_dataframe.apply(lambda row: PHU.compute_crc32(row), axis=1)
    return pd_dataframe



def upsert_parquet(new_df, file_path, key_columns):
    """
    Upserts a Pandas DataFrame into a Parquet file based on key_columns.

    Parameters:
    - new_df: The new DataFrame to upsert.
    - file_path: The Parquet file path.
    - key_columns: List of columns to use as the unique key for upsert.

    Returns:
    - None (Writes back to the same Parquet file)
    """
    if os.path.exists(file_path):
        # Read existing data
        existing_df = pd.read_parquet(file_path)

        # Merge (remove old duplicates)
        updated_df = pd.concat([existing_df, new_df]).drop_duplicates(subset=key_columns, keep='last')
    else:
        # If file doesn't exist, use new DataFrame as is
        updated_df = new_df

    # Write back to Parquet
    updated_df.to_parquet(file_path, index=False)
