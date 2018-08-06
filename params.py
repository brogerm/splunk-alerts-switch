import os

class Params:
	def __init__(self):
		self.baseurl =  os.environ.get('SPLUNK_BASE_URL') if os.environ.get('SPLUNK_BASE_URL') else 'https://localhost:8089'
		self.username = os.environ.get('SPLUNK_USERNAME')
		self.password = os.environ.get('SPLUNK_PASSWORD')
		self.alertsByApp = {
			'appName': ["alert1","alert1"]
		}
		self.disableDuration = 0 # In minutes. If set to 0, alerts must be enabled manually
		