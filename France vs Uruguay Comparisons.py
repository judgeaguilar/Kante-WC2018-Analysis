import seaborn as sns
import pandas as pd
from pandas import json_normalize
import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib as mpl
import matplotlib.mlab as mlab
import matplotlib.lines as mlines
from collections import Counter

###Dataframes
# passes = df.loc[df['type_name'] == 'Pass'].set_index('id')
###Load World Cup 2018 Data
competition_id = 43
with open(r'C:\Users\cherr\PycharmProjects\soccerm8/Statsbomb/data/matches/'+str(competition_id)+'/3.json') as f:
    matches = json.load(f)
#Create Complete Match List
matchlist = []
for match in matches:
    if match['match_id'] == 8658 or match['match_id'] == 8655:
        pass
    elif match['match_id'] == 7530 or match['match_id'] == 7546 or match['match_id'] == 7580 or match['match_id'] == 8649 or match['match_id'] == 7563:
        matchlist.append(match['match_id'])
    else:
        pass

print(matchlist)
#Actions
success = []
failed = []
#Gamesplayed = Recorded instance (playername + matchid) of game where player was involved, gamesplayedcheck = unique recording of games involved
gamesplayed = []
gamesplayedcheck = []
j = 0

###Load World Cup 2018 Data
competition_id = 43
with open(r'C:\Users\cherr\PycharmProjects\soccerm8/Statsbomb/data/matches/'+str(competition_id)+'/3.json') as f:
    matches = json.load(f)
#Create Complete Match List
matchlist = []
for match in matches:
    if match['match_id'] == 8658 or match['match_id'] == 8655:
        pass
    elif match['match_id'] == 7558 or match['match_id'] == 8649 or match['match_id'] == 7578 or match['match_id'] == 7544 or match['match_id'] == 7579 \
            or match['match_id'] == 7530 or match['match_id'] == 7546 or match['match_id'] == 7580 or match['match_id'] == 8649 or match['match_id'] == 7563:
        matchlist.append(match['match_id'])
    else:
        pass

#create empty list for recording actions
francesuccess = []
uruguaysuccess = []
francefailed = []

#Gamesplayed = Recorded instance of game where player was involved,
#gamesplayedcheck = recording single instance (playername + matchid) of games involved, refers to Line 86-97
francegamesplayed = []
uruguaygamesplayed = []
francegamesplayedcheck = []
uruguaygamesplayedcheck = []
j = 0

for i in range(len(matchlist)):
    match_id_required = matchlist[i]
    file_name = str(match_id_required) + ".json"
    with open(r"C:\Users\cherr\PycharmProjects\soccerm8/Statsbomb/data/events/" + file_name,encoding='utf-8') as data_file:
        # print (mypath+'events/'+file)
        data = json.load(data_file)
    #event data and passes
    df = json_normalize(data, sep="_").assign(match_id=file_name[:-5])
    passes = df.loc[df['type_name'] == 'Pass'].set_index('id')
    #ball stopping actions
    tackle = df.loc[df['type_name'] == 'Duel'].set_index('id')
    block = df.loc[df['type_name'] == 'Block'].set_index('id')
    clearance = df.loc[df['type_name'] == 'Clearance'].set_index('id')
    #ball recovering actions
    intercept = df.loc[df['type_name'] == 'Interception'].set_index('id')
    ballrecovery = df.loc[df['type_name'] == 'Ball Recovery'].set_index('id')

    #Recording "Game Played" and "Game Played Check"
    #record passing instance to add the "game played" value to player
    #rationale: more than likely that a player will make a pass sometime during the game
    for i, thepass in passes.iterrows():
        if str(thepass['player_name'])+str(thepass['match_id']) not in gamesplayedcheck:
            if thepass['team_name'] == 'France':
                francegamesplayed.append(thepass['player_name'])
                francegamesplayedcheck.append(str(thepass['player_name']) + str(thepass['match_id']))
            if thepass['team_name'] == 'Uruguay':
                uruguaygamesplayed.append(thepass['player_name'])
                uruguaygamesplayedcheck.append(str(thepass['player_name']) + str(thepass['match_id']))
            else:
                pass
        else:
            pass
    #Loading visual to make sure its going okay
    j = j+0.5
    print(j)

    ##Recording Defensive Contributions
    #Clearances
    for i,clr in clearance.iterrows():
        if clr['team_name'] == 'France':
            if clr['position_name'] == "Goalkeeper":
                pass
            else:
                francesuccess.append((clr['player_name']))
        elif clr['team_name'] == 'Uruguay':
            if clr['position_name'] == "Goalkeeper":
                pass
            else:
                uruguaysuccess.append((clr['player_name']))
        else:
            pass
    #Ball Recovery
    for i, br in ballrecovery.iterrows():
        if br['ball_recovery_recovery_failure'] == True:
            pass
        else:
            if br['position_name'] == "Goalkeeper":
                pass
            else:
                if br['team_name'] == 'France':
                    francesuccess.append((br['player_name']))
                if br['team_name'] == 'Uruguay':
                    uruguaysuccess.append((br['player_name']))
                else:
                    pass
    #Intercepts
    for i, intcpt in intercept.iterrows():
        if intcpt['interception_outcome_name'] == "Won" or intcpt['interception_outcome_name'] == "Success In Play" or intcpt['interception_outcome_name'] == "Success Out" or intcpt['interception_outcome_name'] == "Lost Out":
            if intcpt['team_name'] == 'France':
                if intcpt['position_name'] == "Goalkeeper":
                    pass
                else:
                    francesuccess.append((intcpt['player_name']))
            elif intcpt['team_name'] == 'Uruguay':
                if intcpt['position_name'] == "Goalkeeper":
                    pass
                else:
                    uruguaysuccess.append((intcpt['player_name']))
            else:
                pass
        else:
            pass
    #Blocks
    for i, blk in block.iterrows():
        if blk['team_name'] == 'France':
            if blk['position_name'] == "Goalkeeper":
                pass
            else:
                francesuccess.append((blk['player_name']))
        elif blk['team_name'] == 'Uruguay':
            if blk['position_name'] == "Goalkeeper":
                pass
            else:
                uruguaysuccess.append((blk['player_name']))
        else:
            pass
    #Tackles
    for i, tckl in tackle.iterrows():
        if tckl['duel_type_name'] == "Tackle":
            if tckl['duel_outcome_name'] == "Won" or tckl['duel_outcome_name'] == "Success In Play" or tckl['duel_outcome_name'] == "Success Out" or tckl['duel_outcome_name'] == "Lost Out":
                if tckl['team_name'] == 'France':
                    if tckl['position_name'] == "Goalkeeper":
                        pass
                    else:
                        francesuccess.append((tckl['player_name']))
                elif tckl['team_name'] == 'Uruguay':
                    if tckl['position_name'] == "Goalkeeper":
                        pass
                    else:
                        uruguaysuccess.append((tckl['player_name']))
                else:
                    pass
            else:
                pass
        else:
            pass
    #Loading visual
    j = j+0.5
    print(j)

