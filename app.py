import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import numpy as np

# Read the data
def load_data():
    df = pd.read_csv("data.csv")
    return df

# Function to get color based on sale price
def get_color_for_price(price, min_price, max_price):
    # Calculate normalized price (0 to 1)
    normalized = (price - min_price) / (max_price - min_price)
    # Convert to a color (red with varying opacity)
    return f'rgba(255, 0, 0, {max(0.2, normalized)})'

def main():
    st.title("Manhattan Property Sales Map Visualization")
    
    # Load the data
    df = load_data()
    
    # Get the range of years
    years = sorted(df['YEAR_SOLD'].unique())
    
    # Create a slider for year selection
    selected_year = st.slider(
        "Select Year",
        min_value=int(min(years)),
        max_value=int(max(years)),
        value=int(min(years))
    )
    
    # Filter data for selected year
    year_data = df[df['YEAR_SOLD'] == selected_year]
    
    # Get price range for color scaling
    min_price = year_data['SALE PRICE'].min()
    max_price = year_data['SALE PRICE'].max()
    
    # Create the map centered on Manhattan
    manhattan_coords = [40.7831, -73.9712]  # Manhattan coordinates
    m = folium.Map(
        location=manhattan_coords,
        zoom_start=14  # Increased zoom level for better Manhattan view
    )
    
    # Add markers for each property
    for idx, row in year_data.iterrows():
        color = get_color_for_price(row['SALE PRICE'], min_price, max_price)
        folium.CircleMarker(
            location=[row['LATITUDE'], row['LONGITUDE']],
            radius=8,
            color=color,
            fill=True,
            fill_opacity=0.7,
            popup=f"""
                Year: {row['YEAR_SOLD']}<br>
                Sale Price: ${row['SALE PRICE']:,.2f}
            """,
            tooltip=f"${row['SALE PRICE']:,.2f}"
        ).add_to(m)
    
    # Add a legend
    legend_html = '''
        <div style="position: fixed; 
                    bottom: 50px; right: 50px; width: 150px; height: 90px; 
                    border:2px solid grey; z-index:9999; background-color:white;
                    padding:10px;
                    font-size:14px;
                    ">
            <p><strong>Sale Price Range</strong></p>
            <p>
            <i style="background: rgba(255,0,0,0.2); width:10px; height:10px; display:inline-block"></i> ${:,.0f}<br>
            <i style="background: rgba(255,0,0,1.0); width:10px; height:10px; display:inline-block"></i> ${:,.0f}
            </p>
        </div>
        '''.format(min_price, max_price)
    
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Display the map in Streamlit
    folium_static(m)
    
    # Display statistics
    st.write(f"Number of properties in {selected_year}: {len(year_data)}")
    st.write(f"Sale price range: ${min_price:,.2f} - ${max_price:,.2f}")
    st.write(f"Average sale price: ${year_data['SALE PRICE'].mean():,.2f}")

if __name__ == "__main__":
    main()