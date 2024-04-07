import requests
from constants import API_KEY,DIVISIONS_LEVELS,ROMAN_DIVISIONS_LEVELS


def get_summoner_data(nickname):
    url = f'https://eun1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{nickname}?api_key={API_KEY}'
    summoner_data = requests.get(url).json()
    return summoner_data


def get_puuid(nickname):
    return get_summoner_data(nickname)['puuid']


def get_nickname(puuid):
    url = f'https://europe.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}?api_key={API_KEY}'
    response = requests.get(url).json()
    return response['gameName']


def get_summoner_id(nickname):
    return get_summoner_data(nickname)['id']

def get_summoner_league_entries(nickname):
    url=f'https://eun1.api.riotgames.com/lol/league/v4/entries/by-summoner/{get_summoner_id(nickname)}?api_key={API_KEY}'
    response = requests.get(url).json()
    leagues_dict={}
    for i,league in enumerate( response):
        allinfo_dict = response[i]
        leagues_dict[allinfo_dict['queueType']]=[
            allinfo_dict['tier'],
            allinfo_dict['rank'],
            allinfo_dict['leaguePoints']
        ]
    return {nickname:leagues_dict}

def calculate_league_level(nickname):
    summoner_league_entries = get_summoner_league_entries(nickname)
    ranks_dict = summoner_league_entries[nickname]
    calculated_dict={}
    for k,v in ranks_dict.items():
        calculated_dict[k]= DIVISIONS_LEVELS[ranks_dict[k][0]]+ROMAN_DIVISIONS_LEVELS[ranks_dict[k][1]]+ranks_dict[k][2]
    return calculated_dict

def get_soloduo_level(nickname):
    ranks_dict =calculate_league_level(nickname)
    if "RANKED_SOLO_5x5" in ranks_dict:
        return ranks_dict["RANKED_SOLO_5x5"]
    else:
        return None


