import requests
import pandas as pd
from dataclasses import dataclass
from pathlib import Path


API_KEY = "<Google Geocoding API Key>"
DATA_PATH = Path(".\\<data>.csv")
SAVE_PATH = Path(".\\<newData>.csv")

@dataclass
class Features:
    latitude: float = 0.0
    longitude: float = 0.0
    zipCode: int = 0

def ForwardGeocode(address: str):
    '''
    Returns a list of features for the given address, or None if not found
    Sleep is note needed since the API supports 50 (20ms) requests per second and its average time per request is 80ms
    '''
    try:
        # URL encode the address properly
        encoded_address = requests.utils.quote(address)

        response = requests.get(f"https://maps.googleapis.com/maps/api/geocode/json?address={encoded_address}&key={API_KEY}")
        response.raise_for_status()  # Raise an error for HTTP issues

        data = response.json()  # Convert response to JSON

        # Get the results array (this contains all matching locations)
        results = data.get("results", [])

        if not results:
            return None

        return results  # Returns results

    except requests.RequestException as e:
        print(f"[-] Request failed: {e}")
        return None

def ParseFeatures(results: list[dict]):
    '''
    Returns a Features object from the given results list, or None if not found
    '''
    if not results:
        return None

    try:
        # Get the first result (most relevant match)
        result = results[0]
        
        # Extract coordinates from geometry
        location = result["geometry"]["location"]
        latitude = location["lat"]
        longitude = location["lng"]
        
        # Extract postal code from address components
        zipCode = 0.0  # Default value
        for component in result["address_components"]:
            if "postal_code" in component["types"]:
                zipCode = float(component["long_name"])
                break

        return Features(latitude, longitude, zipCode)

    except (KeyError, IndexError) as e:
        print(f"[-] Error parsing features: {e}")
        return None

def UpdateRow(df: pd.DataFrame, index: int, features: Features):
    df.at[index, "LATITUDE"] = features.latitude
    df.at[index, "LONGITUDE"] = features.longitude
    if postalCode == 0:
        df.at[index, "ZIP CODE"] = features.zipCode
    if postalCode != features.zipCode and features.zipCode != 0:
        df.at[index, "ZIP CODE"] = features.zipCode
        print(f"[!] {index}, {postalCode}, {features.zipCode}")

# Create data frame
df = pd.read_csv(DATA_PATH)
df = df.reset_index()

# Store found addresses features to reduce API calls
foundFeatures: dict[str, Features] = {}


# Go through each row
for index, row in df.iterrows():
    # Convert address to string
    address = str(row["ADDRESS"])
    address = address + ", Manhattan, NY, USA" # Add fixed info for more specific search
    postalCode = row["ZIP CODE"]
    
    # Check if address is already found
    if address in foundFeatures:
        print(f"[+] Using \"{address}\" features from cache")
        features = foundFeatures[address]
        UpdateRow(df, index, features)
        continue

    # Get features
    rawFeatures = ForwardGeocode(address)
    features = ParseFeatures(rawFeatures)

    if rawFeatures is None:
        print("[-] Address \"{address}\" not found")
        continue

    print(f"[+] Address \"{address}\" found")

    # Add features to data frame
    UpdateRow(df, index, features)
    
    # Store features
    foundFeatures[address] = features

# Save the data frame
df.to_csv(SAVE_PATH, index=False)
print(f"\nData frame saved at {SAVE_PATH}")