#!/usr/bin/env python3
# Original: "gpt-3.5-turbo-instruct via Stochastic parrot, <https://github.com/clevcode/skynet-dev>"
#+        @ch3cksout: re-write for gpt-3.5-turbo-instruct playing Black! 

from stockfish import Stockfish

import openai
import chess
import os

#+        @ch3cksout
import datetime
DT = datetime.datetime.now()

import time

# run this before calling: OPENAI_API_KEY=$(cat ~/.local/gptchess/chess_gpt_eval/gpt_inputs/api_key.txt); export OPENAI_API_KEY
#print(openai.api_key)

#+        @ch3cksout        ~loop~
Ngame = 32
for i in range(0, Ngame):        
        stockfish = Stockfish()
        #=        @ch3cksout
        elo_rating = 1800
        MinimumThinkingTime = 2000
        stockfish.set_elo_rating(elo_rating)

        #+        @ch3cksout
        stockfish.update_engine_parameters({"Minimum Thinking Time": MinimumThinkingTime}) 
        # Gets stockfish to use 'MinimumThinkingTime' ms (instead of the default 20)!
        # see: https://github.com/official-stockfish/Stockfish/pull/2225/files
        stockfish.update_engine_parameters({"Threads": 8}) 

        print("\n stockfish.get_stockfish_major_version():")
        print(stockfish.get_stockfish_major_version())

        print("\n stockfish.get_parameters():")
        print(stockfish.get_parameters())

        board = chess.Board(chess.STARTING_FEN)
        print(f"\tInitializing {i}. game\n\t 'stockfish.get_board_visual()':")
        print("\033c" + stockfish.get_board_visual())
        
        pgn = f"""[Event "Testing checkmate_Elo1800.py vs. Stockfish"]
[Site "localhost"]
[Date "{DT}"]
[Round "{i}"]
[White "Stockfish Elo:{elo_rating}, {MinimumThinkingTime} ms"]
[Black "gpt-3.5-turbo-instruct via Stochastic parrot, <https://github.com/clevcode/skynet-dev>"]
[Result "TBD"]
[WhiteElo "{elo_rating}"]
[BlackElo "TBD"]
[TimeControl "TBD"]
[Variant "Standard"]

1."""
#+        @ch3cksout
        print(f"Starting {i}. game\n\t Initial PGN:\n" + pgn +"\n")
        n = 1
#+        @ch3cksout: start with Stockfish as White
        stockfish.set_fen_position(chess.STARTING_FEN)
        
        uci_move = stockfish.get_best_move()
        move = chess.Move.from_uci(uci_move)
        san_move = board.san(move)
        board.push(move)
        pgn += f" {san_move}"

        stockfish.make_moves_from_current_position([f"{uci_move}"])
        print("\033c" + stockfish.get_board_visual())

        while True:
            response = openai.Completion.create(
                model="gpt-3.5-turbo-instruct",
                prompt=pgn,
                temperature=0,
                max_tokens=4,
            )
        
#+        @ch3cksout
            #print(f"\tOpenAI response:\n\t" + response.choices[0].text +"\n")
        
            san_move = response.choices[0].text.strip().split()[0]
            uci_move = board.push_san(san_move).uci()
            pgn += f" {san_move}"

            stockfish.make_moves_from_current_position([f"{uci_move}"])

            #+        @ch3cksout
            print(f" {n}. move")

            print("\033c" + stockfish.get_board_visual())

            if board.is_checkmate():
                print(pgn)
                print("{GPT-3.5 won as Black!}")
                break

            if board.is_stalemate():
                print(pgn)
                print("{Draw!}")
                break

            uci_move = stockfish.get_best_move()
            move = chess.Move.from_uci(uci_move)
            san_move = board.san(move)
            board.push(move)
            n += 1
            pgn += f" {n}."
            pgn += f" {san_move}"

            stockfish.make_moves_from_current_position([f"{uci_move}"])
            print("\033c" + stockfish.get_board_visual())

            if board.is_checkmate():
                print(pgn)
                print("{Stockfish 1800 ELO won as White!}")
                break

            if board.is_stalemate():
                print(pgn)
                print("{Draw!}")
                break

            print(f"\n\twaiting before {n}. move...\n")


        print(f"\tLatest 'san_move':\n\t{san_move}\n")

        print(f"\tLatest 'uci_move':\n\t{uci_move}\n")

        print(f"\nFinished {i}. game\n")
        time.sleep(i+0.1) # throttle OpenAI requests, to avoid getting blocked

