"""
Contains variables that are shared across modules. Needed for multithreading calls
"""
# for scoreboard
winners = []
losers = []

# for news
news_list = []

# for weather
weather_list = []

# didn't really want this huge line of code anywhere else, so I put it here. for NBA team abbreviations
teams = {"Atlanta" : "ATL", "Brooklyn":"BKN", "Boston" : "BOS" , "Charlotte" : "CHA" , "Chicago" : "CHI" , "Cleveland":"CLE", "Dallas" : "DAL" , "Denver" : "DEN" , "Detroit" : "DET" , "Golden State": "GSW" , "Houston": "HOU", "Indiana" : "IND" , "LA Clippers" : "LAC" , "LA Lakers" : "LAL", "Memphis":"MEM", "Miami":"MIA", "Minnesota":"MIN", "New Orleans": "NOP", "New York":"NYK", "Oklahoma City" : "OKC", "Orlando" : "ORL", "Philadelphia": "PHI", "Phoenix" : "PHX" , "Portland":"POR" , "Sacramento" : "SAC", "San Antonio": "SAS" , "Toronto":"TOR" , "Utah" : "UTA", "Washington" : "WAS"}
