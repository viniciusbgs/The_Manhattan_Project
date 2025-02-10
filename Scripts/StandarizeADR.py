import pandas as pd
import re
from pathlib import Path

DATA_PATH = Path(r".\data.csv")
SAVE_PATH = Path(r".\data2.csv")

def StandarizeAddress(address):
    '''
    Standardize address:
    - Removes extra spaces
    - Removes apartment/unit numbers after comma
    - Removes "N/A"
    - Removes periods
    - Removes ordinal suffixes
    - Keeps the first number from ranges
    - Abreviates West and East
    - Abreviates "Street" and "Avenue"
    - Capitalizes words
    '''
    # Remove extra spaces
    address = re.sub(r'\s+', ' ', address)
    
    # Remove everything after comma
    address = address.split(',')[0].strip()

    # Remove N/A 
    address = re.sub(r'\bN/A\b', '', address, flags=re.IGNORECASE)

    # Remove periods
    address = address.replace('.', '')
    
    # Remove ordinal suffixes (st, nd, rd, th)
    address = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', address, flags=re.IGNORECASE)

    # Replace number range with the first number
    address = re.sub(r'^(\d+)[&-]\d+', r'\1', address)

    # Abbreviate West and East
    address = re.sub(r'\b(West|East)\b', 
                     lambda m: m.group(1)[0], 
                     address, 
                     flags=re.IGNORECASE)

    # Replace "Street" with "St"
    address = re.sub(r'\bStreet\b', 'St', address, flags=re.IGNORECASE)

    # Replace "Avenue" with "AVe"
    address = re.sub(r'\bAvenue\b', 'Ave', address, flags=re.IGNORECASE)

    # Capitalize the first letter of each word
    address = ' '.join(word.capitalize() for word in address.split())
    
    return address

# Create data frame
df = pd.read_csv(DATA_PATH)

# Check for ammount of unique addresses
print(f"Unique addresses before the standarization: {df['ADDRESS'].nunique()}")

# Standardize addresses
df["ADDRESS"] = df["ADDRESS"].apply(StandarizeAddress)

# Check for ammount of unique addresses
print(f"Unique addresses after the standarization: {df['ADDRESS'].nunique()}")

# Save the data frame
df.to_csv(SAVE_PATH, index=False)