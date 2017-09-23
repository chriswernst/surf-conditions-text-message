#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 23:30:37 2017

@author: ChrisErnst
"""

# def sendSurfText():
    
import requests, bs4, time, datetime
from twilio.rest import TwilioRestClient


accountSID = 'ACdc4349031e6b84317d5094068c68e1e8'
authToken = 'bb2c8170acf11297272709a35b1fea25'

twilioCli = TwilioRestClient(accountSID, authToken)

myTwilioNumber = '+13109058114'
# Required to send outgoing texts. This is foregone if unused for 30days

myCellPhone = '+13104334826'
#myCellPhone = '+12138840477'



surf = requests.get('http://www.ndbc.noaa.gov/station_page.php?station=46221')
tides = requests.get('https://tidesandcurrents.noaa.gov/noaatidepredictions.html?id=9410840&legacy=1')
# completes the http request        

surf.raise_for_status()
tides.raise_for_status()
# No response is good news!

surfStatusCode = surf.status_code
tidesStatusCode = tides.status_code
# If this returns a 200, that is OK: 
# https://en.wikipedia.org/wiki/List_of_HTTP_status_codes

soupSurfPage = bs4.BeautifulSoup(surf.text, "lxml")
soupTidePage = bs4.BeautifulSoup(tides.text, "lxml")        
# creates a beautiful soup object in lxml format

        
wave = soupSurfPage.select('td')
tidesTD = soupTidePage.select('td')
# Selects the CSS tags 'td' in the HTML code        

# want to choose the CSS selectors the exact piece of the list of 'wave'
# e.g. wave[20-35] is roughly where is forecast is

#then this parses off the rest

waveHeight = wave[20].getText()
# Extracts the 20th 'td' CSS tag which is the Wave Height

waterTemp = wave[32].getText()
# Extracts the 32nd 'td' CSS tag which is the Water Temperature

meanWaveDirection = wave[29].getText()
# Extracts the 29th 'td' CSS tag which is the wave direction

# Tidal data extraction:
tide1Time = tidesTD[0].getText()
tide1Type = tidesTD[1].getText()
tide1Height = tidesTD[2].getText()

tide2Time = tidesTD[3].getText()
tide2Type = tidesTD[4].getText()
tide2Height = tidesTD[5].getText()

tide3Time = tidesTD[6].getText()
tide3Type = tidesTD[7].getText()
tide3Height = tidesTD[8].getText()

tide4Time = tidesTD[9].getText()
tide4Type = tidesTD[10].getText()
tide4Height = tidesTD[11].getText()


wave = soupSurfPage.select('[class=titleDataHeader]')
# This selects the relevant class where our data is located

update = wave[0].getText()


 
message = twilioCli.messages.create(body=
                    ('\n\n\n' + 'Surf Report:' + '\n\n' + waveHeight + ', Water Temp:' + waterTemp + 
                     ', Wave Direction: '+ meanWaveDirection
                     + '\n\n' + tide1Time + ' ' + tide1Type + tide1Height
                     + '\n' + tide2Time + ' ' + tide2Type + tide2Height
                     + '\n' + tide3Time + ' ' + tide3Type + tide3Height 
                     + '\n' + tide4Time + ' ' + tide4Type + tide4Height + 
                     '\n\n' + update[0:14]+'Buoy '+ update[14:39]+ ', '+ update[50:61]), 
                    from_=myTwilioNumber, to=myCellPhone)
                    
# Write a SMS text with the waveheight, waterTemp, and waveDirection


