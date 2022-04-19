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
import lxml.etree
from xmldiff import main, formatting

XSLT = u'''<?xml version="1.0"?>
<xsl:stylesheet version="1.0"
xmlns:diff="http://namespaces.shoobx.com/diff"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:template match="@diff:insert-formatting">
        <xsl:attribute name="class">
          <xsl:value-of select="'insert-formatting'"/>
        </xsl:attribute>
    </xsl:template>

    <xsl:template match="diff:delete">
        <del><xsl:apply-templates /></del>
    </xsl:template>

    <xsl:template match="diff:insert">
        <ins><xsl:apply-templates /></ins>
    </xsl:template>

    <xsl:template match="@* | node()">
      <xsl:copy>
        <xsl:apply-templates select="@* | node()"/>
      </xsl:copy>
    </xsl:template>
 </xsl:stylesheet>'''
XSLT_TEMPLATE = lxml.etree.fromstring(XSLT)

class HTMLFormatter(formatting.XMLFormatter):
     def render(self, result):
         transform = lxml.etree.XSLT(XSLT_TEMPLATE)
         result = transform(result)
         return super(HTMLFormatter, self).render(result)

formatter=HTMLFormatter(text_tags=('p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li'), formatting_tags=('b', 'u', 'i', 'strike', 'em', 'super', 'sup', 'sub', 'link', 'a', 'span'))


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



def send_email(last_page_str, new_page_str):
	# create message object instance
	msg = MIMEMultipart()
	parser = lxml.etree.HTMLParser()
	try:
		last_page_root = lxml.etree.fromstring(last_page_str, parser)[1][1][1] #<section>
		new_page_root = lxml.etree.fromstring(new_page_str, parser)[1][1][1]  #<section>
		#diff_page_str = main.diff_texts(last_page_str, new_page_str, diff_options={'fast_match': True}, formatter=formatter)
		diff_page_str = main.diff_trees(last_page_root, new_page_root, diff_options={'fast_match': True}, formatter=formatter)
		diff_ok = True
	except:
		diff_page_str = new_page_str
		diff_ok = False

	message = '<A HREF=' + WATCH_URL + '>' + WATCH_URL + '</A><P>' + diff_page_str

	# setup the parameters of the message
	msg['From'] = FROM_EMAIL
	msg['To'] = ", ".join(RECIPIENTS)
	msg['Subject'] = SUBJECT

	# add in the message body
	msg.attach(MIMEText(message, 'html'))

	# create server
	server = smtplib.SMTP(SMTP_SERVER_PORT)

	server.starttls()

	# Login Credentials for sending the mail
	server.login(msg['From'], SMTP_PASSWORD)

	# send the message via the server.
	server.sendmail(msg['From'], RECIPIENTS, msg.as_string())

	server.quit()

	logging.info("Successfully sent email to %s:" % (msg['To']) + 'diff OK: ' + str(diff_ok) )


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
			send_email(last_page_str, new_page_str)
		else:
			logging.debug('No changes')
		with open(PAGE_FILENAME, 'w', newline='', encoding='utf8') as f:
			f.write(new_page_str)

except Exception as e:
	logging.error(str(e) + ' ' + str(e.args))