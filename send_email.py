import smtplib,re,logging,os,uuid
from email.message import EmailMessage
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("email_sender")
logger.setLevel(logging.INFO)

handler =RotatingFileHandler(
    "email_app.log",
    maxBytes=1000,
    backupCount=5
)

formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
sender = "zobelahadu@gmail.com"
regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
password = os.getenv("EMAIL_PASSWORD")


def validator(email,pattern):
   return bool(re.match(pattern,email))
def main():

    if not password:
     logger.critical("Email_Password environment variable not set")
     return

    if not validator(sender, regex):
        logger.error("Invalid Sender Email")
        return

    try:
        with open("recipients.txt", "r") as f:
            recipients = [line.strip() for line in f if line.strip()]
    except Exception as e:
        logger.error(f"Failed to read recipients file: {e}")
        return

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            try:
                server.login(sender, password)
            except smtplib.SMTPAuthenticationError:
                logger.error("Login failed: check your email/password or app password")
                return
            except Exception as e:
                logger.error(f"Unexpected login error: {e}")
                return


            for recipient in recipients:
                if not validator(recipient, regex):
                    logger.warning(f"Invalid recipient Email: {recipient}")
                    continue

                msg = EmailMessage()
                msg["Subject"] = "Test Automation Email"
                msg["From"] = sender
                msg["To"] = recipient
                msg.set_content("This is an automated email sent from Python.")

                try:
                    server.send_message(msg)
                    logger.info(f"Message Sent to: {recipient} Successfully")
                except smtplib.SMTPRecipientsRefused:
                    logger.warning(f"Failed to send: recipient email {recipient} not found")
                except Exception as e:
                    logger.error(f"Unexpected error sending email to {recipient}: {e}")

    except smtplib.SMTPConnectError:
        logger.error("Failed to connect to the server: check internet connection")
    except Exception as e:
        logger.error(f"Some other error occurred: {e}")


main()
   

