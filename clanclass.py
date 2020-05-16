# A module containing a class with all its methods and describing a clan.
import numpy as np


class CRClan:
    """Class describing the clan."""

    def __init__(self, title):
        """
        initialization of a dictionary containing all clan members
        and information about them.
        """
        self.members = dict()  # Dict with all players and their statistics
        self.saved = 0  # Save-flag (0 - not saved, 1 - saved)
        self.title = title  # The name of the clan
        self.save_time = None  # Last save time

    def is_not_used(self):
        """PEP-8 cost."""
        pass

    def change_name(self):
        """Change the clan name."""
        self.title = input('Enter the new clan name.')

    def remove_member(self):
        """Remove member from the list."""
        member = input("Enter a removing member's nickname: ")

        if member == 'menu':
            return
        try:
            del self.members[member]
        except KeyError:
            print('Player not found.Try again.')
            self.remove_member()

    def add_member(self):
        """Add new member in the list."""
        member = input("Enter a new member's nickname: ")

        if member == 'menu':
            return
        if member in self.members:
            print('You have already added a player with this name.')
            return
        self.members[member] = {
            'War day results': np.array([]),
            'Collection day results': np.array([]),
            'Longest win streak': 0,
            'Current win streak': 0,
        }

    def update_win_streaks(self, member, result):
        """
        Updates the longest and current win streaks of selected member
        depending on the last War day result.
        """
        self.is_not_used()  # PEP-8 cost

        if result == '0':
            member['Current win streak'] = 0
        else:
            member['Current win streak'] += int(result)
            if int(member['Current win streak']) > int(
                   member['Longest win streak']):
                member['Longest win streak'] = member['Current win streak']

    def set_war_day_result(self, member):
        """Sets War day result of the selected player."""
        active_wd = True
        while active_wd:
            result = input('\nChoose War day result of {0}\n'
                           '(0-lose, 1-win, 2-double win, 3-pass).'
                           '\n'.format(member))

            if result == 'menu':
                return True
            elif result == '3':
                active_wd = False
            elif result in ('0', '1', '2'):
                self.members[member]['War day results'] = \
                    np.append(self.members[member]['War day results'],
                              int(result))
                self.update_win_streaks(self.members[member], result)
                active_wd = False
            else:
                print('Invalid result, try again.')
        return False

    def set_collection_day_result(self, member):
        """Sets Collection day result of the selected player."""
        active_cd = True
        while active_cd:
            result = input('\nChoose Collection day result of {}\n'
                           '(number of collected cards).\n'.format(member))

            if result == 'menu':
                return True
            elif result.isdigit() and (int(result) > 0) and (
                    int(result) % 1 == 0):
                self.members[member]['Collection day results'] = \
                    np.append(self.members[member]['Collection day results'],
                              int(result))
                active_cd = False
            else:
                print('Invalid result, try again.')
        return False

    def save_war_result(self):
        """Save war result for all the players."""
        if len(self.members) == 0:
            print('Your members list is empty.')
            return

        # The flag variable, when set to True, will terminate the loop
        # if the user wants to go to the menu.
        for member in self.members:
            flag = self.set_war_day_result(member)
            if flag:
                return
            flag = self.set_collection_day_result(member)
            if flag:
                return

    def get_members_list(self):
        """
        Displays the nickname of each member in the clan
        and the total number of members.
        """
        for member in self.members:
            print(member)
        print('Total number of members: {}.'.format(len(self.members)))

    def get_loss_streak(self, member):
        """Gets the loss streak of the selected member."""
        self.is_not_used()  # PEP-8 cost

        ls = 0
        for i in member['War day results'][::-1]:
            if i == 0:
                ls += 1
            else:
                break
        return ls

    def get_member_info(self):
        """Displays information about the selected member."""
        member = input('Enter the nickname of the member: ')

        if member == 'menu':
            return
        # Reducing the size.
        try:
            member = self.members[member]
        except KeyError:
            print('Player not found.Try again.')
            return self.get_member_info()
        else:
            wd_results = member['War day results']
            cd_results = member['Collection day results']

        # The number of occurrences of unique elements in the list (np. array),
        # in this case [0, 1, 2],
        # variants of the results of the War Day.
        unique_elemnts_number = np.unique(wd_results, return_counts=True)[1]

        if len(wd_results) == 0:
            print("You haven't saved any war results with this player yet.")
            return

        # Next, we split the "print" function into several separate ones using
        # the try-expect construction. This is necessary in order
        # to avoid IndexError, which appears if the player has not had a single
        # win/loss/double win, i.e. the history of his results does not include
        # at least once all possible options.

        try:
            print('Wars played:',
                  str(len(wd_results) + unique_elemnts_number[2]))
        except IndexError:
            print('Wars played:', str(len(wd_results)))

        print('Wins:', str(int(wd_results.sum())))

        try:
            if 0 in np.unique(wd_results, return_counts=True)[0]:
                print('Loses:', str(unique_elemnts_number[0]))
            else:
                print('Loses: 0')
        except IndexError:
            print('Loses: 0')

        print('Average Cards on Collection day:', str(int(cd_results.mean())))

        try:
            print('Win Rate:',
                  str(round(wd_results.sum() /
                      (len(wd_results) + unique_elemnts_number[2]), 2)))
        except IndexError:
            print('Win Rate:',
                  str(round(wd_results.sum()/len(wd_results), 2)))

        print('Longest win streak:', member['Longest win streak'],
              '\nCurrent win streak:', member['Current win streak'],
              '\nCurrent loss streak:', str(self.get_loss_streak(member)),
              '\nLast results(1-Win, 2-DoubleWin, 0-Loss):',
              int(*wd_results[-7:])
              )

    def show_average_data(self):
        """Displays average data about the entire clan."""
        mb = self.members  # reducing the size

        # We do not use information from players
        # who have not played a single war.
        removing = []
        for member in mb:
            if len(mb[member]['War day results']) == 0:
                removing.append(member)
        for i in removing:
            del mb[i]

        if len(mb) == 0:
            print("You haven't added any clan members yet.")
            return

        # Next, we split the "print" function into several separate ones using
        # the try-expect construction. This is necessary in order
        # to avoid IndexError, which appears if the player has not had a single
        # win/loss/double win, i.e. the history of his results does not include
        # at least once all possible options.

        wars_played = np.array([])
        for i in mb:
            try:
                value = len(mb[i]['War day results']) + \
                        np.unique(mb[i]['War day results'],
                                  return_counts=True)[1][2]
            except IndexError:
                value = len(mb[i]['War day results'])
            wars_played = np.append(wars_played, value)
        print("Average 'Wars Played':", str(wars_played.mean()))

        print("Average 'Wins':",
              str(np.array([mb[i]['War day results'].sum()
                            for i in mb]).mean()))

        try:
            print("Average 'Loses':",
                  str(np.array([np.unique(mb[i]['War day results'],
                                          return_counts=True)[1][0]
                                if (0 in np.unique(mb[i]['War day results'],
                                                   return_counts=True))
                                else 0 for i in mb]).mean()))
        except IndexError:
            print("Average 'Loses': 0")

        print("Average 'Cards on Collection day':",
              str(np.array([mb[i]['Collection day results'].mean()
                            for i in mb]).mean()))

        win_rate = np.array([])
        for i in mb:
            try:
                wr = mb[i]['War day results'].sum() / \
                     (len(mb[i]['War day results']) +
                      np.unique(mb[i]['War day results'],
                                return_counts=True)[1][2])
            except IndexError:
                wr = mb[i]['War day results'].sum() / \
                     len(mb[i]['War day results'])
            win_rate = np.append(win_rate, wr)
        print("Average 'Win Rate':", str(win_rate.mean()))

        print("Average 'Longest win streak':",
              str(np.array([mb[i]['Longest win streak']
                            for i in mb]).mean()),
              "\nAverage 'Current win streak':",
              str(np.array([mb[i]['Current win streak']
                            for i in mb]).mean()),
              "\nAverage 'Current loss streak':",
              str(np.array([self.get_loss_streak(mb[i]) for i in mb]).mean())
              )

    def change_wd_result(self, member):
        """Changes the result of the war day for one player."""
        mb = self.members  # reducing the size

        # The block is triggered if the chronology of results
        # on the war day is empty for the player.
        if len(mb[member]['War day results']) == 0:
            print(f'The player with the nickname {member} did not '
                  f'\nparticipate in the last War day.')
            return

        active_wd = True
        while active_wd:
            result = input('\nChoose War day result of {0}\n'
                           '(0-lose, 1-win, 2-double win, 3-pass).'
                           '\n'.format(member))

            if result == 'menu':
                return True
            elif result == '3':
                mb[member]['War day results'] = np.delete(
                    mb[member]['War day results'], -1)
                active_wd = False
            elif result in ('0', '1', '2'):
                mb[member]['War day results'][-1] = int(result)
                self.update_win_streaks(mb[member], result)
                active_wd = False
            else:
                print('Invalid result, try again.')
        return False

    def change_cd_result(self, member):
        """Changes the result of the collection day for one player."""
        mb = self.members  # reducing the size

        # The block is triggered if the chronology of results
        # on the collection day is empty for the player.
        if len(mb[member]['War day results']) == 0:
            print(f'The player with the nickname {member} did not '
                  f'\nparticipate in the last Collection day.')
            return False

        active_cd = True
        while active_cd:
            result = input('\nChoose Collection day result of {}\n'
                           '(number of collected cards).\n'.format(member))

            if result == 'menu':
                return True
            elif result.isdigit() and (int(result) > 0) and (
                    int(result) % 1 == 0):
                mb[member]['Collection day results'][-1] = int(result)
                active_cd = False
            else:
                print('Invalid result, try again.')
        return False

    def change_war_results(self):
        """Changes the results of the last war."""
        mb = self.members  # reducing the size

        if len(mb) == 0:
            print('Your members list is empty.')
            return False

        # If there are no players who have played at least one war,
        # the function will stop running and notify us about it.
        flag = False
        for i in mb:
            if len(mb[i]['War day results']) == 0:
                continue
            flag = True
        if not flag:
            print("You haven't saved any war results yet.")
            return

        choise = input("Do you want to change the results of the war for all"
                       "\nplayers or for one? To change the results for all"
                       "\nplayers ,enter !all. To change the result for a"
                       "\nplayer, enter his nickname.")

        # The flag variable, when set to True, will terminate the loop
        # if the user wants to go to the menu.
        if choise == 'menu':
            return
        if choise == '!all':
            for i in mb:
                flag = self.change_wd_result(i)
                if flag:
                    return
                flag = self.change_cd_result(i)
                if flag:
                    return
        elif choise in mb:
            flag = self.change_wd_result(choise)
            if flag:
                return
            self.change_cd_result(choise)
        else:
            print('Player not found.')
