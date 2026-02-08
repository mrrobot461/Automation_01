import smtplib
import re
import logging
import os
import datetime
from email.message import EmailMessage
from logging.handlers import RotatingFileHandler

DRY_RUN = False

execution_id = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

logger = logging.getLogger("email_sender")
logger.setLevel(logging.INFO)

handler = RotatingFileHandler(
    "email_app.log",
    maxBytes=100000,
    backupCount=5
)

formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(execution_id)s | %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

sender = "zobelahadu@gmail.com"
regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
password = os.getenv("EMAIL_PASSWORD")

def validator(email, pattern):
    return bool(re.match(pattern, email))

def read_recipients(file):
    
    try:
        with open(file ,"r") as f:
            recipients = [line.strip() for line in f if line.strip()]
    except Exception as e:
        logger.error(f"Failed to read recipients file: {e}", extra={"execution_id": execution_id})
    return recipients
def send_email(recipient,msg,server):
            server.send_message(msg)
            logger.info(f"Message Sent to: {recipient} Successfully", extra={"execution_id": execution_id})
            
        


def main():
    sent_counter = 0
    invalid_counter = 0
    bounced_counter = 0


    if not password:
        logger.critical("Email_Password environment variable not set", extra={"execution_id": execution_id})
        return

    if not validator(sender, regex):
        logger.error("Invalid Sender Email", extra={"execution_id": execution_id})
        return
    
    recipients = read_recipients("recipients.txt")

    if not recipients:
        logger.error("Unable to access recipient file", extra={"execution_id": execution_id})
        return
    
    server = None
    if DRY_RUN == False:
        try:
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server.login(sender, password)
        except smtplib.SMTPAuthenticationError:
            logger.error("Login failed: check your email/password or app password", extra={"execution_id": execution_id})
            return
        except Exception as e:
            logger.error(f"Unexpected login error: {e}", extra={"execution_id": execution_id})
            return

    for recipient in recipients:
        if not validator(recipient, regex):
            logger.warning(f"Invalid recipient Email: {recipient}", extra={"execution_id": execution_id})
            invalid_counter += 1
            continue


        if DRY_RUN == True:

            logger.info(f"DRY RUN: Would send email to {recipient}", 
                        extra={"execution_id": execution_id})
            sent_counter += 1
            continue


        msg = EmailMessage()
        msg["Subject"] = "Test Automation Email"
        msg["From"] = sender
        msg["To"] = recipient
        msg.set_content("This is an automated email sent from Python.")

        try:
                send_email(recipient,msg,server)
                sent_counter+=1
        except smtplib.SMTPRecipientsRefused:
                logger.warning(f"Failed to send: recipient email {recipient} not found", extra={"execution_id": execution_id})
                bounced_counter+=1
        except Exception as e:
                logger.error(f"Unexpected error sending email to {recipient}: {e}", extra={"execution_id": execution_id})
                bounced_counter+=1
   

    
    if server:
        server.quit()

    executive_report = (
        f"Executive Report----------------------\n"
        f"Sent emails: {sent_counter}\n"
        f"Invalid emails: {invalid_counter}\n"
        f"Bounced emails: {bounced_counter}"
    )
    logger.info(executive_report, extra={"execution_id": execution_id})


if __name__ == "__main__":
    main()
