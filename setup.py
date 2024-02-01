import json
import sys

from src.config import STOCKFISH, load_config

if len(sys.argv) < 2:
    print("No command provided")
    exit(1)

command = sys.argv[1]
tokens = sys.argv[2:]
config = load_config()
if command == "uci":
    if len(tokens) < 2:
        print("Not enough tokens provided")
        exit(2)
    config[tokens[0]] = tokens[1]

if command == "stockfish":
    if len(tokens) < 1:
        print("Not enough tokens provided")
        exit(3)
    config[STOCKFISH] = tokens[0]

f = open("config.json", "w")
f.write(json.dumps(config))
f.close()
