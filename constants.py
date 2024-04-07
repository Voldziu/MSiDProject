API_KEY='RGAPI-9960e089-76e1-426b-aba0-f2551888dca9'
DIVISIONS_LEVELS = {
    "IRON": 0,
    "BRONZE": 400,
    "SILVER": 800,
    "GOLD": 1200,
    "PLATINUM": 1600,
    "EMERALD": 2000,
    "DIAMOND": 2400,
    "MASTER": 2800,
    "GRANDMASTER": 2800,  # from master elo is just rank + lp
    "CHALLENGER": 2800
}
ROMAN_DIVISIONS_LEVELS = {
    "I": 300,
    "II": 200,
    "III": 100,
    "IV": 0,

}

LEVELS_DIVISIONS={
    0: "IRON",
    1: "BRONZE",
    2: "SILVER",
    3: "GOLD",
    4: "PLATINUM",
    5: "EMERALD",
    6: "DIAMOND",
    # more is master
}
LEVELS_DIVISIONS_ROMAN={
    0:'IV',
    1:'III',
    2: 'II',
    3:'I'
}