import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import calendar
import streamlit as st
import datetime

day = pd.read_csv('dashboard/day.csv',sep=';')
hour = pd.read_csv('data/day.csv',sep=';')

day.rename(columns={
    'dteday': 'date',
    'yr': 'year',
    'mnth': 'month',
    'cnt': 'count'
}, inplace=True)

hour.rename(columns={
    'dteday': 'date',
    'yr': 'year',
    'mnth': 'month',
    'hr' : 'hour',
    'cnt': 'count'
}, inplace=True)

day.drop(labels='instant', axis=1, inplace=True)
hour.drop(labels='instant', axis=1, inplace=True)

type_col = ['season', 'holiday','weekday','workingday','weathersit']

for i in day.columns:
  if i in type_col:
    day[type_col]=day[type_col].astype('category')

for i in day.columns:
  if i in type_col:
    hour[type_col]=hour[type_col].astype('category')

def convert_to_month_name(month):
    return calendar.month_abbr[month]

day['month'] = day['month'].apply(convert_to_month_name)

def convert_to_month_name(month):
    return calendar.month_abbr[month]

hour['month'] = hour['month'].apply(convert_to_month_name)

day['season'] = day['season'].map({
    1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'
})
hour['season'] = hour['season'].map({
    1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'
})

day['year'] = day['year'].map({
    0: 2011, 1: 2012
})
hour['year'] = hour['year'].map({
    0: 2011, 1: 2012
})

day['weekday'] = day['weekday'].map({
    0: "Sun", 1: 'Mon', 2:'Tue',3:'Wed',4:'Thu',5:'Fri',6:'Sat'
})
hour['weekday'] = hour['weekday'].map({
    0: "Sun", 1: 'Mon', 2:'Tue',3:'Wed',4:'Thu',5:'Fri',6:'Sat'
})

month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
day['month'] = pd.Categorical(day['month'], categories=month_order, ordered=True)
hour['month'] = pd.Categorical(hour['month'], categories=month_order, ordered=True)

day_order = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']
day['weekday'] = pd.Categorical(day['weekday'], categories=day_order, ordered=True)
hour['weekday'] = pd.Categorical(hour['weekday'], categories=day_order, ordered=True)

dyear= day.groupby(by='year').agg({
    'casual': 'sum',
    'registered': 'sum',
    'count' : 'sum'
}).reset_index()

dm1 = day.groupby(['year','month']).agg({
    'casual': 'sum',
    'registered': 'sum',
    'count' : 'sum'
}).reset_index()

t2011 = dm1.query('year == 2011')
t2012 = dm1.query('year == 2011')

dd1 = day.groupby(['year','weekday']).agg({
    'casual': 'sum',
    'registered': 'sum',
    'count' : 'sum'
}).reset_index()

dse= day.groupby(by='season').agg({
    'casual': 'sum',
    'registered': 'sum',
    'count' : 'sum'
}).reset_index()

dwork= day.groupby(by='workingday').agg({
    'casual': 'sum',
    'registered': 'sum',
    'count' : 'sum'
}).reset_index()

st.title('Bike Sharing Mini Dashboard')
tab1,tab2 = st.tabs(['Dashboard','Dataset'])

with tab1:
    st.subheader('Bike rentals based on season')

    colt1,colt2 = st.columns(2)

    with colt1:
        fig1,ax = plt.subplots(figsize=(10, 12))
        ax.set_title("Jumlah Penyewa Sepeda pada setiap musim", loc="center", fontsize=20)
        ax.set_ylabel(None)
        sns.barplot(x = 'season', y = 'count', data = dse, 
            ci = None, palette = 'Blues', label = 'count')
        st.pyplot(fig1)
    
    with colt2:
        tdse = dse.set_index('season').transpose()
        tdse = tdse.iloc[:-1]
        st.pyplot(tdse.plot.bar(stacked=True,figsize=(10, 12),
              color=['navy', 'blue','skyblue', 'lightblue'],rot=0).figure)
    
    st.subheader('Daily Bike Rentals')
    
    fig3,ax = plt.subplots(figsize=(10, 7))
    sns.barplot(x = 'weekday', y = 'count', data = dd1, 
            ci = None, palette = 'Blues')
    ax.bar_label(ax.containers[0])
    plt.title('Jumlah Penyewa Sepeda Harian 2011-2012')
    plt.xlabel('Hari')
    plt.ylabel('Jumlah')
    st.pyplot(fig3)

    col11,col22 = st.columns(2)
    with col11:
        fig4,ax = plt.subplots(figsize=(10, 7))
        sns.barplot(x = 'weekday', y = 'count', data = dd1[dd1['year']==2011], 
            ci = None, palette = 'Blues')
        ax.bar_label(ax.containers[0])
        plt.title('Jumlah Penyewa Sepeda Harian 2011')
        plt.xlabel('Hari')
        plt.ylabel('Jumlah')
        st.pyplot(fig4)

    with col22:
        fig5,ax = plt.subplots(figsize=(10,7))
        sns.barplot(x = 'weekday', y = 'count', data = dd1[dd1['year']==2012], 
            ci = None, palette = 'Blues')
        ax.bar_label(ax.containers[0])
        plt.title('Jumlah Penyewa Sepeda Harian 2012')
        plt.xlabel('Hari')
        plt.ylabel('Jumlah')
        st.pyplot(fig5)
    
    st.subheader('Bike Rentals in Working day')
    dwork1 = dwork.drop(labels='count',axis=1)
    st.pyplot(dwork1.plot.bar(stacked=True, figsize=(10, 6),
              color=['blue','skyblue']).figure
              )
    st.caption('1:Working day 0;Not Working day')

    st.subheader("Monthly Bike Rental Trends")
    users = st.radio(
    label="Users",
    options=('casual', 'registered', 'count'),
    horizontal=True
    )
    coll1,coll2 = st.columns(2)
    
    with coll1:
        fig7,ax = plt.subplots(figsize=(10,7))
        sns.lineplot(x='month', y=users, data=t2011)
        plt.title('Count of Bike Sharing in 2011')
        st.pyplot(fig7)
    with coll2:
        fig8,ax = plt.subplots(figsize=(10,7))
        sns.lineplot(x='month', y=users, data=t2012)
        plt.title('Count of Bike Sharing in 2012')
        st.pyplot(fig8)
        
with tab2:
    st.subheader('Day.csv')
    st.dataframe(day)
    st.subheader('Hour.csv')
    st.dataframe(hour)

st.caption('By Akbar Maulana Ibrahim')
