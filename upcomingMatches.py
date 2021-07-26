from re import T
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from tabulate import tabulate
from os import system,name

class UpcomingMatches:

    def __init__(self,browser):
        self.teams(browser)

    # available teams to scrape data
    def teams(self,br):

        try:
            br.set_page_load_timeout(8)
            br.get('https://www.goal.com/en-in/teams')
        except TimeoutException:
            br.execute_script("window.stop();")
        br.set_page_load_timeout(10)
        teams = br.find_elements_by_class_name('popular-teams__member')
        teams = [i.text for i in teams]

        while True:
            print("The teams that has the available data are: \n")
            for i in range(len(teams)):
                print(f'{i+1}. {teams[i]}')
            print()
            choice = (input('Choose a number or press ENTER to exit to main menu: '))
            if not choice :
                self.clear_screen()
                break
            self.clear_screen()
            chosen_team = teams[int(choice)-1]
            print(f'Schedule of {chosen_team} is listed below: \n')
            br.execute_script('arguments[0].click();',br.find_element_by_link_text(chosen_team))
            self.get_matches(br,chosen_team)

            br.get('https://www.goal.com/en-in/teams')

    # scaping data
    def get_matches(self,br,chosen_team):

        try:
            br.find_element_by_xpath('html/body/div[3]/div[2]/div[2]/div/div/a[2]').click()
        except NoSuchElementException:
            return "No matches found"

        br.implicitly_wait(0.5)

        main_data = br.find_elements_by_class_name('match-main-data')
        br.implicitly_wait(0.5)
        competitions =[i.text for i in br.find_elements_by_class_name('match-additional-data__competition-name')]
        br.implicitly_wait(0.5)

        penalties = False
        try:
            penalties_result = [i.text for i in br.find_elements_by_class_name('match-additional-data__agregate')]
            for i in penalties_result:
                if len(i)!=0:
                    penalties = True
            br.implicitly_wait(0.5)

        except NoSuchElementException:
            penalties = False
    
    
        list_of_all_matches = [match.text.split('\n') for match in main_data]

        # 10 upcoming matches
        if len(list_of_all_matches[0]) == 4:

            for i in range(len(list_of_all_matches)):
                if '-' in list_of_all_matches[i]:
                    list_of_all_matches[i].remove('-')
                list_of_all_matches[i].insert(0,competitions[i])
            print(tabulate(list_of_all_matches,headers=['Competition','Date','Home Team','Away Team'],tablefmt='pretty'))
            print()

        # upcoming and played matches (5+5)
        elif len(list_of_all_matches[0])>4 and len(list_of_all_matches[len(list_of_all_matches)-1]) ==4:
            self.upcomingAndPlayedMatches(list_of_all_matches,competitions, chosen_team,penalties, penalties_result)            

        # 10 played matches
        else:
            self.allPlayedMatches(list_of_all_matches,competitions,chosen_team)

    # mix of fixtures and results
    def upcomingAndPlayedMatches(self,matches, competitions, chosen_team, penalties,pen_result):
        for i in range(len(matches)):
                matches[i].remove('-')
                matches[i].insert(0,competitions[i])
                
                # merge columns, remove unnecessary data and add result
                if len(matches[i])>4:
                    if int(matches[i][2]) == int(matches[i][4]):
                        if penalties == False:
                            matches[i][1] ='Draw'
                            matches[i][4]=f'{matches[i][2]} - {matches[i][4]}'
                            matches[i].remove(matches[i][2])
                        else:
                            matches[i][4]= f'{matches[i][2]} - {matches[i][4]}' +  pen_result[i]
                            if len(pen_result[i])>1:
                                if int(pen_result[i][len(pen_result[i])-6]) < int(pen_result[i][len(pen_result[i])-2]):
                                    if matches[i][3] == chosen_team:
                                        matches[i][1] ='Lost'
                                    else:
                                        matches[i][1] ='Won'
                                else:
                                    if matches[i][3] == chosen_team:
                                        matches[i][1] ='Won'
                                    else:
                                        matches[i][1] ='Lost'
                            matches[i].remove(matches[i][2])

                    elif int(matches[i][2]) > int(matches[i][4]):
                        if matches[i][3] == chosen_team:
                            matches[i][1] ='Won'
                        else:
                            matches[i][1] ='Lost'
                        matches[i][4]=f'{matches[i][2]} - {matches[i][4]}'
                        matches[i].remove(matches[i][2])
                    
                    else:
                        if matches[i][3] == chosen_team:
                            matches[i][1] ='Lost'
                        else:
                            matches[i][1] ='Won'
                        matches[i][4]=f'{matches[i][2]} - {matches[i][4]}'
                        matches[i].remove(matches[i][2])    

                else:
                    matches[i].insert(len(matches[i])-1,'TBP')
        print(tabulate(matches,headers=['Competition','Status/Date','Home Team','Score','Away Team'],tablefmt='pretty'))
        print()

    # last 10 played matches
    def allPlayedMatches(self,matches,competitions,chosen_team):
        
        for i in range(len(matches)):
                
            if '-' in matches[i]:
                matches[i].remove('-')
            matches[i].insert(0,competitions[i])
                
            # merge columns, remove unnecessary data and add result
            if int(matches[i][2]) == int(matches[i][4]) :
                matches[i][1] ='Draw'
                matches[i][4]=f'{matches[i][2]} - {matches[i][4]}'
                matches[i].remove(matches[i][2])
               
            elif int(matches[i][2]) > int(matches[i][4]):
                if matches[i][3] ==chosen_team:
                    matches[i][1] ='Won'
                
                else:
                    matches[i][1] = 'Lost'
                matches[i][4]=f'{matches[i][2]} - {matches[i][4]}'
                matches[i].remove(matches[i][2])
                
            else:
                if matches[i][3] ==chosen_team:
                    matches[i][1] ='Lost'
                else:
                    matches[i][1] = 'Won'
                matches[i][4]=f'{matches[i][2]} - {matches[i][4]}'
                matches[i].remove(matches[i][2])
                
        print(tabulate(matches,headers=['Competition','Status','Home Team','Score','Away Team'],tablefmt='pretty'))
        print()

    # clears terminal for better display
    def clear_screen(self):
        # for windows
        if name == 'nt':
            _ = system('cls')

        # for mac and linux(here, os.name is 'posix')
        else:
            _ = system('clear')
