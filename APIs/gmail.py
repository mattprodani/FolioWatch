import mimetypes
import os.path
import base64
# from __future__ import print_function
from email.message import EmailMessage

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import google.auth



SCOPES = ['https://www.googleapis.com/auth/gmail.compose']

class Gmail():
    def __init__(self):
        """ Initializes and test authentication.
        Stores the credentials in the application's directory.
        """
        creds = None

        if not os.path.exists('credentials.json'):
            print("API keys not found")
            raise Exception("From Google API: No API keys found")
        
        if os.path.exists('token.json'):
            print("Login token found, loading...")
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            print("Login token expired or not found, please log in to your Google account...")
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        if creds.valid:
            print("Login successful!")
            self.creds = creds
            self.sender = self._get_email_address()
        else:
            raise Exception("Failed Authentication")
    
    def send_email(self, to, subject, body, attachment=None):
        """ Sends an email.
        """
        try:
            service = build('gmail', 'v1', credentials=self.creds)
            message = EmailMessage()

            message.set_content(body, subtype='html')

            message['To'] = to
            message['From'] = self.sender
            message['Subject'] = subject

            if attachment:
                type_subtype, _ = mimetypes.guess_type(attachment)
                maintype, subtype = type_subtype.split('/')

                with open(attachment, 'rb') as fp:
                    attachment_data = fp.read()
                message.add_attachment(attachment_data, maintype, subtype, filename = attachment.split('/')[-1])

            # encoded message
            encoded_message = base64.urlsafe_b64encode(message.as_bytes()) \
                .decode()

            create_message = {
                'raw': encoded_message
            }
            # pylint: disable=E1101
            send_message = (service.users().messages().send
                            (userId="me", body=create_message).execute())
            print(F'Message Id: {send_message["id"]}')
        except HttpError as error:
            print(F'An error occurred: {error}')
            send_message = None
        return send_message


    def _get_email_address(self):
        try:
            service = build('gmail', 'v1', credentials=self.creds)
            response = service.users().getProfile(userId='me').execute()
            email = response.get('emailAddress', None)
            if not email:
                raise Exception("From Google API: No email address found")
            return email
        except HttpError as error:
            raise Exception(f"From Google API: {error}")

