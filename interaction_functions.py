# Module for interaction functions.
import sys

import pickle_functions as pf
from clanclass import CRClan


def start():
    """Displays a message when the program starts."""
    print('You are using CRClanStatic 1.0.\nMade by t0efL.')


def reset_data(clan):
    """Irretrievably resets the data about clan."""
    print("Are you sure you're going to delete all your data about the clan?")
    print("Youn won't be able to cancel this action.")
    item = input('Enter(y/n): ')

    if item == 'y':
        title = input('Enter the name of your clan:')
        clan = CRClan(title)
        print('All data has been successfully deleted.',
              '\nA new instance of the clan was created.',
              'Please note that to save the newly created clan and completely',
              'get rid \nof the old one',
              'you need to use the "Save changes" item in the menu.')
    elif item == 'menu':
        return
    else:
        print('canceled')
    return clan


def exit_program(clan):
    """Closes the program, but first notifies if the data is not saved."""
    if clan.saved == 0:
        flag = input('Please note that you have not saved your clan data.'
                     ' Are you sure you want to get out?(y/n)')
        if flag == 'y':
            sys.exit()
        else:
            return
    else:
        sys.exit()


def check_item(clan):
    """Checks the action selected by the user."""
    item = input('Enter: ')
    print()

    if item == '0':
        pf.show_manual()
    elif item == '1':
        clan.add_member()
    elif item == '2':
        clan.remove_member()
    elif item == '3':
        clan.save_war_result()
    elif item == '4':
        clan.get_member_info()
    elif item == '5':
        clan.show_average_data()
    elif item == '6':
        clan.get_members_list()
    elif item == '7':
        clan.change_war_results()
    elif item == '8':
        pf.save_data(clan)
    elif item == '9':
        clan = reset_data(clan)
    elif item == '10':
        clan.change_name()
    elif item == '11':
        exit_program(clan)
    else:
        print('Invalid value. Try again.')
        check_item(clan)
    return clan


def main_menu(clan):
    """Displays the main menu of the program."""
    print('\n--- Main Menu ---')
    print('0)Instruction manual and description.',
          '\n1)Add new Member.',
          '\n2)Remove member.',
          '\n3)Save War results.',
          '\n4)Get information about the selected member.',
          '\n5)Get average data about the entire clan.',
          '\n6)Get members list.',
          '\n7)Change last war results.',
          '\n8)Save changes.',
          '\n9)Reset Data.',
          '\n10)Change the clan name.',
          '\n11)Quit.')

    clan = check_item(clan)
    main_menu(clan)
