import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate():
    """ 
    Uses OAuth to Authenticate the user and get back a token
    Creates a build object based on the credentails to return users calendar
    """
    creds = None
    if os.path.exists('setup/token.pickle'):
        with open('setup/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'setup/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('setup/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('calendar', 'v3', credentials=creds)
