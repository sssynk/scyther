import smtpd
import asyncore
import email
import re
import requests

class CustomSMTPServer(smtpd.SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data, mail_options=None, rcpt_options=None):
        print("Message recd")
        # get 6 digit code from data (search for 6 digit ints which are surrounded in \n)
        code = re.search(r'<h2>(\d{6})</h2>', data.decode('utf-8'))
        if code:
            print("Code found: " + code.group(1) + " to email " +rcpttos[0])
            requests.get("https://WEBHOOK.COM/send?email=" + rcpttos[0] + "&code=" + code.group(1))
            print("Code sent to acc gen")
        else:
            print("Code not found")
        return

server = CustomSMTPServer(('0.0.0.0', 25), None)

print("[scyther-mail] Server running on *:25")

asyncore.loop()
