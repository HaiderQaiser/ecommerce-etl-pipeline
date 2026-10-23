import pandas as pd
import numpy as np

def run_data_cleaning(raw_csv_path):
    #Read raw CSV
    df = pd.read_csv(raw_csv_path)
    #==============================================
    #TRANSFORMATION (Cleaning Data)
    #==============================================
    #dropping duplicates
    initial_rows = len(df)
    df = df.drop_duplicates()

    #Data types and text Standardization
    text_columns = ['city', 'product_category', 'product_name', 'payment_method', 'order_status', 'sales_channel']

    for column in text_columns:
        df[column] = df[column].astype(str).str.strip().str.title()

    #order_date Column Dates Format Standardization
    #og dates ko preserve kr lia pehle
    original_dates = df['order_date'].copy()

    #unko date mn parse krdia
    df['order_date'] = pd.to_datetime(
        original_dates,
        format='%m/%d/%Y',
        errors='coerce'
    )
    #jo dates fail hogyin parse hone se
    mask = df['order_date'].isna()

    df.loc[mask, 'order_date'] = pd.to_datetime(
        original_dates[mask],
        format='%d/%m/%Y',
        errors='coerce'
    )
    ##dubara se wo dates identify kri jo parse na hoskin eg 2026-08-30
    dash_mask = df['order_date'].isna()

    df.loc[dash_mask, 'order_date'] = pd.to_datetime(
        original_dates[dash_mask],
        format='%Y-%m-%d',
        errors='coerce'
    )
    #dubara se wo dates identify kri jo parse na hoskin like 20260920
    mask_no_slash = df['order_date'].isna()

    df.loc[mask_no_slash, 'order_date'] = pd.to_datetime(
        original_dates[mask_no_slash],
        format='%Y%m%d',
        errors='coerce'
    )
    #wo rows lelin jahan date null hai. (unko rejected_records_logs.csv file mn save krunga, aur end mn sab variable ko ek single all_error_rows mn pd.concat krdunga then file mn write)
    null_date_rows = df[df['order_date'].isna()].copy()
    null_date_rows['error_reason'] = 'Missing Order Date'

    df = df[df['order_date'].notna()]

    #ab string format mn parse kr dia dates ko
    df['order_date'] = df['order_date'].dt.strftime('%Y-%m-%d')
    
    #Quantity Column Fix
    #pehle quantity column ko numeric mn convert kr lia.
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')

    #then negative quantities ko positive bana dia
    df['quantity'] = df['quantity'].abs() 

    #error file mn 0 quantity wali rows daal dunga
    zero_qtty_rows = df[df['quantity'] == 0 ].copy()
    zero_qtty_rows['error_reason'] = 'Invalid Quantity (Zero)'

    #null quantity rows ko bhi file mn chipka dunga
    null_qtty_rows = df[df['quantity'].isna()].copy()
    null_qtty_rows['error_reason'] = 'Null Quantity Found'

    df = df[(df['quantity'] > 0) & (df['quantity'].notna())]

    #unit_price_pkr Column Fix
    df['unit_price_pkr'] = pd.to_numeric(df['unit_price_pkr'], errors='coerce')

    #neg prices ko positive kr dia
    df['unit_price_pkr'] = df['unit_price_pkr'].abs()

    #zero price aur null price rows ko file mn daalna
    zero_unit_price_rows = df[df['unit_price_pkr'] == 0].copy()
    zero_unit_price_rows['error_reason'] = 'Zero Unit Price'

    null_unit_price_rows = df[df['unit_price_pkr'].isna()].copy()
    null_unit_price_rows['error_reason'] = 'Null Unit Price'

    #finally zero aur null price wali rows ko df se remove
    df = df[(df['unit_price_pkr'] > 0) & (df['unit_price_pkr'].notna())]

    #discount_pct column fix
    df['discount_pct'] = pd.to_numeric(df['discount_pct'], errors='coerce')

    df['discount_pct'] = df['discount_pct'].abs()

    #filtering out rows that are null (btw my file has no nulls in column discount_pct)
    null_discount_rows = df[df['discount_pct'].isna()].copy()
    null_discount_rows['error_reason'] = 'Null Discount'

    # Agar data % mein hai (e.g. 105%) to > 100, aur agar decimals mein hai to > 1.0 check karein
    invalid_discount_rows = df[df['discount_pct'] > 1.0].copy()
    invalid_discount_rows['error_reason'] = 'Discount Greater Than 100%'

    df = df[(df['discount_pct'] >= 0.0) & (df['discount_pct'] <= 1.0) & (df['discount_pct'].notna())]

    #delivery_days Column Fix
    df['delivery_days'] = pd.to_numeric(df['delivery_days'], errors='coerce')

    #sirf negative days ko handle krna hai isme
    df['delivery_days'] = df['delivery_days'].abs()

    #Ab float se integer ('Int64') mein convert karein
    df['delivery_days'] = df['delivery_days'].astype('Int64')

    #order_line_id column duplicates fix
    #Duplicated Primary Key rows ko Identify aur Capture karo (for rejection log)
    duplicate_pk_rows = df[df.duplicated(subset=['order_line_id'], keep='first')].copy()

    #saving into rejected_records_logs.csv
    duplicate_pk_rows['error_reason'] = 'Duplicate Order Line ID (PK Conflict)'

    #DataFrame se duplicate order_line_ids ko drop karke pehli row retain karo
    df = df.drop_duplicates(subset=['order_line_id'], keep='first')

    #customer_id column fix
    #har group k missing rows ko ffill aur bfill se fill krdia
    df['customer_id'] = df.groupby('order_id')['customer_id'].ffill().bfill()

    #wo customers jinki customer_id fill na hoski (rejected_records_logs.csv mn daal dengy)
    null_customer_id_rows = df[df['customer_id'].isna()].copy()
    null_customer_id_rows['error_reason'] = 'Missing Customer Id'

    #sirf wohi rows rkho jahan customer_id null na ho
    df = df[df['customer_id'].notna()]

    #city column fix
    df['city'] = df.groupby('order_id')['city'].ffill().bfill()

    null_city_rows = df[df['city'].isna()].copy()
    null_city_rows['error_reason'] = 'Missing City'

    df = df[df['city'].notna()]

    #payment_method column fix
    df['payment_method'] = df.groupby('order_id')['payment_method'].ffill().bfill()

    null_payment_method_rows = df[df['payment_method'].isna()].copy()
    null_payment_method_rows['error_reason'] = 'Missing Payment Method'

    df = df[df['payment_method'].notna()]

    #product_category column fix
    df['product_category'] = df.groupby('product_name')['product_category'].ffill().bfill()

    null_prod_cat_rows = df[df['product_category'].isna()].copy()
    null_prod_cat_rows['error_reason'] = 'Missing Product Category'

    df = df[df['product_category'].notna()]

    #product_name Column Fix (isko recover nhi kia jaskta)
    null_prod_name_rows = df[df['product_name'].isna()].copy()
    null_prod_name_rows['error_reason'] = 'Missing Product Name'

    df = df[df['product_name'].notna()]

    #Rejected Data
    #Pehle sab variables ko concat krdia
    rejected_data = pd.concat(
        [null_date_rows, 
        zero_qtty_rows, 
        null_qtty_rows, 
        zero_unit_price_rows,
        null_unit_price_rows,
        null_discount_rows,
        invalid_discount_rows,
        null_customer_id_rows, 
        null_city_rows,
        null_payment_method_rows,
        duplicate_pk_rows])

    # 3. Return clean DataFrame and rejected logs DataFrame
    return df, rejected_data