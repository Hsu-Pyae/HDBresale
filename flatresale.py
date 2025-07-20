import pandas as pd
import streamlit as st
import plotly.express as px
df = pd.read_csv('HDDclean.csv')
st.set_page_config(page_title='HDB Resale Market',page_icon=':bar_chart:',layout='wide')
st.sidebar.header('Please Filter Here')

flat_type = st.sidebar.multiselect(
    'Select Flat Types',
    options = df['flat_type'].unique(),
    default = df['flat_type'].unique()[:5]
)

town_name = st.sidebar.multiselect(
    'Select Town',
    options = df['town'].unique(),
    default = df['town'].unique()[:5]
)

year_name = st.sidebar.multiselect(
    'Select Year',
    options = df['year'].unique(),
    default = df['year'].unique()[:5]
)

st.subheader(':bar_chart: HDB Resale Market')
st.markdown('##')

lowest = df['resale_price'].min()
highest = df['resale_price'].max()
average = df['resale_price'].median()

col1,col2,col3 = st.columns(3)
with col1:
    st.subheader('Lowest Price')
    st.subheader(f'SG $ {lowest}')
    
with col2:
    st.subheader('Highest Price')
    st.subheader(f' SG $ {highest}')
    
with col3:
    st.subheader('Average Price')
    st.subheader(f'SG $ {average}')

df_summary = df.groupby('year')['resale_price'].agg(['max','min','median'])
df_melted = df_summary.reset_index().melt(id_vars='year', value_vars=['max', 'min', 'median'],var_name='price_category', value_name='resale_price')

fig1 = px.line(df_melted,
              x= 'year',
              y= 'resale_price',
              color='price_category',
              markers= True,
              title = 'Resale Price Trends(max,min,average)'
)
st.plotly_chart(fig1)

df_select = df.query('flat_type == @flat_type and town == @town_name and year == @year_name')

a,b = st.columns(2)

aa = df_select.groupby('flat_type')['resale_price'].mean().sort_values()
fig2 = px.bar(
    aa,
    x=aa.values,
    y=aa.index,
    title = 'Resale Prices by Flat Type'
)
a.plotly_chart(fig2,use_container_width=True)

bb = df_select.groupby('town')['resale_price'].mean().sort_values()
fig3 = px.bar(
    bb,
    x=bb.values,
    y=bb.index,
    title = 'Resale Prices by Town'
)
b.plotly_chart(fig3,use_container_width=True)

c,d= st.columns(2)

fig4 = px.density_heatmap(
    df_select,
    x='town',
    y='flat_type',
    z='resale_price',
    histfunc='avg',
    title = 'Resale Prices by Town and Flat Type'
)
c.plotly_chart(fig4,use_container_width=True)

fig5 = px.density_heatmap(
    df_select,
    x='town',
    y='year',
    z='resale_price',
    histfunc='avg',
    title = 'Resale Prices by Town and Year'
)
d.plotly_chart(fig5,use_container_width=True)

e,f = st.columns(2)

df_transactions_by_town=df.groupby('town').agg(num_of_resale=('resale_price','count'))
ee = df_transactions_by_town['num_of_resale'].sort_values()
fig6 = px.bar(
    ee,
    x=ee.values,
    y=ee.index,
    title = 'No. of transactions by town'
)
e.plotly_chart(fig6,use_container_width=True)

bins = [100000, 300000, 500000, 700000, 900000, 1250000]
labels = ['100K-300K', '300K-500K', '500K-700K', '700K-900K','above 900K']
df['price_range'] = pd.cut(df['resale_price'], bins=bins, labels=labels)
fig7 = px.pie(
    df,
    names='price_range',
    title = 'Resale Price Distribution',
    hole = 0.5
)
f.plotly_chart(fig7,use_container_width=True)