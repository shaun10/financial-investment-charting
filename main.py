import os
import smtplib
import charting
import time
import requests
from flask import Flask, render_template, url_for, request, redirect, flash, Response
from flask_mail import Mail
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

app = Flask(__name__)
mail = Mail(app)
app.secret_key = os.environ['secret_key']
app.config['MAILGUN_KEY'] = os.environ['MAILGUN_API_KEY']
app.config['MAILGUN_DOMAIN'] = os.environ['MAILGUN_DOMAIN']

mail.init_app(app)

class Charts(object):
	def __init__(self, tickers):
		self.tickers = tickers
		self.image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "/images/")

	def create_charts(self):
		for chart in range(len(self.tickers)):
			charting.graphData(self.tickers[chart], 50, 100)
			time.sleep(8)


	def send_mail(to_address, from_address, subject, plaintext):
		chart_files = [("attachment", open(image)) for image in os.listdir(self.image_path)]
		r = requests.\
		    post("https://api.mailgun.net/v2/%s/messages" % app.config['MAILGUN_DOMAIN'],
		        auth=("api", app.config['MAILGUN_KEY']),
		        files=chart_files,
		         data={
		             "from": from_address,
		             "to": to_address,
		             "subject": subject,
		             "text": plaintext
		         }
		     )
	   	return r


	def send_email_old(self):
		me = os.environ['MAIL_USERNAME']
		pwd = os.environ['MAIL_PASSWORD']
		os.chdir(self.path)
		images = os.listdir(self.image_path)
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
		try:
			for image in images:
				if not ".txt" in image:
					os.remove(self.path + image)
		except Exception:
			raise


if __name__ == '__main__':
	while 1:
		tickers = ["AAPL"] #Ticker list you would like to chart, type=list
		#email = Add to whom you would like to send emails, type=list
		subject = "Daily Stock Charts {}".format(str(charting.today.today()))
		message = text_message = "You need to buy!"
		daily = Charts(tickers)
		daily.create_charts()
		daily.send_mail(os.environ['MAIL_USERNAME'], os.environ['MAILGUN_SMTP_LOGIN'], subject, text_message)
		daily.delete_images()
		time.sleep(86400)