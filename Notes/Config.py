import configparser


def getDefaultEditor():
    # Load the config
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Access the values
    return str(config['settings']['DEFAULT_EDITOR'])

