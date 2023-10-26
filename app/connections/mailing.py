import yaml
import imaplib
import email
from email.parser import BytesParser
from email.header import decode_header
from datetime import datetime, timedelta
from collections import Counter

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

def count_unique_recievers(username, app_password, days=7):
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
                status, email_data = mail.fetch(email_id, "(BODY[HEADER.FIELDS (TO)])")
                if status == "OK":
                    msg_data = email_data[0][1]
                    msg = BytesParser().parsebytes(msg_data)
                    sender = msg["to"]
                    if sender in unique_senders:
                        unique_senders[sender] += 1
                    else:
                        unique_senders[sender] = 1
            return unique_senders
        else:
            return "Failed to retrieve emails."

    except Exception as e:
        return f"An error occurred: {str(e)}"

def fetch_email_info(username, app_password, days=7):
    data = []

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
            for email_id in email_ids:
                # Fetch the email by ID
                status, email_data = mail.fetch(email_id, '(RFC822)')
                if status == "OK":
                    raw_email = email_data[0][1]
                    email_message = email.message_from_bytes(raw_email)

                    # Extract sender name
                    sender = email_message.get("From")

                    # Extract email subject
                    subject = email_message.get("Subject")

                    # Extract email time
                    time = email_message.get("Date")

                    return_data = {
                        "Sender": sender,
                        "Subject": subject,
                        "Received Time": time
                    }

                    data.append(return_data)
    except Exception as e:
        print(f"An error occurred: {e}")

    return data

def unique_senders_count(username, app_password, days=7):
    unique_senders_count = Counter()

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
            for email_id in email_ids:
                # Fetch the email by ID
                status, email_data = mail.fetch(email_id, '(RFC822)')
                if status == "OK":
                    raw_email = email_data[0][1]
                    email_message = email.message_from_bytes(raw_email)

                    # Extract sender name
                    sender = email_message.get("From")

                    # Update the sender count
                    unique_senders_count[sender] += 1

    except Exception as e:
        print(f"An error occurred: {e}")

    unique_senders_list = [{"Sender": sender, "Count": count} for sender, count in unique_senders_count.items()]

    return unique_senders_list
