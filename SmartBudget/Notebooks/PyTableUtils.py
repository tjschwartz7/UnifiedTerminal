import PyHashUtils as PHU

def addCrcHash(dataframe):
    # Apply the function to each row to create the new CRC32 column
    dataframe['CRC32'] = dataframe.apply(lambda row: PHU.compute_crc32(row), axis=1)
    return dataframe

