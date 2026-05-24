import streamlit as st
import pandas as pd
import numpy as np

st.title('Online Retail Dashboard for Adults Aged 65+')

st.write(
    'This dashboard summarises key online retail patterns using prepared transaction data. '
    'It is designed with simple navigation, clear summaries, and easy-to-read outputs.'
)

department_summary = pd.read_csv('dashboard_department_summary.csv')
weekly_summary = pd.read_csv('dashboard_weekly_summary.csv')
category_summary = pd.read_csv('dashboard_category_summary.csv')
dashboard_sample = pd.read_csv('dashboard_sample.csv')

st.subheader('Key retail summary')

total_sales = department_summary['total_sales_value'].sum()
total_baskets = department_summary['total_baskets'].sum()
total_households = department_summary['unique_households'].sum()
total_products = department_summary['unique_products'].sum()

st.write('Total sales value:', round(total_sales, 2))
st.write('Total baskets:', int(total_baskets))
st.write('Unique households:', int(total_households))
st.write('Unique products:', int(total_products))

st.subheader('Sales value by department')

department_chart = department_summary.set_index('department')['total_sales_value']
st.bar_chart(department_chart)

st.subheader('Weekly sales trend')

weekly_chart = weekly_summary.set_index('week')['total_sales_value']
st.line_chart(weekly_chart)

st.subheader('Top product categories')

number_of_categories = st.slider('Select number of categories to display', 5, 20, 10)

top_categories = category_summary.sort_values(
    'total_sales_value',
    ascending = False
).head(number_of_categories)

category_chart = top_categories.set_index('product_category')['total_sales_value']
st.bar_chart(category_chart)

if st.checkbox('Show sample data'):
    st.subheader('Sample transaction data')
    st.write(dashboard_sample)