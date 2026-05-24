import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title = 'Online Retail Dashboard',
    layout = 'wide'
)

st.title('Online Retail Dashboard for Adults Aged 65+')

st.write(
    'This improved dashboard summarises key online retail patterns using prepared transaction summaries. '
)

st.sidebar.title('Dashboard guide')
st.sidebar.write(
    'Use this dashboard to review sales, baskets, households, products, and product categories. '
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
    department_plot_data = department_summary.sort_values(
        'total_sales_value',
        ascending = False
    )

    department_fig = px.bar(
        department_plot_data,
        x = 'department',
        y = 'total_sales_value',
        title = 'Total Sales Value by Department',
        labels = {
            'department': 'Department',
            'total_sales_value': 'Total Sales Value',
            'total_baskets': 'Total Baskets',
            'unique_households': 'Unique Households',
            'average_sales_per_basket': 'Average Sales per Basket'
        },
        hover_data = [
            'total_baskets',
            'unique_households',
            'average_sales_per_basket'
        ]
    )

    department_fig.update_layout(
        xaxis_tickangle = -45,
        height = 500
    )

    st.plotly_chart(department_fig, use_container_width = True)

with right_col:
    weekly_fig = px.line(
        weekly_summary,
        x = 'week',
        y = 'total_sales_value',
        title = 'Weekly Sales Value Trend',
        labels = {
            'week': 'Week',
            'total_sales_value': 'Total Sales Value',
            'total_baskets': 'Total Baskets',
            'unique_households': 'Unique Households',
            'average_sales_per_basket': 'Average Sales per Basket'
        },
        hover_data = [
            'total_baskets',
            'unique_households',
            'average_sales_per_basket'
        ]
    )

    weekly_fig.update_layout(
        height = 500
    )

    st.plotly_chart(weekly_fig, use_container_width = True)

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

category_fig = px.bar(
    top_categories.sort_values('total_sales_value', ascending = True),
    x = 'total_sales_value',
    y = 'product_category',
    orientation = 'h',
    title = 'Top Product Categories by Sales Value',
    labels = {
        'total_sales_value': 'Total Sales Value',
        'product_category': 'Product Category',
        'department': 'Department',
        'total_baskets': 'Total Baskets',
        'unique_households': 'Unique Households',
        'average_sales_per_basket': 'Average Sales per Basket'
    },
    hover_data = [
        'department',
        'total_baskets',
        'unique_households',
        'average_sales_per_basket'
    ]
)

category_fig.update_layout(
    height = 550
)

st.plotly_chart(category_fig, use_container_width = True)

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