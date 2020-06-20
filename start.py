import datetime
import re
from setup.auth import authenticate

class Calendar:
    def __init__(self, service):
        self._service = service
        self.now = datetime.datetime.utcnow().isoformat() + "Z"

    def find_all_events(self, max_events=10):
        """
        Finds the upcoming 10 events on the users calendar and displays them in a readable format
        """
        print("Fetching your upcoming {} Events".format(max_events))
        events_result = self._service.events().list(calendarId="primary", timeMin=self.now, maxResults=max_events, singleEvents=True, orderBy="startTime").execute()
        events = events_result.get("items", [])
        if not events:
            print("No upcoming events found")
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            date1 = re.search(r"\d\d\d\d-\d\d-\d\d", start)
            date2 = re.search(r"\d\d:\d\d", start)
            date3 = str(date1.group(0) + " " + date2.group(0))
            print("{} : {}".format(date3, event["summary"]))


    def add_event(self, event):
        """
        Takes in an event JSON string and then inserts that event into the users calendar
        """
        response = self._service.events().insert(calendarId="primary", body=event).execute()
        if response != None:
            print("Successfully Added to Calendar")


def main():
    cal = Calendar(authenticate())
    
    cal.find_all_events(2)

    start_time = datetime.datetime.utcnow()
    end_time = start_time + datetime.timedelta(hours=3)
    event = {
        "summary": "Learning Google Calendar API",
        "location": "Lincoln",
        "description": "A chance to use as a portfolio project",
        "start": {
            "dateTime": str(start_time.isoformat()),
            "timeZone": "Europe/London",
        },
        "end": {
            "dateTime": str(end_time.isoformat()),
            "timeZone": "Europe/London",
        },
    }
 

if __name__ == "__main__":
    main()
