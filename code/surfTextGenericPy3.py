#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 23:30:37 2017

@author: ChrisErnst
"""

# This version is currently working well with Python 3 on Rasberry Pi - Raspbian Linux

def sendSurfText():
    
    import requests, bs4
    from twilio.rest import Client
    
    accountSID = 'aaaaaaa111111111' # Your Twilio SID here
    authToken = 'aaaaaaa111111111' # Your Twilio Token here

    twilioCli = Client(accountSID, authToken)

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
    # If this returns a 200, that is OK: 
    # https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
    
    soupSurfPage = bs4.BeautifulSoup(surf.text, "html.parser")
    soupTidePage = bs4.BeautifulSoup(tides.text, "html.parser")    
    # creates a beautiful soup object 
    
    wave = soupSurfPage.select('td')
    tidePre = soupTidePage.select('pre')
    # Selects the CSS tags 'td' in the HTML code        
    
    #then this parses off the rest
    tideText = tidePre[0].getText()
    selectTideText = (tideText[50:378])
    
    # want to choose the CSS selectors the exact piece of the list of 'wave'
    # e.g. wave[20-35] is roughly where is forecast is
    waveHeight = wave[20].getText()
    # Extracts the 20th 'td' CSS tag which is the Wave Height
    
    waterTemp = wave[32].getText()
    # Extracts the 32nd 'td' CSS tag which is the Water Temperature
    
    meanWaveDirection = wave[29].getText()
    # Extracts the 29th 'td' CSS tag which is the wave direction
    
    wave = soupSurfPage.select('[class=titleDataHeader]')
    # This selects the relevant class where our data is located
    
    update = wave[0].getText()
    
    message = twilioCli.messages.create(body=
                        ('\n\n\n' + 'Surf Report:' + '\n\n' + waveHeight + ', Water Temp:' + waterTemp + 
                         ', Wave Direction: '+ meanWaveDirection
                         + '\n\n' + 'TIDES:\n' + selectTideText + 
                         '\n\n' + update[0:14]+'Buoy '+ update[14:38]+ ', '+ update[50:60]), 
                        from_=myTwilioNumber, to=myCellPhone)
                        
    # Write a SMS text with the waveheight, waterTemp, and waveDirection
                        
sendSurfText()