import seaborn as sns
import pandas as pd
from pandas import json_normalize
import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib as mpl
import matplotlib.mlab as mlab

##Player Values for reference
#Pogba = 20004
#Kante = 3961

#Match Data preparation
competition_id = 43
with open(r'C:\Users\cherr\PycharmProjects\soccerm8/Statsbomb/data/matches/'+str(competition_id)+'/3.json',encoding='utf-8') as f:
    matches = json.load(f)

home_team_required = "France"
matchlist = []
opposition = []
for match in matches:
    home_team_name=match['home_team']['country']['name']
    away_team_name = match['away_team']['country']['name']
    if (home_team_name == home_team_required):
        matchlist.append(match['match_id'])
        opposition.append(away_team_name)
    elif away_team_name == home_team_required:
        matchlist.append(match['match_id'])
        opposition.append(home_team_name)
print(matchlist,opposition)

##Creating Ball Recovery Histogram
ballrectimesk=[]
ballrectimesp=[]
mistakes = []

for i in range(len(matchlist)):
    match_id_required = matchlist[i]
    file_name = str(match_id_required) + '.json'
    with open(r'C:\Users\cherr\PycharmProjects\soccerm8/Statsbomb/data/events/' + file_name,encoding='utf-8') as data_file:
        data = json.load(data_file)
    df = json_normalize(data, sep="_").assign(match_id=file_name[:-5])
    ballrecovery = df.loc[df['type_name'] == 'Ball Recovery'].set_index('id')
    intercept = df.loc[df['type_name'] == 'Interception'].set_index('id')

    for i,ball in ballrecovery.iterrows():
        #Kante
        if ball['team_name'] == "France" and ball['player_id'] == 3961:
            if ball['ball_recovery_recovery_failure'] == True:
                mistakes.append(ball['minute'])
            else:
                ballrectimesk.append(ball['minute'])
        #Pogba
        elif ball['team_name'] == "France" and ball['player_id'] == 20004:
            if ball['ball_recovery_recovery_failure'] == True:
                pass
            else:
                ballrectimesp.append(ball['minute'])
        else:
            pass

    for i,intcpt in intercept.iterrows():
        if intcpt['team_name'] == "France" and intcpt['player_id'] == 3961:
            if intcpt['interception_outcome_name'] == "Won" or intcpt['interception_outcome_name'] == "Success In Play" or intcpt['interception_outcome_name'] == "Success Out" or intcpt['interception_outcome_name'] == "Lost Out":
                ballrectimesk.append(intcpt['minute'])
            else:
                mistakes.append(intcpt['minute'])
        elif intcpt['team_name'] == "France" and intcpt['player_id'] == 20004:
            if intcpt['interception_outcome_name'] == "Won" or intcpt['interception_outcome_name'] == "Success In Play" or intcpt['interception_outcome_name'] == "Success Out" or intcpt['interception_outcome_name'] == "Lost Out":
                ballrectimesp.append(intcpt['minute'])
            else:
                mistakes.append(intcpt['minute'])
        else:
            pass

#Kante Distplot
fig, ax = plt.subplots()
num_bins = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90]
ytick = [0,1,2,3,4,5,6]
sns.distplot(a=ballrectimesk,bins = num_bins, kde = False,hist_kws=dict(edgecolor="black"))
sns.despine()
plt.xlabel("Minute")
plt.ylabel("Ball Recovering Actions")
plt.title("When Does Kante Tend to Recover the Ball?")
plt.xticks(num_bins)
plt.yticks(ytick)
plt.show()

#Pogba Distplot
fig, ax = plt.subplots()
num_bins = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90]
ytick = [0,1,2,3,4,5,6]
sns.distplot(a=ballrectimesp,bins = num_bins, kde = False,hist_kws=dict(edgecolor="black"))
sns.despine()
plt.xlabel("Minute")
plt.ylabel("Ball Recovering Actions")
plt.title("When Does Pogba Tend to Recover the Ball?")
plt.xticks(num_bins)
plt.yticks(ytick)
plt.show()

#Ball Stopping Distplots
ballstoptimesk=[]
ballstoptimesp=[]
mistakes = []

for i in range(len(matchlist)):
    match_id_required = matchlist[i]
    file_name = str(match_id_required) + '.json'
    with open(r'C:\Users\cherr\PycharmProjects\soccerm8/Statsbomb/data/events/' + file_name,encoding='utf-8') as data_file:
        data = json.load(data_file)
    df = json_normalize(data, sep="_").assign(match_id=file_name[:-5])
    block = df.loc[df['type_name'] == 'Block'].set_index('id')
    tackle = df.loc[df['type_name'] == 'Duel'].set_index('id')
    clearance = df.loc[df['type_name'] == 'Clearance'].set_index('id')

    for i,tckl in tackle.iterrows():
        if tckl['duel_type_name'] == "Tackle":
            if tckl['team_name'] == "France" and tckl['player_id'] == 3961:
                if tckl['duel_outcome_name'] == "Won" or tckl['duel_outcome_name'] == "Success In Play" or tckl['duel_outcome_name'] == "Success Out" or tckl['duel_outcome_name'] == "Lost Out":
                    ballstoptimesk.append(tckl['minute'])
                else:
                    pass
            elif tckl['team_name'] == "France" and tckl['player_id'] == 20004:
                if tckl['duel_outcome_name'] == "Won" or tckl['duel_outcome_name'] == "Success In Play" or tckl['duel_outcome_name'] == "Success Out" or tckl['duel_outcome_name'] == "Lost Out":
                    ballstoptimesp.append(tckl['minute'])
                else:
                    pass
            else:
                pass
        else:
            pass
    for i,blck in block.iterrows():
        if blck['team_name'] == "France" and blck['player_id'] == 3961:
            ballstoptimesk.append(blck['minute'])
        elif blck['team_name'] == "France" and blck['player_id'] == 20004:
            ballstoptimesp.append(blck['minute'])
        else:
            pass
    for i,clr in clearance.iterrows():
        if clr['team_name'] == "France" and clr['player_id'] == 3961:
            ballstoptimesk.append(clr['minute'])
        elif clr['team_name'] == "France" and clr['player_id'] == 20004:
            ballstoptimesp.append(clr['minute'])
        else:
            pass

#Kante Dist Plot
fig, ax = plt.subplots()
num_bins = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90]
ytick = [0,1,2,3,4]
sns.distplot(a=ballstoptimesk,bins = num_bins, kde = False,hist_kws=dict(edgecolor="black"))
sns.despine()
plt.xlabel("Minute")
plt.ylabel("Ball Stopping Actions")
plt.title("When Does Kante Tend to Stop the Ball?")
plt.xticks(num_bins)
plt.yticks(ytick)
plt.show()

#Pogba Dist Plot
fig, ax = plt.subplots()
num_bins = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90]
ytick = [0,1,2,3,4]
sns.distplot(a=ballstoptimesp,bins = num_bins, kde = False,hist_kws=dict(edgecolor="black"))
sns.despine()
plt.xlabel("Minute")
plt.ylabel("Ball Stopping Actions")
plt.title("When Does Pogba Tend to Stop the Ball?")
plt.xticks(num_bins)
plt.yticks(ytick)
plt.show()
