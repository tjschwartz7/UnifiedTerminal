import configparser


def getEmergencySavingsBuffer():
    # Load the config
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Access the values
    return float(config['settings']['EMERGENCY_SAVINGS_BUFFER'])

def getEmergencySavingMonths():
    # Load the config
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Access the values
    return float(config['settings']['EMERGENCY_SAVINGS_MONTHS'])

def getEmergencyRentPercentage():
    # Load the config
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Access the values
    return float(config['settings']['SUGGESTED_RENT_PERCENTAGE'])

def getEmergencySavingsPerMonth():
    # Load the config
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Access the values
    return float(config['settings']['SUGGESTED_SAVINGS_PER_MONTH'])



