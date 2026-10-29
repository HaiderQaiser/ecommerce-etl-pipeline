import pandas as pd
import matplotlib.pyplot as plt

def bar_chart_generate(clean_data_csv_path,):
    df = pd.read_csv(clean_data_csv_path)

    df['net_revenue'] = (df['quantity'] * df['unit_price_pkr'] * (1 - df['discount_pct']))

    category_summary = df.groupby('product_category')['net_revenue'].sum().sort_values(ascending=False)
    #plt.figure(figsize=(8,5))
    category_summary.plot(kind='bar')
    plt.title("Category wise Net Revenue Summary", fontsize=18,  fontweight = 'bold')
    plt.xlabel("Product Category", fontsize=12)
    plt.ylabel("Net Revenue (PKR in Thousands)", fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig("05-images/category_revenue_summary.png", dpi=300)
    plt.close()
    print("Category Revenue Summary Chart Successfully Exported!")

def line_chart_generate(clean_data_csv_path):
    df = pd.read_csv(clean_data_csv_path)

    df['net_revenue'] = (df['quantity'] * df['unit_price_pkr'] * (1 - df['discount_pct']))

    df['order_date'] = pd.to_datetime(df['order_date'])
    daily_summary = df.groupby('order_date')['net_revenue'].sum()

    plt.figure(figsize=(10, 5))
    daily_summary.plot(kind='line', marker='o', color='#27ae60', linewidth=2)

    plt.title("Daily Net Revenue Trend", fontsize=16, fontweight='bold')
    plt.xlabel("Order Date", fontsize=12)
    plt.ylabel("Net Revenue (PKR)", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6) # Both X and Y grid lines for trend view
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    plt.savefig("05-images/daily_revenue_trend.png", dpi=300)
    plt.close()

    print("Daily Revenue Trend Chart successfully exported!") 

def pie_chart_generate(clean_data_csv_path):
    df = pd.read_csv(clean_data_csv_path)

    order_summary = df['order_status'].value_counts()

    plt.figure(figsize=(7, 7))

    order_summary.plot(kind='pie', autopct='%1.1f%%', startangle=140)

    plt.title("Order Status Distribution", fontsize=16, fontweight='bold')
    plt.ylabel('') 
    plt.tight_layout()

    plt.savefig("05-images/order_status_distribution.png", dpi=300)
    plt.close()

    print("Order Status Distribution Chart successfully exported!") 

#File Path
clean_data_csv_path = "01-data/02-processed/karachi_ecommerce_orders_clean.csv"

#Generating Reports
bar_chart_generate(clean_data_csv_path)
line_chart_generate(clean_data_csv_path)
pie_chart_generate(clean_data_csv_path)