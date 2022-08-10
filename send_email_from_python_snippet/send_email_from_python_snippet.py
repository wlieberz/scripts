#!/usr/bin/env python3

import smtplib, json

# Handling sensitive vars with secrets file.
# remember to keep this file locked down. 
SecretsFile = open('email_secrets.json')
jsonData = json.load(SecretsFile)
SecretsFile.close()

# Vars:
emailSubject = "Subject: hello from python\n\n"
emailBody = "Notification from python."
email = emailSubject + emailBody

# Setup connection:
conn = smtplib.SMTP(jsonData["smtpServer"], jsonData["smtpPort"])
conn.ehlo()
conn.starttls()
conn.login(jsonData["SenderUser"], jsonData["SenderPassword"])

# Send message:
conn.sendmail(jsonData["SenderUser"], jsonData["DestAddress"], email)

# Clean-up:
conn.quit()