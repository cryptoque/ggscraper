import mysql.connector 
from bs4 import BeautifulSoup
import os
import re
import email 

class saveToDB:

	def __init__(self, baseDir):
		self.threadID = 0
		self.msgID = 0
		self.subject = ''
		self.date = ''
		self.sender = ''
		self.netIDSender = ''
		self.receiver = ''
		self.netIDReceiver = ''
		self.messageContent = ''
		
		self.baseDir = baseDir

	def listdir_nohidden(self, path):
		for f in os.listdir(path):
			if not f.startswith('.'):
				yield f

	def extractItems(self, message):
		msg = email.message_from_string(message)
		for part in msg.walk():
			if part.get_content_type() == 'text/plain':
				self.messageContent = part.get_payload()

		message = message.splitlines()		
		for line in message:
			if line.startswith('Date:'):
				self.date = str(line[6:])
				continue
			if line.startswith('From:'):
				sender = re.findall(r'[\w\.-]+@[\w\.-]+', line)
				self.sender = ','.join(sender) #get sender email address
				self.netIDSender = ','.join(list(map((lambda x: x.split('@')[0]), sender)))
				continue 
			if line.startswith('To:'):
				receiver = re.findall(r'[\w\.-]+@[\w\.-]+', line)
				self.receiver = ','.join(receiver)
				self.netIDReceiver = ','.join(list(map((lambda x: x.split('@')[0]), receiver)))
			if line.startswith('Subject:'):
				self.subject = str(line[9:])
	
	def saveItems(self, db):
		cur = db.cursor()

		cur.execute("""CREATE TABLE IF NOT EXISTS nethealthmsg(
			id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
			threadID int(11) NOT NULL,
			msgID int(11) NOT NULL,
			sentTime varchar(255) NOT NULL,
			subject varchar(255) NOT NULL,
			sender varchar(255) NOT NULL,
			netIDSender varchar(255) NOT NULL,
			receiver varchar(255) NOT NULL,
			netIDReceiver varchar(255) NOT NULL,
			messageContent LONGTEXT NOT NULL)""")
		db.commit()

		print('table nethealthmsg created...')

		add_params = ("INSERT INTO nethealthmsg "
				"(threadID, msgID, sentTime, subject, sender, netIDSender, receiver, netIDReceiver, messageContent) "
				"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")

		self.threadID = 0 
		for thread in self.listdir_nohidden(self.baseDir):
			self.msgID = 0 
			for message in self.listdir_nohidden(self.baseDir+'/'+thread):
				html = open(self.baseDir+'/'+thread+'/'+message, "r+").read()
				msg = BeautifulSoup(html, 'html.parser').get_text() # returns a list
				self.extractItems(msg) # update values 
				values = [self.threadID, self.msgID, self.date, self.subject, self.sender, self.netIDSender, self.receiver, self.netIDReceiver, self.messageContent]
				print(self.messageContent)
				print('values updated for 1 message...')
				cur.execute(add_params, values)
				db.commit()

				self.msgID += 1 
				print('1 message added...')

			self.threadID += 1 
		
		cur.close()
		db.close()

	def connectToDB(self):
		db = mysql.connector.connect(host="xx",    # your host, usually localhost
                     user="xx",         # your username
                     passwd="xx",  # your password
                     db="xx")        # name of the data base
		print('connected to db...')
		return db


if __name__ == "__main__":
	
	baseDir="/PathToScrapedGoogleGroupData/"

	stdb = saveToDB(baseDir)
	db = stdb.connectToDB()
	stdb.saveItems(db)
