from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib
from typing import List
from fastapi import BackgroundTasks
from decorators.Threading import run_in_thread
from dotenv import load_dotenv, find_dotenv

from schemas.Emails import SendEmails
load_dotenv(find_dotenv('.env'))

class Envs:
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_FROM = os.getenv('MAIL_FROM')
    MAIL_PORT = os.getenv('MAIL_PORT')

@run_in_thread()
def send_email(to_email: str, subject: str,body:str):
    # email details
    username=Envs.MAIL_USERNAME
    email = Envs.MAIL_FROM
    password = Envs.MAIL_PASSWORD
    print(email)
    # create message object
    msg = MIMEMultipart()
    msg['From'] = f"{username} <{email}>"
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    # create SMTP session
    s = smtplib.SMTP(host = 'smtp.office365.com', port = Envs.MAIL_PORT,local_hostname='hotmail')

    s.starttls()
    # login with email and password
    s.login(email, password)

    # send message
    s.send_message(msg)
    print('zzz')

    # terminate session
    s.quit()

    return {"message": "Email sent successfully"}


@run_in_thread()
def send_emails(object:SendEmails):
    # email details
    username = Envs.MAIL_USERNAME
    email = Envs.MAIL_FROM
    password = Envs.MAIL_PASSWORD
    print(email)
    # create SMTP session
    s = smtplib.SMTP(host='smtp.office365.com', port=Envs.MAIL_PORT, local_hostname='hotmail')
    s.starttls()
    # login with email and password
    s.login(email, password)
    for to_email in object.emails:
        # create message object
        msg = MIMEMultipart()
        msg['From'] = f"{username} <{email}>"
        msg['To'] = to_email
        msg['Subject'] = object.subject
        msg.attach(MIMEText(object.body, 'plain'))
        # send message
        s.send_message(msg)
        print(f"Email sent to {to_email}")
    # terminate session
    s.quit()
    return {"message": "Email sent successfully"}

