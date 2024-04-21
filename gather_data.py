import os.path
import sys
import time

import constants
import summoner
import match
import graph
import json

def process_summoners():

    summoners = constants.SUMMONERS_TO_CHECK

    for rank in list(summoners.keys())[2:]:
        for summonername in summoners[rank]:
            print(summonername)
            puuid = summoner.get_puuid(summonername)
            print(puuid)
            process_player_matches(puuid,rank)



def process_player_matches(puuid,rank):

    match_ids  = match.get_match_ids(puuid,'ranked',100)
    for i,match_id in enumerate(match_ids):
        filename = f"MatchData/{rank}/{rank}_{puuid}_{i}.json"
        if not os.path.exists(filename):
            try:
                jason = match.get_match_json(match_id)
            except:
                print(f'Exception, skipping match  {i}',file=sys.stderr)
            if jason:

                with open(filename,'w') as json_file:
                    json.dump(jason,json_file)
            else:
                print(f"Probably match is too short to analyze, skip {i}")

        else:
            print(f'skip {i}')

            #time.sleep(WAIT_INTERVAL)



if __name__ =="__main__":
    print(process_summoners())











