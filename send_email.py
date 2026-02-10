import smtplib
import re
import logging
import os
import datetime
import yaml
import subprocess
from pathlib import Path
from email.message import EmailMessage
from logging.handlers import RotatingFileHandler




BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config.yaml"

with open(CONFIG_PATH, "r") as f:
  
    config = yaml.safe_load(f)

BASE_DIR = Path(__file__).resolve().parent
LOG_PATH = BASE_DIR / "email_app.log"

BASE_DIR = Path(__file__).resolve().parent
RECIPIENTS_PATH = BASE_DIR / "recipients.txt"

cron_config = config.get("cron", {})
minute = cron_config.get("minute", "*")
hour = cron_config.get("hour", "*")
day_of_month = cron_config.get("day_of_month", "*")
month = cron_config.get("month", "*")
day_of_week = cron_config.get("day_of_week", "*")

BASE_DIR = Path(__file__).resolve().parent
SCRIPT_PATH = BASE_DIR / "send_email.py"
LOG_PATH = BASE_DIR / "cron_output.log"

cron_line = f"{minute} {hour} {day_of_month} {month} {day_of_week} /usr/bin/python3 {SCRIPT_PATH} >> {LOG_PATH} 2>&1"

# Write to current user's crontab
try:
    # Get existing crontab
    existing_cron = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    cron_jobs = existing_cron.stdout if existing_cron.returncode == 0 else ""
    
    # Avoid duplicate entries
    if cron_line not in cron_jobs:
        cron_jobs += cron_line + "\n"
        process = subprocess.run(["crontab", "-"], input=cron_jobs, text=True)
        print("Cron job installed/updated successfully.")
    else:
        print("Cron job already exists.")
except Exception as e:
    print("Error setting cron job:", e)




    
DRY_RUN = config["app"]["dry_run"]


execution_id = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")



logger = logging.getLogger("email_sender")
logger.setLevel(logging.INFO)


handler = RotatingFileHandler(
   LOG_PATH,
    maxBytes=100000,
    backupCount=5
)

formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(execution_id)s | %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)



sender = config["email"]["sender_email"]
regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
password = config["auth"]["sender_password"]


def validator(email, pattern):
    return bool(re.match(pattern, email))


def read_recipients(file):
    recipients = []
    try:
        with open(file ,"r") as f:
            recipients = [line.strip() for line in f if line.strip()]
    except Exception as e:
        logger.error(f"Failed to read recipients file: {e}", extra={"execution_id": execution_id})
    return recipients
def send_email(recipient,msg,server):
            server.send_message(msg)
            logger.info(f"Message Sent to: {recipient} Successfully", extra={"execution_id": execution_id})
            

def processor(recipients,server=None,dry_run=True):
    sent_counter = 0
    invalid_counter = 0
    bounced_counter = 0
    for recipient in recipients:
        if not validator(recipient, regex):
            logger.warning(f"Invalid recipient Email: {recipient}", extra={"execution_id": execution_id})
            invalid_counter += 1
            continue

        if dry_run:
            logger.info(f"DRY RUN: Would send email to {recipient}", extra={"execution_id": execution_id})
            sent_counter += 1
            continue
        
      
        msg = EmailMessage()
        msg["Subject"] = "Test Automation Email"
        msg["From"] = sender
        msg["To"] = recipient
        msg.set_content("This is an automated email sent from Python.")

        try:
            send_email(recipient, msg, server)
            sent_counter += 1
        except smtplib.SMTPRecipientsRefused:
            logger.warning(f"Failed to send: recipient email {recipient} not found", extra={"execution_id": execution_id})
            bounced_counter += 1
        except Exception as e:
            logger.error(f"Unexpected error sending email to {recipient}: {e}", extra={"execution_id": execution_id})
            bounced_counter += 1

    return {
        "sent": sent_counter,
        "invalid": invalid_counter,
        "bounced": bounced_counter
    }

def main():
    

    if not password:
        logger.critical("Email_Password environment variable not set", extra={"execution_id": execution_id})
        return

    if not validator(sender, regex):
        logger.error("Invalid Sender Email", extra={"execution_id": execution_id})
        return
    
    recipients = read_recipients(RECIPIENTS_PATH)

    if not recipients:
        logger.error("Unable to access recipient file", extra={"execution_id": execution_id})
        return
    
    server = None
    if DRY_RUN == False:
        try:
           server = smtplib.SMTP_SSL(config["email"]["smtp_server"], config["email"]["smtp_port"])
           server.login(sender, password)

        except smtplib.SMTPAuthenticationError:
            logger.error("Login failed: check your email/password or app password", extra={"execution_id": execution_id})
            return
        except Exception as e:
            logger.error(f"Unexpected login error: {e}", extra={"execution_id": execution_id})
            return

    report = processor(recipients, server=server, dry_run=DRY_RUN)

    if server:
        server.quit()

    executive_report = (
        f"Executive Report----------------------\n"
        f"Sent emails: {report['sent']}\n"
        f"Invalid emails: {report['invalid']}\n"
        f"Bounced emails: {report['bounced']}"
    )
    logger.info(executive_report, extra={"execution_id": execution_id})


if __name__ == "__main__":
    main()