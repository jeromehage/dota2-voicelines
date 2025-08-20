import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

data = pd.read_csv('results_ti12_n723.csv', encoding = 'utf-16', sep = ';', index_col = 0)
data = data[['name', 'chatwheels', 'language', 'games', 'wins',
       'winrate', 'mean_uses', 'median_uses', 'max_uses', 'laning', 'midgame',
       'lategame', 'median_first_use_minutes', 'spammability']]
data.sort_values(by = 'games', ascending = True, inplace = True)
data = data[data['games'] >= 25]
data['label'] = data['name'] + '\n' + data['chatwheels'].astype(str)

fig, ax = plt.subplots(layout = 'constrained')

fields = {
    'games': 'Games',
    'wins': 'Wins',
    'max_uses': 'Max uses',
    'median_uses': 'Average uses per player',
    }

x = np.arange(len(data))
width = 0.4  # the width of the bars
multiplier = 0

for i, (atr, name) in enumerate(fields.items()):
    offset = width * multiplier
    rects = ax.barh(x + offset, data[atr], width, label = name)
    ax.bar_label(rects, padding = 3)
    if i % 2 == 1:
        multiplier += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
#ax.set_ylabel('Talent', fontsize = 16)
ax.set_yticks(x + width, data['label'])
ax.set_title('TI12 talent voiceline performance')
ax.legend(loc = 'lower right', ncols = 2)
#ax.set_xlim(0, 250)

plt.show()
