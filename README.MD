## Chess Engine Evaluator

Tools to test uci chess engines

### Features

- Automatic puzzle solving
- Evaluating engine strength
- Playing matches between engines
- Playing matches against stockfish

### Setup

- Set stockfish path:
  `` py setup.py stockfish STOCKFISH_PATH``
- Set uci engine path:
  ``py setup.py uci ENGINE_NAME ENGINE_PATH``
- Download puzzles:
  ``py setup.py puzzles``

### Usage

- Evaluate uci engine
  ``py evaluate.py ENGINE``

- Play a match between two uci engines
  ``py play.py ENGINE1 ENGINE2 GAMES_PER_COLOR``

- Play a match between uci engine and stockfish
  ``py play_stockfish.py ENGINE STOCKFISH_ELO GAMES_PER_COLOR``

- Solve puzzles with engine:
  ``py solve.py ENGINE PUZZLES_COUNT``

### Flags:

- #### Debug

    - Display uci messages: ``--verbose=uci``

    - Display board and clock: ``--verbose=board``

    - Both of above: ``--verbose=full``

- #### Threading

  Enable threading and set number of threads by flags:

    - ``--threads=2``

    - ``--threads=5``

    - ``--threads=10``

    - ``--threads=20``

- #### Evaluation length

  Set number of games played in evaluation:

    - 50 ``--length=short`` (DEFAULT)

    - 100 ``--length=medium``

    - 250 ``--length=long``

- #### Time Control

  Set time control of games:

    - 1 minute per game ``--time=bullet``

    - 5 minutes per game ``--time=blitz`` (DEFAULT)

    - 10 minutes per game ``--time=rapid``