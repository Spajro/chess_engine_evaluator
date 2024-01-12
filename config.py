import json
import os.path
import sys

STOCKFISH = "stockfish"


def get_path(engine_name: str) -> str | None:
    config = __load_config()
    return config[engine_name]


def __load_config() -> dict:
    if not os.path.exists("config.json"):
        return dict()
    f = open("config.json", "r")
    json_config = f.read()
    f.close()
    return json.loads(json_config)


def __cli():
    if len(sys.argv) < 2:
        print("No command provided")
        exit(1)

    command = sys.argv[1]
    tokens = sys.argv[2:]
    config = __load_config()
    if command == "set_uci":
        if len(tokens) < 2:
            print("Not enough tokens provided")
            exit(2)
        config[tokens[0]] = tokens[1]

    if command == "set_stock":
        if len(tokens) < 1:
            print("Not enough tokens provided")
            exit(3)
        config[STOCKFISH] = tokens[0]

    f = open("config.json", "w")
    f.write(json.dumps(config))
    f.close()


if __name__ == "__main__":
    __cli()
