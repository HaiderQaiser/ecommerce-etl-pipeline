import pyodbc as odbc
import pandas as pd

def load_to_sql_server(df, table_name, server_name, database_name):
    #Pehle Object type mein cast karo, phir saare NaNs / pd.NA ko None (SQL NULL) banao
    df_sql = df.astype(object).where(pd.notnull(df), None)
    
    data_to_insert = []
    for row in df_sql.to_numpy():
        data_to_insert.append(tuple(row))

    SERVER_NAME = server_name
    DATABASE_NAME = database_name

    connection_string = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={SERVER_NAME};"
        f"DATABASE={DATABASE_NAME};"
        f"Trusted_connection=yes;"
    )
    try:
        conn = odbc.connect(connection_string)
        cursor = conn.cursor()
        #parameterized query
        insert_query = f"""
            INSERT INTO {table_name}(order_id, order_line_id, order_date, customer_id, city,product_category, product_name, quantity,unit_price_pkr, discount_pct, payment_method, order_status, delivery_days, sales_channel)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """
        cursor.execute(f"TRUNCATE TABLE {table_name}")
        cursor.executemany(insert_query, data_to_insert)

        conn.commit()

        cursor.close()
        conn.close()
    except Exception as e:
        print("Oops! An Error Occured.\nError Details: ", e)