#!/bin/bash
# bash script to capture stderr, stdout from debug_GPT_Black-checkmate_Elo1800.py
source ~/.local/gptchess/bin/activate

OPENAI_API_KEY=$(cat ~/.local/gptchess/chess_gpt_eval/gpt_inputs/api_key.txt); export OPENAI_API_KEY
pushd ~/.local/gptchess/skynet-dev/GPT_Black
~/.local/gptchess/bin/python debug_GPT_Black-checkmate_Elo1800.py 2>checkmate_Elo1800.stderr |tee checkmate_Elo1800.stdout


