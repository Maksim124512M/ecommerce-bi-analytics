import pandas as pd
import numpy as np

n = 500

df = pd.DataFrame({
    'product_id': np.arange(1000, 1000 + n),
    'category': np.random.choice(a=['Electronics', 'Home & Kitchen', 'Fashion', 'Beauty'], size=n),
    'price': np.random.randint(20, 4000, size=n),
    'rating': np.random.uniform(3.0, 5.0, size=n).round(1),
    'reviews': np.random.randint(0, 400, size=n),
    'discount': np.random.randint(0, 70, size=n),
    'stock_qty': np.random.randint(0, 200, size=n)
})

base_sales = np.random.randint(1, 50, size=n)
influence = (df['rating'] / 5) + (df['discount'] / 100)
df['sales_last_7d'] = (base_sales * influence).astype(int)

df['revenue_last_7d'] = (df['price'] * 0.2) * df['sales_last_7d']

df['revenue_next_7d'] = (df['price'] * (1 - df['discount']/100) * df['sales_last_7d'] * 0.2) \
                        * np.random.uniform(0.8, 1.2, size=n)

df['revenue_last_7d'] = df['revenue_last_7d'].round(2)
df['revenue_next_7d'] = df['revenue_next_7d'].round(2)

df.to_csv('data/products.csv', index=False)

print(df[['product_id', 'category', 'revenue_last_7d', 'revenue_next_7d']].head())