import json

def get_champion_mapping(champ_id_list):
    with open('./metadata/champion.json') as f:
        champ_data = json.load(f)

    champ_mapping = {int(champ_data['data'][key]['key']):champ_data['data'][key]['name'] for key in champ_data['data'].keys()}
    champ_list = {champ_mapping[key] for key in champ_id_list}
    return champ_list