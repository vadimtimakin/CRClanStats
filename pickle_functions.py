# Module for saving and loading data about the clan.
import pickle
from time import gmtime, strftime

from clanclass import CRClan


def show_manual():
    """Displays Instructions and descriptions."""
    try:
        with open('manual_and_description.txt', 'r') as file:
            text = file.read()
    except FileNotFoundError:
        print('There were problems displaying the file. Make sure',
              '\nthat you have downloaded the file manual_and_description.txt')
    else:
        print(text)


def load_data():
    """Loads data from pickle file."""
    with open('data.pickle', 'rb') as file:
        clan = pickle.load(file)
    return clan


def save_data(clan):
    """Saves data to pickle file."""
    clan.save_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    with open('data.pickle', 'wb') as file:
        pickle.dump(clan, file)
    clan.saved = 1

    print('The data was saved successfully.')
    print(clan.save_time)


def create_clan():
    """Creates or loads clan data."""
    try:
        clan = load_data()
        print('Latest update:', clan.save_time)
    except FileNotFoundError:
        title = input('Enter the name of your clan:')
        clan = CRClan(title)
        print('\nA new instance of the clan was created.')
    except EOFError:
        title = input('Enter the name of your clan:')
        clan = CRClan(title)
        print('\nA new instance of the clan was created.')
    else:
        if isinstance(clan, CRClan):
            print('\nThe clan data was uploaded successfully.')
        else:
            title = input('Enter the name of your clan:')
            clan = CRClan(title)
            print('\nA new instance of the clan was created.')
    return clan
