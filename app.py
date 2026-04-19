import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots 

@st.cache_data
def load_data():
    return pd.read_csv('data/products.csv')

df = load_data()

# Streamlit App
st.title('🚀 E-commerce Business Intelligence')
st.markdown('Аналітична панель моніторингу товарів та прогнозів прибутку')

# Filters
categories_selectbox = st.selectbox('Обрати категорію:', set(df['category']))
st.write('Категорія: ', categories_selectbox)

col1, col2, col3 = st.columns(3)  # Create three columns for metrics

# Calculate metrics
total_revenue_last_7d = df['revenue_last_7d'].sum()
avg_product_rating_per_category = round(df.groupby('category')['rating'].mean(), 2)
out_of_stock = len(df[df['stock_qty'] < 10])

# Display metrics in columns
col1.metric('Весь прибуток за останні 7 днів: ', total_revenue_last_7d)
col2.metric(f'Середній дохід по "{categories_selectbox}":  ', avg_product_rating_per_category[categories_selectbox])
col3.metric('Немає в наявності: ', out_of_stock)

# Visualizations
fig = make_subplots(rows=2, cols=2,
                    subplot_titles=('Ціна vs Продажі', 'Розподіл знижок', 'Виручка за категоріями', 'Прогноз виручки'))

m, b = np.polyfit(df['price'], df['sales_last_7d'], 1)

fig.add_trace(go.Scatter(
    x=df['price'], y=df['sales_last_7d'], mode='markers', name='Товари'
), row=1, col=1)

fig.add_trace(go.Scatter(
    x=df['price'], 
    y=m*df['sales_last_7d'] + b, 
    mode='lines', 
    name='Тренд',
    line=dict(color='red', width=3)
), row=1, col=1)

fig.add_trace(go.Histogram(
    x=df['discount'], name='Знижки', 
    marker_color='#EB89B5',
), row=1, col=2)

fig.add_trace(go.Bar(
    x=df['category'], y=df['revenue_last_7d'], 
    name='Поточна',
), row=2, col=1)

fig.add_trace(go.Bar(
    x=df['category'], y=df['revenue_next_7d'], 
    name='Прогноз', marker_color='#3300FF',
), row=2, col=2)

fig.update_layout(
    height=700, showlegend=False, 
    title_text='Комплексний аналіз продуктів', bargap=0.3,
)  # Adjust height and title
fig.update_traces(
    marker_line_color='rgb(255, 100, 200)',
    marker_line_width=2,
    opacity=0.85,
    row=1, col=2
)
st.plotly_chart(fig, width='stretch')

sort_by = st.selectbox('Sort by: ', df.columns)

df_sorted = df.sort_values(by=sort_by, ascending=False).reset_index(drop=True).head(30)
csv_df_sorted = df_sorted.to_csv(index=False, sep=';').encode('utf-8')
st.dataframe(df_sorted)

st.download_button(
    label='📥 Завантажити відсортовану таблицю',
    data=csv_df_sorted,
    file_name='sorted_products_data.csv',
    mime='text/csv',
)