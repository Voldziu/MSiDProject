import os
import constants
import json
import pandas as pd




"""
Script responsible for creating dataframe from folders

"""

def create_df(folder_rank_directory):
    data_list = []
    for file in os.listdir(folder_rank_directory):
        file_path = os.path.join(folder_rank_directory, file)
        with open(file_path, 'r') as f:
            data = json.load(f)
            data_list.append(data)

    df = pd.DataFrame(data_list)
    return df


def all_ranks_list_df(path):

    folder_names = constants.SUMMONERS_TO_CHECK.keys()
    list_of_dfs=[]

    for name in folder_names:
        folder_path = os.path.join(path,name)
        rank_df = create_df(folder_path)
        list_of_dfs.append(rank_df)

    return list_of_dfs


def make_big_df(ldf):

    return pd.concat(ldf)











