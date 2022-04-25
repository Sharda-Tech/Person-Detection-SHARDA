#send an email using python

import smtplib

def send_email(mess):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('sh.dee2022@gmail.com', 'deepaksh2022')
    subject = "Count for TIPPER, TRUCK & TRACTOR"
    msg = f"Subject: {subject}\n\n\n{mess}"
    server.sendmail('sh.dee2022@gmail.com', 'gauravbarua614@gmail.com', msg)
    print("Email sent!")

x = {
  "Truck": '5',
  "Tipper": '10',
  "Tractor": '7'
}

if __name__=='__main__':
  send_email(x)