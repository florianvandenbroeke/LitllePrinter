import toml


def update_settings(dict):
    with open("config.toml", "w") as file:
        toml.dump(dict, file)


def read_settings():
    with open("config.toml", "r") as file:
        return toml.load(file)

def getAPINinjasKey():
    return read_settings()["APINinjasKey"]

def getTriviaList():
    return read_settings()["triviaList"]