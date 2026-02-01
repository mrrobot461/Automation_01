import smtplib
from email.message import EmailMessage

msg = EmailMessage()
msg.set_content("This is an automated email sent from Python 2.")

sender = "zobelahadu@gmail.com"
Recipient = "gashafeysa@gmail.com"

msg["Subject"] = "Test Automation Email"
msg["From"] = sender
msg["To"] = Recipient

try:
 with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    try:
     server.login("zobelahadu@gmail.com", "ipopskttsctstqib")
    except smtplib.SMTPAuthenticationError:
      print("Login failed: check your email/password or app password")
      raise 
    except Exception as e:
      print(f"Unexpected login error: {e}")
      raise
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



print("Email sent.")
