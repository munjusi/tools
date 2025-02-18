#!/usr/bin/env python3

#This is a simple script that checks whether a website is reachable
#If the website is unreachable, it sends an email and logs the occurence
#Requires a .env with smtp connection details


import requests
import logging
import os  
from dotenv import load_dotenv
import smtplib  
from email.mime.text import MIMEText  
from email.utils import formataddr  
from datetime import datetime


website = 'http://githubxyz.com'

#configure logging
logging.basicConfig(filename="/tmp/website.log",level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def email_sender(msg):
    load_dotenv()
    smtp_server = os.getenv('SMTP_SERVER')  
    smtp_port = os.getenv('SMTP_PORT')  
    from_address = os.getenv('FROM_EMAIL')  
    smtp_pass = os.getenv('SMTP_PASS')  
    email_recipient = os.getenv('TO_EMAIL')

    if not all([smtp_server,smtp_port,from_address,smtp_pass,email_recipient]):
        print("Variable not found") 
        exit(1)

    time = datetime.now()
    time = time.strftime("%Y-%m-%d %H:%M:%S")
    subject = msg  # Email subject.
    body = f"This is to notify you that website {website} was unreachable at {time}. \n" # Email body.

    # Create a plain text email message.
    message = MIMEText(body, "plain")
        
    # Format the "From" address with a display name.
    message["From"] = formataddr(('Server Monitor', from_address))
        
    # Set the recipient's email address.
    message["To"] = email_recipient
        
    # Set the email subject.
    message["Subject"] = subject
    print(smtp_port)
    try:
        
        # Connect to the SMTP server and send the email.
        with smtplib.SMTP(smtp_server, smtp_port) as mailserver:
            print(message)
            mailserver.set_debuglevel(1)
            mailserver.starttls()  # Upgrade the connection to TLS for security.
            mailserver.login(from_address, smtp_pass)  # Log in to the SMTP server.
            mailserver.sendmail(from_address, email_recipient, message.as_string())  # Send the email.
            logging.info("Email sent successfully")  # Notify that the email was sent.

    except Exception as er:
        # Handle any errors that occur during email sending.
        logging.error(f"SMTP Error: {er}")
try:
    response = requests.get(website,timeout=5)
    status_code = response.status_code
    website_status = 'up' if status_code == 200 else 'f"Unreachable: Status code:{status_code}"'
    if website_status =="down":
        status_message = "Website Down"
        email_sender(status_message)

except requests.exceptions.ConnectionError as e:
    status_message = "Name or service not known."
    email_sender(status_message)




exit(1)  # Exit the script 

        
        
      