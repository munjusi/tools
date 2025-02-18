#!/usr/bin/env python3
# A simple script that checks whether a server is up and sends an email notification if the server is down
# Uses SMTP auth 

"""For the script to send emails, you need to add the following environment variables
SMTP_SERVER eg export SMTP_SERVER=mail.myserver.com
SMTP_PORT eg export SMTP_PORT=465
FROM_EMAIL eg export FROM_EMAIL=me@myserver.com
SMTP_PASS eg export SMTP_PASS=myverysecurepassword
TO_EMAIL eg export TO_EMAIL=recipient@theirdomain.com"""

import platform
import subprocess  
import os  
import smtplib  
from email.mime.text import MIMEText  
from email.utils import formataddr  
from datetime import datetime

# Retrieve environment variables for SMTP configuration.
smtp_server = os.getenv('SMTP_SERVER')  
smtp_port = os.getenv('SMTP_PORT')  
from_address = os.getenv('FROM_EMAIL')  
smtp_pass = os.getenv('SMTP_PASS')  

# Retrieve the recipient's email address from environment variables.
email_recipient = os.getenv('TO_EMAIL')

# Define the server to monitor (IP address or hostname).
server = '192.168.10.32'

time = datetime.now()
time = time.strftime("%Y-%m-%d %H:%M:%S")
try:
    ping_count = "-c 20" if platform.system().lower() != "windows" else "-n 20" #checks whether the os is linux or windows
    # Ping the server 20 times to check if it's reachable.
    # `subprocess.run` runs the command and captures the output.
    ping = subprocess.run(['ping', ping_count, server], capture_output=True, text=True, check=True)
    
     
except subprocess.CalledProcessError as e:
    #Prepare an email notification.
    subject = f"Server {server} is currently down"  # Email subject.
    body = f"This is to notify you that server {server} was down at {time}. \n {e.stdout}" # Email body.

    # Create a plain text email message.
    message = MIMEText(body, "plain")
    
    # Format the "From" address with a display name.
    message["From"] = formataddr(('Server Monitor', from_address))
    
    # Set the recipient's email address.
    message["To"] = email_recipient
    
    # Set the email subject.
    message["Subject"] = subject

    try:
        # Connect to the SMTP server and send the email.
        with smtplib.SMTP(smtp_server, smtp_port) as mailserver:
            mailserver.starttls()  # Upgrade the connection to TLS for security.
            mailserver.login(from_address, smtp_pass)  # Log in to the SMTP server.
            mailserver.sendmail(from_address, email_recipient, message.as_string())  # Send the email.
            print("Email sent successfully")  # Notify that the email was sent.

    except Exception as er:
        # Handle any errors that occur during email sending.
        print(f"SMTP Error: {er}")

    exit(1)  # Exit the script 