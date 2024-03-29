import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

data = pd.read_csv('data_ti12_n5887.csv', encoding = 'utf-16', sep = ';')
data = data[['name', 'chatwheels', 'games', 'wins',
       'winrate', 'mean_uses', 'median_uses', 'max_uses', 'laning', 'midgame',
       'lategame', 'median_first_use_minutes', 'spammability']]
data.sort_values(by = 'games', ascending = True, inplace = True)
data = data[data['games'] >= 100]
data['label'] = data['name'] + '\n' + data['chatwheels'].astype(str)

fig, ax = plt.subplots(layout = 'constrained', figsize = (7, 8))
ax2 = ax.twiny()

x = np.arange(len(data))
width = 0.4  # the width of the bars

rects = ax.barh(x, data['max_uses'], width, label = 'Max uses', color = 'tab:red')
ax.bar_label(rects, padding = 3)
rects = ax.barh(x, data['median_uses'], width, label = 'Average uses per player', color = 'tab:green')
ax.bar_label(rects, padding = 3)

rects = ax2.barh(x + width, data['games'], width, label = 'Games', color = 'tab:blue')
ax2.bar_label(rects, padding = 6)
rects = ax2.barh(x + width, data['wins'], width, label = 'Wins', color = 'tab:orange')
ax2.bar_label(rects, padding = 3)

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_yticks(x + width, data['label'])
ax.set_title('TI12 talent voiceline performance')

li, lb = ax.get_legend_handles_labels()
li2, lb2 = ax2.get_legend_handles_labels()
ax.legend(li + li2, lb + lb2, loc = 'lower right', ncols = 2)

plt.show()
