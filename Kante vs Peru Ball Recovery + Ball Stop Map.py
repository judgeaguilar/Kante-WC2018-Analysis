#Function to draw the pitch
import matplotlib.pyplot as plt
import numpy as np
import json
import pandas as pd
from pandas import json_normalize
import matplotlib.patches as mpatches
import matplotlib as mpl
import matplotlib.lines as mlines

##Pitch map setup, size of pitch in yards
pitchLengthX=120
pitchWidthY=80

##Match data setup
competition_id = 43
with open(r'C:\Users\cherr\PycharmProjects\soccerm8/Statsbomb/data/matches/'+str(competition_id)+'/3.json',encoding='utf-8') as f:
    matches = json.load(f)

#Finding France's matches
home_team_required = "France"
matchlist = []
opposition = []

for match in matches:
    home_team_name=match['home_team']['country']['name']
    away_team_name = match['away_team']['country']['name']
    if (home_team_name == home_team_required):
        matchlist.append(match['match_id'])
    elif away_team_name == home_team_required:
        matchlist.append(match['match_id'])

###Ball Recovering Actions (Ball Recoveries + Interceptions) vs. Peru
#Draw pitch map
from mplsoccer.pitch import Pitch
pitch = Pitch(pitch_type='statsbomb', orientation='horizontal',
              pitch_color='#22312b', line_color='#c7d5cc', figsize=(16, 11),
              constrained_layout=True, tight_layout=False)
(fig,ax) = pitch.draw()
fig.set_size_inches(10,7)

#Event data setup for France vs. Peru
match_id_required = 7546
file_name = str(match_id_required) + '.json'
with open(r'C:\Users\cherr\PycharmProjects\soccerm8/Statsbomb/data/events/' + file_name,encoding='utf-8') as data_file:
    # print (mypath+'events/'+file)
    data = json.load(data_file)
df = json_normalize(data, sep="_").assign(match_id=file_name[:-5])

#Creating variables for all ball action types
passes = df.loc[df['type_name'] == 'Pass'].set_index('id')
ballrecovery = df.loc[df['type_name'] == 'Ball Recovery'].set_index('id')
block = df.loc[df['type_name'] == 'Block'].set_index('id')
intercept = df.loc[df['type_name'] == 'Interception'].set_index('id')
tackle = df.loc[df['type_name'] == 'Duel'].set_index('id')
carry = df.loc[df['type_name'] == 'Carry'].set_index('id')
dispossessed = df.loc[df['type_name'] == 'Dispossessed'].set_index('id')
miscontrol = df.loc[df['type_name'] == 'Miscontrol'].set_index('id')
foulwon = df.loc[df['type_name'] == 'Foul Won'].set_index('id')
foulagainst = df.loc[df['type_name'] == 'Foul Committed'].set_index('id')
dribble = df.loc[df['type_name'] == 'Dribble'].set_index('id')
shot = df.loc[df['type_name'] == 'Shot'].set_index('id')
player = df.loc[df['type_name'] == 'Player'].set_index('id')
clearance = df.loc[df['type_name'] == 'Clearance'].set_index('id')

#included 11 because of a ball recovery -> pass action from 10:58 to 11:00
ballrectimes = [11]
ballrecminsec = []
ballrectimestamp =[]
playerdf = pd.DataFrame()

for i, ball in ballrecovery.iterrows():
    if ball['team_name'] == "France" and ball['player_id'] == 3961:
        x = ball['location'][0]
        y = ball['location'][1]
        if ball['ball_recovery_recovery_failure'] == True:
            ballrecoveryCircle = plt.Circle((x, y), 1, facecolor='maroon', edgecolor='black',zorder=3)
            ax.add_patch(ballrecoveryCircle)
            # plt.text((x + 1), y + 1, str(ball['minute']) + ":" + str(ball['second']))
        else:
            ballrecoveryCircle = plt.Circle((x, y), 1, facecolor='lime', edgecolor='black',zorder=3)
            # d5b942
            ax.add_patch(ballrecoveryCircle)
            #plt.text(x, y, str(ball['minute']))
            #label = ax.annotate(str(ball['minute']), xy=(x, y), fontsize=10, ha="center",va = "center")
            ballrectimes.append(ball['minute'])
            ballrecminsec.append(str(ball['minute']) + ":" + str(ball['second']))
            # plt.text((x + 1), y + 1, str(ball['minute']) + ":" + str(ball['second']))
