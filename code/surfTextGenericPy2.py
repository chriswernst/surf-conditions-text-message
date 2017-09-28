#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 07:19:39 2017

@author: ChrisErnst
github @chriswernst
"""
# This version works with Python 2

def sendSurfText():
	    
	import requests, bs4, time, datetime
	from twilio.rest import TwilioRestClient

	accountSID = 'aaaaaaa111111111' # Your Twilio SID here
	authToken = 'aaaaaaa111111111' # Your Twilio Token here

	twilioCli = TwilioRestClient(accountSID, authToken)

	myTwilioNumber = '+13105555555' # Your assigned Twilio Number
	# Required to send outgoing texts. If unused for 30 days, number will be lost
	myCellPhone = '+13105555555' #The number you want to text here

    surf = requests.get('http://www.ndbc.noaa.gov/station_page.php?station=46221')
    tides = requests.get('http://tides.mobilegeographics.com/locations/5620.html')
    # completes the http request        
    
	surf.raise_for_status()
	tides.raise_for_status()
	# No response is good news!

	surfStatusCode = surf.status_code
	tidesStatusCode = tides.status_code
	# The above lines are not mandatory, it simply gives you the status code
	# If this returns a 200, that is OK: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes

	soupSurfPage = bs4.BeautifulSoup(surf.text, "lxml")
	soupTidePage = bs4.BeautifulSoup(tides.text, "lxml")        
	# Creates a couple beautiful soup object in lxml 
	     
    wave = soupSurfPage.select('td')
    tidePre = soupTidePage.select('pre')
    # Selects the CSS tags 'td' and 'pre' in the HTML code       

     #then this parses off the rest
    tideText = tidePre[0].getText()
    selectTideText = (tideText[50:378]) 
    
	# Want to choose the CSS selectors the exact piece of the list of 'wave'
	# e.g. wave[20-35] is roughly where is forecast is

	waveHeight = wave[20].getText()
	# Extracts the 20th 'td' CSS tag which is the Wave Height

	waterTemp = wave[32].getText()
	# Extracts the 32nd 'td' CSS tag which is the Water Temperature

	meanWaveDirection = wave[29].getText()
	# Extracts the 29th 'td' CSS tag which is the Wave Direction

	wave = soupSurfPage.select('[class=titleDataHeader]')
	# This selects the relevant class where the header data is located

	update = wave[0].getText()
	# Parses the header
	 
    message = twilioCli.messages.create(body=
                        ('\n\n\n' + 'Surf Report:' + '\n\n' + waveHeight + ', Water Temp:' + waterTemp + 
                         ', Wave Direction: '+ meanWaveDirection
                         + '\n\n' + 'TIDES:\n' + selectTideText + 
                         '\n\n' + update[0:14]+'Buoy '+ update[14:38]+ ', '+ update[50:60]), 
                        from_=myTwilioNumber, to=myCellPhone)
                        
    # Write a SMS text with the waveheight, waterTemp, and waveDirection

# Example of SMS Response:
# Surf Report:
#
#  3.0 ft, Water Temp: 72.0 °F, Wave Direction: SSW ( 209 deg true )
#
# 3:37 AM low -0.04 ft.
# 9:49 AM high 4.79 ft.
# 3:22 PM low 1.46 ft.
# 9:28 PM high 5.95 ft.
#
# Conditions at Buoy 46221 as of(7:30 am PDT), 09/05/2017

sendSurfText()
