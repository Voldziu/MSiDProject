import requests
from constants import API_KEY,DIVISIONS_LEVELS,ROMAN_DIVISIONS_LEVELS


def get_summoner_data(nickname):
    url = f'https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{nickname}/EUNE?api_key={API_KEY}'
    response = requests.get(url)

    print(f'username:{nickname}summdata: {response}')
    summoner_data = response.json()
    return summoner_data


def get_puuid(nickname):
    return get_summoner_data(nickname)['puuid']


def get_nickname(puuid):
    url = f'https://europe.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}?api_key={API_KEY}'
    response = requests.get(url).json()
    print(response)
    return response['gameName']


def get_summoner_id(puuid):
    url =f'https://eun1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}?api_key={API_KEY}'
    response = requests.get(url)
    print(f'id summ response {response}')
    jason = response.json()
    return jason['id']

def get_summoner_league_entries(puuid):
    url=f'https://eun1.api.riotgames.com/lol/league/v4/entries/by-summoner/{get_summoner_id(puuid)}?api_key={API_KEY}'
    resp = requests.get(url)
    print(f'summ leag entr response: {resp}')
    response = resp.json()
    leagues_dict={}
    for i,league in enumerate( response):
        allinfo_dict = response[i]
        leagues_dict[allinfo_dict['queueType']]=[
            allinfo_dict['tier'],
            allinfo_dict['rank'],
            allinfo_dict['leaguePoints']
        ]
    return {puuid:leagues_dict}

def calculate_league_level(puuid):
    summoner_league_entries = get_summoner_league_entries(puuid)
    ranks_dict = summoner_league_entries[puuid]
    calculated_dict={}
    for k,v in ranks_dict.items():
        calculated_dict[k]= DIVISIONS_LEVELS[ranks_dict[k][0]]+ROMAN_DIVISIONS_LEVELS[ranks_dict[k][1]]+ranks_dict[k][2]
    return calculated_dict

def get_soloduo_level(puuid):
    ranks_dict =calculate_league_level(puuid)
    if "RANKED_SOLO_5x5" in ranks_dict:
        return ranks_dict["RANKED_SOLO_5x5"]
    else:
        return None


