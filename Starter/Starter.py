def send_mail():
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(sender, password)