for i,intcpt in intercept.iterrows():
    if intcpt['team_name'] == "France" and intcpt['player_id'] == 3961:
        x = intcpt['location'][0]
        y = intcpt['location'][1]

        if intcpt['interception_outcome_name'] == "Won":
            ax.plot(x, y, color='lime', marker="v", markeredgecolor='black', markersize=15)
            ballrectimes.append(intcpt['minute'])
            ballrecminsec.append(str(intcpt['minute']) + ":" + str(intcpt['second']))
            #plt.text((x + 1), y + 1, str(intcpt['minute']) + ":" + str(intcpt['second']))
        elif intcpt['interception_outcome_name'] == "Success In Play":
            ax.plot(x, y, color='lime', marker="v", markeredgecolor='black', markersize=15)
            ballrectimes.append(intcpt['minute'])
            ballrecminsec.append(str(intcpt['minute']) + ":" + str(intcpt['second']))
            #plt.text((x + 1), y + 1, str(intcpt['minute']) + ":" + str(intcpt['second']))
        else:
            ax.plot(x, y, color='maroon', marker="v", markeredgecolor='black', markersize=15,zorder=1)
            ballrectimes.append(intcpt['minute'])
            ballrecminsec.append(str(intcpt['minute']) + ":" + str(intcpt['second']))
            #plt.text((x + 1), y + 1, str(intcpt['minute']) + ":" + str(intcpt['second']))


#rest
for i, dr in dribble.iterrows():
    if dr['team_name'] == "France" and dr['player_id'] == 3961 and dr['minute'] in ballrectimes:
        x = dr['location'][0]
        y = dr['location'][1]
        drCircle = plt.Circle((x, y), 1, facecolor='tomato', edgecolor='black',zorder=3)
        #ax.add_patch(drCircle)
        ax.plot(x, y, color='white', marker="$D$", markeredgecolor='black', markersize=15)
        #plt.text((x + 1), y + 1, str(dr['minute']) + ":" + str(dr['second']))
for i, fa in foulagainst.iterrows():
    if fa['team_name'] == "France" and fa['player_id'] == 3961 and fa['minute'] in ballrectimes:
        x = fa['location'][0]
        y = fa['location'][1]
        faCircle = plt.Circle((x, y), 1, facecolor='yellow', edgecolor='black')
        ax.plot(x, y, color='white', marker="$F$", markeredgecolor='black', markersize=15)
        #ax.add_patch(faCircle)
        #plt.text((x + 1), y + 1, str(fa['minute']) + ":" + str(fa['second']))
for i, dp in dispossessed.iterrows():
    if dp['team_name'] == "France" and dp['player_id'] == 3961 and dp['minute'] in ballrectimes:
        x = str(dp['minute']) + ":" + str(dp['second'])
        if x == "32:7" or x == "10:56":
            pass
        else:
            x = dp['location'][0]
            y = dp['location'][1]
            ax.plot(x, y, color='maroon', marker=r'$\bigotimes$', markeredgecolor='black', markersize=15)
            # dpCircle = plt.Circle((x, y), 1, facecolor='purple', edgecolor='black',zorder = 3)
            # ax.add_patch(dpCircle)
            # plt.text((x + 1), y + 1, str(dp['minute']) + ":" + str(dp['second']))
for i, mc in miscontrol.iterrows():
    if mc['team_name'] == "France" and mc['player_id'] == 3961 and mc['minute'] in ballrectimes:
        x = mc['location'][0]
        y = mc['location'][1]
        mcCircle = plt.Circle((x, y), 1, facecolor='pink', edgecolor='black')
        ax.add_patch(mcCircle)
        #plt.text((x + 1), y + 1, str(mc['minute']) + ":" + str(mc['second']))
