import sqlite3
import pandas as pd
import os

# Path to CSV folder (relative to project folder)
data_dir = os.path.join(os.path.dirname(__file__), "data")

# Connect to database
conn = sqlite3.connect("mining_db.sqlite")
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")

# Loop through all CSV files in folder
for file in os.listdir(data_dir):
    if file.endswith(".csv"):
        table = file.replace(".csv", "")  # assumes file name = table name
        file_path = os.path.join(data_dir, file)
        
        print(f"\n📁 Processing: {file}")
        print(f"📂 File path: {file_path}")
        
        try:
            # Read CSV file
            df = pd.read_csv(file_path)
            print(f"📊 CSV loaded: {len(df)} rows, {len(df.columns)} columns")
            print(f"📋 Columns: {list(df.columns)}")
            print(f"👀 First 3 rows:")
            print(df.head(3))
            
            # Insert data into database
            df.to_sql(table, conn, if_exists="replace", index=False)
            print(f"✅ Table '{table}' created/replaced with {len(df)} rows")
                
        except Exception as e:
            print(f"❌ Failed to process '{file}': {e}")
            print(f"🔍 Error details: {type(e).__name__}")

conn.close()
print("\n🎉 Import process completed!")
