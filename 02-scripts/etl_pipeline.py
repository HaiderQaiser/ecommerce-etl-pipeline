import os
from transform_clean import run_data_cleaning
from load_sql import load_to_sql_server

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RAW_DATA_PATH = os.path.join(BASE_DIR, '01-data', '01-raw', 'karachi_ecommerce_orders_dirty.csv')
CLEAN_DATA_PATH = os.path.join(BASE_DIR, '01-data', '02-processed', 'karachi_ecommerce_orders_clean.csv')
REJECTED_DATA_PATH = os.path.join(BASE_DIR, '01-data', '03-rejected', 'rejected_records_logs.csv')

def main():
    print("Starting PakCart ETL Pipeline...")
    
    # Step 1: Clean Data
    df, rejected_data = run_data_cleaning(RAW_DATA_PATH)
    
    # Step 2: Save Processed Files
    df.to_csv(CLEAN_DATA_PATH, index=False)

    rejected_data.to_csv(REJECTED_DATA_PATH, index=False)

    # Step 3: Push to SQL
    DB_NAME = "Karachi_ecommerce"
    load_to_sql_server(df, table_name="orders", server_name=".", database_name=DB_NAME)
    
    print("Pipeline executed successfully!")

if __name__ == "__main__":
    main()