from chessdotcom import *
import pprint
from game_analysis import get_player_games


username = 'imonteij'
header = {"User-Agent": "My-Application/1.0"}


printer = pprint.PrettyPrinter()
Client.request_config["headers"]["User-Agent"] = (
   "Exploring chessdotcom api"
   "Contact me at jovan@monteij.com"
)

def get_player_ratings(username):
    player_data = get_player_stats(username).json
    formats = ['chess_blitz', 'chess_rapid', 'chess_bullet']
    for format in formats:
        print(format,f': {player_data["stats"][format]["last"]["rating"]}')

get_player_ratings(username)
get_player_games(username, header)
print("DONE")