for i, fw in foulwon.iterrows():
    if fw['team_name'] == "France" and fw['player_id'] == 3961:
        x = fw['location'][0]
        y = fw['location'][1]
        fwCircle = plt.Circle((x, y), 1, facecolor='white', edgecolor='black')
        ax.plot(x, y, color='yellow', marker="$f$", markeredgecolor='black', markersize=15)

        #ax.add_patch(fwCircle)
        plt.text((x + 1), y + 1, str(fw['minute']) + ":" + str(fw['second']))
for i, sht in shot.iterrows():
    if sht['team_name'] == "France"and sht['player_id'] == 3961:
        x = sht['location'][0]
        y = sht['location'][1]
        ftyCircle = plt.Circle((x, y), 1, facecolor='red', edgecolor='black')
        ax.add_patch(ftyCircle)
        plt.text((x + 1), y + 1, str(sht['minute']) + ":" + str(sht['second']))

for i, thepass in passes.iterrows():
    if thepass['team_name'] == "France" and thepass['player_id'] == 3961:
        if thepass['minute'] in ballrectimes:
            x = str(thepass['minute']) + ":" + str(thepass['second'])
            if str(thepass['minute']) + ":" + str(thepass['second']) in ballrecminsec:
                x = thepass['location'][0]
                y = thepass['location'][1]
                dx = thepass['pass_end_location'][0]
                dy = thepass['pass_end_location'][1]

                plt.annotate("", xy=(dx, dy), xytext=(x, y),
                            arrowprops=dict(facecolor = '#2371a3',edgecolor = 'black', headlength = 8,width = 4),zorder = 2)
                # plt.text((x + 1), y + 1, str(thepass['minute']) + ":" + str(thepass['second']))
                # plt.text((x + 1), y + 1, thepass['pass_recipient_name'])
            # elif x == "49:11" or x=="32:40" or x=="51:32" or x=="32:4" or x=="36:58":
            #     pass

            else:
                x = thepass['location'][0]
                y = thepass['location'][1]
                # dx = thepass['pass_end_location'][0] - x
                # dy = thepass['pass_end_location'][1] - y
                dx = thepass['pass_end_location'][0]
                dy = thepass['pass_end_location'][1]
                x1 = str(thepass['minute']) + ":" + str(thepass['second'])
                if x1 == "64:42" or x1 == "58:12":
                    pass
                else:
                    plt.annotate("", xy=(dx, dy), xytext=(x, y),
                                arrowprops=dict(facecolor = '#2371a3',edgecolor = 'black', headlength = 8,width = 4),zorder = 2)
                    #passArrow = plt.Arrow(x,y, dx, dy, width=3,zorder=2)
                    passCircle = plt.Circle((x, y), 0.5, facecolor='black', edgecolor='black',zorder=3)
                    #ax.add_patch(passArrow)
                    ax.add_patch(passCircle)
                    # plt.text((x + 1), y + 1, str(thepass['minute']) + ":" + str(thepass['second']))

        elif thepass['pass_type_name'] == "Recovery":
            x = thepass['location'][0]
            y = thepass['location'][1]
            dx = thepass['pass_end_location'][0]
            dy = thepass['pass_end_location'][1]
            plt.annotate("", xy=(dx, dy), xytext=(x, y),
                         arrowprops=dict(facecolor='#2371a3', edgecolor='black', headlength=8, width=4), zorder=2)
            passCircle = plt.Circle((x, y), 1, facecolor='lime', edgecolor='black',zorder=3)
            # ax.add_patch(passArrow)
            ax.add_patch(passCircle)
            #plt.text((x + 1), y + 1, str(thepass['minute']) + ":" + str(thepass['second']))
        else:
            pass

