import constants
import summoner
import match
import graph
import json


summoners = constants.SUMMONERS_TO_CHECK

for rank in summoners.keys():
    for summonername in summoners[rank]:
        puuid = summoner.get_puuid(summonername)




