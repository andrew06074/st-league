import streamlit as st
import awesome_streamlit as ast

import numpy as np
import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt

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

    #selected team is stored
    selected_team = st.sidebar.selectbox('Select blue team :',team)

    #selected season is stored
    selected_season = st.sidebar.multiselect('Select season',options=list(df['Season'].unique()),default=['Spring'])

    #selected year is stored
    selected_year = st.sidebar.slider('Select year :',min(years),max(years),(min(years),max(years)))
    
    #DYNAMIC TITLE
    #create list to hold items for title
    title_list = []

    #selected season team
    for item in selected_team:
        title_list.append(item)
    #blanks space for after team name
    title_list.append(" ")
    
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
        title_list.pop(7)

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

    #return datafram with selected components
    def get_selected_data(selected_season,selected_year,selected_team,df):
        new_df = df.loc[

            #the input from the sidebars queries the dataframe here
            #year is equal to or between selcted 
            (df['Year'] >= selected_year[0]) & (df['Year'] <= selected_year[1]) & 
            
            #and selected team is either blue side OR read side
            ((df['blueTeamTag'] == selected_team) | (df['redTeamTag'] == selected_team)) &
            
            #and selected season 
            (df['Season'].isin(selected_season))
            ]

        return new_df

    new_df = get_selected_data(selected_season,selected_year,selected_team,df)

    def get_win_loss(new_df,selected_team):
        #wins
        blue_wins = new_df.loc[(new_df['blueTeamTag'] == selected_team) & (new_df['bResult'] == 1)]
        red_wins = new_df.loc[(new_df['redTeamTag'] == selected_team) & (new_df['rResult'] == 1)]

        blue_wins = len(blue_wins.index)
        red_wins = len(red_wins.index)

        #losses
        blue_losses =  new_df.loc[(new_df['blueTeamTag'] == selected_team) & (new_df['bResult'] == 0)]
        red_losses = new_df.loc[(new_df['redTeamTag'] == selected_team) & (new_df['rResult'] == 0)]

        blue_losses = len(blue_losses.index)
        red_losses = len(red_losses.index)

        #win/loss
        wins = blue_wins + red_wins
        losses = blue_losses + red_losses

        win_loss = wins / (wins + losses)

        return blue_wins,red_wins,blue_losses,red_losses,win_loss

    blue_wins,red_wins,blue_losses,red_losses,win_loss = get_win_loss(new_df,selected_team)


    ## Write content
    #print df, hide with checkbox
    if st.checkbox('Show raw data'):
        st.write(new_df.reset_index(drop=True))   
    st.title('------------------------')    
    st.title('Overview')
    times_played_blue = new_df.blueTeamTag.value_counts()
    times_played_red = new_df.redTeamTag.value_counts()
    #Overview section
    st.subheader('Total games played: ' + str(times_played_blue[0] + times_played_red[0])) 
    st.subheader('Times played blue side: ' + str(times_played_blue[0]))
    st.subheader('Times played red side: ' + str(times_played_red[0]))
    st.subheader('Wins: ' + str(blue_wins+red_wins))
    st.subheader('Losses: ' + str(blue_losses+red_losses))
    st.subheader('Win percentage: ' + str(round(win_loss,2)))
    st.title('------------------------')
    #Team Members
    st.title('Team roles')
    blue_filter = new_df['blueTeamTag'] == selected_team
    red_filter = new_df['redTeamTag'] == selected_team

    #create filter for new dataframes
    blue_df = new_df.where(blue_filter)
    blue_df = blue_df.dropna()
    red_df = new_df.where(red_filter)
    red_df = red_df.dropna()

    #get all players to play top role, only one side matters
    top = blue_df['blueTop'].unique()
    #get counts of each champion played
    blue_top_champs = blue_df['blueTopChamp'].value_counts()
    red_top_champs = red_df['redTopChamp'].value_counts()
    #combine counts of both sides
    blue_top_champs.add(red_top_champs)
    
    #jungle
    jungle = blue_df['blueJungle'].unique()
    #get counts of each champion played
    blue_jungle_champs = blue_df['blueJungleChamp'].value_counts()
    red_jungle_champs = red_df['redJungleChamp'].value_counts()
    #combine counts of both sides
    blue_jungle_champs.add(red_jungle_champs)

    #middle
    mid = blue_df['blueMiddle'].unique()
    #get counts of each champion played
    blue_middle_champs = blue_df['blueMiddleChamp'].value_counts()
    red_middle_champs = red_df['redMiddleChamp'].value_counts()
    #combine counts of both sides
    blue_middle_champs.add(red_middle_champs)

    #adc
    adc = blue_df['blueADC'].unique()
    #get counts of each champion played
    blue_adc_champs = blue_df['blueADCChamp'].value_counts()
    red_adc_champs = red_df['redADCChamp'].value_counts()
    #combine counts of both sides
    blue_adc_champs.add(red_adc_champs)

    #support
    support = blue_df['blueSupport'].unique()
    #get counts of each champion played
    blue_support_champs = blue_df['blueSupportChamp'].value_counts()
    red_support_champs = red_df['redSupportChamp'].value_counts()
    #combine counts of both sides
    blue_support_champs.add(red_support_champs)

    #wite and plot
    #top 
    st.subheader('Top')
    st.write(str(top))
    #plot
    fig, ax = plt.subplots(figsize=(10,5))
    ax = sns.barplot(palette="Blues_r",alpha=0.8,y=blue_top_champs.index, x=blue_top_champs.values)
    st.pyplot(fig)

    #jungle
    st.subheader('Jungle')
    st.write(str(jungle))
    #plot
    fig, ax = plt.subplots(figsize=(10,5))
    ax = sns.barplot(palette="Blues_r",alpha=0.8,y=blue_jungle_champs.index, x=blue_jungle_champs.values)
    st.pyplot(fig)

    #middle
    st.subheader('Middle')
    st.write(str(mid))
    #plot
    fig, ax = plt.subplots(figsize=(10,5))
    ax = sns.barplot(palette="Blues_r",alpha=0.8,y=blue_middle_champs.index, x=blue_middle_champs.values)
    st.pyplot(fig)

    #adc
    st.subheader('ADC')
    st.write(str(adc))
    #plot
    fig, ax = plt.subplots(figsize=(10,5))
    ax = sns.barplot(palette="Blues_r",alpha=0.8,y=blue_adc_champs.index, x=blue_adc_champs.values)
    st.pyplot(fig)

    #support
    st.subheader('Support')
    st.write(str(support))
    #plot
    fig, ax = plt.subplots(figsize=(10,5))
    ax = sns.barplot(palette="Blues_r",alpha=0.8,y=blue_support_champs.index, x=blue_support_champs.values)
    st.pyplot(fig)
