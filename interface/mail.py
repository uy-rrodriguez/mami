#!/usr/bin/python
# -*- coding: utf-8 -*-

#############################################################################
#    Mail :                                                                 #
#        Classe pour envoyer les alertes à des addresses mail.              #
#        Permet la définition d'un fichier de template qui sera chargé avec #
#        les données correspondantes avant d'être envoyé.                   #
#                                                                           #
#############################################################################

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


#############################################################################
#    Mail.                                                                  #
#############################################################################

class Mail:
    FROM = "uyric.gm@gmail.com"
    PWD = "uyric9090"
    TO = "rr.ricci@gmail.com"

    def __init__(self):
        self.smtp = smtplib.SMTP("smtp.gmail.com", "587")
        self.smtp.ehlo()
        self.smtp.starttls()
        self.smtp.login(self.FROM, self.PWD)

    def send(self, subject):
        # On ouvre le fichier template
        fp = open("mail_template.html", "rb")
        template = fp.read()
        fp.close()

        msg = MIMEMultipart('alternative')

        msg.attach(MIMEText(template, 'plain'))
        msg.attach(MIMEText(template, 'html'))

        msg['Subject'] = subject
        msg['From'] = self.FROM
        msg['To'] = self.TO

        # On envoie via SMTP
        self.smtp.sendmail(self.FROM, [self.TO], msg.as_string())

    def __destroy__(self):
        self.smtp.quit()


#############################################################################
#    Main pour tester le module.                                            #
#############################################################################

def main():
    print("Mail")
    m = Mail()
    m.send("Mami t'informe")

if __name__=='__main__':
    main()
