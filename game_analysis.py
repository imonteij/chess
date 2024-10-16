from chessdotcom import *
import stockfish
import requests
import json
from io import StringIO
import chess
import chess.pgn
import chess.engine

def get_player_games(username, header):
    win_code = ['win']
    draw_code = ['agreed', 'repetition', 'stalemate', 'insufficient', 
                 '50move', 'timevsinsufficient']
    lose_code = ['checkmated', 'timeout', 'resigned', 'lose', 
                 'abandoned', 'kingofthehill', 'threecheck', 'bughousepartnerlose']

    engine = chess.engine.SimpleEngine.popen_uci("stockfish/stockfish-windows-x86-64-avx2.exe")
    game_count = 1
    all_games_data = []  # Store all game data here

    player_games = get_player_game_archives(username, 0).json
    print(player_games)
    print(len(player_games['archives']))

    for i in range(len(player_games['archives'])):
        url = player_games['archives'][i]
        try:
            game = requests.get(url, headers=header).json()
        except Exception as e:
            print(f"Error fetching game archive from {url}: {e}")
            continue  # Skip this archive and move to the next one

        for item in game['games']:
            try:
                game_data = {}  # Data for the current game

                # Determine which side the player was
                side = 'white' if item['white']['username'] == username else 'black'
                time_format = item['time_class']
                time_control = item['time_control']
                opening = item['eco']
                result = item[side]['result']
                pgn = item['pgn']

                print(f"Game: {game_count} | {side} | {time_format} | {opening} | {result}")

                # Store the game metadata
                game_data['game_count'] = game_count
                game_data['side'] = side
                game_data['time_format'] = time_format
                game_data['time_control'] = time_control
                game_data['opening'] = opening
                game_data['pgn'] = pgn
                game_data['result'] = result
                game_data['move_evaluations'] = []  # Store move evaluations here

                # Parse and evaluate the moves if PGN exists
                pgn_content = item.get('pgn', "NA")
                if pgn_content != "NA":
                    temp_board = chess.Board() 
                    pgn = StringIO(pgn_content)
                    pgn_board = chess.pgn.read_game(pgn)

                    # Evaluate each move in the game
                    for move in pgn_board.mainline_moves():
                        temp_board.push(move)
                        eval_time = 0.001
                        engine_depth = 20
                        evaluation = engine.analyse(temp_board, chess.engine.Limit(time=eval_time))

                        # Append the evaluation to the move list
                        game_data['move_evaluations'].append(
                            evaluation['score'].relative.score(mate_score=10000)
                        )

                # Add the game data to the overall list of games
                all_games_data.append(game_data)
                game_count += 1

            except Exception as e:
                print(f"Error processing game {game_count}: {e}")
                continue  # Skip this game and move to the next one

    # Write all collected game data to game_eval.json
    with open("game_eval.json", 'w', encoding='utf-8') as f:
        json.dump(
            all_games_data, f, ensure_ascii=False, separators=(',', ': '), indent=0
        )

    engine.quit()
