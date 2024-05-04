import pandas as pd
import sqlite3

# Define Excel file path and sheet name
excel_file = r"C:\Users\omerf\Downloads\sitedatabase.xlsx"
sheet_name = "Sheet1"  # Update sheet name if needed

# Connect to the database (replace 'your_database.db' with your filename)
conn = sqlite3.connect("URL_database.db")

# Read the Excel table into a Pandas DataFrame
try:
  df = pd.read_excel(excel_file, sheet_name=sheet_name)
except FileNotFoundError:
  print("Error: Excel file not found!")
  exit()

# Assign a name to the DataFrame (optional)
table_name = "Site"  # Replace with your preferred name
df = df.copy()  # Optional: Create a copy to avoid modifying the original DataFrame
df.name = table_name

# Define SQL statement to create the table (modify columns and data types as needed)
create_table_sql = f"""
CREATE TABLE IF NOT EXISTS {table_name} (
  column1 TEXT,
  column2 TEXT,
);
"""



# Insert DataFrame data into the table
df.to_sql(table_name, conn, index=False)

# Commit changes and close connection
conn.commit()

conn.close()