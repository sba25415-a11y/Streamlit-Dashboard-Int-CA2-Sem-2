import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title = 'Online Retail Dashboard',
    layout = 'wide'
)

st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        font-size: 20px !important;
        color: #1F1F1F !important;
    }

    p, div, span, label {
        font-size: 20px !important;
        color: #1F1F1F !important;
    }

    h1 {
        font-size: 42px !important;
        color: #1F1F1F !important;
    }

    h2 {
        font-size: 34px !important;
        color: #1F1F1F !important;
    }

    h3 {
        font-size: 28px !important;
        color: #1F1F1F !important;
    }

    [data-testid="stMetricLabel"] {
        font-size: 22px !important;
        color: #1F1F1F !important;
    }

    [data-testid="stMetricValue"] {
        font-size: 34px !important;
        color: #1F1F1F !important;
    }

    .access-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 20px;
        color: #1F1F1F;
    }

    .access-table th {
        background-color: #2F5D7C;
        color: white;
        padding: 12px;
        text-align: left;
        font-size: 21px;
    }

    .access-table td {
        padding: 12px;
        border: 1px solid #B8B8B8;
        font-size: 20px;
    }

    .access-table tr:nth-child(even) {
        background-color: #F4F7F9;
    }

    .access-table tr:nth-child(odd) {
        background-color: #FFFFFF;
    }
    </style>
    """,
    unsafe_allow_html = True
)

department_summary = pd.read_csv('dashboard_department_summary_improved.csv')
weekly_summary = pd.read_csv('dashboard_weekly_summary_improved.csv')
category_summary = pd.read_csv('dashboard_category_summary_improved.csv')
dashboard_sample = pd.read_csv('dashboard_sample_improved.csv')

dark_text = '#1F1F1F'
blue_dark = '#2F5D7C'
blue_light = '#5B8DB8'
teal_dark = '#2F7773'
teal_light = '#72B7B2'
orange_dark = '#B75E00'
orange_light = '#F28E2B'
green_dark = '#2E6B35'

chart_font = dict(size = 22, color = dark_text)
title_font = dict(size = 26, color = dark_text)
axis_title_font = dict(size = 24, color = dark_text)
tick_font = dict(size = 22, color = dark_text)
hover_label = dict(
    font = dict(size = 20, color = dark_text),
    bgcolor = 'white',
    bordercolor = dark_text
)

def improve_chart_layout(fig, height):
    fig.update_layout(
        height = height,
        title_font = title_font,
        font = chart_font,
        plot_bgcolor = 'white',
        paper_bgcolor = 'white',
        showlegend = False,
        xaxis = dict(
            title_font = axis_title_font,
            tickfont = tick_font,
            color = dark_text
        ),
        yaxis = dict(
            title_font = axis_title_font,
            tickfont = tick_font,
            color = dark_text
        )
    )
    return fig

def show_accessible_table(df):
    st.markdown(
        df.to_html(index = False, classes = 'access-table'),
        unsafe_allow_html = True
    )

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

if selected_section == 'Retail overview':

    st.subheader('Retail overview')

    st.write(
        'This section summarises the most important aspects of the retail dataset: sales value, basket activity, '
        'weekly behaviour, and the strongest product categories.'
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
    ).copy()

    department_plot_data['bar_colour'] = [
        blue_dark if i % 2 == 0 else blue_light
        for i in range(len(department_plot_data))
    ]

    department_sales_fig = px.bar(
        department_plot_data,
        x = 'department',
        y = 'total_sales_value',
        color = 'bar_colour',
        color_discrete_map = 'identity',
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

    department_sales_fig.update_traces(hoverlabel = hover_label)
    department_sales_fig = improve_chart_layout(department_sales_fig, 750)
    department_sales_fig.update_layout(xaxis_tickangle = -35)

    st.plotly_chart(department_sales_fig, use_container_width = True)

    st.write(
        'This chart identifies which departments generate the highest sales value. '
        'It shows that the dataset contains strong differences between departments.'
    )

    st.markdown('---')

    st.subheader('2. Total baskets by department')

    department_basket_fig = px.bar(
        department_plot_data,
        x = 'department',
        y = 'total_baskets',
        color = 'bar_colour',
        color_discrete_map = 'identity',
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

    department_basket_fig.update_traces(hoverlabel = hover_label)
    department_basket_fig = improve_chart_layout(department_basket_fig, 750)
    department_basket_fig.update_layout(xaxis_tickangle = -35)

    st.plotly_chart(department_basket_fig, use_container_width = True)

    st.write(
        'This chart focuses on customer activity rather than sales value. '
        'Departments with many baskets show frequent customer interaction.'
    )

    st.markdown('---')

    st.subheader('3. Weekly sales trend')

    weekly_fig = px.line(
        weekly_summary,
        x = 'week',
        y = 'total_sales_value',
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
        line_color = green_dark,
        line_width = 5,
        hoverlabel = hover_label
    )

    weekly_fig = improve_chart_layout(weekly_fig, 700)

    st.plotly_chart(weekly_fig, use_container_width = True)

    st.write(
        'This chart shows how sales changed across the year. '
        'The weekly structure confirms that the dataset contains time-based behaviour.'
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
    ).head(number_of_categories).copy()

    top_categories = top_categories.sort_values('total_sales_value', ascending = True)
    top_categories['bar_colour'] = [
        orange_dark if i % 2 == 0 else orange_light
        for i in range(len(top_categories))
    ]

    category_fig = px.bar(
        top_categories,
        x = 'total_sales_value',
        y = 'product_category',
        orientation = 'h',
        color = 'bar_colour',
        color_discrete_map = 'identity',
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

    category_fig.update_traces(hoverlabel = hover_label)
    category_fig = improve_chart_layout(category_fig, 750)

    st.plotly_chart(category_fig, use_container_width = True)

    st.write(
        'This chart shows which product categories are most important by sales value. '
        'Category differences are useful for recommendation systems and Market Basket Analysis.'
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

    ml_table = pd.DataFrame({
        'Selected visualisation': [visualisation_choice],
        'What it identifies': [selected_info[0]],
        'Why it supports ML suitability': [selected_info[1]]
    })

    show_accessible_table(ml_table)

    st.success(
        'Conclusion: the retail dataset is suitable for machine-learning models because it contains customer behaviour, '
        'basket-level transactions, product metadata, category structure, sales values, and time information.'
    )

elif selected_section == 'Recommendation findings':

    st.subheader('Recommendation system findings')

    st.write(
        'The project tested three recommendation approaches. These results are summarised here in plain language.'
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

    show_accessible_table(rec_summary)

    st.subheader('Why the dataset supports recommendation systems')

    st.write(
        'The dataset is suitable for recommendation systems because it contains household IDs, product IDs, basket IDs, '
        'product metadata, and transaction behaviour.'
    )

    rec_col1, rec_col2, rec_col3 = st.columns(3)

    rec_col1.metric('Recommendation approaches', '3')
    rec_col2.metric('User field', 'household_id')
    rec_col3.metric('Item field', 'product_id')

    st.write(
        'The implementation used implicit interaction data rather than explicit ratings. '
        'This is appropriate because the retail dataset records purchases and basket behaviour, not rating scores.'
    )

elif selected_section == 'Market Basket Analysis':

    st.subheader('Market Basket Analysis findings')

    st.write(
        'Market Basket Analysis was used to identify product categories that are commonly purchased together.'
    )

    mba_summary = pd.DataFrame({
        'Algorithm': ['Apriori', 'FP-Growth'],
        'Frequent itemsets': [1198, 1198],
        'Association rules': [2098, 2098],
        'Minimum support': [0.01, 0.01],
        'Maximum itemset length': [2, 2],
        'Item level': ['product_category', 'product_category']
    })

    show_accessible_table(mba_summary)

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

    show_accessible_table(mba_rules)

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
        'basket-level transactions, product metadata, product categories, sales values, and time information.'
    )