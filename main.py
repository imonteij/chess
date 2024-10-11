from chessdotcom import *
import pprint
import requests
import json

printer = pprint.PrettyPrinter()
Client.request_config["headers"]["User-Agent"] = (
   "Exploring chessdotcom api"
   "Contact me at jovan@monteij.com"
)

def print_leaderboards():
    leaderboard_data = get_leaderboards().json
    categories = leaderboard_data.keys()



def get_player_ratings(username,tts=0):
    player_data = get_player_stats(username).json
    #categories = player_data.keys()
    #print(categories)
    formats = ['chess_blitz', 'chess_rapid', 'chess_bullet']
    for format in formats:
        print(format,f': {player_data["stats"][format]["last"]["rating"]}')
get_player_ratings('imonteij')
#printer.pprint(get_player_stats('imonteij').json)
