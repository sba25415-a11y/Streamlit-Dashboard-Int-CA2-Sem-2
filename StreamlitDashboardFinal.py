import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title='Online Retail Patterns Dashboard',
    layout='wide'
)

department_summary = pd.read_csv('dashboard_department_summary_improved.csv')
weekly_summary = pd.read_csv('dashboard_weekly_summary_improved.csv')
category_summary = pd.read_csv('dashboard_category_summary_improved.csv')
dashboard_sample = pd.read_csv('dashboard_sample_improved.csv')

dark_text = '#1F1F1F'

def paragraph(text):
    st.markdown(
        f"<p style='font-size:18px; color:{dark_text}; line-height:1.5;'>{text}</p>",
        unsafe_allow_html=True
    )

def bold_label(text):
    st.markdown(
        f"<p style='font-size:18px; color:{dark_text}; line-height:1.5; font-weight:700;'>{text}</p>",
        unsafe_allow_html=True
    )

def ml_support_table(df):
    st.markdown(
        """
        <style>
        .ml-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 18px;
            color: #1F1F1F;
        }
        .ml-table th {
            background-color: #2F5D7C;
            color: white;
            padding: 12px;
            text-align: left;
            font-size: 18px;
        }
        .ml-table td {
            padding: 12px;
            border: 1px solid #B8B8B8;
            font-size: 18px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        df.to_html(index=False, classes='ml-table'),
        unsafe_allow_html=True
    )

def improve_chart(fig, height):
    fig.update_layout(
        title_text='',
        height=height,
        font=dict(size=16, color=dark_text),
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(
            title_font=dict(size=17, color=dark_text),
            tickfont=dict(size=16, color=dark_text),
            color=dark_text
        ),
        yaxis=dict(
            title_font=dict(size=17, color=dark_text),
            tickfont=dict(size=16, color=dark_text),
            color=dark_text
        )
    )
    return fig

st.sidebar.title('Dashboard menu')

selected_section = st.sidebar.radio(
    'Go to section',
    [
        'Retail overview',
        'Recommendation Systems',
        'Market Basket Analysis',
        'Sample data'
    ]
)

st.sidebar.markdown('---')
st.sidebar.subheader('Quick guide')
st.sidebar.write('1. Start with the retail overview.')
st.sidebar.write('2. Review recommendation systems.')
st.sidebar.write('3. Review basket-analysis results.')
st.sidebar.write('4. Open sample data only if needed.')

st.sidebar.markdown('---')
st.sidebar.subheader('Design focus')
st.sidebar.write('Readable text')
st.sidebar.write('Clear journey')
st.sidebar.write('Low clutter')
st.sidebar.write('Balanced colours')
st.sidebar.write('Focused charts')
st.sidebar.write('Plain language')

st.title('Online Retail Patterns Dashboard')

if selected_section == 'Retail overview':
    paragraph(
        'This dashboard summarises grocery retail transaction patterns and shows why the dataset is '
        'suitable for machine-learning methods in a retail business context.'
    )

elif selected_section == 'Recommendation Systems':
    paragraph(
        'This dashboard summarises grocery retail transaction patterns and presents the main findings showing that '
        'the dataset is suitable for recommendation-system machine-learning methods in a retail business context.'
    )

elif selected_section == 'Market Basket Analysis':
    paragraph(
        'This dashboard summarises grocery retail transaction patterns and presents the main findings showing that '
        'the dataset is suitable for Market Basket Analysis methods, including Apriori and FP-Growth, in a retail business context.'
    )

total_sales = department_summary['total_sales_value'].sum()
total_baskets = department_summary['total_baskets'].sum()
total_households = department_summary['unique_households'].sum()
total_products = department_summary['unique_products'].sum()

if selected_section == 'Retail overview':

    st.subheader('Retail overview')

    paragraph(
        'This section gives a simple summary of the grocery retail transaction dataset. It shows total '
        'sales value, basket activity, weekly shopping patterns, and the strongest product categories.'
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric('Total sales value', f'{total_sales:,.2f}')
    col2.metric('Total baskets', f'{int(total_baskets):,}')
    col3.metric('Unique households', f'{int(total_households):,}')
    col4.metric('Unique products', f'{int(total_products):,}')

    st.markdown('---')

    st.subheader('1. Sales value by department')

    department_plot_data = department_summary.sort_values(
        'total_sales_value',
        ascending=False
    )

    department_sales_fig = px.bar(
        department_plot_data,
        x='department',
        y='total_sales_value',
        labels={
            'department': 'Department',
            'total_sales_value': 'Total Sales Value',
            'total_baskets': 'Total Baskets',
            'unique_households': 'Unique Households',
            'average_sales_per_basket': 'Average Sales per Basket'
        },
        hover_data=[
            'total_baskets',
            'unique_households',
            'average_sales_per_basket'
        ]
    )

    department_sales_fig.update_traces(
        marker_color='#4C78A8',
        hoverlabel=dict(
            font=dict(size=16, color=dark_text),
            bgcolor='white',
            bordercolor=dark_text
        )
    )

    department_sales_fig = improve_chart(department_sales_fig, 700)
    department_sales_fig.update_layout(xaxis_tickangle=-35)

    st.plotly_chart(department_sales_fig, use_container_width=True)

    paragraph(
        'This chart shows which departments have the highest total sales value.'
    )

    st.markdown('---')

    st.subheader('2. Total baskets by department')

    department_basket_fig = px.bar(
        department_plot_data,
        x='department',
        y='total_baskets',
        labels={
            'department': 'Department',
            'total_baskets': 'Total Baskets',
            'total_sales_value': 'Total Sales Value',
            'unique_households': 'Unique Households',
            'average_sales_per_basket': 'Average Sales per Basket'
        },
        hover_data=[
            'total_sales_value',
            'unique_households',
            'average_sales_per_basket'
        ]
    )

    department_basket_fig.update_traces(
        marker_color='#72B7B2',
        hoverlabel=dict(
            font=dict(size=16, color=dark_text),
            bgcolor='white',
            bordercolor=dark_text
        )
    )

    department_basket_fig = improve_chart(department_basket_fig, 700)
    department_basket_fig.update_layout(xaxis_tickangle=-35)

    st.plotly_chart(department_basket_fig, use_container_width=True)

    paragraph(
        'This chart focuses on customer activity, not only on sales value.'
    )

    st.markdown('---')

    st.subheader('3. Weekly sales trend')

    weekly_fig = px.line(
        weekly_summary,
        x='week',
        y='total_sales_value',
        labels={
            'week': 'Week',
            'total_sales_value': 'Total Sales Value',
            'total_baskets': 'Total Baskets',
            'unique_households': 'Unique Households',
            'average_sales_per_basket': 'Average Sales per Basket'
        },
        hover_data=[
            'total_baskets',
            'unique_households',
            'average_sales_per_basket'
        ]
    )

    weekly_fig.update_traces(
        line_color='#54A24B',
        line_width=4,
        hoverlabel=dict(
            font=dict(size=16, color=dark_text),
            bgcolor='white',
            bordercolor=dark_text
        )
    )

    weekly_fig = improve_chart(weekly_fig, 650)

    st.plotly_chart(weekly_fig, use_container_width=True)

    paragraph(
        'This chart shows how total sales changed week by week.'
    )

    st.markdown('---')

    st.subheader('4. Top product categories')

    bold_label('Select number of categories to display')

    number_of_categories = st.slider(
        ' ',
        5,
        20,
        10
    )

    top_categories = category_summary.sort_values(
        'total_sales_value',
        ascending=False
    ).head(number_of_categories)

    category_fig = px.bar(
        top_categories.sort_values('total_sales_value', ascending=True),
        x='total_sales_value',
        y='product_category',
        orientation='h',
        labels={
            'total_sales_value': 'Total Sales Value',
            'product_category': 'Product Category',
            'department': 'Department',
            'total_baskets': 'Total Baskets',
            'unique_households': 'Unique Households',
            'average_sales_per_basket': 'Average Sales per Basket'
        },
        hover_data=[
            'department',
            'total_baskets',
            'unique_households',
            'average_sales_per_basket'
        ]
    )

    category_fig.update_traces(
        marker_color='#F58518',
        hoverlabel=dict(
            font=dict(size=16, color=dark_text),
            bgcolor='white',
            bordercolor=dark_text
        )
    )

    category_fig = improve_chart(category_fig, 700)

    st.plotly_chart(category_fig, use_container_width=True)

    paragraph(
        'This chart shows which product categories have the highest sales value.'
    )

    st.markdown(
        """
        <div style='font-size:18px; color:#1F1F1F; line-height:1.5; background-color:#EAF2F8; padding:14px; border-radius:8px; border-left:6px solid #2F5D7C;'>
        <strong>Interpretation note:</strong> COUPON/MISC ITEMS is a mixed category. It includes fuel-related and miscellaneous purchases, not only coupons or discounts.<br><br>
        The fuel sales value may be high because fuel purchases usually have higher transaction values than many regular grocery items. This means it is not a typical grocery product category.<br><br>
        For this reason, results from this category should not be treated as normal grocery-product behaviour.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown('---')

    st.subheader('How these visualisations support machine-learning suitability')

    bold_label('Select a visualisation to see how it supports machine-learning suitability')

    visualisation_choice = st.selectbox(
        ' ',
        [
            'Sales value by department',
            'Total baskets by department',
            'Weekly sales trend',
            'Top product categories'
        ]
    )

    ml_explanation = {
        'Sales value by department': [
            'Product and purchasing behaviour: where the strongest sales performance is concentrated.',
            'Differences between departments show that the dataset contains useful product-group patterns.',
            'Recommendation systems'
        ],
        'Total baskets by department': [
            'Customer activity: departments where customers shop more often.',
            'Repeated customer-product interactions can be used to understand purchasing behaviour.',
            'Recommendation systems'
        ],
        'Weekly sales trend': [
            'Time-based shopping behaviour: how total sales changed week by week.',
            'Useful for retail monitoring because it shows when customer purchasing activity changes over time.',
            'Recommendation systems'
        ],
        'Top product categories': [
            'Product-level patterns: sales value of product categories.',
            'Differences between categories allow similar or related products to be compared and allow product categories to be analysed to identify items commonly bought together.',
            'Recommendation systems and Market Basket Analysis'
        ]
    }

    selected_info = ml_explanation[visualisation_choice]

    ml_table = pd.DataFrame({
        'What it identifies': [selected_info[0]],
        'Why it supports ML suitability': [selected_info[1]],
        'ML Method': [selected_info[2]]
    })

    ml_support_table(ml_table)

    st.markdown(
        """
        <div style='font-size:18px; color:#1F1F1F; line-height:1.5; background-color:#EAF7EA; padding:14px; border-radius:8px; border-left:6px solid #2E6B35;'>
        <strong>Conclusion:</strong> the dataset is suitable for ML because the dashboard shows customer-product interactions, basket-level behaviour, product/category structure, sales variation, and time-based patterns.<br><br>
        These features support the ML methods of recommendation systems and Market Basket Analysis with Apriori and FP-Growth, and practical retail decision-making processes.
        </div>
        """,
        unsafe_allow_html=True
    )

elif selected_section == 'Recommendation Systems':

    st.subheader('Recommendation system findings')

    paragraph(
        'Recommendation systems were used to identify products that may be relevant to a household based on '
        'product information and purchasing behaviour. This section summarises the three recommendation approaches used in the project.'
    )

    rec_summary = pd.DataFrame({
        'Approach': [
            'Content-based filtering',
            'User-user collaborative filtering',
            'Item-item collaborative filtering'
        ],
        'Main input used': [
            'Product information such as department, category, product type, and brand',
            'Patterns in how households interact with products',
            'Similarities between products based on household purchasing patterns'
        ],
        'Main purpose': [
            'Recommends products that are similar to a selected product',
            'Recommends products based on households with similar purchasing behaviour',
            'Recommends products similar to items that a household has already interacted with'
        ],
        'Business value': [
            'Helps suggest related products when product details are available',
            'Supports personalised recommendations based on customer behaviour',
            'Supports cross-selling and helps customers discover related products'
        ]
    })

    ml_support_table(rec_summary)

    st.subheader('Why the dataset supports recommendation systems')

    paragraph(
        'The dataset is suitable for recommendation systems because it includes household IDs, product IDs, '
        'product information, and purchasing behaviour.'
    )

    paragraph(
        'The project used purchase data instead of customer ratings, because the dataset records what households bought. '
        'So, the dataset fields help identify user-item relationships and product-similarity patterns.'
    )

    rec_col1, rec_col2, rec_col3 = st.columns(3)

    rec_col1.metric('Recommendation approaches', '3')
    rec_col2.metric('User field', 'household_id')
    rec_col3.metric('Item field', 'product_id')

elif selected_section == 'Market Basket Analysis':

    st.subheader('Market Basket Analysis findings')

    paragraph(
        'Market Basket Analysis was used to find product categories that are often bought together.'
    )

    mba_col1, mba_col2, mba_col3 = st.columns(3)

    mba_col1.metric('Baskets analysed', '155,655')
    mba_col2.metric('Product-category columns', '302')
    mba_col3.metric('Rules found by each model', '2,098')

    st.subheader('Strongest business-logical associations')

    mba_rules = pd.DataFrame({
        'Association pattern': [
            'Dry noodles/pasta and pasta sauce',
            'Cheeses and deli meats',
            'Onions and peppers',
            'Bath tissues and paper towels',
            'Carrots and other vegetables'
        ],
        'Business interpretation': [
            'Useful for meal-solution placement or pasta-related promotions',
            'Useful for sandwich, lunch, or deli-related cross-selling',
            'Useful for cooking-ingredient grouping',
            'Useful for household essentials placement',
            'Useful for vegetable and fresh-food promotions'
        ]
    })

    ml_support_table(mba_rules)

    paragraph(
        'The Apriori and FP-Growth results were consistent under the selected settings.'
    )

    paragraph(
        'This supports the reliability of the main category-level patterns, because both methods found the same type of product associations.'
    )

    st.subheader('Why the dataset supports Market Basket Analysis')

    paragraph(
        'The dataset is suitable for Market Basket Analysis using Apriori and FP-Growth because it contains basket-level co-purchase patterns.'
    )

    paragraph(
        'From a retail perspective, these results can support product placement, bundle promotions, cross-selling, and recommendation prompts.'
    )

elif selected_section == 'Sample data':

    st.subheader('Sample transaction data')

    paragraph(
        'This section shows a small sample of the prepared transaction data.'
    )

    st.dataframe(dashboard_sample, use_container_width=True)

    st.subheader('Data dictionary')

    bold_label('Select a column to see its meaning')

    selected_column = st.selectbox(
        ' ',
        [
            'household_id',
            'basket_id',
            'product_id',
            'department',
            'product_category',
            'product_type',
            'quantity',
            'sales_value',
            'week',
            'transaction_timestamp'
        ]
    )

    data_dictionary = {
        'household_id': 'Unique identification number for each household. It helps show which household made the purchase.',
        'basket_id': 'Unique identification number for each shopping basket or transaction. One basket can contain one or more products purchased together.',
        'product_id': 'Unique identification number for each product purchased.',
        'department': 'The broad retail department where the product belongs, such as grocery, pastry, or other store departments.',
        'product_category': 'The product category within the department. This gives more detail about the type of product purchased.',
        'product_type': 'A more specific product description within the product category.',
        'quantity': 'The number of units purchased for that product in the basket.',
        'sales_value': 'The sales value of the product purchased in that transaction line.',
        'week': 'The week number when the transaction happened. This helps analyse shopping behaviour over time.',
        'transaction_timestamp': 'The date and time when the transaction was recorded.'
    }

    selected_dictionary_table = pd.DataFrame({
        'Column': [selected_column],
        'Meaning': [data_dictionary[selected_column]]
    })

    ml_support_table(selected_dictionary_table)

    st.markdown(
        """
        <div style='font-size:18px; color:#1F1F1F; line-height:1.5; background-color:#EAF2F8; padding:14px; border-radius:8px; border-left:6px solid #2F5D7C;'>
        <strong>Note:</strong> the sample table is included only for inspection. The main dashboard findings are based on prepared summary files, not on loading the full transaction dataset into the dashboard.
        </div>
        """,
        unsafe_allow_html=True
    )