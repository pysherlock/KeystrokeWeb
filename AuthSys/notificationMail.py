from __future__ import print_function
import httplib2
import os
from email.mime.text import MIMEText
import base64

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from googleapiclient import errors

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
# SCOPES = 'https://www.googleapis.com/auth/gmail.send'
SCOPES = 'https://mail.google.com/'
CLIENT_SECRET_FILE = '../client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'
SRC_MAIL_ADDRESS = 'pu.leo.yang@gmail.com'

PROFILE_UPDATE = '''Dear user,\n\n
                    According to your login habit, our system changed your profile of Environmental Login,
                    so that the new profile could follow your new habit. \n
                    Thank you for using Environmental Login. \n\n
                    Environmental Login Team'''

KEYSTROKE_READY = '''Dear user, \n\n
                     You keystroke profile has already been built. In the following authentications,
                     your keystroke of typing Office ID will be taken into account. \n
                     Thank you for using Environmental Login. \n\n
                     Environmental Login Team'''

KEYSTROKE_UPDATE = '''Dear user,\n\n
                    According to your login habit, our system changed your keystroke profile of Environmental Login,
                    so that our system could keep following your typing habit. \n
                    Thank you for using Environmental Login. \n\n
                    Environmental Login Team'''

class SendNotificationMail:

    def __init__(self, dst, type=0):
        self._dst = dst
        self._type = type

    def get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'gmail-python-quickstart.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    # create a message
    def CreateMessage(self, sender, to, subject, message_text):
        """Create a message for an email.
        Args:
            sender: Email address of the sender.
            to: Email address of the receiver.
            subject: The subject of the email message.
            message_text: The text of the email message.

            Returns:
                An object containing a base64 encoded email object.
        """

        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        return {'raw': base64.b64encode(message.as_string())}

    #send message
    def SendMessage(self, service, user_id, message):
        """Send an email message.

        Args:
         service: Authorized Gmail API service instance.
         user_id: User's email address. The special value "me"
         can be used to indicate the authenticated user.
         message: Message to be sent.

        Returns:
         Sent Message.
        """
        try:
            message = (service.users().messages().send(userId=user_id, body=message).execute())
            # print 'Message Id: %s' % message['id']
            print ("Send message successfully! " + 'Message Id: %s' % message['id'])
            return message
        except errors.HttpError, error:
            print ('An error occurred: %s' % error)

    def run(self):
        """Shows basic usage of the Gmail API.

        Creates a Gmail API service object and outputs a list of label names
        of the user's Gmail account.
        """
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('gmail', 'v1', http=http)

        msg_body = PROFILE_UPDATE
        if self._type == 1:
            msg_body = KEYSTROKE_READY
        elif self._type == 2:
            msg_body = KEYSTROKE_UPDATE

        print ("Dst mail address: ", self._dst, type(self._dst))
        message = self.CreateMessage(SRC_MAIL_ADDRESS, 'pu.leo.yang@gmail.com',
                                "Notification: Authentication Profile is Updated", msg_body)

        self.SendMessage(service, "me", message)

        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])

        if not labels:
            print('No labels found.')
        else:
          print('Labels:')
          for label in labels:
            print(label['name'])


# if __name__ == '__main__':
#     main()