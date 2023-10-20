import yaml
import imaplib
import email
from email.parser import BytesParser
from email.header import decode_header
from datetime import datetime, timedelta


def count_emails_received(username, app_password, days=7):
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(username, app_password)

        mail.select("inbox")

        today = datetime.today()
        start_date = (today - timedelta(days=days)).strftime("%d-%b-%Y")
        end_date = today.strftime("%d-%b-%Y")

        search_query = f'(SINCE "{start_date}" BEFORE "{end_date}")'
        status, email_ids = mail.search(None, search_query)

        if status == "OK":
            email_ids = email_ids[0].split()
            total_emails_received = len(email_ids)
            return total_emails_received
        else:
            return "Failed to retrieve emails."

    except Exception as e:
        return f"An error occurred: {str(e)}"

def count_unique_senders(username, app_password, days=7):
    try:
        # Connect to the Gmail IMAP server.
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(username, app_password)

        mail.select("inbox")

        today = datetime.today()
        start_date = (today - timedelta(days=days)).strftime("%d-%b-%Y")
        end_date = today.strftime("%d-%b-%Y")

        search_query = f'(SINCE "{start_date}" BEFORE "{end_date}")'
        status, email_ids = mail.search(None, search_query)

        unique_senders = {}

        if status == "OK":
            email_ids = email_ids[0].split() if email_ids else []
            for email_id in email_ids:
                status, email_data = mail.fetch(email_id, "(BODY[HEADER.FIELDS (FROM)])")
                if status == "OK":
                    msg_data = email_data[0][1]
                    msg = BytesParser().parsebytes(msg_data)
                    sender = msg["from"]
                    if sender in unique_senders:
                        unique_senders[sender] += 1
                    else:
                        unique_senders[sender] = 1
            return unique_senders
        else:
            return "Failed to retrieve emails."

    except Exception as e:
        return f"An error occurred: {str(e)}"
