import datetime
import time


class FindUrl:

    live = 'live-scores'
    results = 'results/'
    fixtures = 'fixtures/'
    final = ''
    enter = ''

    def __init__(self,enter = ''):

        self.enter = enter
        self.findUrl(self.enter)

    def findUrl(self,enter = ''):
        enter = input("Press ENTER for today's schedule\n\t\t(OR)\nEnter the date on which you want the schedule in yyyy-mm-dd format: ")
        if enter != '' and len(enter)==10:
            list_entered_date = enter.split('-')

            enter_date = int(list_entered_date[2])
            enter_month = int(list_entered_date[1])
            enter_year = int(list_entered_date[0])

            entered_date = datetime.date(enter_year,enter_month,enter_date)
            today = datetime.date.today()

            today_date = today.day
            today_month = today.month
            today_year = today.year

            date = datetime.date(today_year,today_month,today_date)

            if date == entered_date:
                # Today's matches
                self.final = self.live
            elif date > entered_date:
                # The matches held on
                self.final = self.results + enter
            else:
                # The matches to be held
                self.final = self.fixtures + enter
        
        elif len(enter) < 10 and enter!= '':
            print("Enter a valid date")
            self.findUrl()
            
        else:
            self.final = self.live