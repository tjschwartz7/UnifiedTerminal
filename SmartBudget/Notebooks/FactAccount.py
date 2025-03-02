import pandas as pd
from datetime import datetime
import os


SRC_ENRICHED_PATH = "Enriched/"
SRC_ENRICHED_LORMET_PATH = "Enriched/Lormet/LormetTable.parquet"
SRC_ENRICHED_FIDELITY_PATH = "Enriched/Fidelity/FidelityTable.parquet"
SRC_ENRICHED_MARCUS_PATH = "Enriched/Marcus/MarcusTable.parquet"
SRC_ENRICHED_CITI_PATH = "Enriched/CitiAccount/CitiTable.parquet"
DEST_CURATED_PATH = 'Curated/FactAccount.parquet'

COLUMNS=['Date', 'Balance', 'Credit', 'Debit', 'Type', 'Sub Type', 'Name,' 'Institution', 'Description', 'CRC32']

def Transform():
    lormetDF = pd.read_parquet(SRC_ENRICHED_LORMET_PATH)
    fidelityDF = pd.read_parquet(SRC_ENRICHED_FIDELITY_PATH)
    marcusDF = pd.read_parquet(SRC_ENRICHED_MARCUS_PATH)
    citiDF = pd.read_parquet(SRC_ENRICHED_CITI_PATH)

    #['Date', 'Description', 'Amount', 'Balance', 'Account Type', 'CRC32']
    #print(lormetDF.columns)
    #print()
    #['Type', 'Sub Type', 'Account Name', 'Institution', 'Balance', 'Balance As Of', 'Hidden', 'CRC32']
    #print(fidelityDF.columns)
    #print()
    #['CRC32', 'Date', 'Description', 'Credits', 'Debits', 'Balance']
    #print(marcusDF.columns)
    #print()
    #['CRC32', 'Status', 'Date', 'Description', 'Debit', 'Credit']
    #print(citiDF.columns)

    #Add columns where necessary

    try:
        lormetDF = lormetDF.rename(columns={'Amount': 'Debit', 'Account Type': 'Name'})

        lormetDF['Institution'] = 'Lormet'
        lormetDF['Type'] = 'Brokerage'
        lormetDF['Sub Type'] = lormetDF['Type']
        lormetDF['Credit'] = 0
        lormetDF['Date'] = pd.to_datetime(lormetDF['Date'])
        lormetDF.reindex(columns=COLUMNS)

        print(lormetDF)

        marcusDF = marcusDF.rename(columns={'Debits': 'Debit'})

        marcusDF['Name'] = 'High Yield Savings'
        marcusDF['Institution'] = 'Marcus'
        marcusDF['Type'] = 'Brokerage'
        marcusDF['Sub Type'] = marcusDF['Type']
        marcusDF['Date'] = pd.to_datetime(marcusDF['Date'])
        marcusDF.reindex(columns=COLUMNS)
        print(marcusDF)

        citiDF['Name'] = 'Loan'
        citiDF['Institution'] = 'Citi'
        citiDF['Type'] = 'Credit cards'
        citiDF['Sub Type'] = 'Credit cards'
        citiDF['Balance'] = pd.NA
        citiDF.drop(columns=["Status"], inplace=True)
        citiDF['Date'] = pd.to_datetime(citiDF['Date'])
        citiDF.reindex(columns=COLUMNS)

        print(citiDF)

        # Convert to float
        fidelityDF['Balance'] = fidelityDF['Balance'].str.replace('[$, ]', '', regex=True).astype(float)

        fidelityDF = fidelityDF.rename(columns={'Balance As Of': 'Date', 'Account Name': 'Name'})
        fidelityDF.drop(columns=["Hidden"], errors="ignore", inplace=True)
        fidelityDF['Institution'] = 'Fidelity Investments'
        fidelityDF['Date'] = pd.to_datetime(fidelityDF['Date'])
        fidelityDF = fidelityDF.dropna(subset=['Date'])
        fidelityDF.reindex(columns=COLUMNS)

        print(fidelityDF)
        factDF = pd.DataFrame(columns=COLUMNS)
        factDF = pd.concat([lormetDF, marcusDF, citiDF, fidelityDF], axis=0, ignore_index=True)
        factDF.to_parquet(DEST_CURATED_PATH)
    except Exception as e:
        print(f"Exception occurred: {e}")




if __name__ == "__main__":
    Transform()


