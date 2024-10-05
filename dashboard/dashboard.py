import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
from datetime import date

sns.set(style='dark')

all_df = pd.read_csv('dashboard/all_data.csv')

min_date = pd.to_datetime(all_df['dteday']).dt.date.min()
max_date = pd.to_datetime(all_df['dteday']).dt.date.max()

with st.sidebar:
    start_date, end_date = st.date_input(
        label='Select Date', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df['dteday'] >= str(start_date)) &
                 (all_df['dteday'] <= str(end_date))]

st.title("Bike Sharing Data Analysis")
st.markdown("""
## Business Questions:
- *How do environmental conditions affect the number of bicycle rentals?*
- *How do seasons, months, and days affect the usage patterns of bike sharing services?*
""")

# Menampilkan data yang difilter
st.header("Sharing Bike in Selected Date:")
st.dataframe(main_df[['dteday', 'casual_day', 'registered_day', 'cnt_day']])

if 'show_hourly_data' not in st.session_state:
    st.session_state.show_hourly_data = False
def toggle_hourly_data():
    st.session_state.show_hourly_data = not st.session_state.show_hourly_data
st.button('Details', on_click=toggle_hourly_data)
if st.session_state.show_hourly_data:
    st.write("Hourly data based on a 2-hour time span:")
    st.dataframe(main_df[['dteday', 'casual_hour', 'registered_hour', 'cnt_hour']])

if 'show_condition_data' not in st.session_state:
    st.session_state.show_condition_data = False
def toggle_condition_data():
    st.session_state.show_condition_data = not st.session_state.show_condition_data
st.button('Condition', on_click=toggle_condition_data)
if st.session_state.show_condition_data:
    st.write("Condition in Selected Date:")
    st.dataframe(main_df[['dteday', 'temp_day','atemp_day', 'hum_day', 'windspeed_day', 'weathersit_day',]])

st.header("Season, Month, & Day:")

if 'show_season_data' not in st.session_state:
    st.session_state.show_season_data = False
def toggle_season_data():
    st.session_state.show_season_data = not st.session_state.show_season_data
st.button('Bike Renters By Season', on_click=toggle_season_data)
if st.session_state.show_season_data:
    plt.figure(figsize=(8, 5))
    most_season = all_df.groupby('season_day')['cnt_day'].sum().reset_index()
    colors = ['#D3D3D3', '#D3D3D3', '#72BCD4', '#D3D3D3']
    bars = plt.bar(most_season['season_day'], most_season['cnt_day'], color=colors)
    plt.title('Bike Renters By Season')
    plt.xlabel('Season')
    plt.ylabel('Count')
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x(), yval, int(yval), va='bottom')
    st.pyplot(plt)
    plt.close()

if 'show_month_data' not in st.session_state:
    st.session_state.show_month_data = False
def toggle_month_data():
    st.session_state.show_month_data = not st.session_state.show_month_data
st.button('Bike Renters By Month', on_click=toggle_month_data)
if st.session_state.show_month_data:
    plt.figure(figsize=(8, 5))
    most_month = all_df.groupby('mnth_day')['cnt_day'].sum().reset_index()
    colors = ['#D3D3D3', '#D3D3D3', '#D3D3D3', '#D3D3D3', '#D3D3D3', '#D3D3D3', '#D3D3D3','#72BCD4','#D3D3D3','#D3D3D3','#D3D3D3','#D3D3D3']
    bars = plt.bar(most_month['mnth_day'], most_month['cnt_day'], color=colors)
    plt.title('Bike Renters By Month')
    plt.xlabel('Month')
    plt.ylabel('Count')
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x(), yval, int(yval), va='bottom', fontsize=6)
    st.pyplot(plt)
    plt.close()

if 'show_day_data' not in st.session_state:
    st.session_state.show_day_data = False
def toggle_day_data():
    st.session_state.show_day_data = not st.session_state.show_day_data
st.button('Bike Renters By Day', on_click=toggle_day_data)
if st.session_state.show_day_data:
    plt.figure(figsize=(8, 5))
    weekday_group = all_df.groupby('weekday_hour')['cnt_hour'].mean().reset_index()
    colors = ['#D3D3D3', '#D3D3D3', '#D3D3D3', '#D3D3D3', '#D3D3D3', '#72BCD4', '#D3D3D3']
    bars = plt.bar(weekday_group['weekday_hour'], weekday_group['cnt_hour'], color=colors)
    plt.title('Bike Renters By Day')
    plt.xlabel('Day')
    plt.ylabel('Count')
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x(), yval, int(yval), va='bottom',)
    st.pyplot(plt)
    plt.close()