for i, crry in carry.iterrows():
    if crry['team_name'] == "France" and crry['player_id'] == 3961 and crry['minute'] in ballrectimes:
        if str(crry['minute']) + ":" + str(crry['second']) in ballrecminsec:
            x = crry['location'][0]
            y = crry['location'][1]
            dx = crry['carry_end_location'][0] - x
            dy = crry['carry_end_location'][1] - y
            x1 = [x,x + dx]
            y1 = [y,y + dy]
            #crryArrow = plt.Arrow(x, y, dx, dy, width=1, linestyle='dashed',color='red')
            ax.plot(x1, y1, 'white',linewidth = 2, linestyle=':', marker='',zorder=1)
            #ax.add_patch(crryArrow)
            #plt.text((x + 1), y + 1, str(crry['minute']) + ":" + str(crry['second']))
        # else:
        #     x = crry['location'][0]
        #     y = crry['location'][1]
        #     dx = crry['carry_end_location'][0] - x
        #     dy = crry['carry_end_location'][1] - y
        #     x1 = [x,x + dx]
        #     y1 = [y,y + dy]
        #     crryArrow = plt.Arrow(x,y, dx, dy, width=3)
        #     crryCircle = plt.Circle((x, y), 1, facecolor='orange', edgecolor='black',zorder=3)
        #     ax.add_patch(crryCircle)
        #     ax.plot(x1, y1, 'white',linewidth = 2, linestyle=':', marker='',zorder=1)
        #     plt.text((x + 1), y + 1, str(crry['minute']) + ":" + str(crry['second']))
        #     #plt.text((x + 1), y + 1, thepass['pass_recipient_name'])

###Result
brwonpatch = mpatches.Patch(facecolor='lime',edgecolor = 'black', label='Successful')
brlost = mpatches.Patch(facecolor='maroon', edgecolor='black', label='Failed')

###Action
intpatch = mlines.Line2D([],[],color='white',mec = 'black', marker = 'v',linestyle = 'none', label='Interception',markersize=15)
brpatch = mlines.Line2D([],[],color='white',mec = 'black', marker = '.',linestyle = 'none', label='Ball Recovery',markersize=15)
# tacklepatch = mlines.Line2D([],[],color='white',mec = 'black', marker = '^',linestyle = 'none', label='Attempted Tackle',markersize=12)
# blockpatch = mlines.Line2D([],[],color='white',mec = 'black', marker = 's',linestyle = 'none', label='Block',markersize=10)
# clearancepatch = mlines.Line2D([],[],color='white',mec = 'black', marker = '*',linestyle = 'none', label='Clearance',markersize=13)

#Post Action
carrypatch = mlines.Line2D([],[],color='grey',mec = 'black',  linestyle = ':', label='Movement With Ball',markersize=15)
passpatch = mlines.Line2D([],[],color='black',mec = 'black',  marker = '.',linestyle = 'none', label='Pass Location',markersize=10)
arrowpatch = mlines.Line2D([],[],color='steelblue',  marker = r'$\to$',linestyle = 'none', label='Pass Direction + Length',markersize=15)
dribblepatch = mlines.Line2D([],[],color='white',mec = 'black', marker = '$D$',linestyle = 'none', label='Dribble',markersize=12)
foulpatch = mlines.Line2D([],[],color='white',mec = 'black', marker = '$F$',linestyle = 'none', label='Committed a Foul',markersize=12)
# miscontrolpatch = mlines.Line2D([],[],color='tomato',mec = 'black', marker = r'$\bigotimes$',linestyle = 'none', label='Dispossessed by Opponent',markersize=12)

plt.legend(handles=[brwonpatch, brlost,intpatch,brpatch,carrypatch,passpatch,arrowpatch,dribblepatch,foulpatch],loc = 'lower left')
# plt.legend(handles=[brwonpatch, brlost,tacklepatch,blockpatch,clearancepatch,carrypatch,passpatch,arrowpatch,miscontrolpatch],loc = 'upper left')
plt.arrow(49,-2,20,0,color='white', head_width =2, width = 0.80)
plt.arrow(49,82,20,0,color='white', head_width =2, width = 0.80)
# ax.text(30, -0.3, ' Attacking direction', fontsize = 16, fontname = 'Corbel', color = 'white')
ax.text(30, 82.7, ' Attacking direction', fontsize = 16, fontname = 'Corbel', color = 'white')


title_font = "Arial"
ax.set_title("N'Golo Kante Ball Retrieving Actions vs. Peru",
          fontweight = "bold",
          fontsize = 18,
          fontfamily = title_font)

# title_font = "Arial"
# ax.set_title("N'Golo Kante Ball Stopping Actions vs. Peru",
#           fontweight = "bold",
#           fontsize = 18,
#           fontfamily = title_font)


