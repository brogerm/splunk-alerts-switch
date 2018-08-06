import os, urllib, httplib2, json, threading 
from time import sleep
from tkinter import *

BASE_URL = None
USER = None
PASSWORD = None
SESSION_KEY = None
myhttp = httplib2.Http(disable_ssl_certificate_validation=True)

def connect(urlPrefix, username, password):
	"""
		Creates a connection with a Splunk enterprise instance and 
		sets a global session key to be used in subsequent requests.
		Parameters:
			urlPrefix (required) = the base URL for all requests (i.e. https://host:port)
			username (required) = Splunk username
			password (required) = Splunk password
	"""
	print("[CONNECT]")
	global BASE_URL, USER, PASSWORD
	BASE_URL = urlPrefix
	USER = username
	PASSWORD = password
	
	response, content = myhttp.request(
		BASE_URL + '/services/auth/login?output_mode=json',
		'POST',
		headers={},
		body=urllib.parse.urlencode({'username':username, 'password':password, 'autoLogin':True}))
		
	decodedContent = json.loads(content.decode('utf-8'))
	
	if response.status == 200:
		global SESSION_KEY
		SESSION_KEY = decodedContent["sessionKey"]
		print("Successfully connected to Splunk server")
	else:
		errorMessage = decodedContent["messages"][0]["text"]
		raise Exception("%s - %s" % (response.status, errorMessage))


def disableAlerts(alertsByApp, disableDuration=0):
	"""
		Disables alerts.
		Parameters:
			alertsByApp (required) = A JSON object with the following format { "appName": ["alert1","alert2"] }
			disableDuration (optional) = How long to disable the alerts (in minutes). If not set, the alerts must be enabled manually
	"""
	for app, alerts in alertsByApp.items():
		for alert in alerts:
			alert = alert.replace(' ', '%20')
			url = BASE_URL + ("/servicesNS/%s/%s/saved/searches/%s?output_mode=json" % (USER, app, alert))
				
			response, content = myhttp.request(
				url,
				'POST', 
				headers={'Authorization':('Splunk %s' % SESSION_KEY)},
				body=urllib.parse.urlencode({'disabled':True}))

			decodedContent = json.loads(content.decode('utf-8'))
			
			if response.status != 200:
				errorMessage = json.loads(content.decode('utf-8'))["messages"][0]["text"]
				raise Exception(errorMessage)

	if disableDuration:
		thread = threading.Thread(target=autoEnableAlerts, args=(alertsByApp, disableDuration))
		thread.start()
		return("Successfully disabled %s. They will automatically be enabled after %s minutes.\nDO NOT stop this script!" % (alertsByApp, disableDuration))
	else:
		return("Successfully disabled %s" % alertsByApp)
		
				
def enableAlerts(alertsByApp):
	"""
		Enables alerts.
		Parameters:
			alertsByApp (required) = A JSON object with the following format { "appName": ["alert1","alert2"] }
	"""
	for app, alerts in alertsByApp.items():
		for alert in alerts:
			alert = alert.replace(' ', '%20')
			url = BASE_URL + ("/servicesNS/%s/%s/saved/searches/%s?output_mode=json" % (USER, app, alert))
				
			response, content = myhttp.request(
				url,
				'POST', 
				headers={'Authorization':('Splunk %s' % SESSION_KEY)},
				body=urllib.parse.urlencode({'disabled':False}))

			decodedContent = json.loads(content.decode('utf-8'))
			
			if response.status != 200:
				errorMessage = json.loads(content.decode('utf-8'))["messages"][0]["text"]
				raise Exception(errorMessage)

	return("Successfully enabled %s" % alertsByApp)

	
def autoEnableAlerts(alertsByApp, disableDuration):
	"""
		Enables alerts after the specified time.
		Parameters:
			alertsByApp (required) = A JSON object with the following format { "appName": ["alert1","alert2"] }
			disableDuration (required) = How long to disable the alerts (in minutes)
	"""
	def callEnable():
		connect(BASE_URL, USER, PASSWORD) # reconnect in case the disableDuration was longer than an hour
		print(enableAlerts(alertsByApp))
		master.destroy() # close the current tkinter window
		
	def callAutoEnable():
		thread = threading.Thread(target=autoEnableAlerts, args=(alertsByApp, 0.05))
		thread.start()
		master.destroy() # close the current tkinter window
		return
	
	sleep(disableDuration * 60) # transform to minutes
	master = Tk()
	master.title("Auto Enable Splunk Alerts")
	
	Label(master, text="Would you like to enable the following alerts?", anchor="w").grid(row=0, sticky=W)
	transformedAlerts = ("%s" % alertsByApp).replace(":",":\n").replace("',","'\n\t").replace("[","\t").replace("],","\n").replace("{","").replace("]}","")
	Message(master, text=transformedAlerts, anchor="w", width=300).grid(row=1, sticky=W)
	
	buttonFrame = Frame(master)
	buttonFrame.grid(row=2, column=0, columnspan=3)
	Button(buttonFrame, text='Yes', command=callEnable).grid(row=2, column=0, sticky=W, padx=4, pady=4)
	Button(buttonFrame, text="I'll do it manually", command=master.quit).grid(row=2, column=1, sticky=W, padx=4, pady=4)
	Button(buttonFrame, text='Remind me in 30 minutes', command=callAutoEnable).grid(row=2, column=2, sticky=W, padx=4, pady=4)
	
	master.mainloop()

	
