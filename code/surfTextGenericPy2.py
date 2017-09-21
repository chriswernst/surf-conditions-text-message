#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 07:19:39 2017

@author: ChrisErnst
github @chriswernst
"""

# This version works with Python 2

def main():
	    
	import requests, bs4, time, datetime
	from twilio.rest import TwilioRestClient


	accountSID = 'aaaaaaa111111111' # Your Twilio SID here
	authToken = 'aaaaaaa111111111' # Your Twilio Token here

	twilioCli = TwilioRestClient(accountSID, authToken)

	myTwilioNumber = '+13105555555' # Your assigned Twilio Number
	# Required to send outgoing texts. If unused for 30 days, number will be lost

	myCellPhone = '+13105555555' #The number you want to text here


	surf = requests.get('http://www.ndbc.noaa.gov/station_page.php?station=46221')
	tides = requests.get('https://tidesandcurrents.noaa.gov/noaatidepredictions.html?id=9410840&legacy=1')
	# Completes the http request for wave and tidal conditions specific to Buoy 46221 in Santa Monica Bay        

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
	tidesTD = soupTidePage.select('td')
	# Selects the CSS tags 'td' in the HTML code        

	# Want to choose the CSS selectors the exact piece of the list of 'wave'
	# e.g. wave[20-35] is roughly where is forecast is

	waveHeight = wave[20].getText()
	# Extracts the 20th 'td' CSS tag which is the Wave Height

	waterTemp = wave[32].getText()
	# Extracts the 32nd 'td' CSS tag which is the Water Temperature

	meanWaveDirection = wave[29].getText()
	# Extracts the 29th 'td' CSS tag which is the Wave Direction


	# Tidal data extraction:
	    
	# First tide of the day:
	tide1Time = tidesTD[0].getText()
	tide1Type = tidesTD[1].getText()
	tide1Height = tidesTD[2].getText()

	# Second tide of the day:
	tide2Time = tidesTD[3].getText()
	tide2Type = tidesTD[4].getText()
	tide2Height = tidesTD[5].getText()

	# Third tide of the day:
	tide3Time = tidesTD[6].getText()
	tide3Type = tidesTD[7].getText()
	tide3Height = tidesTD[8].getText()

	# Fourth tide of the day:
	tide4Time = tidesTD[9].getText()
	tide4Type = tidesTD[10].getText()
	tide4Height = tidesTD[11].getText()


	wave = soupSurfPage.select('[class=titleDataHeader]')
	# This selects the relevant class where the header data is located

	update = wave[0].getText()
	# Parses the header
	 
	message = twilioCli.messages.create(body=
	                    ('\n\n\n' + 'Surf Report:' + '\n\n' + waveHeight + ', Water Temp:' + waterTemp + 
	                     ', Wave Direction: '+ meanWaveDirection
	                     + '\n\n' + tide1Time + ' ' + tide1Type + tide1Height
	                     + '\n' + tide2Time + ' ' + tide2Type + tide2Height
	                     + '\n' + tide3Time + ' ' + tide3Type + tide3Height 
	                     + '\n' + tide4Time + ' ' + tide4Type + tide4Height + 
	                     '\n\n' + update[0:14]+'Buoy '+ update[14:39]+ ', '+ update[50:61]), 
	                    from_=myTwilioNumber, to=myCellPhone)
	                    
# Write a SMS text with the waveheight, waterTemp, and waveDirection with a few other stats

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

main()
