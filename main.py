from data_analyser import ChessDataAnalyser

if __name__ == "__main__":
    analyser = ChessDataAnalyser("cheydb", "cheydb@rocketmail.com")
    pgn_text_list = analyser.extract_and_process_data("live")
    game_data, move_data = analyser.parse_pgn(pgn_text_list)
    
    print(len(game_data), len(move_data))
