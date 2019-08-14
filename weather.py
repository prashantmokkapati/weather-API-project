#Import the necessary packages
import urllib.request
import json
import smtplib, ssl
import schedule
import time

def job():
	#The key for the Dark Sky weather API
	key = """Enter your own key here"""

	longitude = """Enter your own info here"""
	latitude = """Enter your own info here"""

	#Defining port and server smtp
	port = 465
	smtp_server = "smtp.gmail.com"

	#Email information
	sender_email = """Enter your own info here"""
	receiver_email = """Enter your own info here"""
	password = """Enter your own info here"""

	#Creating API url to return weather data for a specific place
	url = 'https://api.darksky.net/forecast/' + key + '/' + latitude + ',' + longitude + '?exclude=currently,minutely,hourly,alerts,flags'

	#Opens the given url, then reads and stores the data into a variable
	response = urllib.request.urlopen(url).read()
	json_obj = str(response,'utf-8')
	data = json.loads(json_obj)

	#Break down data so it focuses on the necessary section
	condensedData = data['daily']['data']

	#Function determines if there will be rain or not depending on data from weather API
	def rain():
		precipVar = condensedData[0]['precipIntensity']
		if precipVar == 0:
			return "No"
		else:
			return "Yes"

	#Message the email will send
	message = "\nIn *Your Location* today: \n\n\n" + "The highest temperature is " + str(condensedData[0]['temperatureMax']) + " F\n" + "The lowest temperature is " + str(condensedData[0]['temperatureMin']) + " F"+ "\nSummary for the day: " + str(condensedData[0]['summary']) + "\n Will there be rain? " + rain() + "\n\n\nPowered by Dark Sky" + "\nhttps://darksky.net/poweredby/"

	#Creating a ssl context
	context = ssl.create_default_context()

	#Function to send the email
	with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
		server.login(sender_email, password)
		server.sendmail(sender_email, receiver_email, message)

#Job runs at 7:30 AM everyday
schedule.every().day.at("07:30").do(job) # Enter whatever time you wish

#Function to space the program runs out
while 1:
    schedule.run_pending()
    time.sleep(1)
