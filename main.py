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
		me = os.environ['MAIL_USERNAME']
		pwd = os.environ['MAIL_PASSWORD']
		os.chdir(self.path)
		images = os.listdir(self.path)
		COMMASPACE = ', '
		msg = MIMEMultipart()
		msg['Subject'] = "Daily Stock Charts " + str(charting.today.today())
		#Add thoughts below on overall sentiment
		msg['Body'] = "None"
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
			if not ".txt" in image:
				os.remove(self.path + image)
		return "Cleaner"

if __name__ == '__main__':
	ticker = ["AAPL"] #Ticker list you would like to chart, type=list
	#email = Add to whom you would like to send emails, type=list
	daily = Charts(ticker,email)
	daily.create_charts()
	daily.send_email()
	daily.delete_images()