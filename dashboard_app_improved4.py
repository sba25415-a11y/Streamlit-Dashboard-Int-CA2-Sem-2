import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title = 'Online Retail Dashboard',
    layout = 'wide'
)

department_summary = pd.read_csv('dashboard_department_summary_improved.csv')
weekly_summary = pd.read_csv('dashboard_weekly_summary_improved.csv')
category_summary = pd.read_csv('dashboard_category_summary_improved.csv')
dashboard_sample = pd.read_csv('dashboard_sample_improved.csv')

st.sidebar.title('Dashboard menu')

selected_section = st.sidebar.radio(
    'Go to section',
    [
        'Retail overview',
        'Recommendation findings',
        'Market Basket Analysis',
        'Sample data'
    ]
)

st.sidebar.markdown('---')
st.sidebar.subheader('Quick guide')
st.sidebar.write('1. Start with the retail overview.')
st.sidebar.write('2. Review recommendation findings.')
st.sidebar.write('3. Review basket-analysis results.')
st.sidebar.write('4. Open sample data only if needed.')

st.sidebar.markdown('---')
st.sidebar.subheader('Design focus')
st.sidebar.write('Large summaries')
st.sidebar.write('Clear labels')
st.sidebar.write('Simple navigation')
st.sidebar.write('Low visual clutter')

st.title('Online Retail Dashboard for Adults Aged 65+')

st.write(
    'This dashboard summarises online retail patterns and key machine-learning findings.'
)

total_sales = department_summary['total_sales_value'].sum()
total_baskets = department_summary['total_baskets'].sum()
total_households = department_summary['unique_households'].sum()
total_products = department_summary['unique_products'].sum()

chart_font = dict(size = 18)
title_font = dict(size = 24)
axis_title_font = dict(size = 20)
hover_font = dict(font = dict(size = 18))

