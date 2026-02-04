import smtplib
import re
from email.message import EmailMessage
import logging


logging.basicConfig(
    filename = "email_app.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)



sender = "zobelahadu@gmail.com"
regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
password = "ipopskttsctstqib"


def validator(email,pattern):
   return bool(re.match(pattern,email))
def main():
    if not validator(sender, regex):
        logging.error("Invalid Sender Email")
        return

    try:
        with open("recipients.txt", "r") as f:
            recipients = [line.strip() for line in f if line.strip()]
    except Exception as e:
        logging.error(f"Failed to read recipients file: {e}")
        return

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            try:
                server.login(sender, password)
            except smtplib.SMTPAuthenticationError:
                logging.error("Login failed: check your email/password or app password")
                return
            except Exception as e:
                logging.error(f"Unexpected login error: {e}")
                return


            for recipient in recipients:
                if not validator(recipient, regex):
                    logging.warning(f"Invalid recipient Email: {recipient}")
                    continue

                msg = EmailMessage()
                msg["Subject"] = "Test Automation Email"
                msg["From"] = sender
                msg["To"] = recipient
                msg.set_content("This is an automated email sent from Python.")

                try:
                    server.send_message(msg)
                    logging.info(f"Message Sent to: {recipient} Successfully")
                except smtplib.SMTPRecipientsRefused:
                    logging.warning(f"Failed to send: recipient email {recipient} not found")
                except Exception as e:
                    logging.error(f"Unexpected error sending email to {recipient}: {e}")

    except smtplib.SMTPConnectError:
        logging.error("Failed to connect to the server: check internet connection")
    except Exception as e:
        logging.error(f"Some other error occurred: {e}")


main()
   

