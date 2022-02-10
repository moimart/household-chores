from datetime import datetime, timedelta

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

class GoogleCalendar:
    def __init__(self):
        self.words = [ 'Biogut', 'Hausmüll', 'Wertstoffe', 'Paper']
        self.translations = {
            "Biogut" : 'Bio' ,
            "Hausmüll" : 'Gray Garbage',
            "Wertstoffe" : 'Plastic',
            'Paper' : 'Paper'
        }

    def string_date(self, date):
        if datetime.today().day + 2 == date.day:
            return "After Tomorrow"

        if datetime.today().day + 1 == date.day:
            return "Tomorrow"

        day = int(date.strftime("%d"))

        strday = ""
        if day == 1:
            strday = "1st"
        elif day == 2:
            strday = "2nd"
        elif day == 3:
            strday = "3rd"
        else:
            strday = str(day) + "th"
    
        return "{} {}".format(date.strftime("%A"),strday)

    def get_events(self):
        creds = None
        creds = service_account.Credentials.from_service_account_file("creds.json", scopes=SCOPES)
        print(creds)

        try:
            service = build('calendar', 'v3', credentials=creds)

            now = datetime.utcnow() + timedelta(days=1)
            now = now.isoformat() + 'Z'  # 'Z' indicates UTC time
            events_result = service.events().list(calendarId='kve59bt6c3fqvbln1ghvc1qg98@group.calendar.google.com', timeMin=now,
                                                maxResults=3, singleEvents=True,
                                                orderBy='startTime').execute()
            events = events_result.get('items', [])

            if not events:
                print('No upcoming events found.')
                return

            next_events = []

            for event in events:
                for garbage in self.words:
                    if garbage in event['summary']:
                        date = self.string_date(datetime.strptime(event['start'].get('date'),"%Y-%m-%d").date())
                        event = { 
                            "garbage": self.translations[garbage], 
                            "when":  date
                        }
                        next_events.append(event)
                        break
                
            return next_events
        except HttpError as error:
            print('An error occurred: %s' % error)
