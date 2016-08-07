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
    HOST = "smtp.gmail.com"
    PORT = "587"
    FROM = "uyric.gm@gmail.com"
    PWD = ""

    def __init__(self):
        self.smtp = smtplib.SMTP(self.HOST, self.PORT)
        self.smtp.ehlo()
        self.smtp.starttls()
        self.smtp.login(self.FROM, self.PWD)

        # Paramètres qui sont définies en temps d'exécution
        self.params = {}


    # Ajoute un paramètres à remplacer
    def set_param(self, param, value):
        self.params[param] = value

    # Remplace tous les paramètres dans le texte par les valeurs stockés dans self.params
    def replace_params(self, text):
        for key, value in self.params.items():
            text = text.replace("<!--var:" + key + "-->", str(value))
        return text

    def send(self, to, subject, templateHTML="mail_template.html", templateTXT="mail_template.txt"):
        # On ouvre le fichier template HTML
        fp = open(templateHTML, "rb")
        templateHTML = fp.read()
        fp.close()

        # On ouvre le fichier template TXT
        fp = open(templateTXT, "rb")
        templateTXT = fp.read()
        fp.close()

        # Remplacement des paramètres
        templateHTML = self.replace_params(templateHTML)
        templateTXT = self.replace_params(templateTXT)

        msg = MIMEMultipart('alternative')
        msg.attach(MIMEText(templateTXT, 'plain'))
        msg.attach(MIMEText(templateHTML, 'html'))

        msg['Subject'] = subject
        msg['From'] = self.FROM
        msg['To'] = to

        # On envoie via SMTP
        self.smtp.sendmail(self.FROM, [to], msg.as_string())

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
