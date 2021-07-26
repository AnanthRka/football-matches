from re import L
from selenium.common.exceptions import TimeoutException
from tabulate import PRESERVE_WHITESPACE, tabulate
from os import system,name



class LeagueTable:

    competitons = []

    def __init__(self, browser):
        self.get_competitions(browser)

    # prints table after modifying it
    def get_table(self, rows, headers, heading, league):
        for i in rows:
            if len(i) >1 :
                temp = i[len(i)-1].split(' ')
                temp[8:] = [' '.join(temp[8:])]
                i.remove(i[len(i)-1])
                rows[rows.index(i)] = rows[rows.index(i)]+ temp

        rows.remove(rows[0])

        print(f'The {league} table is as follows: ')
        print()
        j = 0
        temp = []
        for i in rows:
            if (len(i) == 1  and j <= len(headers)) or (rows.index(i) == len(rows)-1):
                if rows.index(i) == len(rows)-1  :
                    temp.append(i)
                print(f'\t\t\t{headers[j]}')
                print(tabulate(temp,headers=heading,tablefmt='pretty'))
                print()
                temp = []
                j+=1
            else:
                temp.append(i)

    # scraping for data
    def get_competitions(self, browser):
        try:
            browser.set_page_load_timeout(8)
            browser.get('https://www.goal.com/en-in/tables')
        except TimeoutException:
            browser.execute_script("window.stop();")

        
        leagues = browser.find_elements_by_class_name('p0c-competition-tables__full-table-link')
        list_leagues = [i.text for i in leagues]

        while True:
            print('The available leagues are: \n')
            for i in range(len(list_leagues)):
                print(f'{i+1}. {list_leagues[i]}')
            print()
            choice = input("Choose a number or press ENTER to exit to main menu: ")
            if not choice:
                break
            self.clear_screen()
            choice = int(choice)
            browser.get(leagues[choice-1].get_attribute('href'))
            headers = browser.find_elements_by_class_name('widget-match-standings__header-text')
            rows = browser.find_elements_by_tag_name('tr')

            heading = rows[0].text.split('\n')[0].split(' ')
            rows = [i.text.split('\n') for i in rows]
            headers = [i.text for i in headers]        

            self.get_table(rows, headers, heading,list_leagues[choice-1])


    def clear_screen(self):
        # for windows
        if name == 'nt':
            _ = system('cls')

        # for mac and linux(here, os.name is 'posix')
        else:
            _ = system('clear')

