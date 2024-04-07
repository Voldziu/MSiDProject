import requests
import numpy as np

from summoner import get_nickname,get_soloduo_level
from constants import API_KEY
import constants




def get_match_ids(puuid ,type ,n):
    """
    get last n matches of given type (ranked,normal) played by puuid player

    :param puuid:  summoner puuuid
    :param type: 'ranked',...
    :param n:  number of matches given, max 100
    :return: list of matches_id
    """
    url =f'https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?type={type}&start=0&count={n}&api_key={API_KEY}'
    match_ids = requests.get(url).json()
    return match_ids


def get_match_by_id(match_id):
    """

    :param match_id: match id
    :return: metadata of finished match
    """
    url = f'https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={API_KEY}'
    response = requests.get(url).json()
    return response


def get_queue_id(match_id):
    match = get_match_by_id(match_id)
    id = match['info']['queueId']
    return id

def calculate_team_level(match_id ,queueID=420):
    match =get_match_by_id(match_id)
    if (get_queue_id(match_id) == queueID):
        participants = match['metadata']['participants']  # 0-5 indecies blueside, 5: redside
        blue_side_list_of_levels = []
        red_side_list_of_levels = []

        for puuid in participants[0:5]:
            summoner_name = get_nickname(puuid)
            solo_duo_level = get_soloduo_level(summoner_name)
            blue_side_list_of_levels.append(solo_duo_level)

        for puuid in participants[5:]:
            summoner_name = get_nickname(puuid)
            solo_duo_level = get_soloduo_level(summoner_name)
            red_side_list_of_levels.append(solo_duo_level)

        blue_side_array = np.array(blue_side_list_of_levels).astype(float)
        blue_side_array[blue_side_array == None] = np.nan
        b_mean = round(np.nanmean(blue_side_array))
        red_side_array = np.array(red_side_list_of_levels).astype(float)
        red_side_array[red_side_array == None] = np.nan
        r_mean = round(np.nanmean(red_side_array))
        blue_side_array[np.isnan(blue_side_array)] = b_mean
        red_side_array[np.isnan(red_side_array)] = r_mean

        return {"blue": blue_side_array,
                "red": red_side_array}


def calculate_match_level(match_id,queueID=420):
    teams_levels=calculate_team_level(match_id,queueID)
    blue_avg = np.mean(teams_levels['blue'],axis=0)
    red_avg = np.mean(teams_levels['red'], axis=0)

    return int((0.5*(blue_avg+red_avg) // 100) *100)


def get_literal_match_level(match_level:int):
    main_rank_level = match_level //400
    rest = match_level - main_rank_level * 400


    main_rank_string_value=""
    if(main_rank_level>=7):
        main_rank_string_value='MASTER'
        return f'{main_rank_string_value} {rest} lp'
    else:
        roman_rank_level = rest // 100


        main_rank_string_value=contants.LEVELS_DIVISIONS[main_rank_level]
        roman_rank_string_value = contants.LEVELS_DIVISIONS_ROMAN[roman_rank_level]
        return f'{main_rank_string_value} {roman_rank_string_value}'







def get_match_timeline(matchid:str):
    url=f'https://europe.api.riotgames.com/lol/match/v5/matches/{matchid}/timeline?api_key={API_KEY}'
    response = requests.get(url).json()
    return response


def get_match_info(match_timeline):
    return match_timeline['info']
def get_timeline_frames(match_info):
    return match_info['frames']



if __name__=="__main__":
    lvl = (calculate_match_level('EUN1_3576787586'))
    print(get_literal_match_level(lvl))