plt.show()


####Ball stop

###Ball Recovering Actions (Ball Recoveries + Interceptions) vs. Peru
#Draw pitch map
from mplsoccer.pitch import Pitch
pitch = Pitch(pitch_type='statsbomb', orientation='horizontal',
              pitch_color='#22312b', line_color='#c7d5cc', figsize=(16, 11),
              constrained_layout=True, tight_layout=False)
(fig,ax) = pitch.draw()
fig.set_size_inches(10,7)


#included 11 because of a ball recovery -> pass action from 10:58 to 11:00
ballstoptimes = []
ballstopminsec = []
ballstoptimestamp =[]
playerdf = pd.DataFrame()

for i,tckl in tackle.iterrows():
    if tckl['team_name'] == "France" and tckl['player_id'] == 3961:
        x = tckl['location'][0]
        y = tckl['location'][1]
        if tckl['duel_type_name'] == "Tackle":
            if tckl['duel_outcome_name'] == "Won":
                ax.plot(x, y, color='lime', marker="^", markeredgecolor='black', markersize=15)
                ballstoptimes.append(tckl['minute'])
                ballstopminsec.append(str(tckl['minute']) + ":" + str(tckl['second']))
                # plt.text((x + 1), y + 1, str(tckl['minute']) + ":" + str(tckl['second']))
            elif tckl['duel_outcome_name'] == "Success In Play":
                ax.plot(x, y, color='lime', marker="^", markeredgecolor='black', markersize=15)
                ballstoptimes.append(tckl['minute'])
                ballstopminsec.append(str(tckl['minute']) + ":" + str(tckl['second']))
                # plt.text((x + 1), y + 1, str(tckl['minute']) + ":" + str(tckl['second']))
            else:
                ax.plot(x, y, color='maroon', marker="^", markeredgecolor='black', markersize=15)
                ballstoptimes.append(tckl['minute'])
                ballstopminsec.append(str(tckl['minute']) + ":" + str(tckl['second']))
                # plt.text((x + 1), y + 1, str(tckl['minute']) + ":" + str(tckl['second']))

        else:
                ax.plot(x, y, color='black', marker="^", markeredgecolor='black', markersize=15)
                ballstoptimes.append(tckl['minute'])
                ballstopminsec.append(str(tckl['minute']) + ":" + str(tckl['second']))
                # plt.text((x + 1), y + 1, str(tckl['minute']) + ":" + str(tckl['second']))
for i,blck in block.iterrows():
    if blck['team_name'] == "France" and blck['player_id'] == 3961:
        x = blck['location'][0]
        y = blck['location'][1]
        #plt.text((pitchLengthX - x + 1), y + 1, block['block_offensive'])
        ax.plot(x, y, color='lime', marker="s", markeredgecolor='black', markersize=13)
        # plt.text((x + 1), y + 1, str(blck['minute']) + ":" + str(blck['second']))
        ballstopminsec.append(str(blck['minute']) + ":" + str(blck['second']))
        ballstoptimes.append(blck['minute'])
for i,clr in clearance.iterrows():
    if clr['team_name'] == "France" and clr['player_id'] == 3961:
        x = clr['location'][0]
        y = clr['location'][1]
        #plt.text((pitchLengthX - x + 1), y + 1, block['block_offensive'])
        ax.plot(x, y, color='lime', marker="*", markeredgecolor='black', markersize=16)
        # plt.text((x + 1), y + 1, str(clr['minute']) + ":" + str(clr['second']))
        ballstopminsec.append(str(clr['minute']) + ":" + str(clr['second']))
        ballstoptimes.append(clr['minute'])
#rest
for i, dr in dribble.iterrows():
    if dr['team_name'] == "France" and dr['player_id'] == 3961 and dr['minute'] in ballstoptimes:
        x = dr['location'][0]
        y = dr['location'][1]
        drCircle = plt.Circle((x, y), 1, facecolor='tomato', edgecolor='black',zorder=3)
        #ax.add_patch(drCircle)
        ax.plot(x, y, color='white', marker="$D$", markeredgecolor='black', markersize=15)
        # plt.text((x + 1), y + 1, str(dr['minute']) + ":" + str(dr['second']))
