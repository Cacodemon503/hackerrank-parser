#!/usr/bin/python3
#----------------------------------------------------------#
import sys
import os
import time
import requests
import csv
import pathlib
import threading


#----------------------------------------------------------#
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
#----------------------------------------------------------#


#----------------------------------------------------------#
#-------------------------MENU-----------------------------#
#----------------------------------------------------------#

# MAIN MENU:


def main_menu():
    try:
        os.system('cls')
        print('''{red}
                  ─────█─▄▀█──█▀▄─█─────
                  ────▐▌──────────▐▌────
                  ────█▌▀▄──▄▄──▄▀▐█────
                  ───▐██──▀▀──▀▀──██▌───
                  ──▄████▄──▐▌──▄████▄── {endcolor} \n'''.format(red='\033[31m', endcolor='\033[0m'))
        print('          {yellow}#---HackerRank LEADERBOARDS PARSER---#{endcolor} \n'.format(
            yellow='\033[93m', endcolor='\033[0m'))
        print('Please choose the type:')
        print(':c [contests]')
        print(':p [practice]')

        print(':q [QUIT] \n')
        choice = input('>>>  ')
        executor(choice)
        return
    except KeyboardInterrupt:
        kill()

# EXECUTOR:


def executor(choice):
    option = choice.lower().strip(' ')
    if option == '':
        main_menu()
    else:
        try:
            menu_actions[option]()
        except KeyError:
            os.system('cls')
            print('Invalid selection, new try in 1 sec. \n')
            time.sleep(1)
            main_menu()
    return

# CONTESTS MENU:


def contests_menu():
    os.system('cls')
    print('#----------CONTESTS----------# \n')
    print('-cal [Algorithms]')
    print('-cmath [Mathematics]')
    print('-cfun [Functional Programming]')
    print('-cai [Artificial Intelligence]')
    print('#----------------------------#')
    print('../ [Back]')
    print(':q [Quit]')
    print('#----------------------------# \n')
    choice = input('>>> ')
    executor(choice)
    return

# PRACTICE MENU:


def practice_menu():
    os.system('cls')
    print('#----------PRACTICE----------# \n')
    print('-pal [Algorithms]')
    print('-pmath [Mathematics]')
    print('-cpp [C++]')
    print('-py [Python]')
    print('-sql [SQL]')
    print('-dist [Distributed Systems]')
    print('-pfun [Functional Programming]')
    print('-data [Data Structures]')
    print('-pai [Artificial Intelligence]')
    print('-jar [Java]')
    print('-rb [Ruby]')
    print('-db [Databases]')
    print('-sh [Linux Shell]')
    print('-sec [Security]')
    print('#----------------------------#')
    print('../ [Back]')
    print(':q [Quit]')
    print('#----------------------------# \n')
    choice = input(">>> ")
    executor(choice)
    return

# BACK FUNCTION:


def back():
    main_menu()

# EXIT FUNCTION:


def exit():
    os.system('cls')
    sys.exit()
#----------------------------------------------------------#
#----------------------------------------------------------#

#----------------------------------------------------------#
#----------------------KNOW LIMIT--------------------------#
#----------------------------------------------------------#


