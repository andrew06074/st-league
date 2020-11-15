import streamlit as st
import awesome_streamlit as ast

import numpy as np
import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt

pd.options.mode.chained_assignment = None  # default='warn'

#load data
def load_data(nrows):
    df = pd.read_csv('LeagueofLegends.csv', nrows=nrows)
    #return all values of NALCS and only teams that make it past the promotional stage
    df = df.loc[(df['League'] == 'NALCS') & (df['Type'] == 'Season')]
    return df

#dataframe variable
df = load_data(10000)

#create lists to hold values for search params
#years
years = []
for item in df['Year'].unique():
    x = item
    years.append(x)
years = list(map(int,years))

#team
team = []
for item in df['blueTeamTag'].unique():
    x = item
    team.append(x)

def write():
    st.sidebar.title("Select your search params")
    
    #selected year is stored
    selected_year = st.sidebar.slider('Select year :',min(years),max(years),(min(years),max(years)))

    #selected season is stored
    selected_season = st.sidebar.multiselect('Select season',options=list(df['Season'].unique()),default=['Spring','Summer'])
    
    #return datafram with selected components
    def get_selected_data(selected_year,df):
        new_df = df.loc[(df['Year'] >= selected_year[0]) & (df['Year'] <= selected_year[1]) &
        #and selected season 
        (df['Season'].isin(selected_season))
        ]

        return new_df
    
    new_df = get_selected_data(selected_year,df)
    
    #show raw data
    if st.checkbox('Show raw data'):
        st.write(new_df.reset_index(drop=True))  

    def get_win_loss(new_df):
        #count wins and losses for selected frame
        win_loss_df = pd.DataFrame()

        #count wins
        #create mask for loop
        mask = new_df['bResult'] == 1
        new_df['Win'] = np.where(mask,new_df.blueTeamTag,new_df.redTeamTag)

        #count losses
        #create mask for loop
        mask = new_df['bResult'] == 0
        new_df['Loss'] = np.where(mask,new_df.blueTeamTag,new_df.redTeamTag)

        #count values of wins and losses
        wins = new_df['Win'].value_counts()
        losses = new_df['Loss'].value_counts()

        #create new df of clount values
        win_loss = pd.concat([wins,losses],axis=1)
        win_loss['Total'] = win_loss['Win'] + win_loss['Loss']
        win_loss = win_loss.reset_index()

        #melt df to be used for multi-series barplot,  arrange so total most games is first
        win_loss = pd.melt(win_loss,id_vars="index", var_name="count_type",value_name="count")
        #win_loss = win_loss.sort_values('count',ascending=False)

        #plot
        fig, ax = plt.subplots(figsize=(10,10))
        x = sns.barplot(y='index', x='count', hue='count_type', data=win_loss)
        ax.set_xlabel('Number of games',fontsize=18)
        ax.set_ylabel('Team name',fontsize=18)
        st.pyplot(fig)

        #return new_df

    get_win_loss(new_df)


    '''
    ----------INDIVIDUAL WINS AND LOSSES----------------
    #win loss dataframe created
    win_loss = get_win_loss(new_df)
    
    #win count dataframe
    wins = win_loss['Win'].value_counts()
    st.write(wins)

    #plot wins
    fig, ax = plt.subplots(figsize=(10,5))
    x = sns.barplot(palette="Blues_r",alpha=0.8,y=wins.index, x=wins.values)
    st.pyplot(fig)

    #loss count dataframe
    losses = win_loss['Loss'].value_counts()
    st.write(losses)
    
    #plot wins
    fig, ax = plt.subplots(figsize=(10,5))
    x = sns.barplot(palette="Blues_r",alpha=0.8,y=losses.index, x=losses.values)
    st.pyplot(fig)
    '''
    
   