for i, fa in foulagainst.iterrows():
    if fa['team_name'] == "France" and fa['player_id'] == 3961 and fa['minute'] in ballstoptimes:
        x = fa['location'][0]
        y = fa['location'][1]
        faCircle = plt.Circle((x, y), 1, facecolor='yellow', edgecolor='black')
        ax.plot(x, y, color='white', marker="$F$", markeredgecolor='black', markersize=15)
        #ax.add_patch(faCircle)
        # plt.text((x + 1), y + 1, str(fa['minute']) + ":" + str(fa['second']))
for i, dp in dispossessed.iterrows():
    if dp['team_name'] == "France" and dp['player_id'] == 3961 and dp['minute'] in ballstoptimes:
        x = str(dp['minute']) + ":" + str(dp['second'])
        if x == "32:7":
            pass
        else:
            x = dp['location'][0]
            y = dp['location'][1]
            ax.plot(x, y, color='maroon', marker=r'$\bigotimes$', markeredgecolor='black', markersize=15)
            # dpCircle = plt.Circle((x, y), 1, facecolor='purple', edgecolor='black',zorder = 3)
            # ax.add_patch(dpCircle)
            # plt.text((x + 1), y + 1, str(dp['minute']) + ":" + str(dp['second']))
for i, mc in miscontrol.iterrows():
    if mc['team_name'] == "France" and mc['player_id'] == 3961 and mc['minute'] in ballstoptimes:
        x = mc['location'][0]
        y = mc['location'][1]
        mcCircle = plt.Circle((x, y), 1, facecolor='pink', edgecolor='black')
        ax.add_patch(mcCircle)
        #plt.text((x + 1), y + 1, str(mc['minute']) + ":" + str(mc['second']))
for i, fw in foulwon.iterrows():
    if fw['team_name'] == "France" and fw['player_id'] == 3961:
        x = fw['location'][0]
        y = fw['location'][1]
        fwCircle = plt.Circle((x, y), 1, facecolor='white', edgecolor='black')
        ax.plot(x, y, color='yellow', marker="$f$", markeredgecolor='black', markersize=15)

        #ax.add_patch(fwCircle)
        plt.text((x + 1), y + 1, str(fw['minute']) + ":" + str(fw['second']))
for i, sht in shot.iterrows():
    if sht['team_name'] == "France"and sht['player_id'] == 3961:
        x = sht['location'][0]
        y = sht['location'][1]
        ftyCircle = plt.Circle((x, y), 1, facecolor='red', edgecolor='black')
        ax.add_patch(ftyCircle)
        plt.text((x + 1), y + 1, str(sht['minute']) + ":" + str(sht['second']))

for i, thepass in passes.iterrows():
    if thepass['team_name'] == "France" and thepass['player_id'] == 3961:
        if thepass['minute'] in ballstoptimes:
            x = str(thepass['minute']) + ":" + str(thepass['second'])
            if str(thepass['minute']) + ":" + str(thepass['second']) in ballstopminsec:
                x = thepass['location'][0]
                y = thepass['location'][1]
                dx = thepass['pass_end_location'][0]
                dy = thepass['pass_end_location'][1]

                plt.annotate("", xy=(dx, dy), xytext=(x, y),
                            arrowprops=dict(facecolor = '#2371a3',edgecolor = 'black', headlength = 8,width = 4),zorder = 2)
                # plt.text((x + 1), y + 1, str(thepass['minute']) + ":" + str(thepass['second']))
                # plt.text((x + 1), y + 1, thepass['pass_recipient_name'])
            # elif x == "49:11" or x=="32:40" or x=="51:32" or x=="32:4" or x=="36:58":
            #     pass

            else:
                x = thepass['location'][0]
                y = thepass['location'][1]
                # dx = thepass['pass_end_location'][0] - x
                # dy = thepass['pass_end_location'][1] - y
                dx = thepass['pass_end_location'][0]
                dy = thepass['pass_end_location'][1]
                x1 = str(thepass['minute']) + ":" + str(thepass['second'])
                if x1 == "64:42" or x1 == "58:12" or x1 == "51:32" or x1 == "32:4" or x1 == "49:11" or x1 == "32:40" or x1 == "36:58":
                    pass
                else:
                    plt.annotate("", xy=(dx, dy), xytext=(x, y),
                                arrowprops=dict(facecolor = '#2371a3',edgecolor = 'black', headlength = 8,width = 4),zorder = 2)
                    #passArrow = plt.Arrow(x,y, dx, dy, width=3,zorder=2)
                    passCircle = plt.Circle((x, y), 0.5, facecolor='black', edgecolor='black',zorder=3)
                    #ax.add_patch(passArrow)
                    ax.add_patch(passCircle)
                    # plt.text((x + 1), y + 1, str(thepass['minute']) + ":" + str(thepass['second']))
        else:
            pass

