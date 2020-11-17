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
    #df = df.loc[(df['League'] == 'NALCS') & (df['Type'] == 'Season')]
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
    
    #selected league is selected
    selected_league = st.sidebar.multiselect('Select league',options=list(df['League'].unique()),default=['NALCS'])

    #selected season type is selected
    selected_type = st.sidebar.multiselect('Select season type',options=list(df['Type'].unique()),default=['Playoffs'])

    #selected season is stored
    selected_season = st.sidebar.multiselect('Select season',options=list(df['Season'].unique()),default='Spring')

    #selected year is stored
    selected_year = st.sidebar.slider('Select year :',min(years),max(years),(min(years),max(years)))
    
    #return datafram with selected components
    def get_selected_data(selected_year,df):
        new_df = df.loc[(df['Year'] >= selected_year[0]) & (df['Year'] <= selected_year[1]) &
        #and selected season 
        (df['Season'].isin(selected_season)) &
        #and selected league
        (df['League'].isin(selected_league)) &
        #and selected season type
        (df['Type'].isin(selected_type))
        ]

        return new_df
    
    new_df = get_selected_data(selected_year,df)
    #show raw data
    if st.checkbox('Show raw data'):
        st.write(new_df.reset_index(drop=True))  

    #DYNAMIC TITLE
    #create list to hold items for title
    title_list = []
    #selected league item
    for item in selected_league:
        title_list.append(item + " ")

    #selected season
    if len(selected_season) < 2:
        #selected season item
        for item in selected_season:
            title_list.append(item + " ")
    else:
        #more than one item in list, put 'and' between items
        for item in selected_season:
            title_list.append(item + " ")
            title_list.append(" and ")
        #remove second 'and'
        title_list.pop(4)

    #selected season type
    for item in selected_type:
        title_list.append(item + " ")

    #selected year
    title_list.append(str(selected_year[0]) + ' to ' + str(selected_year[1]))

    #take list of selected item and concat a string
    def list_to_str(title_list):
        #init empty string
        title_string = ""
        #return concat string
        return title_string.join(title_list)

    #function output variable
    title_string = list_to_str(title_list)
    #print on title as subheader
    st.title(title_string)
    st.title("\n")
    
    def win_loss_plot(new_df):
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
        win_loss['Total Games Played'] = win_loss['Win'] + win_loss['Loss']
        win_loss = win_loss.reset_index()

        #melt df to be used for multi-series barplot,  arrange so total most games is first
        win_loss_m = pd.melt(win_loss,id_vars="index", var_name="Total Games Played",value_name="count")
        #win_loss = win_loss.sort_values('count',ascending=False)

        #plot
        fig, ax = plt.subplots(figsize=(10,10))
        x = sns.barplot(y='index', x='count', hue='Total Games Played', data=win_loss_m)
        ax.set_xlabel('Number of games',fontsize=18)
        ax.set_ylabel('Team name',fontsize=18)
        ax.set_title('Outcome of total games played',fontsize=28)
        ax.legend(title='Type')
        st.pyplot(fig)

        return win_loss

    win_loss_df = win_loss_plot(new_df)

    def get_current_stats(win_loss_df):
        win_loss_df['Win_rate'] = win_loss_df['Win'] / win_loss_df['Total Games Played']
        win_loss_df['Loss_rate'] = win_loss_df['Loss'] / win_loss_df['Total Games Played']
        win_loss_df.columns = ['Team','Win','Loss','Total','Win Rate','Loss Rate']
        return win_loss_df
    
    #win loss df created from selected params
    win_loss_df = get_current_stats(win_loss_df)
    #print table
    st.dataframe(win_loss_df)

    #count blue wins
    mask = new_df['bResult'] == 1
    new_df['Winning Side'] = np.where(mask,'Blue','Red')
    rb_ratio = new_df['Winning Side'].value_counts()
    st.write(rb_ratio)
    


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
    
   