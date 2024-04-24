import chess
import chess.engine
import chess.pgn
from data_extractor import ChessDataExtractor
from datetime import datetime
import io

class ChessDataAnalyser(ChessDataExtractor):
    def __init__(self, username, password):
        super().__init__(username, password)
    
    def extract_and_process_data(self, game_type: str) -> list[str]:
        filtered_games = self.extract_games_by_type(game_type)
        pgn_text_list = self.extract_pgn(filtered_games)
        return pgn_text_list
    
    def parse_pgn(self, pgn_text_list):
        game_data = []
        move_data = []
        for pgn_text in pgn_text_list:
            pgn = io.StringIO(pgn_text)
            game = chess.pgn.read_game(pgn)

            # Extract game-level data
            game_data.append({
                "Game ID": game.headers["Link"].split("/")[-1],
                "Date": game.headers.get("Date"),
                "Start Time": game.headers.get("UTCTime"),
                "End Time": game.headers.get("EndTime"),
                "White Player": game.headers.get("White"),
                "Black Player": game.headers.get("Black"),
                "White Player ELO(After game)": game.headers.get("WhiteElo"),
                "Black Player ELO(After game)": game.headers.get("BlackElo"),
                "Final Position(FEN)": game.headers.get("CurrentPosition"),
                "Opening Name": game.headers.get("ECOUrl").split("/")[-1] if game.headers.get("ECOUrl") else None,
                "ECO": game.headers.get("ECO"),
                "ECO url": game.headers.get("ECOUrl"),
                "Time Control": game.headers.get("TimeControl"),
                "Winner": game.headers.get("Result"),
                "I Won": True if game.headers.get("White") == "CheyDB" and game.headers.get("Result") == "1-0" or game.headers.get("Black") == "CheyDB" and game.headers.get("Result") == "0-1" else False,
                "Result": game.headers.get("Result"),
                "Termination": game.headers.get("Termination"),
                "Total Time Spent": str(datetime.strptime(game.headers.get("EndTime"), '%H:%M:%S') - datetime.strptime(game.headers.get("UTCTime"), '%H:%M:%S')),
                "Game Link": game.headers.get("Link")
            })
            
            
            # Extract move-level data
            move_number = 1
            board = chess.Board()
            for move in game.mainline_moves():
                # best_move = stockfish.get_best_move() if move_number > 1 else None
                san = board.san(move)
                is_capture = board.is_capture(move)
                board.push(move)
                fen_after = board.fen()
                # stockfish_fen_position = stockfish.set_fen_position(fen_after)
                # board_eval_after_move = stockfish.get_evaluation()

                move_data.append({
                    "Game ID": game.headers["Link"].split("/")[-1],
                    "Move Number": (move_number),
                    "Move": move.uci(),
                    "San": san,
                    "Move Colour": "White" if board.turn == chess.BLACK else "Black",  # Color is based on turn after move
                    "Piece Moved": board.piece_at(move.to_square),
                    "Starting Square": chess.square_name(move.from_square),
                    "Ending Square": chess.square_name(move.to_square),
                    "FEN After Move": fen_after,
                    # "Best Move": best_move,
                    # "Board Eval After Move(type)": board_eval_after_move['type'],
                    # "Board Eval After Move(type)": board_eval_after_move['value'],
                    "Capture": is_capture,
                    "Check": board.is_check(),
                    "Checkmate": board.is_checkmate(),
                    "Promotion": bool(move.promotion)
                })
            
                # Update move number
                if board.turn == chess.WHITE:
                    move_number += 1

        return game_data, move_data
        
