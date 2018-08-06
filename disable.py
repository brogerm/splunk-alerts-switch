import splunkMethods as splunk
from params import Params

p = Params()

splunk.connect(p.baseurl, p.username, p.password)
print(splunk.disableAlerts(p.alertsByApp, p.disableDuration))