# FIFA FUT CLUB PLAYERS PRICE SORT
Script for FC24 game to sort the players of your club from highest to lowest price.

# Requirements
- Python 3
- Paletools
- Excel

## Important steps
1. To use the script you must first install paletools from [https://pale.tools/fifa/paletools.html](url)
2. Run it with the FC Companion webapp
3. Go to Club Analyzer -> Export as CSV
4. Convert the CSV to Excel, separating data by columns
5. Run the python script with ```python3 script_values.py```
6. Change the "your_file.xlsx" with the actual file name of the new Excel created
7. Convert the CSV created to Excel and sort it as you want :)

## You will need to use PIP to install the following libraries:
- requests
- csv
- bs4
- openpyxl

## Players data ouput format:
- After running the script the user will have the data saved as CSV file, which must be converted to .xmls to sort by price
