#TBD: добавить логирование, перенаправляя stdout? файловые операции, запрос к сайту, отправка письма. общий try except - print(Exception). в папку logs. notifieryy-mm-dd.log каждый день - новый файл, если файлов > 7 - удалять самый старый
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import requests
import os
if os.path.exists('settings_secret.py'):
	from settings_secret import *
else:
	from settings import *
import logging
from logging.handlers import RotatingFileHandler #просто import logging недостаточно!


# logger = logging.getLogger(__name__)
# logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s:%(message)s', filename='logs/notifier.log', encoding='utf-8', level=logging.INFO, datefmt='%m-%d-%Y %H:%M:%S') #вызывать 1 раз
#..., datefmt='%m/%d/%Y %I:%M:%S %p')
if not os.path.exists('logs'):
	os.mkdir('logs')
file_handler = logging.handlers.RotatingFileHandler(filename='logs/notifier.log', encoding='utf-8', mode='a', maxBytes=1000000, backupCount=2, delay=False)
handlers_list = [file_handler]
logging.basicConfig(handlers = handlers_list, format='%(asctime)s %(name)s line %(lineno)s %(levelname)s: %(message)s', level=logging.DEBUG, datefmt='%m-%d-%Y %H:%M:%S') #вызывать 1 раз
# logging.warning('Warning!')
# logging.info('INFO!')
# logging.error('Ошибка')
# logging.info('%s is cool', 'Max')
# exit()



def send_email():
	# create message object instance
	msg = MIMEMultipart()

	message = WATCH_URL

	# setup the parameters of the message
	msg['From'] = FROM_EMAIL
	msg['To'] = ", ".join(RECIPIENTS)
	msg['Subject'] = SUBJECT

	# add in the message body
	msg.attach(MIMEText(message, 'plain'))

	# create server
	server = smtplib.SMTP(SMTP_SERVER_PORT)

	server.starttls()

	# Login Credentials for sending the mail
	server.login(msg['From'], SMTP_PASSWORD)

	# send the message via the server.
	server.sendmail(msg['From'], RECIPIENTS, msg.as_string())

	server.quit()

	logging.info("Successfully sent email to %s:" % (msg['To']))


try:
	file_exists = os.path.exists(PAGE_FILENAME)
	res = requests.get(WATCH_URL)
	if res.status_code != 200:
		exit()
	new_page_str = res.text
	if not file_exists:
		with open(PAGE_FILENAME, 'w', newline='', encoding ='utf8') as f:
			f.write(new_page_str)
	else:
		with open(PAGE_FILENAME, 'r', newline='', encoding ='utf8') as f:
			last_page_str = f.read()
		if last_page_str != new_page_str:
			send_email()
		else:
			logging.debug('No changes')
		with open(PAGE_FILENAME, 'w', newline='', encoding='utf8') as f:
			f.write(new_page_str)

except Exception as e:
	logging.error(str(e) + ' ' + str(e.args))