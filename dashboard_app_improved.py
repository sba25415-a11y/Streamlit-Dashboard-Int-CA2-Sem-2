import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title = 'Online Retail Dashboard',
    layout = 'wide'
)

st.title('Online Retail Dashboard for Adults Aged 65+')

st.write(
    'This improved dashboard summarises key online retail patterns using prepared transaction summaries. '
    'The layout is designed to be simple, readable, and easy to navigate.'
)

st.sidebar.title('Dashboard guide')
st.sidebar.write(
    'Use this dashboard to review sales, baskets, households, products, and product categories. '
    'The charts use prepared summary files to keep the dashboard responsive.'
)

department_summary = pd.read_csv('dashboard_department_summary_improved.csv')
weekly_summary = pd.read_csv('dashboard_weekly_summary_improved.csv')
category_summary = pd.read_csv('dashboard_category_summary_improved.csv')
dashboard_sample = pd.read_csv('dashboard_sample_improved.csv')

total_sales = department_summary['total_sales_value'].sum()
total_baskets = department_summary['total_baskets'].sum()
total_households = department_summary['unique_households'].sum()
total_products = department_summary['unique_products'].sum()

st.subheader('Key retail summary')

col1, col2, col3, col4 = st.columns(4)

col1.metric('Total sales value', f'{total_sales:,.2f}')
col2.metric('Total baskets', f'{int(total_baskets):,}')
col3.metric('Unique households', f'{int(total_households):,}')
col4.metric('Unique products', f'{int(total_products):,}')

st.write(
    'These summary values provide a quick overview of the retail activity represented in the prepared dashboard data.'
)

st.subheader('Department and weekly overview')

left_col, right_col = st.columns(2)

with left_col:
    st.write('Sales value by department')
    department_chart = department_summary.set_index('department')['total_sales_value']
    st.bar_chart(department_chart)

with right_col:
    st.write('Weekly sales trend')
    weekly_chart = weekly_summary.set_index('week')['total_sales_value']
    st.line_chart(weekly_chart)

st.subheader('Top product categories')

number_of_categories = st.slider(
    'Select number of categories to display',
    5,
    20,
    10
)

top_categories = category_summary.sort_values(
    'total_sales_value',
    ascending = False
).head(number_of_categories)

category_chart = top_categories.set_index('product_category')['total_sales_value']
st.bar_chart(category_chart)

st.write(
    'The product category chart helps identify the categories with the highest sales value. '
    'This supports retail decisions such as product placement, promotional planning, and recommendation opportunities.'
)

st.subheader('Why this dataset is suitable for machine learning')

st.write(
    'The dataset contains customer, basket, product, category, sales, and time-related fields. '
    'These fields are suitable for recommendation systems because they show interactions between households and products. '
    'They are also suitable for Market Basket Analysis because baskets can be used to identify categories that are purchased together.'
)

if st.checkbox('Show sample transaction data'):
    st.subheader('Sample transaction data')
    st.write(
        'This table shows a small sample of the prepared transaction data. '
        'Only 1,000 rows are used to keep the dashboard responsive.'
    )
    st.write(dashboard_sample)