def know_limit(filter, location, choice, _type_):
    try:
        data = requests.get('https://www.hackerrank.com/rest/contests/master/tracks/' + str(choice)
                            + '/leaderboard' + filter + '?type=' +
                            str(_type_) + '&offset=0&limit=1&level=1' + location,
                            headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36'})
        print('\nLeaderboard contains: ' + str(data.json()['total']) + ' users \n')
    except(requests.exceptions.ConnectionError):
        os.system('cls')
        yellow = '\033[93m'
        endcolor = '\033[0m'
        print(f'{yellow}Check internet connection ...{endcolor}')
        time.sleep(2)
        if _type_ == 'practice':
            practice_menu()
        elif _type_ == 'contest':
            contests_menu()
#----------------------------------------------------------#
#----------------------------------------------------------#

#----------------------------------------------------------#
#---------------------LEADERBOARDS-------------------------#
#----------------------------------------------------------#


def leaderboard(filter, location, choice, _type_, offset_limit):
    try:
        stop_threads = False
        t1 = threading.Thread(target=animation, args=(lambda: stop_threads, ))
        t1.start()
        offset = 0
        data = requests.get('https://www.hackerrank.com/rest/contests/master/tracks/' + str(choice)
                            + '/leaderboard' + filter + '?type=' +
                            str(_type_) + '&offset=' + str(offset) +
                            '&limit=100&level=1' + location,
                            headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36'})
        lst.extend(data.json()['models'])
        while offset < int(offset_limit):
            # while data.json()['models']) <--- GET ALL
            offset = offset + 100
            data = requests.get('https://www.hackerrank.com/rest/contests/master/tracks/' + str(choice)
                                + '/leaderboard' + filter + '?type=' +
                                str(_type_) + '&offset=' + str(offset) +
                                '&limit=100&level=1' + location,
                                headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36'})
            lst.extend(data.json()['models'])
        stop_threads = True
        t1.join()
        git_status(lst)
    except(requests.exceptions.ConnectionError):
        stop_threads = True
        t1.join()
        yellow = '\033[93m'
        endcolor = '\033[0m'
        print(f'{yellow}Check internet connection ...{endcolor}')
        time.sleep(2)
        if _type_ == 'practice':
            practice_menu()
        elif _type_ == 'contest':
            contests_menu()

    except ValueError:
        stop_threads = True
        t1.join()
        red = '\033[31m'
        yellow = '\033[93m'
        endcolor = '\033[0m'
        print(f'{red}INVALID INPUT:{endcolor} {yellow}Non-numeric data found in the offset limit{endcolor}')
        time.sleep(2)
        sys.stdout.write("\033[F")
        sys.stdout.write("\033[K")
        print('Redirecting to main menu ...')
        time.sleep(4)
        del lst[:]
        main_menu()

    except KeyboardInterrupt:
        stop_threads = True
        t1.join()
        print('Program killed by user')
        time.sleep(0.5)
        os.system('cls')
        sys.exit()
#----------------------------------------------------------#
#--------------------GIT CHECK STATUS----------------------#
#----------------------------------------------------------#


def git_status(lst):
    os.system('cls')

    print('Collected: '
          + str(len(lst)) + ' users \n')
    print('Check these users for GitHub accounts?')
    print('[y]/[n]')
    print('#-----------------#')
    print('[../] to main menu \n')
    user_answer = input('>>> ')
    git_check_status = user_answer.lower().strip(' ')

    if git_check_status == 'y':
        git_checker(lst, git_check_status)

    elif git_check_status == 'n':
        csvwriter(lst, git_check_status)

    elif git_check_status == '../':
        del lst[:]
        main_menu()

    else:
        os.system('cls')
        git_status(lst)
#----------------------------------------------------------#
#----------------------------------------------------------#

#----------------------------------------------------------#
#----------------------GIT CHECKER-------------------------#
#----------------------------------------------------------#


def git_checker(lst, git_check_status):
    try:
        os.system('cls')
        git_names = []
        git_emails = []
        print('Press [ENTER] to start\n')
        print('#---------------------------------#')
        print('print [help] for guide')
        print('print [limits] to check your token')
        print('print [setup] to setup your token')
        print('print [../] to change your choice')
        print('#---------------------------------#\n')
        user_input = input('>>> ').lower().strip(' ')
        os.system('cls')

        if user_input == '../':
            git_status(lst)

        elif user_input == 'help':
            helper(lst, git_check_status)

        elif user_input == 'limits':
            limits(lst, git_check_status)

        elif user_input == 'setup':
            auth(lst, git_check_status)
        else:
            try:
                stop_threads = False
                t1 = threading.Thread(target=animation_2, args=(lambda: stop_threads, ))
                t1.start()
                for i in lst:
                    f = open(resource_path('token.txt'), "r")
                    token = f.read()
                    headers = {'Authorization': 'token ' + str(token)}
                    URL = 'https://api.github.com/users/' + i['hacker']
                    r = requests.get(url=URL, headers=headers)
                    git_api_data = r.json()
                    headers_info = r.headers

                    if headers_info['Status'] == "200 OK":
                        git_names.append(git_api_data['login'])
                        git_emails.append(git_api_data['email'])
                        status = 'OK'
                        api_warning(status)

                    elif headers_info['Status'] == '404 Not Found':
                        git_names.append('null')
                        git_emails.append('null')
                        status = 'OK'
                        api_warning(status)

                    elif headers_info['Status'] == '401 Unauthorized':
                        stop_threads = True
                        t1.join()
                        red = '\033[91m'
                        endcolor = '\033[0m'
                        print(f'{red}INVALID TOKEN{endcolor}')
                        time.sleep(2)
                        git_checker(lst, git_check_status)

                    elif headers_info['Status'] == '403 Forbidden':
                        git_names.append('API LIMITS EXCEEDED')
                        git_emails.append('API LIMITS EXCEEDED')
                        status = 'API RATE LIMITS EXCEEDED'
                        api_warning(status)

                for i, obj in enumerate(lst):
                    obj['github name'] = git_names[i]
                    obj['github email'] = git_emails[i]
                    users_amount = len(lst)

                stop_threads = True
                t1.join()

                answer = api_warning(status)
                print('API RATE LIMITS STATUS:', answer)
                print("Checked: " + str(users_amount) + " users")
                time.sleep(3.5)
                csvwriter(lst, git_check_status)
            except KeyboardInterrupt:
                os.system('cls')
                stop_threads = True
                t1.join()
                print('Program killed by user')
                time.sleep(0.5)
                os.system('cls')
                sys.exit()

    except(requests.exceptions.ConnectionError):
        stop_threads = True
        t1.join()
        yellow = '\033[93m'
        endcolor = '\033[0m'
        print(f'{yellow}Check internet connection ...{endcolor}')
        time.sleep(2)
        sys.stdout.write("\033[F")
        sys.stdout.write("\033[K")
        print('Another try in 2 sec ...')
        time.sleep(2)
        git_checker(lst, git_check_status)

    except FileNotFoundError:
        stop_threads = True
        t1.join()
        red = '\033[91m'
        yellow = '\033[93m'
        endcolor = '\033[0m'
        print(f'{red}AUTHENTICATION REQUIRED:{endcolor} {yellow}You have no token!{endcolor}')
        time.sleep(3)
        auth(lst, git_check_status)

    except KeyboardInterrupt:
        kill()
#----------------------------------------------------------#
#----------------------------------------------------------#


#----------------------------------------------------------#
#----------------------API STATUS--------------------------#
#----------------------------------------------------------#


def api_warning(status):
    r = '\033[31m'
    y = '\033[93m'
    g = '\033[32m'
    e = '\033[0m'
    if status == 'API RATE LIMITS EXCEEDED':
        answer = f'''{r}WARNING:{e} {y}API RATE LIMITS EXCEEDED{e}
Some users were not checked(see saved ".txt" file).\n'''
        return answer
    else:
        answer = f'{g}OK{e}'
        return answer
#----------------------------------------------------------#
#----------------------------------------------------------#


#----------------------------------------------------------#
#----------------------CSV WRITER--------------------------#
#----------------------------------------------------------#


def csvwriter(lst, git_check_status):
    try:
        os.system('cls')
        y = '\033[93m'
        e = '\033[0m'
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        print(f'{y}File will be saved at:{e}', base_path)
        p_choice = input(f'Set the path manualy? [y/n]: ').lower().strip(' ')

        if p_choice == 'y':
            file_path = input(f'{y}Set the path:{e} ').strip(' ')
        elif p_choice == 'n':
            file_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        else:
            csvwriter(lst, git_check_status)

        file_name = input(f'\n{y}Enter file name:{e} ')
        with open(f'{file_path}/{file_name}.txt', 'w', encoding='utf-8') as filename:
            os.system('cls')
            writer = None
            for i in lst:
                if git_check_status == 'y':
                    stdout = {'Username': i['hacker'], 'Location': i['country'],
                              'Profile link': 'https://www.hackerrank.com/' + i['hacker'],
                              'Github': 'https://www.github.com/' + i['github name'],
                              'Git email': i['github email']}
                    if not writer:
                        writer = csv.DictWriter(filename, delimiter=';', fieldnames=stdout.keys())
                    writer.writerow(stdout)
                else:
                    stdout = {'Username': i['hacker'], 'Location': i['country'],
                              'Profile link': 'https://www.hackerrank.com/' + i['hacker']}
                    if not writer:
                        writer = csv.DictWriter(filename, delimiter=';', fieldnames=stdout.keys())
                    writer.writerow(stdout)
            print(f'{y}File saved at:{e}', os.path.realpath(filename.name))
            time.sleep(2)
            os.system('cls')
            print('''{yellow}
          ▄████  ██▀███  ▄▄▄       ▄▄▄▄    ▄▄▄▄   ▓█████ ▓█████▄
          ██▒ ▀█▒▓██ ▒ ██▒████▄    ▓█████▄ ▓█████▄ ▓█   ▀ ▒██▀ ██▌
          ▒██░▄▄▄░▓██ ░▄█ ▒██  ▀█▄  ▒██▒ ▄██▒██▒ ▄██▒███   ░██   █▌
          ░▓█  ██▓▒██▀▀█▄ ░██▄▄▄▄██ ▒██░█▀  ▒██░█▀  ▒▓█  ▄ ░▓█▄   ▌
          ░▒▓███▀▒░██▓ ▒██▒▓█   ▓██▒░▓█  ▀█▓░▓█  ▀█▓░▒████▒░▒████▓
          ░▒   ▒ ░ ▒▓ ░▒▓░▒▒   ▓▒█░░▒▓███▀▒░▒▓███▀▒░░ ▒░ ░ ▒▒▓  ▒
          ░   ░   ░▒ ░ ▒░ ▒   ▒▒ ░▒░▒   ░ ▒░▒   ░  ░ ░  ░ ░ ▒  ▒
          ░ ░   ░   ░░   ░  ░   ▒    ░    ░  ░    ░    ░    ░ ░  ░
          ░    ░          ░  ░ ░       ░         ░  ░   ░
                                    ░       ░         ░
                  {endcolor}'''.format(yellow='\033[93m', endcolor='\033[0m'))
            print('                         {red}COLLECTED{endcolor} '.format(red='\033[31m', endcolor='\033[0m') + str(
                len(lst)) + ' {red}USERS{endcolor} \n'.format(red='\033[31m', endcolor='\033[0m'))
            print('                   #-----------------------------#')
            print('                             {yellow}PRESS ENTER{endcolor}'.format(
                yellow='\033[93m', endcolor='\033[0m'))
            print('                   #-----------------------------#')

        del lst[:]

        choice = input('').lower().strip(' ')
        if choice:
            main_menu()
        else:
            main_menu()
    except FileNotFoundError:
        print('\nERROR: I see no such directory')
        time.sleep(2)
        os.system('cls')
        csvwriter(lst, git_check_status)
    except PermissionError:
        print(
            '\nERROR: Due to OS settings, I have no permisson to write the file in the following directory')
        time.sleep(4)
        os.system('cls')
        csvwriter(lst, git_check_status)
#----------------------------------------------------------#
#----------------------------------------------------------#

#----------------------------------------------------------#
#---------------------TECHNOLOGIES-------------------------#
#----------------------------------------------------------#

#-----------------------EXECUTOR---------------------------#
#----------------------------------------------------------#


def tech_executor(choice, _type_):
    print('''
Choose the country: \n
Russia (CIS): [rus]
Belarus (CIS): [by]
Kazakhstan (CIS): [kz]
Armenia (CIS): [am]
Ukraine: [ua]
#---------------------#
Get all users: [all]''')
    country = input('>>> ').lower().strip(' ')

    # RUSSIAN USERS
    if country == 'rus':
        filter = str('/filter')
        location = str('&elo_version=true&country=Russian%20Federation')
        know_limit(filter, location, choice, _type_)
        print('Set the offset limit')
        print('#-------------------#')
        print('To learn about offset limit, print [help]')

        offset_limit = input('>>> ').lower().strip(' ')
        if offset_limit == '../':
            if _type_ == 'practice':
                practice_menu()
            elif _type_ == 'contest':
                contests_menu()
        elif offset_limit == ':q':
            sys.exit()
        elif offset_limit == 'help':
            os.system('cls')
            print('#-----------HELP----------# \n')
            print('0 == <= first 100 users \n')
            print('100 == <= 200 users \n')
            print('200 == <= 300 users \n')
            print('etc. \n')
            print('#-------------------------#')
            print('press ENTER to turn back')
            back = input('').lower().strip(' ')
            if back:
                if _type_ == 'practice':
                    practice_menu()
                elif _type_ == 'contest':
                    contests_menu()
            else:
                if _type_ == 'practice':
                    practice_menu()
                elif _type_ == 'contest':
                    contests_menu()
        else:
            os.system('cls')
            # print('Collecting users... ')
            leaderboard(filter, location, choice, _type_, offset_limit)
            # print(lst) -- PRINTS PRE-STDOUT

    # BELARUS USERS
    if country == 'by':
        filter = str('/filter')
        location = str('&elo_version=true&country=Belarus')
        know_limit(filter, location, choice, _type_)
        print('Set the offset limit')
        print('#-------------------#')
        print('To learn about offset limit, print [help]')

        offset_limit = input('>>> ').lower().strip(' ')
        if offset_limit == '../':
            if _type_ == 'practice':
                practice_menu()
            elif _type_ == 'contest':
                contests_menu()
        elif offset_limit == ':q':
            sys.exit()
        elif offset_limit == 'help':
            os.system('cls')
            print('#-----------HELP----------# \n')
            print('0 == <= first 100 users \n')
            print('100 == <= 200 users \n')
            print('200 == <= 300 users \n')
            print('etc. \n')
            print('#-------------------------#')
            print('press ENTER to turn back')
            back = input('').lower().strip(' ')
            if back:
                if _type_ == 'practice':
                    practice_menu()
                elif _type_ == 'contest':
                    contests_menu()
            else:
                if _type_ == 'practice':
                    practice_menu()
                elif _type_ == 'contest':
                    contests_menu()
        else:
            os.system('cls')
            # print('Collecting users... ')
            leaderboard(filter, location, choice, _type_, offset_limit)

    # UKRAINE USERS
    if country == 'ua':
        filter = str('/filter')
        location = str('&elo_version=true&country=Ukraine')
        know_limit(filter, location, choice, _type_)
        print('Set the offset limit')
        print('#-------------------#')
        print('To learn about offset limit, print [help]')

        offset_limit = input('>>> ').lower().strip(' ')
        if offset_limit == '../':
            if _type_ == 'practice':
                practice_menu()
            elif _type_ == 'contest':
                contests_menu()
        elif offset_limit == ':q':
            sys.exit()
        elif offset_limit == 'help':
            os.system('cls')
            print('#-----------HELP----------# \n')
            print('0 == <= first 100 users \n')
            print('100 == <= 200 users \n')
            print('200 == <= 300 users \n')
            print('etc. \n')
            print('#-------------------------#')
            print('press ENTER to turn back')
            back = input('').lower().strip(' ')
            if back:
                if _type_ == 'practice':
                    practice_menu()
                elif _type_ == 'contest':
                    contests_menu()
            else:
                if _type_ == 'practice':
                    practice_menu()
                elif _type_ == 'contest':
                    contests_menu()
        else:
            os.system('cls')
            # print('Collecting users... ')
            leaderboard(filter, location, choice, _type_, offset_limit)

    # ARMENIA USERS
    if country == 'am':
        filter = str('/filter')
        location = str('&elo_version=true&country=Armenia')
        know_limit(filter, location, choice, _type_)
        print('Set the offset limit')
        print('#-------------------#')
        print('To learn about offset limit, print [help]')

        offset_limit = input('>>> ').lower().strip(' ')
        if offset_limit == '../':
            if _type_ == 'practice':
                practice_menu()
            elif _type_ == 'contest':
                contests_menu()
        elif offset_limit == ':q':
            sys.exit()
        elif offset_limit == 'help':
            os.system('cls')
            print('#-----------HELP----------# \n')
            print('0 == <= first 100 users \n')
            print('100 == <= 200 users \n')
            print('200 == <= 300 users \n')
            print('etc. \n')
            print('#-------------------------#')
            print('press ENTER to turn back')
            back = input('').lower().strip(' ')
            if back:
                if _type_ == 'practice':
                    practice_menu()
                elif _type_ == 'contest':
                    contests_menu()
            else:
                if _type_ == 'practice':
                    practice_menu()
                elif _type_ == 'contest':
                    contests_menu()
        else:
            os.system('cls')
            # print('Collecting users... ')
            leaderboard(filter, location, choice, _type_, offset_limit)

    # KAZAKHSTAN USERS
    if country == 'kz':
        filter = str('/filter')
        location = str('&elo_version=true&country=Kazakhstan')
        know_limit(filter, location, choice, _type_)
        print('Set the offset limit')
        print('#-------------------#')
        print('To learn about offset limit, print [help]')

        offset_limit = input('>>> ').lower().strip(' ')
        if offset_limit == '../':
            if _type_ == 'practice':
                practice_menu()
            elif _type_ == 'contest':
                contests_menu()
        elif offset_limit == ':q':
            sys.exit()
        elif offset_limit == 'help':
            os.system('cls')
            print('#-----------HELP----------# \n')
            print('0 == <= first 100 users \n')
            print('100 == <= 200 users \n')
            print('200 == <= 300 users \n')
            print('etc. \n')
            print('#-------------------------#')
            print('press ENTER to turn back')
            back = input('').lower().strip(' ')
            if back:
                if _type_ == 'practice':
                    practice_menu()
                elif _type_ == 'contest':
                    contests_menu()
            else:
                if _type_ == 'practice':
                    practice_menu()
                elif _type_ == 'contest':
                    contests_menu()
        else:
            os.system('cls')
            # print('Collecting users... ')
            leaderboard(filter, location, choice, _type_, offset_limit)

    # ALL USERS
    elif country == 'all':
        filter = str('')
        location = str('&elo_version=true')
        know_limit(filter, location, choice, _type_)
        print('Set the offset limit')
        print('#-------------------#')
        print('To learn about offset limit, print [help]')

        offset_limit = input('>>> ').lower().strip(' ')
        if offset_limit == '../':
            if _type_ == 'practice':
                practice_menu()
            elif _type_ == 'contest':
                contests_menu()
        elif offset_limit == ':q':
            sys.exit()
        elif offset_limit == 'help':
            os.system('cls')
            print('#-----------HELP----------# \n')
            print('0 == <= first 100 users \n')
            print('100 == <= 200 users \n')
            print('200 == <= 300 users \n')
            print('etc. \n')
            print('#-------------------------#')
            print('press ENTER to turn back')
            back = input('').lower().strip(' ')
            if back:
                if _type_ == 'practice':
                    practice_menu()
                elif _type_ == 'contest':
                    contests_menu()
            else:
                if _type_ == 'practice':
                    practice_menu()
                elif _type_ == 'contest':
                    contests_menu()
        else:
            os.system('cls')
            # print('Collecting users... ')
            leaderboard(filter, location, choice, _type_, offset_limit)
            # print(lst) -- PRINTS PRE-STDOUT

    elif country == '../':
        if _type_ == 'practice':
            practice_menu()
        elif _type_ == 'contest':
            contests_menu()

    elif country == ':q':
        sys.exit()

    else:
        os.system('cls')
        print('Invalid selection, new try in 1 sec.')
        time.sleep(1)
        if _type_ == 'practice':
            practice_menu()
        elif _type_ == 'contest':
            contests_menu()


# SHOULD ADD MORE COUNTRIES
#----------------------------------------------------------#
#----------------------------------------------------------#
# PRACTICE PYTHON
def python():
    choice = 'python'
    _type_ = 'practice'
    tech_executor(choice, _type_)
#----------------------------------------------------------#
# PRACTICE JAVA


def java():
    choice = 'java'
    _type_ = 'practice'
    tech_executor(choice, _type_)
#----------------------------------------------------------#
# PRACTICE RUBY


def ruby():
    choice = 'ruby'
    _type_ = 'practice'
    tech_executor(choice, _type_)
#----------------------------------------------------------#
# PRACTICE C++


def cpp():
    choice = 'cpp'
    _type_ = 'practice'
    tech_executor(choice, _type_)
#----------------------------------------------------------#
# PRACTICE ALGORITHMS


def p_algorithms():
    choice = 'algorithms'
    _type_ = 'practice'
    tech_executor(choice, _type_)
#----------------------------------------------------------#
# PRACTICE MATHEMATICS


def p_mathematics():
    choice = 'mathematics'
    _type_ = 'practice'
    tech_executor(choice, _type_)
#----------------------------------------------------------#
# PRACTICE FUNCTIONAL PROGRAMMING


def p_functional_prog():
    choice = 'fp'
    _type_ = 'practice'
    tech_executor(choice, _type_)
#----------------------------------------------------------#
# PRACTICE DATA STRUCTURES


def data_structures():
    choice = 'data-structures'
    _type_ = 'practice'
    tech_executor(choice, _type_)
#----------------------------------------------------------#
# PRACTICE ARTIFICIAL INTELLIGENCE


def p_artificial_int():
    choice = 'ai'
    _type_ = 'practice'
    tech_executor(choice, _type_)
#----------------------------------------------------------#
# PRACTICE SQL


def sql():
    choice = 'sql'
    _type_ = 'practice'
    tech_executor(choice, _type_)
#----------------------------------------------------------#
# PRACTICE DATABASES


def databases():
    choice = 'databases'
    _type_ = 'practice'
    tech_executor(choice, _type_)
#----------------------------------------------------------#
# PRACTICE DISTRIBUTED SYSTEMS


def distributed_sys():
    choice = 'distributed-systems'
    _type_ = 'practice'
    tech_executor(choice, _type_)
#----------------------------------------------------------#
# PRACTICE LINUX SHELL


def linux_shell():
    choice = 'shell'
    _type_ = 'practice'
    tech_executor(choice, _type_)
#----------------------------------------------------------#
# PRACTICE SECURITY


def security():
    choice = 'security'
    _type_ = 'practice'
    tech_executor(choice, _type_)
#----------------------------------------------------------#
# CONTESTS ALGORITHMS


def c_algorithms():
    choice = 'algorithms'
    _type_ = 'contest'
    tech_executor(choice, _type_)
#----------------------------------------------------------#
# CONTESTS MATHEMATICS


def c_mathematics():
    choice = 'mathematics'
    _type_ = 'contest'
    tech_executor(choice, _type_)
#----------------------------------------------------------#
# CONTESTS FUNCTIONAL PROGRAMMING


def c_functional_prog():
    choice = 'fp'
    _type_ = 'contest'
    tech_executor(choice, _type_)
#----------------------------------------------------------#
# CONTESTS ARTIFICIAL INTELLIGENCE


def c_artificial_int():
    choice = 'ai'
    _type_ = 'contest'
    tech_executor(choice, _type_)
#----------------------------------------------------------#
#----------------------------------------------------------#


#----------------------------------------------------------#
#--------------------MENU DICTIONARY-----------------------#
#----------------------------------------------------------#
menu_actions = {
    ':c': contests_menu,
    ':p': practice_menu,
    '../': back,
    ':q': exit,
    '-py': python,
    '-cal': c_algorithms,
    '-cmath': c_mathematics,
    '-cfun': c_functional_prog,
    '-cai': c_artificial_int,
    '-pal': p_algorithms,
    '-pmath': p_mathematics,
    '-cpp': cpp,
    '-sql': sql,
    '-dist': distributed_sys,
    '-pfun': p_functional_prog,
    '-data': data_structures,
    '-pai': p_artificial_int,
    '-jar': java,
    '-rb': ruby,
    '-db': databases,
    '-sh': linux_shell,
    '-sec': security


}
#----------------------------------------------------------#
#----------------------------------------------------------#

#----------------------------------------------------------#
#----------------------ANIMATION---------------------------#
#----------------------------------------------------------#


def animation(stop):
    while True:
        print('''{yellow}
                    __
                   / _)     Collecting users
          _.----._/ /       Please, wait ..
         /         /   O
      __/ (  | (  |
     /__.-'|_|--|_| {endcolor}'''.format(yellow='\033[93m', endcolor='\033[0m'))
        time.sleep(0.2)
        os.system('cls')

        print('''{yellow}

                   ____     Collecting users
          _.----._/ __ )    Please, wait ....
         /         /   O
      __/ (  | (  |
     /__.-'|_|--|_| {endcolor}'''.format(yellow='\033[93m', endcolor='\033[0m'))
        time.sleep(0.2)
        os.system('cls')

        print('''{yellow}

                            Collecting users
          _.----._ _____    Please, wait ......
         /         ___   )
      __/ (  | (  |   \\
     /__.-'|_|--|_| {endcolor}'''.format(yellow='\033[93m', endcolor='\033[0m'))
        time.sleep(0.2)
        os.system('cls')

        if stop():
            break


def animation_2(stop):
    while True:
        print('{yellow}Checking if users exist on GitHub, please wait .'.format(
            yellow='\033[93m', endcolor='\033[0m'))
        time.sleep(0.2)
        os.system('cls')
        print('{yellow}Checking if users exist on GitHub, please wait   .'.format(
            yellow='\033[93m', endcolor='\033[0m'))
        time.sleep(0.2)
        os.system('cls')
        print('{yellow}Checking if users exist on GitHub, please wait     .'.format(
            yellow='\033[93m', endcolor='\033[0m'))
        time.sleep(0.2)
        os.system('cls')
        print('{yellow}Checking if users exist on GitHub, please wait   .'.format(
            yellow='\033[93m', endcolor='\033[0m'))
        time.sleep(0.2)
        os.system('cls')
        print('{yellow}Checking if users exist on GitHub, please wait .'.format(
            yellow='\033[93m', endcolor='\033[0m'))
        time.sleep(0.2)
        os.system('cls')
        print('{yellow}Checking if users exist on GitHub, please wait{endcolor} '.format(
            yellow='\033[93m', endcolor='\033[0m'))
        time.sleep(0.2)
        os.system('cls')

        if stop():
            break
#----------------------------------------------------------#
#----------------------------------------------------------#


#----------------------------------------------------------#
#--------------------AUTHENTICATION------------------------#
#----------------------------------------------------------#


def auth(lst, git_check_status):
    try:
        os.system('cls')
        yellow = '\033[93m'
        endcolor = '\033[0m'
        print(f'    {yellow}AUTHENTICATION PROCEDURE INITIATED{endcolor}')
        print('#----------------------------------------#')
        print('            [../] to go back \n')

        token = input('Please, enter your GitHub token: ').lower().replace(' ', '')
        if token == '../':
            git_checker(lst, git_check_status)
        else:
            os.system('cls')
            base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
            print('Current program directory is:', base_path)
            path_choice = input(
                '\nShould I generate path myself or you will insert it manualy ? [man/auto]: ')
            if path_choice == 'man':
                try:
                    os.system('cls')
                    file_path = input(
                        'Insert the correct path to the program directory: ').strip(' ')
                    f = open(f'{file_path}/token.txt', 'w')
                    f.write(token)
                    f.close()
                    limits(lst, git_check_status)
                except FileNotFoundError:
                    print('\nERROR: I see no such directory')
                    time.sleep(2)
                    os.system('cls')
                    auth(lst, git_check_status)
                except PermissionError:
                    print(
                        '\nERROR: Due to OS settings, I have no permisson to write the file in the following directory')
                    time.sleep(4)
                    os.system('cls')
                    auth(lst, git_check_status)
            elif path_choice == 'auto':
                os.system('cls')
                f = open(resource_path('token.txt'), "w")
                f.write(token)
                f.close()
                print('File saved at', os.path.realpath(f.name))
                y = '\033[93m'
                e = '\033[0m'
                print(f'\nNew authentication try in {y}5{e} sec')
                time.sleep(1)
                os.system('cls')
                print('File saved at', os.path.realpath(f.name))
                print(f'\nNew authentication try in {y}4{e} sec. ')
                time.sleep(1)
                os.system('cls')
                print('File saved at', os.path.realpath(f.name))
                print(f'\nNew authentication try in {y}3{e} sec.. ')
                time.sleep(1)
                os.system('cls')
                print('File saved at', os.path.realpath(f.name))
                print(f'\nNew authentication try in {y}2{e} sec... ')
                time.sleep(1)
                os.system('cls')
                print('File saved at', os.path.realpath(f.name))
                print(f'\nNew authentication try in {y}1{e} sec.... ')
                time.sleep(1)
                limits(lst, git_check_status)
            else:
                auth(lst, git_check_status)
    except KeyboardInterrupt:
        kill()
#----------------------------------------------------------#
#----------------------------------------------------------#


#----------------------------------------------------------#
#---------------------TOKEN LIMITS-------------------------#
#----------------------------------------------------------#


def limits(lst, git_check_status):
    try:
        os.system('cls')
        f = open(resource_path('token.txt'), "r")
        token = f.read()
        os.system('cls')
        URL = f'https://api.github.com/rate_limit'
        headers = {'Authorization': 'token ' + token}
        r = requests.get(url=URL, headers=headers)
        r_limit = r.json()
        x_limit = r_limit['rate']
        limit = x_limit['limit']
        remaining = x_limit['remaining']
        green = '\033[32m'
        endcolor = '\033[0m'
        print(
            f'TOKEN CHECK: {green}VALID{endcolor}\nRequests limit: {limit}\nRequests remains: {remaining}')
        time.sleep(4)
        git_checker(lst, git_check_status)
    except (ValueError, KeyError):
        try:
            os.system('cls')
            red = '\033[31m'
            yellow = '\033[93m'
            endcolor = '\033[0m'
            print(f'{red}INVALID TOKEN:{endcolor} {yellow}This token is not valid{endcolor}')
            time.sleep(2)
            git_checker(lst, git_check_status)
        except KeyboardInterrupt:
            kill()
    except(requests.exceptions.ConnectionError):
        try:
            os.system('cls')
            red = '\033[31m'
            endcolor = '\033[0m'
            print(f'{red}NO INTERNET CONNECTION{endcolor}')
            time.sleep(2)
            git_checker(lst, git_check_status)
        except KeyboardInterrupt:
            kill()
    except KeyboardInterrupt:
        kill()
    except FileNotFoundError:
        try:
            red = '\033[91m'
            yellow = '\033[93m'
            endcolor = '\033[0m'
            print(f'{red}AUTHENTICATION REQUIRED:{endcolor} {yellow}You have no token!{endcolor}')
            time.sleep(3)
            auth(lst, git_check_status)
        except KeyboardInterrupt:
            kill()
#----------------------------------------------------------#
#----------------------------------------------------------#


#----------------------------------------------------------#
#-------------------KEYBOARD INTERRUPT---------------------#
#----------------------------------------------------------#


def kill():
    os.system('cls')
    print('Program killed by user')
    time.sleep(0.5)
    os.system('cls')
    sys.exit()
#----------------------------------------------------------#
#----------------------------------------------------------#


#----------------------------------------------------------#
#-----------------------TOKEN HELP-------------------------#
#----------------------------------------------------------#


def helper(lst, git_check_status):
    try:
        print('#-----------HELP----------# \n')
        print('1. Sign in or sign up on GitHub.com \n')
        print('2. Follow this link:')
        print('https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line#creating-a-token \n')
        print('3. Initiate authentication procedure [setup] \n')
        print('4. Copy your token and paste it \n')
        print('#-------------------------#')
        print('press ENTER to turn back')
        back = input('').lower().strip(' ')
        if back:
            git_checker(lst, git_check_status)
        else:
            git_checker(lst, git_check_status)
    except KeyboardInterrupt:
        kill()
#----------------------------------------------------------#
#----------------------------------------------------------#


#----------------------------------------------------------#
#----------------------MAIN PROGRAM------------------------#
#----------------------------------------------------------#
lst = []
main_menu()
#----------------------------------------------------------#
#----------------------------------------------------------#