if selected_section == 'Retail overview':

    st.subheader('Retail overview')

    st.write(
        'This section summarises the most important aspects of the retail dataset: sales value, basket activity, '
        'weekly behaviour, and the strongest product categories. These views help show that the dataset contains '
        'clear product, customer, basket, and time-based patterns suitable for machine-learning analysis.'
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
        ascending = False
    )

    department_sales_fig = px.bar(
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

    department_sales_fig.update_traces(
        marker_color = '#4C78A8',
        hoverlabel = hover_font
    )

    department_sales_fig.update_layout(
        height = 700,
        title_font = title_font,
        font = chart_font,
        xaxis_title_font = axis_title_font,
        yaxis_title_font = axis_title_font,
        xaxis_tickangle = -35,
        plot_bgcolor = 'white'
    )

    st.plotly_chart(department_sales_fig, use_container_width = True)

    st.write(
        'This chart identifies which departments generate the highest sales value. '
        'It shows that the dataset contains strong differences between departments, which is useful for retail analysis.'
    )

    st.markdown('---')

    st.subheader('2. Total baskets by department')

    department_basket_fig = px.bar(
        department_plot_data,
        x = 'department',
        y = 'total_baskets',
        title = 'Total Baskets by Department',
        labels = {
            'department': 'Department',
            'total_baskets': 'Total Baskets',
            'total_sales_value': 'Total Sales Value',
            'unique_households': 'Unique Households',
            'average_sales_per_basket': 'Average Sales per Basket'
        },
        hover_data = [
            'total_sales_value',
            'unique_households',
            'average_sales_per_basket'
        ]
    )

    department_basket_fig.update_traces(
        marker_color = '#72B7B2',
        hoverlabel = hover_font
    )

    department_basket_fig.update_layout(
        height = 700,
        title_font = title_font,
        font = chart_font,
        xaxis_title_font = axis_title_font,
        yaxis_title_font = axis_title_font,
        xaxis_tickangle = -35,
        plot_bgcolor = 'white'
    )

    st.plotly_chart(department_basket_fig, use_container_width = True)

    st.write(
        'This chart focuses on customer activity rather than sales value. '
        'Departments with many baskets show frequent customer interaction, which supports recommendation-system logic.'
    )

    st.markdown('---')

    st.subheader('3. Weekly sales trend')

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

    weekly_fig.update_traces(
        line_color = '#54A24B',
        line_width = 4,
        hoverlabel = hover_font
    )

    weekly_fig.update_layout(
        height = 650,
        title_font = title_font,
        font = chart_font,
        xaxis_title_font = axis_title_font,
        yaxis_title_font = axis_title_font,
        plot_bgcolor = 'white'
    )

    st.plotly_chart(weekly_fig, use_container_width = True)

    st.write(
        'This chart shows how sales changed across the year. '
        'The weekly structure confirms that the dataset contains time-based behaviour useful for business monitoring.'
    )

    st.markdown('---')

    st.subheader('4. Top product categories')

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

    category_fig.update_traces(
        marker_color = '#F58518',
        hoverlabel = hover_font
    )

    category_fig.update_layout(
        height = 700,
        title_font = title_font,
        font = chart_font,
        xaxis_title_font = axis_title_font,
        yaxis_title_font = axis_title_font,
        plot_bgcolor = 'white'
    )

    st.plotly_chart(category_fig, use_container_width = True)

    st.write(
        'This chart shows which product categories are most important by sales value. '
        'Category differences are useful for recommendation systems and Market Basket Analysis because they show product-level structure.'
    )

    st.info(
        'Interpretation note: COUPON/MISC ITEMS should be interpreted carefully. '
        'Earlier checks showed that this category is strongly linked to fuel and miscellaneous items, not simply normal coupon-discount activity.'
    )

    st.markdown('---')

    st.subheader('How these visualisations support machine-learning suitability')

    visualisation_choice = st.selectbox(
        'Select a visualisation to see how it supports machine-learning suitability',
        [
            'Sales value by department',
            'Total baskets by department',
            'Weekly sales trend',
            'Top product categories',
            'Recommendation findings',
            'Market Basket Analysis findings'
        ]
    )

    ml_explanation = {
        'Sales value by department': [
            'Shows that departments behave differently in sales value.',
            'This supports machine learning because useful patterns exist across product groups.'
        ],
        'Total baskets by department': [
            'Shows where customer basket activity is concentrated.',
            'This supports recommendation systems because customer-product interactions are visible.'
        ],
        'Weekly sales trend': [
            'Shows sales behaviour across time.',
            'This supports business monitoring and shows that the dataset contains time-based structure.'
        ],
        'Top product categories': [
            'Shows that some product categories are much more important than others.',
            'This supports recommendation systems and Market Basket Analysis because product categories show meaningful variation.'
        ],
        'Recommendation findings': [
            'Shows that the dataset supports content-based, user-user, and item-item recommendation logic.',
            'This is possible because the dataset contains household IDs, product IDs, and product metadata.'
        ],
        'Market Basket Analysis findings': [
            'Shows that products/categories are bought together in meaningful ways.',
            'This supports Apriori and FP-Growth because the dataset contains basket-level transactions.'
        ]
    }

    selected_info = ml_explanation[visualisation_choice]

    st.table(pd.DataFrame({
        'Selected visualisation': [visualisation_choice],
        'What it identifies': [selected_info[0]],
        'Why it supports ML suitability': [selected_info[1]]
    }))

    st.success(
        'Conclusion: the retail dataset is suitable for machine-learning models because it contains customer behaviour, '
        'basket-level transactions, product metadata, category structure, sales values, and time information.'
    )

elif selected_section == 'Recommendation findings':

    st.subheader('Recommendation system findings')

    st.write(
        'The project tested three recommendation approaches. '
        'These results are summarised here in plain language for dashboard users.'
    )

    rec_summary = pd.DataFrame({
        'Approach': [
            'Content-based filtering',
            'User-user collaborative filtering',
            'Item-item collaborative filtering'
        ],
        'Main input used': [
            'Product metadata such as department, category, type, and brand',
            'Household-product interaction patterns',
            'Similarity between products based on household interactions'
        ],
        'Main purpose': [
            'Recommend products similar to a selected product',
            'Recommend products based on similar household behaviour',
            'Recommend products similar to items a household has interacted with'
        ],
        'Business value': [
            'Useful when product information is available',
            'Useful for personalisation based on customer behaviour',
            'Useful for cross-selling and product discovery'
        ]
    })

    st.dataframe(rec_summary, use_container_width = True)

    st.subheader('Why the dataset supports recommendation systems')

    st.write(
        'The dataset is suitable for recommendation systems because it contains household IDs, product IDs, basket IDs, '
        'product metadata, and transaction behaviour. These fields make it possible to build user-item relationships '
        'and item-similarity patterns.'
    )

    rec_col1, rec_col2, rec_col3 = st.columns(3)

    rec_col1.metric('Recommendation approaches', '3')
    rec_col2.metric('User field', 'household_id')
    rec_col3.metric('Item field', 'product_id')

    st.write(
        'The implementation used implicit interaction data rather than explicit ratings. '
        'This is appropriate because the retail dataset records purchases and basket behaviour, not customer rating scores.'
    )

elif selected_section == 'Market Basket Analysis':

    st.subheader('Market Basket Analysis findings')

    st.write(
        'Market Basket Analysis was used to identify product categories that are commonly purchased together. '
        'Both Apriori and FP-Growth were applied using the same prepared basket-category structure.'
    )

    mba_summary = pd.DataFrame({
        'Algorithm': ['Apriori', 'FP-Growth'],
        'Frequent itemsets': [1198, 1198],
        'Association rules': [2098, 2098],
        'Minimum support': [0.01, 0.01],
        'Maximum itemset length': [2, 2],
        'Item level': ['product_category', 'product_category']
    })

    st.dataframe(mba_summary, use_container_width = True)

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

    st.dataframe(mba_rules, use_container_width = True)

    st.write(
        'The Apriori and FP-Growth outputs were consistent under the selected settings. '
        'This supports the reliability of the main category-level association patterns.'
    )

    st.write(
        'From a retail perspective, these rules can support product placement, bundle promotions, '
        'cross-selling, and recommendation prompts.'
    )

elif selected_section == 'Sample data':

    st.subheader('Sample transaction data')

    st.write(
        'This section shows a small sample of the prepared transaction data. '
        'Only 1,000 rows are used so the dashboard remains responsive.'
    )

    st.dataframe(dashboard_sample, use_container_width = True)

    st.subheader('Dataset suitability summary')

    st.write(
        'The dataset is suitable for machine-learning work in online retail because it includes customer behaviour, '
        'basket-level transactions, product metadata, product categories, sales values, and time information. '
        'These fields support recommendation systems, Market Basket Analysis, and interactive business visualisation.'
    )