import os
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

DIGITS = 3

# https://www.reddit.com/r/DotA2/comments/xt9qj4/chatwheel_say_numbers_for_the_new_sticker/
talent = pd.read_csv('talent.csv', encoding = 'utf-16', sep = ';')
talent[['talent', 'line']] = talent['chatwheel message'].str.split(' - ', 1, True)
talent.drop('chatwheel message', axis = 1, inplace = True)

# chat summary for each game
chatdata = []
for f in os.listdir('chat'):
    df = pd.read_csv(os.path.join('chat', f), index_col = 0)
    df = df[df['key'].isin(talent['voiceline_id'].values)]
    match_id = f.split('_')[0]

    if len(df) == 0:
        # skip games with no TI 11 talent voicelines
        continue

    # usage time
    df['laning'] = (df['time'] < 600).astype(int) # pre min 10
    df['midgame'] = ((df['time'] >= 600) & (df['time'] < 1500)).astype(int) # 10 < min < 25
    df['lategame'] = (df['time'] >= 1500).astype(int) # past min 25
    
    grp = df.groupby(['key', 'player_slot']) # combine multiple uses

    data = pd.DataFrame()
    data['win'] = grp['win'].first()
    data['count'] = grp['win'].count()
    data['first_use'] = grp['time'].min()
    data['count_laning'] = grp['laning'].sum()
    data['count_midgame'] = grp['midgame'].sum()
    data['count_lategame'] = grp['lategame'].sum()
    data['match_id'] = match_id

    chatdata += [data]

# results for all games
grouped = pd.concat(chatdata).groupby('key') # group each (player, voiceline, match_id) as a "game", even if it is the same match_id
results = pd.DataFrame()
results['games'] = grouped['win'].count()
results['wins'] = grouped['win'].sum()
results['winrate'] = grouped['win'].mean().round(DIGITS) * 100
results['mean_uses'] = grouped['count'].mean().round(DIGITS)
results['median_uses'] = grouped['count'].median()
results['max_uses'] = grouped['count'].max()

# time it is often used
results['laning'] = grouped['count_laning'].mean()
results['midgame'] = grouped['count_midgame'].mean()
results['lategame'] = grouped['count_lategame'].mean()
results['tot'] = results['laning'] + results['midgame'] + results['lategame']
results['laning'] = (results['laning'] / results['tot']).round(DIGITS) * 100
results['midgame'] = (results['midgame'] / results['tot']).round(DIGITS) * 100
results['lategame'] = (results['lategame'] / results['tot']).round(DIGITS) * 100
results.drop('tot', axis = 1, inplace = True)
results['median_first_use_minutes'] = (grouped['first_use'].median() / 60).astype(int)

# "analysis"
def verience(arr, dummy):
    return np.append(arr, dummy).var()
dummy = [0, 33.3, 66.6, 100] # helps with edge cases
results['spammability'] = results.apply(lambda x: 100000 * x['mean_uses'] / verience(x[['laning', 'midgame', 'lategame']], dummy), axis = 1).astype(int) # median uses divided by variance, like a coefficient of variation

# save results
results['match_ids'] = grouped['match_id'].agg(list)
output = talent.merge(results, left_on = 'voiceline_id', right_index = True)
output.to_csv('results_n{}.csv'.format(len(chatdata)), sep = ';', encoding = 'utf-16')

## winrate vs time used
usegrp = pd.concat(chatdata).reset_index().groupby(['key', 'win'], as_index = False)
usage = usegrp[['count_laning', 'count_midgame', 'count_lategame']].agg(lambda x: (x > 0).sum()) # count non 0
usage2 = usage.set_index('key') / usage.groupby('key').sum() # divide by total
usage2 = usage2[usage2['win'] == 1].fillna(0).drop('win', axis = 1)
output2 = talent.merge(usage2, left_on = 'voiceline_id', right_index = True)

# plots
def plotwinrate(n):
    top_ids = results['games'].sort_values(ascending = False)[:n].index
    top = output2[output2['voiceline_id'].isin(top_ids)].copy()
    top.rename({'count_laning': 'laning',
                'count_midgame': 'midgame',
                'count_lategame': 'lategame'}, axis = 1, inplace = True)
    plotdf = top.melt(id_vars = ['talent'], value_vars = ['laning', 'midgame', 'lategame'], var_name = 'stage', value_name = 'winrate')
    plotdf['winrate'] = plotdf['winrate'].round(DIGITS) * 100
    sns.catplot(data = plotdf, x = 'stage', y = 'winrate', hue = 'talent', kind = 'point', linewidth = 5)
    plt.show()

plotwinrate(8)
