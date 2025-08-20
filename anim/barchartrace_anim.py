import os
import pandas as pd
import numpy as np
import bar_chart_race as bcr
from matplotlib import pyplot as plt

import matplotlib.font_manager as fm
import matplotlib as mpl
#mpl.rcParams['font.sans-serif'] = ['SimSun'] # SimHei
mpl.rcParams['axes.unicode_minus'] = False
# font = fm.FontProperties(fname = 'C:\\Windows\\Fonts\\simsun.ttc')  # simsun.ttc simhei.ttf

talent = pd.read_csv('ti12_talent.csv', encoding = 'utf-8', sep = ';')
chatwheelkey = 'chatwheels' # chat_wheel_preview chatwheels
talent['label'] = talent['name'] + '\n' + talent['chatwheels'].astype(str)

# chat summary for each game
chatdata = []
for fn, f in enumerate(os.listdir('chat')):

    if fn % 100 == 0:
        print(fn)

    df = pd.read_csv(os.path.join('chat', f), index_col = 0)
    df = df[df['key'].isin(talent[chatwheelkey].values)]
    match_id = f.split('_')[0]

    if len(df) == 0:
        # skip games with no TI 11 talent voicelines
        continue

    grp = df.groupby(['key', 'player_slot']) # combine multiple uses

    data = pd.DataFrame()
    data['win'] = grp['win'].first()
    data['count'] = grp['win'].count()
    data['match_id'] = match_id

    chatdata += [data]

# prep wide data
games = pd.concat(chatdata).reset_index().merge(talent, right_on = chatwheelkey, left_on = 'key')
games = games.assign(**{'used': 1})
games = games.pivot_table(index = 'match_id', columns = ['label'], aggfunc = np.sum)['used'].fillna(0).astype(int)
games = games.cumsum()

# format
keep_every_games = 100
extra_periods = 20
games4 = games.iloc[keep_every_games - 1::keep_every_games, :]
games4 = games4.append(games4.iloc[[-1] * extra_periods])

# plot
bcr.bar_chart_race(
    df = games4,
    filename = 'talent_race4.mp4',
    orientation = 'h', # horizontal
    sort = 'desc', # descending
    n_bars = 10, # top 10
    fixed_order = False, # bars will keep shuffling
    fixed_max = False, # max x limit is dynamic, will grow with more matches

    interpolate_period = False,
    steps_per_period = 1,
    period_length = 250, # number of milliseconds per n steps = 1 period

    label_bars = {'x': .8, 'y': .8, 'ha': 'right', 'va': 'center' }, # bars have label on their right
    bar_size=.95, # gap between bars
    period_label = True, # use index as text label

    figsize = (3, 4),
    dpi = 200,
    #cmap = 'dark12',
    #title = 'TI11 talent voiceline usage',
    #title_size = 10,
    bar_label_size = 10,
    tick_label_size = 10,
    shared_fontdict = {'family' : 'SimSun', 'color' : '.1'},
    scale = 'linear', # linear or log
    writer = None, # probably means ffmpeg
    fig = None,
    bar_kwargs = {'alpha': .9},
    filter_column_colors = True)
