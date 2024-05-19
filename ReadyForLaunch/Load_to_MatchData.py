from constants import SUMMONERS_TO_CHECK,API_KEY
import os

"""
Script for creating folders for match data
"""
def create_folders():
    os.makedirs("MatchData", exist_ok=True)
    os.chdir("MatchData/")
    folder_names = SUMMONERS_TO_CHECK.keys()

    for name in folder_names:
        os.makedirs(name,exist_ok=True)


if __name__=="__main__":
    create_folders()


