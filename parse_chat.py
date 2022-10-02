import os
import pandas as pd
import numpy as np

data1 = [pd.read_csv(os.path.join('chat', f)) for f in os.listdir('chat')]
data2 = [d.groupby(['key', 'player_slot', 'win'], as_index = False)['time'].count() for d in data1]
data3 = pd.concat(data2).groupby('key')

results = pd.DataFrame()
results['games'] = data3['win'].count()
results['wins'] = data3['win'].sum()
results['winrate'] = data3['win'].mean()
results['avg_uses'] = data3['time'].mean()
results['max_uses'] = data3['time'].max()

# https://www.reddit.com/r/DotA2/comments/xt9qj4/chatwheel_say_numbers_for_the_new_sticker/
df = pd.read_csv('talent.csv', encoding = 'utf-16', sep = ';')
df[['talent', 'line']] = df['chatwheel message'].str.split(' - ', 1, True)
df.drop('chatwheel message', axis = 1, inplace = True)

# save results
output = df.merge(results, left_on = 'voiceline_id', right_index = True)
output.to_csv('results.csv', sep = ';', encoding = 'utf-16')
