# Overview 

A script for disabling/enabling Splunk alerts. 

# Setup
1. Set the following environment variables with their respective values
   > SPLUNK_USERNAME

   > SPLUNK_PASSWORD
2. Optionally set a "SPLUNK_BASE_URL" environment variable or modify "params.py" with the base url for your Splunk instance.
	(Note: the Splunk REST API runs on port 8089)
3. Modify "params.py"
	1. Modify the "alertsByApp" object with the names of the alerts to be disabled/enabled
	2. Optionally set the "disableDuration" if you want the alerts to automatically be enabled. You will be prompted before alerts are enabled.

# Running
Open Windows Command Prompt to the project directory and run
```
	python disable.py
```
Or
```
	python enable.py
```

# Disclaimer
The Splunk UI seems to be a bit out of sync with the operations performed by the REST API. Even after disabling
an alert with this script, the alert status will most likely still show that it is enabled in the Splunk UI. The Splunk UI
is incorrect, the alert is in fact disabled.  