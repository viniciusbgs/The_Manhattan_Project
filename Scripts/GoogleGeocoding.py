import requests
import pandas as pd
import time
from dataclasses import dataclass
from pathlib import Path

API_KEY = "<Google API key>"
DATA_PATH = Path("<Data.csv>")
SAVE_PATH = Path("<Save.csv>")

@dataclass
class Features:
    latitude: float = 0.0
    longitude: float = 0.0
    zipCode: int = 0

def ForwardGeocode(address: str):
    '''
    Returns a list of features for the given address, or None if not found
    '''
    try:
        address = address.replace(" ", "+")
        response = requests.get(f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={API_KEY}")
        response.raise_for_status()  # Raise an error for HTTP issues

        data = response.json()  # Convert response to JSON
        features = data.get("response", {}).get("features", [])

        if not features:
            return None

        return features  # Returns features

    except requests.RequestException as e:
        print(f"[-] Request failed: {e}")
        return None

def ParseFeatures(features: list[dict]):
    '''
    Returns a Features object from the given features list, or None if not found
    '''
    if not features:
        return None

    # Parse features
    feature = features[0]
    latitude, longitude = feature["geometry"]["coordinates"]
    
    # Some don't have postal code
    try:
        zipCode = float(feature["properties"]["postalcode"])
    except Exception:
        zipCode = 0

    return Features(latitude, longitude, zipCode)

# Create data frame
df = pd.read_csv(DATA_PATH)
df = df.reset_index()

# Store found addresses features to reduce API calls
foundFeatures: dict[str, Features] = {}


# Go through each row
for index, row in df.iterrows():
    address = row["ADDRESS"].strip() + ", Manhattan, NY, USA" # Add fixed info for more specific search
    postalCode = row["ZIP CODE"]
    
    # Check if address is already found
    if address in foundFeatures:
        print(f"[+] Using \"{address}\" features from cache")
        features = foundFeatures[address]
        df.at[index, "LATITUDE"] = features.latitude
        df.at[index, "LONGITUDE"] = features.longitude
        if postalCode == 0:
            df.at[index, "ZIP CODE"] = features.zipCode
        continue

    # Get features
    rawFeatures = ForwardGeocode(address)
    features = ParseFeatures(rawFeatures)
    time.sleep(1) # Prevents API rate limit

    if rawFeatures is None:
        print("[-] Address \"{address}\" not found")
        continue

    print(f"[+] Address \"{address}\" found")

    # Store features
    foundFeatures[address] = features

    # Add features to data frame
    df.at[index, "LATITUDE"] = features.latitude
    df.at[index, "LONGITUDE"] = features.longitude
    if postalCode == 0:
        df.at[index, "ZIP CODE"] = features.zipCode


# Save the data frame
df.to_csv(SAVE_PATH, index=False)
print(f"\nData frame saved at {SAVE_PATH}")