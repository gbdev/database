import urllib3
import datetime

class Logger():
    def __init__(self):
        # since this error is gonna be prompted many times making everything too verbose
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        # global logger: it will be used to diagnose what's wrong (skipped files, 404 errors...)
        self.fd = open("log.txt", 'w+')
        
    def write(self, msgtype, msg):
        currentTime = datetime.datetime.now()
        self.fd.write(str(msgtype) + " " + str(currentTime) + ':' + msg + "\n")

    def close(self):
        self.fd.close()

