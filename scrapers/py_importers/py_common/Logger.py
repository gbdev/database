import urllib3
import datetime

class Logger():
    def __init__(self, log_mode):
        self.log_mode = log_mode

        # since this error is gonna be prompted many times making everything too verbose
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        # global logger: it will be used to diagnose what's wrong (skipped files, 404 errors...)
        # log_mode: if set to LOG, it will log to file, else it will normally print on your console
        if self.log_mode == "LOG" or self.log_mode == "log":
            self.fd = open("log.txt", 'w+')
        
    def write(self, msgtype, msg):
        currentTime = datetime.datetime.now()
        outstring = str(msgtype) + " " + str(currentTime) + ':' + msg + "\n"

        # if LOG mode is activated, it will print in file, else it will print on console
        if self.log_mode == "LOG" or self.log_mode == "log":
            self.fd.write(outstring)
        else:
            print(outstring)

    def close(self):
        self.fd.close()

