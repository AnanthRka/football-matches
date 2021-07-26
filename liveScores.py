from selenium.common.exceptions import NoSuchElementException, TimeoutException
from tabulate import tabulate
from findUrl import FindUrl
from os import remove, system,name


class LiveScores:

    time = 8    # for page  load timeout

    def __init__(self, br):

            # gets the date to find the result/fixture/live score
            #         
            url_class = FindUrl()
            url_append = url_class.final
            self.clear_screen()
            self.scrapping(br,url_append)

    def scrapping(self,br, url = ''):

        try:
            br.set_page_load_timeout(self.time)
            try:
                br.get(r"https://www.goal.com/en-in/"+url)
            except TimeoutException:
                br.execute_script("window.stop();")
            br.set_page_load_timeout(self.time)

            competitions = br.find_elements_by_class_name('competition-name')
            matches_in_competitions = br.find_elements_by_class_name('match-row-list')
            br.implicitly_wait(0.5)
            all_matches = br.find_elements_by_class_name('match-main-data')
            
            try:
                aggregate_scores = br.find_elements_by_class_name( 'match-additional-data')
            except NoSuchElementException:
                aggregate_scores = []

            # makings lists to accompany data
            list_of_matches_in_competitions = [i.text.split('\n') for i in matches_in_competitions]
            list_of_competitions = [competition.text for competition in competitions]
            list_of_all_matches= [all_match.text.split('\n') for all_match in all_matches]
            last_team = [i[len(i)-2] if '(' not  in i[len(i)-2] else i[len(i)-3] for i in list_of_matches_in_competitions]
            aggregate_scores = [i.text for i in aggregate_scores]

            #function calls based on specified date
            if 'results' in url:
                self.results(list_of_all_matches,list_of_competitions,last_team,aggregate_scores)
            
            elif 'live-scores' in url:
                self.live_score(list_of_all_matches, list_of_competitions, last_team,aggregate_scores)
            
            else:
                self.fixtures(list_of_all_matches, list_of_competitions, last_team, aggregate_scores)
            
            # Dictionary to map competitions/leagues with matches
            dict_competitions= {}

            for (match, competition) in zip(list_of_matches_in_competitions, list_of_competitions):
                dict_competitions[competition] = match

            # Leagues which does not have match on the specified date
            while True:
                choice = input('Do you want to see missing leagues next match date? (y/n): ').lower()
                if choice == 'y' or choice == 'n':
                    break
                print("Enter a valid choice...")
            if choice == 'y':
                print("\nMissing Leagues/Competitions:")
                print()

                for key in dict_competitions:
                    if len(dict_competitions.get(key)) == 1:
                        print(f'\t{key}')
                        print(tabulate({key : [dict_competitions[key][0]]},tablefmt='pretty'))
                        print()

        except TimeoutException:
            self.time += 2
            self.scrapping(br,url)

        print()

    # Results of matches held in the past
    def results(self, all_matches,competitions, teams, agg_scores):
        j = 0
        matches = []    

        for i in range(len(all_matches)):
            if int(all_matches[i][1]) < int(all_matches[i][4]):
                all_matches[i][0] = f'{all_matches[i][5]} won'
            elif int(all_matches[i][1]) == int(all_matches[i][4]):
                all_matches[i][0] = f'Draw'
            else:
                all_matches[i][0]= f'{all_matches[i][2]} won'
            all_matches[i][3] = f'{all_matches[i][1]} - {all_matches[i][4]}'
            all_matches[i].remove(all_matches[i][1])
            all_matches[i].remove(all_matches[i][len(all_matches[i])-2])
            
            if len(agg_scores[i])>2:
                all_matches[i].append(agg_scores[i][1:len(agg_scores[i])-1])
            matches.append(all_matches[i])
            
            if teams[j] in all_matches[i]:
                print(f'\n\t\t\t{competitions[j]}')
                if len(matches[0])>4:
                    print(tabulate(matches,headers=['Status', 'Home Team', 'Score', 'Away Team', 'Aggregate Score'], tablefmt='pretty'))
                else:
                    print(tabulate(matches,headers=['Status', 'Home Team', 'Score', 'Away Team'], tablefmt='pretty'))
                j+=1
                matches = []
    
    # Details of matches to be held in the future     
    def fixtures(self, all_matches,competitions, teams, agg_scores):
        j=0
        matches = []
        for i in range(len(all_matches)):
            if '-' in all_matches[i]:
               all_matches[i].remove('-')
            if len(agg_scores[i]) >2:
                all_matches[i].append(agg_scores[i][1:len(agg_scores[i])-1])
            matches.append(all_matches[i])
            if teams[j] in all_matches[i]:
                print(f'\n\t\t{competitions[j]}')
                if len(matches[0]) > 3:
                    print(tabulate(matches,headers=['Time', 'Home Team', 'Away Team', 'Aggregate Score'], tablefmt='pretty'))
                else:
                    print(tabulate(matches,headers=['Time', 'Home Team', 'Away Team'], tablefmt='pretty'))
                j+=1
                matches = []
        
    # Today's schedule and results
    def live_score(self, all_matches, competitions, teams, agg_scores):
        j = 0
        matches = []    

        for i in range(len(all_matches)):
            if int(all_matches[i][1]) < int(all_matches[i][4]):
                all_matches[i][0] = f'{all_matches[i][5]} won'
            elif int(all_matches[i][1]) == int(all_matches[i][4]):
                all_matches[i][0] = f'Draw'
            else:
                all_matches[i][0]= f'{all_matches[i][2]} won'
            all_matches[i][3] = f'{all_matches[i][1]} - {all_matches[i][4]}'
            all_matches[i].remove(all_matches[i][1])
            all_matches[i].remove(all_matches[i][len(all_matches[i])-2])
            
            if len(agg_scores[i])>2:
                all_matches[i].append(agg_scores[i][1:len(agg_scores[i])-1])
            matches.append(all_matches[i])
            
            if teams[j] in all_matches[i]:
                print(f'\n\t\t\t{competitions[j]}')
                if len(matches[0])>4:
                    print(tabulate(matches,headers=['Status', 'Home Team', 'Score', 'Away Team', 'Aggregate Score'], tablefmt='pretty'))
                else:
                    print(tabulate(matches,headers=['Status', 'Home Team', 'Score', 'Away Team'], tablefmt='pretty'))
                j+=1
                matches = []
    
    # clears terminal for better output display
    def clear_screen(self):
        # for windows
        if name == 'nt':
            _ = system('cls')

        # for mac and linux(here, os.name is 'posix')
        else:
            _ = system('clear')