import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

def create_seasonal_users_df(df):
    seasonal_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    df['season_x'] = df['season_x'].map(seasonal_mapping)
    return df.groupby('season_x')['cnt_x'].sum().reset_index().rename(columns={'season_x': 'Season', 'cnt_x': 'Users'})

def create_monthly_users_df(df):
    month_mapping = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
        7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    df['mnth_x'] = df['mnth_x'].map(month_mapping)
    return df.groupby('mnth_x')['cnt_x'].sum().reset_index().rename(columns={'mnth_x': 'Month', 'cnt_x': 'Users'})

def create_daily_orders_df(df):
    df['dteday_x'] = pd.to_datetime(df['dteday_x'])
    daily_orders_df = df.resample(rule='D', on='dteday_x').agg({"cnt_x": "sum"}).reset_index()
    daily_orders_df.rename(columns={"cnt_x": "total_users"}, inplace=True)
    return daily_orders_df

all_df = pd.read_csv("dashboard/main_data.csv")
all_df["dteday_x"] = pd.to_datetime(all_df["dteday_x"])
all_df.sort_values(by="dteday_x", inplace=True)

st.sidebar.image("https://github.com/MidoriyaTenten/PicturesExample/blob/main/bikesharinglogo.png?raw=true")
min_date, max_date = all_df["dteday_x"].min(), all_df["dteday_x"].max()
start_date, end_date = st.sidebar.date_input("Rentang Waktu", [min_date, max_date], min_value=min_date, max_value=max_date)

main_df = all_df[(all_df["dteday_x"] >= pd.Timestamp(start_date)) & (all_df["dteday_x"] <= pd.Timestamp(end_date))]

st.header('Bike_Sharing Dashboard 🚲')

st.subheader("Daily Rentals")
daily_orders_df = create_daily_orders_df(main_df)
col1, col2 = st.columns(2)
col1.metric("Total Orders", value=len(daily_orders_df))
col2.metric("Total Users", value=daily_orders_df["total_users"].sum())

st.subheader('Seasonal Bike-Sharing Trends')
seasonal_users_df = create_seasonal_users_df(main_df)
fig, ax = plt.subplots()
ax.pie(seasonal_users_df['Users'], labels=seasonal_users_df['Season'], autopct='%1.1f%%', colors=['#D2691E', '#FFD700', '#00FF7F', '#ADD8E6'], explode=[0.1, 0, 0, 0])
st.pyplot(fig)

st.subheader("Monthly Bike-Sharing Trends")
monthly_users_df = create_monthly_users_df(main_df)
fig, ax = plt.subplots(figsize=(12, 6))
colors = ['#FF4500' if val == monthly_users_df['Users'].max() else '#1E90FF' if val == monthly_users_df['Users'].min() else '#ADD8E6' for val in monthly_users_df['Users']]
sns.barplot(y=monthly_users_df['Month'], x=monthly_users_df['Users'], palette=colors, ax=ax)
ax.set_title("Bike-Sharing Users by Month")
st.pyplot(fig)
