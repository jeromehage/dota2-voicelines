import requests, json, time, os
import pandas as pd
os.chdir(os.path.dirname(os.path.realpath(__file__)))

OPEN_DOTA_DELAY = 5.1

## opendota
# download match data from open dota
def download_match_by_id(match_id):
    path = os.path.join('data', '{}_data.json'.format(match_id))
    url = 'https://api.opendota.com/api/matches/{}'
    request = requests.get(url.format(match_id))
    time.sleep(OPEN_DOTA_DELAY)
    if request.ok:
        with open(path, 'w') as f:
            json.dump(request.json(), f)

def get_parsed_matches(**params):
    url = 'https://api.opendota.com/api/parsedMatches{}'
    p = ''
    if params:
        p = '?' + '&'.join('{}={}'.format(k, v) for k, v in params.items())
    request = requests.get(url.format(p))
    time.sleep(OPEN_DOTA_DELAY)
    if request.ok:
        return [m['match_id'] for m in request.json()]

# read or download match
def get_match_by_id(match_id, force = False):
    path = os.path.join('data', '{}_data.json'.format(match_id))
    # check if it already exists
    if force or not os.path.isfile(path):
        print('GET:', match_id, end = ' ')
        download_match_by_id(match_id)
    else:
        print('READ:', match_id, end = ' ')
    # read back after download
    if not os.path.isfile(path):
        print('FAIL')
        return {}
    else:
        print('OK')
        with open(path, 'r') as f:
            # print('read:', path)
            data = json.load(f)
        return data

## get list of parsed matches
match_id_min = 8424549400 # random game 8 PM aug 20 2025
match_id_max = 9900000001

match_id = match_id_max
while match_id >= match_id_min:
    matches = get_parsed_matches(less_than_match_id = match_id)
    print(match_id)

    for m in matches:

        if m < match_id_min:
            continue
        
        data = get_match_by_id(m)

        # empty data
        if len(data) == 0:
            continue

        # extract chat data
        # ex: 6786771319 no chat
        if data['chat']:
            df = pd.DataFrame(data['chat'])
            df = df[df['type'] == 'chatwheel']
            if len(df): # ex: 6787090580 sometimes chat exists, but no chatwheel
                if data['radiant_win'] is not None: # 6789712989 not scored?
                    df['win'] = df.apply(lambda x: data['radiant_win'] ^ int(x['player_slot'] // 128), axis = 1)
                    df.to_csv(os.path.join('chat', '{}_chat.csv'.format(m)))

    match_id = matches[-1]
