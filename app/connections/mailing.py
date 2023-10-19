import yaml
import imaplib
import email
from email.header import decode_header
from datetime import datetime, timedelta


def read_recent_emails(username, app_password, days=7):
    try:
        # Connect to the Gmail IMAP server.
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(username, app_password)

        # Select the mailbox you want to access (e.g., "inbox").
        mail.select("inbox")

        # Calculate the date range for filtering.
        today = datetime.today()
        start_date = (today - timedelta(days=days)).strftime("%d-%b-%Y")
        end_date = today.strftime("%d-%b-%Y")

        # Search for email messages within the specified date range.
        search_query = f'(SINCE "{start_date}" BEFORE "{end_date}")'
        status, email_ids = mail.search(None, search_query)

        if status == "OK":
            email_ids = email_ids[0].split()
            # Limit the number of emails to retrieve.
            max_emails = 5 if len(email_ids) >= 5 else len(email_ids)
            recent_emails = []

            for email_id in email_ids[-max_emails:]:
                # Fetch the email message using its ID.
                status, email_data = mail.fetch(email_id, "(RFC822)")
                if status == "OK":
                    raw_email = email_data[0][1]
                    msg = email.message_from_bytes(raw_email)
                    # Get email subject and sender.
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding or "utf-8")
                    from_ = msg.get("From")
                    body = ""
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(
                                decode=True).decode("utf-8")
                    recent_emails.append(
                        {"Subject": subject, "From": from_, "Body": body})

            # Logout and close the connection.
            mail.logout()

            return recent_emails
        else:
            return "Failed to retrieve emails."

    except Exception as e:
        return f"An error occurred: {str(e)}"

def count_emails_received(username, app_password, days=7):
    try:
        # Connect to the Gmail IMAP server.
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(username, app_password)

        # Select the mailbox you want to access (e.g., "inbox").
        mail.select("inbox")

        # Calculate the date range for filtering.
        today = datetime.today()
        start_date = (today - timedelta(days=days)).strftime("%d-%b-%Y")
        end_date = today.strftime("%d-%b-%Y")

        # Search for email messages within the specified date range.
        search_query = f'(SINCE "{start_date}" BEFORE "{end_date}")'
        status, email_ids = mail.search(None, search_query)

        if status == "OK":
            email_ids = email_ids[0].split()
            count = len(email_ids)

            # Logout and close the connection.
            mail.logout()

            return count
        else:
            return "Failed to retrieve email count."

    except Exception as e:
        return f"An error occurred: {str(e)}"
