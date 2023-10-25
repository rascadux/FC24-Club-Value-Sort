import requests
import csv
from bs4 import BeautifulSoup
import openpyxl

# Define the URL where you can look up player prices
base_url = "https://www.fut.gg/players/?name="  # Replace with the actual URL

# Load your Excel file
excel_file = "your_file.xlsx"  # Replace with the actual file name
wb = openpyxl.load_workbook(excel_file)
sheet = wb.active

# Create a CSV file to store the results
csv_file = "player_prices.csv"

# Initialize an empty list to store player data
player_data = []

# Loop through the Excel rows
for row in sheet.iter_rows(min_row=2, values_only=True):
    player_id = row[0]  
    is_untradeable = row[12] 
    ratings = row[3] 

    if is_untradeable == "false" and ratings <= 74 and ratings >= 65:
        # Construct the URL for the player
        player_url = base_url + str(player_id)

        # Send an HTTP request to the player's URL
        response = requests.get(player_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # Find the element with data-price attribute
            price_element = soup.find(attrs={"data-js-selector": "prices-blob-app"})

            if price_element:
                # Extract the price from the data-price attribute
                player_price = price_element.get("data-price")
            else:
                player_price = "Price element not found"
        else:
            player_price = "Error"

        # Append the player ID and price to the list
        player_data.append((player_id, player_price))

# Write the data to a CSV file
with open(csv_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Player ID", "Price"])  # Write header row
    writer.writerows(player_data)

print("Data extraction and CSV creation complete.")
