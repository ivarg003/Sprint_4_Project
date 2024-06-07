import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from datetime import datetime

st.header('Used Cars for Sale')
st.write('Get your used car today!!!')

df = pd.read_csv('vehicles_us.csv')

df = pd.read_csv('vehicles_us.csv')
df['model_year'] = df['model_year'].fillna(df['model_year'].median())
df['odometer'] = df.groupby("model_year")["odometer"].transform(lambda x: x.fillna(x.median()))
df['paint_color'] = df['paint_color'].fillna('unknown')  
df['is_4wd'] = df['is_4wd'].fillna(0)
df['cylinders'] = df.groupby("model_year")["cylinders"].transform(lambda x: x.fillna(x.median()))

model_choice = df['model'].unique()

selected_model = st.selectbox('Select a model', model_choice)

min_year, max_year = int(df['model_year'].min()), int(df['model_year'].max())  

year_range = st.slider('Choose Year Range', min_value=min_year, max_value=max_year, value=(min_year, max_year))

actual_range = list(range(year_range[0], year_range[1]+1))

df_filtered = df[(df['model'] == selected_model) & (df['model_year'].isin(actual_range))]

df_filtered 

st.header('Price Analysis') 
list_for_his = ['transmission', 'type', 'model']
selected_type = st.selectbox('Split For Price Distribution', list_for_his)

fig1 = px.histogram(df_filtered, color=selected_type, x= 'price')  
fig1.update_layout(title='<b>Split Price by {}</b>'.format(selected_type))
st.plotly_chart(fig1)

def age_category(x):
    if x < 5: 
        return '<5'
    elif 5 <= x < 10:  
        return '5-10'
    elif 10 <= x < 20:  
        return '10-20'
    else: 
        return '>20'

current_year = datetime.now().year
df['age'] = current_year - df['model_year']
df['age_category'] = df['age'].apply(age_category)   

scatter_list = ['odometer', 'cylinders', 'is_4wd']  
scatter_choice = st.selectbox('Price Dependency on', scatter_list)

fig2 = px.scatter(df, x='price', y=scatter_choice, color='age_category', hover_data=['model_year'])
fig2.update_layout(title='<b>Price VS {}</b>'.format(scatter_choice))  
st.plotly_chart(fig2)
