#!/usr/bin/python
# -*- coding: utf-8 -*-

#############################################################################
#    Stockage :                                                             #
#        Module pour récuperer les alertes avec beautifulSoup.              #
#        récupération de la dernière alerte et du flux rss                  #
#                                                                           #
#                                                                           #
#                                                                           #
#############################################################################


from  bs4 import BeautifulSoup
import urllib
import re 
class scrapper(object):

	def _init_(self):
		self.alertes = []
		self.avis = []
		self.last_alert =[]



	def get_last_alert(self):
		r = urllib.urlopen('http://www.cert.ssi.gouv.fr/').read()
		soup = BeautifulSoup(r)
		
		corps=soup.find("td", {"class": "corps"})
		title=corps.findAll("td", {"class": "mg"})
		alert=corps.find("a", {"class": "mg"})
		print(title[1].contents)
		print(alert['href'])
		print(title[1])

	def get_alert_cert_rss(self):
		rss = urllib.urlopen('http://www.cert.ssi.gouv.fr/site/cert-fr_alerte.rss').read()
		doc = BeautifulSoup(rss,'xml')
		for  item in doc.findAll('item'):
			print (item.find('title').contents)
			print (item.find('link').get('href'))

	def get_alert_cert_complet(self):
		rss = urllib.urlopen('http://www.cert.ssi.gouv.fr/site/cert-fr.rss').read()
		doc = BeautifulSoup(rss,'xml')

		for item in doc.findAll('item'):
			print (item.find('title').contents)
			print (item.find('link').contents)



#############################################################################
#    Main pour tester le module.                                            #
#############################################################################	



def main():
    s = scrapper()
    s.get_last_alert()
    

if __name__=='__main__':
    main()		

