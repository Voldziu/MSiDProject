import requests
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import match
from summoner import get_nickname,get_soloduo_level
from constants import API_KEY,DIVISIONS_LEVELS,ROMAN_DIVISIONS_LEVELS





def get_gold_history_per_champion(timeline_frames):
    return_dict ={str(i): np.array([]) for i in range(1 ,11)}

    for frame in timeline_frames:
        for participantid in range(1 ,11):
            s_participantid = str(participantid)
            gold_value = frame['participantFrames'][s_participantid]['totalGold']
            return_dict[s_participantid] = np.append( return_dict[s_participantid], gold_value)
    return return_dict

def sum_graph_into_teams(ghistory_per_champion_dict):
    values = list(ghistory_per_champion_dict.values())

    sum_groups = {"blue": np.sum(values[:5] ,axis=0),
                  "red": np.sum(values[5:] ,axis=0)}
    return sum_groups

def get_team_graph_diff(sum_graph_teams):
    return sum_graph_teams['blue' ] -sum_graph_teams['red']

def get_graph(match_id):
    return get_team_graph_diff(sum_graph_into_teams(get_gold_history_per_champion(match.get_timeline_frames(match.get_match_info(match.get_match_timeline(match_id))))))

def print_graph(team_gold_diff_array):
    plt.figure(figsize=(10 ,6))
    sns.lineplot(x=np.arange(len(team_gold_diff_array)) ,y=team_gold_diff_array)
    plt.axhline(y=0, color='black', linestyle='--', linewidth=0.5)
    plt.ylabel('Gold Diff')
    plt.xlabel('Time')
    plt.show()

def get_sum_of_abs_diffs(match_id):
    return get_sum_graph_absdiffs(get_team_graph_diff(sum_graph_into_teams(get_gold_history_per_champion(match.get_timeline_frames(match.get_match_info(match.get_match_timeline(match_id)))))))

def get_sum_graph_absdiffs(tmgd):
    sum_diff=0
    for i in range(1, len(tmgd)):
        diff = abs(tmgd[i]-tmgd[i-1])
        sum_diff+=diff
    return sum_diff



if __name__ =="__main__":
    tmgd = get_team_graph_diff(sum_graph_into_teams(get_gold_history_per_champion(match.get_timeline_frames(match.get_match_info(match.get_match_timeline('EUN1_3576787586'))))))
    print(list(tmgd))
    print_graph(tmgd)


