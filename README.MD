## Chess Engine Evaluator

### Setup

Set stockfish path:

`` py setup.py stockfish STOCKFISH_PATH``

Set uci engine path:

``py setup.py uci ENGINE_NAME ENGINE_PATH``

### Usage

Evaluate uci engine

``py evaluate.py ENGINE``

Play a match between two uci engines

``py play.py ENGINE1 ENGINE2 GAMES_PER_COLOR``

Play a match between uci engine and stockfish of elo

``py play_stockfish.py ENGINE STOCKFISH_ELO GAMES_PER_COLOR``

### Debug

Display uci messages: ``--verbose=uci``

Display board and clock: ``--verbose=board``

All of above: ``--verbose=full``

### Threading

Enable threading and set number of threads by flags:

``--threads=2``

``--threads=5``

``--threads=10``

### Evaluation length

Set number of games played in evaluation:

``--length=short``

``--length=medium``

``--length=long``

### Time Control

Set time control of games:

``--time=bullet``

``--time=blitz``

``--time=rapid``