fig, ax = plt.subplots()
#Counts tackle and gamecount lists and assigns to player (Counter())
actioncountFRA = Counter(francesuccess)
actioncountURU = Counter(uruguaysuccess)
gamecountFRA = Counter(francegamesplayed)
gamecountURU = Counter(uruguaygamesplayed)

##Change Counter value into dataframes, set column labels
#France
successfulactionFRA = pd.DataFrame.from_dict(actioncountFRA, orient='index').reset_index()
successfulactionFRA = successfulactionFRA.rename(columns={'index':'Player Name', 0:'Total DEF Contr'})
totalgamesFRA = pd.DataFrame.from_dict(gamecountFRA, orient='index').reset_index()
totalgamesFRA = totalgamesFRA.rename(columns={'index':'Player Name', 0:'Games Played'})
successfulactionFRA['Country'] = 'FRA'
#Uruguay
successfulactionURU = pd.DataFrame.from_dict(actioncountURU, orient='index').reset_index()
successfulactionURU = successfulactionURU.rename(columns={'index':'Player Name', 0:'Total DEF Contr'})
totalgamesURU = pd.DataFrame.from_dict(gamecountURU, orient='index').reset_index()
totalgamesURU = totalgamesURU.rename(columns={'index':'Player Name', 0:'Games Played'})
successfulactionURU['Country'] = 'URU'

#Combine Data Frames on 'players' column, create Per Game column which is Tackles per games played
frames = [successfulactionFRA,successfulactionURU]
combine = pd.concat(frames)
print(combine)

#Creating barplot for France
import numpy as np

successfulactionFRA = successfulactionFRA.sort_values(by = 'Total DEF Contr', ascending = False)
successfulactionFRA2 = successfulactionFRA[:10]
pal = sns.color_palette("Blues_d", len(successfulactionFRA2))
ax = sns.barplot(x="Total DEF Contr",y="Player Name",orient = 'h', data = successfulactionFRA2, palette = np.array(pal[::-1]))
for p in ax.patches:
    width = p.get_width()
    plt.text(2 + p.get_width(), p.get_y()+0.55*p.get_height(),
             '{:1.2f}'.format(width),
             ha='center', va='center')

for i,t in enumerate(ax.get_yticklabels()):
    if t.get_text() in ['N"Golo Kanté']:
        ## bold ticklabels
        t.set_weight("bold")
        ## bar edges
        ax.patches[i].set_edgecolor("gold")
        ax.patches[i].set_linewidth(2)
        ## arrow annotations
        # ax.annotate("Z Fund",(i, ax.patches[i].get_height()),
        #             xytext=(0,30), textcoords='offset points', ha="center",
        #             arrowprops=dict(facecolor='black', shrink=0.05))


plt.title("France's Defensive Contributions After Quarter-Finals")
plt.show()



#Creating barplot for Uruguay
successfulactionURU = successfulactionURU.sort_values(by = 'Total DEF Contr', ascending = False)
successfulactionURU2 = successfulactionURU[:10]
pal = sns.color_palette("Oranges_d", len(successfulactionURU2))
ax = sns.barplot(x="Total DEF Contr",y="Player Name",orient = 'h', data = successfulactionURU2, palette = np.array(pal[::-1]))
for p in ax.patches:
    width = p.get_width()
    plt.text(2 + p.get_width(), p.get_y()+0.55*p.get_height(),
             '{:1.2f}'.format(width),
             ha='center', va='center')
plt.title("Uruguay's Defensive Contributions After Quarter-Finals")
plt.show()

#Box and Whiskers Plot
sns.boxplot(x="Total DEF Contr", y="Country",orient = 'h', data=combine)
sns.swarmplot(x="Total DEF Contr", y="Country", data=combine, color=".25")
plt.title("Distribution of Team Defensive Contributions")
plt.show()





