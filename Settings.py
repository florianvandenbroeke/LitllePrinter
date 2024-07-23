import toml


def update_settings(settings_dict):
    with open("/home/florianvdb/LitllePrinter/config.toml", "w") as file:
        toml.dump(settings_dict, file)


def read_settings():
    with open("/home/florianvdb/LitllePrinter/config.toml", "r") as file:
        return toml.load(file)


def getAPINinjasKey():
    return read_settings()["APINinjasKey"]


def getTriviaList():
    return read_settings()["triviaList"]


def getPrefList():
    return read_settings()["prefList"]


def getDebugMode():
    return read_settings()["debugMode"]