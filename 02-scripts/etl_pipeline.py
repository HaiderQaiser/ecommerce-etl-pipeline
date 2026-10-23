from transform_clean import run_data_cleaning
from load_sql import load_to_sql_server

def main():
    print("Starting PakCart ETL Pipeline...")
    
    # Step 1: Clean Data
    df, rejected_data = run_data_cleaning("D:/ETL-Project/01-data/01-raw/karachi_ecommerce_orders_dirty.csv")
    
    # Step 2: Save Processed Files
    processed_csv_path = "D:/ETL-Project/01-data/02-processed/karachi_ecommerce_orders_clean.csv"
    df.to_csv(processed_csv_path, index=False)

    rejected_csv_path = "D:/ETL-Project/01-data/03-rejected/rejected_records_logs.csv"
    rejected_data.to_csv(rejected_csv_path, index=False)

    # Step 3: Push to SQL
    load_to_sql_server(df, table_name="orders", server_name="HAIDERs-LAPTOP", database_name="Karachi_ecommerce")
    
    print("✅ Pipeline executed successfully!")

if __name__ == "__main__":
    main()