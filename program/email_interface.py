# import the required libraries
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path
import base64
import datetime
from bs4 import BeautifulSoup

# Define the SCOPES. If modifying it, delete the token.pickle file.
SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.send",
]

CREDS = None
SERVICE = None


def initalize():
    global CREDS
    global SERVICE

    # Variable creds will store the user access token.
    # If no valid token found, we will create one.
    CREDS = None

    # The file token.pickle contains the user access token.
    # Check if it exists
    if os.path.exists("token.pickle"):
        # Read the token from the file and store it in the variable creds
        with open("token.pickle", "rb") as token:
            CREDS = pickle.load(token)

    # If credentials are not available or are invalid, ask the user to log in.
    if not CREDS or not CREDS.valid:
        if CREDS and CREDS.expired and CREDS.refresh_token:
            CREDS.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            CREDS = flow.run_local_server(port=0)

        # Save the access token in token.pickle file for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(CREDS, token)

    # Connect to the Gmail API
    SERVICE = build("gmail", "v1", credentials=CREDS)


def get_emails(_maxResults=10, _unread=True) -> list:
    global SERVICE
    global CREDS

    if SERVICE == None:
        raise RuntimeError("email master is not initialized; SERVICE is None")

    # request a list of all the messages
    result = (
        SERVICE.users()
        .messages()
        .list(
            maxResults=_maxResults,
            userId="me",
            labelIds=["INBOX", "UNREAD"] if _unread else ["INBOX"],
        )
        .execute()
    )

    # We can also pass maxResults to get any number of emails. Like this:
    # result = service.users().messages().list(maxResults=200, userId='me').execute()
    messages = result.get("messages")

    # messages is a list of dictionaries where each dictionary contains a message id.

    # iterate through all the messages

    return_data = []

    if messages is None:
        return return_data

    for msg in messages:
        # Get the message from its id
        txt = (
            SERVICE.users().messages().get(userId="me", id=msg["id"]).execute()
        )

        # print(txt)

        # Use try-except to avoid any Errors
        try:
            # Get value of 'payload' from dictionary 'txt'
            payload = txt["payload"]
            headers = payload["headers"]

            # Look for Subject and Sender Email in the headers
            for d in headers:
                if d["name"] == "Subject":
                    subject = d["value"]
                if d["name"] == "From":
                    sender = d["value"]
                if d["name"] == "Date":
                    date = d["value"]

            body = "<empty>"
            # "data" key not present
            # print (payload)
            if "data" in payload["body"].keys():
                # The Body of the message is in Encrypted format. So, we have to decode it.
                # Get the data and decode it with base 64 decoder.
                data = payload["body"]["data"]
                data = data.replace("-", "+").replace("_", "/")
                decoded_data = base64.b64decode(data)

                # Now, the data obtained is in lxml. So, we will parse
                # it with BeautifulSoup library
                soup = BeautifulSoup(decoded_data, "lxml")

                if soup.body is not None:
                    body = soup.body()
                else:
                    body = "<empty>"
            else:
                data = payload["parts"][0]["body"]["data"]
                data = data.replace("-", "+").replace("_", "/")
                decoded_data = base64.b64decode(data)

                # Now, the data obtained is in lxml. So, we will parse
                # it with BeautifulSoup library
                soup = BeautifulSoup(decoded_data, "lxml")

                if soup.body is not None:
                    body = soup.body()
                else:
                    body = "<empty>"

            # Parsing data a bit
            splt = sender.split(" <")
            sender_name = splt[0]
            sender_email = splt[1][:-1]

            body = str(body)
            body = body.replace("\r\n", "\n")[4:-5]

            date = date[5:-6]

            splt = date.split(" ")
            day = int(splt[0])

            # Convert string-month to int
            month = splt[1].lower()
            if month == "jan":
                month = 1
            elif month == "feb":
                month = 2
            elif month == "mar":
                month = 3
            elif month == "apr":
                month = 4
            elif month == "may":
                month = 5
            elif month == "jun":
                month = 6
            elif month == "jul":
                month = 7
            elif month == "aug":
                month = 8
            elif month == "sep":
                month = 9
            elif month == "oct":
                month = 10
            elif month == "nov":
                month = 11
            elif month == "dec":
                month = 12
            year = int(splt[2])

            time = splt[3]
            time = time.split(":")
            hour = int(time[0])
            minute = int(time[1])
            second = int(time[2])

            dt = datetime.datetime(year, month, day, hour, minute, second)

            # Assemble dict
            return_data.append(
                {
                    "date": dt,
                    "subject": subject,
                    "sender_info": {
                        "sender_name": sender_name,
                        "sender_email": sender_email,
                    },
                    "body": body,
                }
            )

            # remove unread label (mark as read)
            if _unread:
                SERVICE.users().messages().modify(
                    userId="me",
                    id=msg["id"],
                    body={"removeLabelIds": ["UNREAD"]},
                ).execute()

        except Exception as ex:
            print(
                f"email_interface: an error occured while retreiving emails: {ex}"
            )

    return return_data


from email.mime.text import MIMEText
from requests import HTTPError


def send_email(_target_email, _subject, _body) -> int:
    global CREDS
    global SERVICE

    if SERVICE == None:
        raise RuntimeError("email master is not initialized; SERVICE is None")

    _body = "<pre>" + _body + "</pre>"
    message = MIMEText(_body, "html")
    message["to"] = _target_email
    message["subject"] = _subject
    create_message = {
        "raw": base64.urlsafe_b64encode(message.as_bytes()).decode()
    }

    try:
        message = (
            SERVICE.users()
            .messages()
            .send(userId="me", body=create_message)
            .execute()
        )
        # print(f'sent message to {message} Message Id: {message["id"]}')
        return 0
    except HTTPError as error:
        print(
            f"email_interface: an error occurred while sending email: {error}"
        )
        message = None
        return -1


if __name__ == "__main__":
    initalize()
    #     send_email(
    #         "**replaced ALIAS using filter-repo****replaced EMAIL using filter-repo**,
    #         "test email",
    #         """<strong>
    # <b>asd</b>
    # </strong>""",
    #     )
    print(get_emails(1, False))
