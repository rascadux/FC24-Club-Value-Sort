import os
import sys

# Check if the required libraries are installed, if not, install them
try:
    import requests
    import csv
    from bs4 import BeautifulSoup
    import openpyxl
    import pandas as pd
    import unicodedata
except ImportError:
    print("Installing required libraries...")
    os.system("pip install requests csvkit beautifulsoup4 openpyxl pandas")

    # If you encounter issues with the 'cchardet' library on Windows, you can add it to the command above:
    # os.system("pip install requests csvkit beautifulsoup4 openpyxl pandas cchardet")

    python_executable = sys.executable
    os.execl(python_executable, python_executable, *sys.argv)

####################################### CORRECTION OF THE NAMES ###########################################################################

# FUnction to correct characters
def correct_characters(text):
    return ''.join(unicodedata.normalize('NFKD', text).encode('utf-8', 'ignore').decode('utf-8'))

# Read the original CSV file
with open('club-analyzer.csv', mode='r', encoding='utf-8') as original_file:
    lector = csv.reader(original_file)
    corrected_data = []

    for row in lector:
        corrected_row = [correct_characters(cell) for cell in row]
        corrected_data.append(corrected_row)

# Write the corrected data to a new CSV file
with open('my_club.csv', mode='w', newline='', encoding='utf-8') as corrected_file:
    writer = csv.writer(corrected_file)
    writer.writerows(corrected_data)


###########################################################################################################################################

####################################### FROM CSV TO EXCEL ##################################################################################

def csv_to_excel(csv_file, excel_file):
    # Read CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)

    # Write DataFrame to Excel file
    df.to_excel(excel_file, index=False)

if __name__ == "__main__":
    input_csv_file = 'my_club.csv'
    output_excel_file = 'output.xlsx'

    try:
        csv_to_excel(input_csv_file, output_excel_file)
        print(f"Conversion successful. Excel file saved as '{output_excel_file}'.")
    except Exception as e:
        print(f"Error: {e}")

###########################################################################################################################################


# Define the URL where you can look up player prices
base_url = "https://www.fut.gg/players/?name="  

# Load your Excel file
excel_file = 'output.xlsx'
wb = openpyxl.load_workbook(excel_file)
sheet = wb.active

# Create a CSV file to store the results
csv_file = "player_prices.csv"

# Initialize an empty list to store player data
player_data = []

# Loop through the Excel rows
for row in sheet.iter_rows(min_row=2, values_only=True):
    player_id = row[0]  
    player_name = row[2]
    player_surname = row[1]
    is_untradeable = row[12] 

    if is_untradeable == False:

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
        player_data.append((player_id, player_price, player_name, player_surname))

# Write the data to a CSV file
with open(csv_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Player ID", "Price", "Name", "Surname"]) 
    writer.writerows(player_data)

print("Data extraction and CSV creation complete.")

def csv_to_sorted_excel(csv_file, excel_file):
    # Read CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)

    # Sort DataFrame by the "Price" column in descending order
    df = df.sort_values(by='Price', ascending=False)

    # Write the sorted DataFrame to an Excel file
    df.to_excel(excel_file, index=False)

if __name__ == "__main__":
    input_csv_file = 'player_prices.csv'
    output_sorted_excel_file = 'player_prices.xlsx'

    try:
        csv_to_sorted_excel(input_csv_file, output_sorted_excel_file)
        print(f"Conversion and sorting successful. Excel file saved as '{output_sorted_excel_file}'.")
    except Exception as e:
        print(f"Error: {e}")
