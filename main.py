import os
import smtplib
import charting
import time
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

class Charts(object):
	def __init__(self, tickers, emails):
		self.tickers = tickers
		self.emails = emails
		#self.path = os.getcwd() + "/images/"
		self.path = os.path.dirname(os.path.realpath(__file__))+ "/images/"
	def create_charts(self):
		for chart in range(len(self.tickers)):
			charting.graphData(self.tickers[chart], 50, 100)
			time.sleep(8)
	def send_email(self):
		#pwd = 
		os.chdir(self.path)
		images = os.listdir(self.path)
		COMMASPACE = ', '
		#me = 
		msg = MIMEMultipart()
		msg['Subject'] = "Daily Stock Charts " + str(charting.today.today())
		#msg['Body'] = "Overall bearish close equities yesterday continued preference towards bonds, rate hike imminent 2015"
		#message_subject = "Daily Stock Charts " + str(charting.today.today())
		#message = "From: %s\r\n" % fromaddr
        #+ "To: %s\r\n" % toaddr
        #+ "CC: %s\r\n" % ",".join(cc)
        #+ "BCC: %s\r\n" % ",".join(bcc)
        #+ "Subject: %s\r\n" % message_subject
        #+ "\r\n" 
        #+ message_text
		msg['From'] = me
		msg["BCC"] = COMMASPACE.join(self.emails)
		for image in images:
			fp = open(image, 'rb')
			img = MIMEImage(fp.read(), _subtype="png")
			fp.close()
			msg.attach(img)
		smtpserver = smtplib.SMTP("smtp.mail.yahoo.com",587)
		smtpserver.ehlo()
		smtpserver.starttls()
		smtpserver.ehlo()
		smtpserver.login(me, pwd)
		smtpserver.sendmail(me, self.emails, msg.as_string())
		return "Email has been sent"
	def delete_images(self):
		os.chdir(self.path)
		images = os.listdir(self.path)
		for image in images:
			os.remove(self.path + image)
		return "Cleaner"

if __name__ == '__main__':
	#ticker = ["AAPL", "POT", "WWE", "UA", "SCTY", "AMZN", "KORS", "LNKD","TTWO","MSFT", "GOOGL","CMG", "EOG","DIS", "VZ", "TDY", "TASR", "NFLX", "PLD", "AMT", "FB", "F", "YHOO", "TLT", "TSLA", "AGNC", "USO", "YELP","TWTR", "GLD", "SPY", "AMBA", "GPRO", "WFM"]
	#email = #Add the email here to who this should be sent
	daily = Charts(ticker,email)
	daily.create_charts()
	daily.send_email()
	daily.delete_images()