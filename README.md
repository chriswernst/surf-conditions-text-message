# Python Surf Text automated with Raspberry Pi
[//]: # (Image References)

[image1]: ./images/text.jpg
[image2]: ./images/swell.jpg
[image3]: ./images/tides.jpg
[image4]: ./images/pizero.jpg


![][image1]

##### Overview
*Python Surf Text* scrapes NOAA sites to retrieve tide and buoy (swell height) for the Santa Monica Bay in California (Buoy #46221).

We will step through a brief overview, then go on to how to make this run remotely with the $10 Raspberry Pi Zero W.

##### Versioning
surfTextGenericPy2.py is for use with Python 2
surfTextGenericPy3.py is for use with Python 3

##### Dependencies
Both versions rely on the Python modules:
 - requests
 - beautifulSoup
 - time
 - datetime
 - twilio.rest

You must also have a Twilio account and active phone number set up. Learn more at https://www.twilio.com

##### Altering Swell and Tidal Data
The two lines of code you need to alter to change the location are the URLs we're creating beautifulSoup objects from. One for the swell:
`
surf = requests.get('http://www.ndbc.noaa.gov/station_page.php?station=46221')
`
And one for the tide:
`
tides = requests.get('https://tidesandcurrents.noaa.gov/noaatidepredictions.html?id=9410840&legacy=1')
`
As long as requests are made from those two sites' pages, the scraper should work correctly.

For referenence, they are scraping the data from:
![][image2]
![][image3]

##### *So this is great and all, but how do we automate the code to run remotely, and periodically send me a report of what's going on in the ocean?*
###
###
##### Automation
This can be done a variety of ways, but since I've been wanting to get more exposure to the Raspberry Pi, I decided to pick up the new Raspberry PI Zero W - which boasts WiFi, Bluetooth LE, and a 1 Ghz processor for $10! Check them out at: https://www.raspberrypi.org/products/raspberry-pi-zero-w/

![][image1]

**You'll also need to get:**
- Power Supply (5V, >2A) Micro USB
- 8GB or larger Micro SD
- USB to Micro USB OTG adapter
- Micro USB Hub (Not all compatible, one that is: https://www.amazon.com/LoveRPi-MicroUSB-Port-Raspberry-Zero/dp/B019BUA81U)
- HDMI adapter
- Wired/Wireless Keyboard & Mouse

Now you have your parts, we'll install Raspbian Jessie Linux OS onto the SD card. If your card came pre-installed with NOOBS, you may still want to do this as NOOBS updates are pushed regularly, and critical to operation. 

You'll want to download NOOBS (not NOOBS lite) from: https://www.raspberrypi.org/downloads/noobs/

Plug your microSD card into your computer. Make sure your card is wiped clean using software like that from sdcard.org

Once downloaded, extract those files, and drop into your newly formatted SD card(FAT format is suggested). An easy walkthrough of install is here: https://www.raspberrypi.org/documentation/installation/noobs.md

Now, plug in your Micro SD card, USB hub, HDMI, power supply(in the 'PWR' port), keyboard and mouse, and turn on the power. Raspian OS should start up. A green light on the device is a good sign.
#
###### Environment Setup
#
Once the system is up, go to the upper right-hand corner and setup your WiFi details.

Now, open a terminal (ctrl-alt-t on Linux) and type:
`sudo apt-get update`
then
`sudo apt-get upgrade`

Verify you have package manager for Python3 with:
`sudo apt-get install python3-pip`

and install the required modules with:
`pip3 install requests bs4 time datetime twilio`
#
###### File Transfer
#
We now need to get the python script onto the Raspberry Pi.

To go from my Raspberry Pi terminal out to my Mac, I used the command:
`scp UserName@192.XXX.X.XX:/Users/Path/To/surfTextGenericPy3.py ~`
(change UserName and IP address above to your personal details)

Make sure your save the file in the directory: `/home/pi/`  That `~` and the end of the line dictates the destination on the local machine.

 I'm not going to get into this heavily, but search `ssh`  and your OS + Raspberry Pi file transfer on Google if you get stuck.
#
###### Shell Script
#
In order to run the Python file we just transferred onto our Raspberry Pi, we need to make a call to it repeatedly.
Open a text editor on the Raspberry Pi, and type:
```
#!/bin/bash
cd
python3 surfTextGenericPy3.py
```
Save the file as `surfJob.sh` and put it in your home directory `/home/pi/`
###### Cron
#
We're going to use Cron to automate the running of the shell script we just created above, that runs the python script.  Learn more about Cron here: https://en.wikipedia.org/wiki/Cron

Open a new terminal and type:
`crontab -e`
If it asks you to select a text editor, choose `nano`

A text file should open up explaining how Cron and its syntax works. I'll leave the exploring up to you. Scroll to the bottom of this file and type:
`0 */3 * * * /home/pi/surfJob.sh`
This sets the `surfJob.sh` script to run every 3 hours, at zero minutes. 

As an example, to make it run every 6 hours, at the 15th minute, change it to: 
`15 */6 * * * /home/pi/surfJob.sh`
ctrl-x will exit, make sure to save your changes, and press enter to finalize saving.

##### And that's it! Keep your Raspberry Pi Zero W plugged in and it should continuously send you text updates!