st.header("Effect of environmental conditions: ")

if 'show_temp_data' not in st.session_state:
    st.session_state.show_temp_data = False
def toggle_temp_data():
    st.session_state.show_temp_data = not st.session_state.show_temp_data
st.button('Effect of Temperature', on_click=toggle_temp_data)
if st.session_state.show_temp_data:
    plt.figure(figsize=(8, 5))
    sns.regplot(x='temp_day',
                y='cnt_day',
                data=all_df,
                scatter_kws={'alpha':0.5},
                line_kws={'color':'red'})

    plt.title('Temperature vs Count')
    plt.xlabel('Temperature')
    plt.ylabel('Count')
    st.pyplot(plt)
    plt.close()

    temp_group = all_df.groupby('temp_hour')['cnt_hour'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(x='temp_hour', y='cnt_hour', data=temp_group, marker='o', ax=ax)
    ax.set_title('Temperature vs Count')
    ax.set_xlabel('Temprature (Normalized)')
    ax.set_ylabel('Count')
    ax.grid(True)
    st.pyplot(fig)
    plt.close()

if 'show_hum_data' not in st.session_state:
    st.session_state.show_hum_data = False
def toggle_hum_data():
    st.session_state.show_hum_data = not st.session_state.show_hum_data
st.button('Effect of Humidity', on_click=toggle_hum_data)
if st.session_state.show_hum_data:
    plt.figure(figsize=(8, 5))
    sns.regplot(x='hum_day',
                y='cnt_day',
                data=all_df,
                scatter_kws={'alpha':0.5},
                line_kws={'color':'red'})

    plt.title('Humidity vs Count')
    plt.xlabel('Humidity')
    plt.ylabel('Count')
    st.pyplot(plt)
    plt.close()

    hum_group = all_df.groupby('hum_hour')['cnt_hour'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(x='hum_hour', y='cnt_hour', data=hum_group, marker='o', ax=ax)
    ax.set_title('Humidity vs Count')
    ax.set_xlabel('Humidity (Normalized)')
    ax.set_ylabel('Count')
    ax.grid(True)
    st.pyplot(fig)
    plt.close()

if 'show_windspeed_data' not in st.session_state:
    st.session_state.show_windspeed_data = False
def toggle_windspeed_data():
    st.session_state.show_windspeed_data = not st.session_state.show_windspeed_data
st.button('Effect of Windspeed', on_click=toggle_windspeed_data)
if st.session_state.show_windspeed_data:
    plt.figure(figsize=(8, 5))
    sns.regplot(x='windspeed_day',
                y='cnt_day',
                data=all_df,
                scatter_kws={'alpha':0.5},
                line_kws={'color':'red'})

    plt.title('Windspeed vs Count')
    plt.xlabel('Windspeed')
    plt.ylabel('Count')
    st.pyplot(plt)
    plt.close()

    windspeed_group = all_df.groupby('windspeed_hour')['cnt_hour'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(x='windspeed_hour', y='cnt_hour', data=windspeed_group, marker='o', ax=ax)
    ax.set_title('Windspeed vs Count')
    ax.set_xlabel('Windspeed (Normalized)')
    ax.set_ylabel('Count')
    ax.grid(True)
    st.pyplot(fig)
    plt.close()

if 'show_weathersit_data' not in st.session_state:
    st.session_state.show_weathersit_data = False
def toggle_weathersit_data():
    st.session_state.show_weathersit_data = not st.session_state.show_weathersit_data
st.button('Effect of Weathersit', on_click=toggle_weathersit_data)
if st.session_state.show_weathersit_data:
    plt.figure(figsize=(8, 5))
    weathersit_group = all_df.groupby('weathersit_day')['cnt_day'].mean().reset_index()
    colors = ['#72BCD4', '#D3D3D3', '#D3D3D3']
    bars = plt.bar(weathersit_group['weathersit_day'], weathersit_group['cnt_day'], color=colors)
    plt.title('Bike Renters')
    plt.xlabel('Weather')
    plt.ylabel('Count')
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x(), yval, int(yval), va='bottom',)
    st.write('note: 1: Sunny, 2: Misty, 3: Light Rain/Snow')
    st.pyplot(plt)
    plt.close()
