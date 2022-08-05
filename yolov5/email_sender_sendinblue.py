import smtplib

sender = "gauravbarua614@gmail.com"
receiver = "gauravbarua614@gmail.com"

message = f"""\
Subject: Hi Mailtrap
To: {receiver}
From: {sender}

This is a test e-mail message."""

with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
    server.login("f2100fc456e757", "2bc872e517a594")
    server.sendmail(sender, receiver, message)