for i, crry in carry.iterrows():
    if crry['team_name'] == "France" and crry['player_id'] == 3961 and crry['minute'] in ballstoptimes:
        if str(crry['minute']) + ":" + str(crry['second']) in ballstopminsec:
            x = crry['location'][0]
            y = crry['location'][1]
            dx = crry['carry_end_location'][0] - x
            dy = crry['carry_end_location'][1] - y
            x1 = [x,x + dx]
            y1 = [y,y + dy]
            #crryArrow = plt.Arrow(x, y, dx, dy, width=1, linestyle='dashed',color='red')
            ax.plot(x1, y1, 'white',linewidth = 2, linestyle=':', marker='',zorder=1)
            #ax.add_patch(crryArrow)
            #plt.text((x + 1), y + 1, str(crry['minute']) + ":" + str(crry['second']))

###Result
brwonpatch = mpatches.Patch(facecolor='lime',edgecolor = 'black', label='Successful')
brlost = mpatches.Patch(facecolor='maroon', edgecolor='black', label='Failed')

###Action
tacklepatch = mlines.Line2D([],[],color='white',mec = 'black', marker = '^',linestyle = 'none', label='Attempted Tackle',markersize=12)
blockpatch = mlines.Line2D([],[],color='white',mec = 'black', marker = 's',linestyle = 'none', label='Block',markersize=10)
clearancepatch = mlines.Line2D([],[],color='white',mec = 'black', marker = '*',linestyle = 'none', label='Clearance',markersize=13)

#Post Action
carrypatch = mlines.Line2D([],[],color='grey',mec = 'black',  linestyle = ':', label='Movement With Ball',markersize=15)
passpatch = mlines.Line2D([],[],color='black',mec = 'black',  marker = '.',linestyle = 'none', label='Pass Location',markersize=10)
arrowpatch = mlines.Line2D([],[],color='steelblue',  marker = r'$\to$',linestyle = 'none', label='Pass Direction + Length',markersize=15)
dribblepatch = mlines.Line2D([],[],color='white',mec = 'black', marker = '$D$',linestyle = 'none', label='Dribble',markersize=12)
foulpatch = mlines.Line2D([],[],color='white',mec = 'black', marker = '$F$',linestyle = 'none', label='Committed a Foul',markersize=12)
miscontrolpatch = mlines.Line2D([],[],color='tomato',mec = 'black', marker = r'$\bigotimes$',linestyle = 'none', label='Dispossessed by Opponent',markersize=12)

plt.legend(handles=[brwonpatch, brlost,tacklepatch,blockpatch,clearancepatch,carrypatch,passpatch,arrowpatch,miscontrolpatch],loc = 'upper left')
plt.arrow(49,-2,20,0,color='white', head_width =2, width = 0.80)
plt.arrow(49,82,20,0,color='white', head_width =2, width = 0.80)
# ax.text(30, -0.3, ' Attacking direction', fontsize = 16, fontname = 'Corbel', color = 'white')
ax.text(30, 82.7, ' Attacking direction', fontsize = 16, fontname = 'Corbel', color = 'white')

title_font = "Arial"
ax.set_title("N'Golo Kante Ball Stopping Actions vs. Peru",
          fontweight = "bold",
          fontsize = 18,
          fontfamily = title_font)

plt.show()
