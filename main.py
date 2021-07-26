from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import liveScores
import leagueTable
import upcomingMatches
from os import system,name
import sys

def menu(main_browser):
    clear_screen()

    while True:
        print('What do you want to do?')
        print("1. See fixtures/results/live scores on a day for all competitions")
        print("2. See a League table")
        print("3. List the upcoming matches and recent results for a team")
        print('4. Exit')
        try:
            choice = int(input('Your choice: '))
            if choice not in range(1,5):
                break
        except ValueError:
            print('Enter a valid input: ')
        clear_screen()
        if choice == 1:
            liveScores.LiveScores(main_browser)
        elif choice ==2:
            leagueTable.LeagueTable(main_browser)
        elif choice ==3:
            upcomingMatches.UpcomingMatches(main_browser)
        else:
            main_browser.quit()
            sys.exit()

def clear_screen():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

if '__main__':

    # initializing the browser
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    option.add_argument("--log-level=3")
    option.add_experimental_option('excludeSwitches', ['enable-logging'])

    CDM = ChromeDriverManager(log_level='0')
    browser = webdriver.Chrome(CDM.install(), options=option)
    menu(browser)