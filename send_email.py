import smtplib
import re
from email.message import EmailMessage


msg = EmailMessage()
msg.set_content("This is an automated email sent from Python 2.")

sender = "zobelahadu@gmail.com"
recipient = "gashafeysa@gmail.com"
regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
password = "ipopskttsctstqib"

def main():
    msg["Subject"] = "Test Automation Email"
    msg["From"] = sender
    msg["To"] = recipient

    try:
      with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
       try:
        server.login(sender, password )
       except smtplib.SMTPAuthenticationError:
        print("Login failed: check your email/password or app password")
       except Exception as e:
        print(f"Unexpected login error: {e}")
      try:
        server.send_message(msg)
        print("Message Sent Successfully")
      except smtplib.SMTPRecipientsRefused:
        print("Failed to send: recipient email not found")
      except Exception as e:
                print(f"Unexpected error sending email: {e}")
    except smtplib.SMTPConnectError:
          print("Failed to connect to the server: check internet connection")
    except Exception as e:
        print(f"Some other error occurred: {e}")


def validator(email,pattern):
   return bool(re.match(pattern,email))

if not validator(sender,regex):
   print ("Invalid Sender Email")

elif not validator(recipient,regex):
   print ("Invalid Recipeint Email")

else:
 main()
   

