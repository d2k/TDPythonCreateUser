#!/yourPath/python

##########################################################
### Author: Ulrich Arndt
### Company: data2knowledge Gmbh
### website: www.data2knowledge.de
### First creation date: 18.11.2015
### License:
# The MIT License (MIT)
#
# Copyright (c) 2015 by data2knowledge GmbH, Germany
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
##########################################################

import teradata
import argparse
import logging

import os
import random
import string

# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

logger = logging.getLogger(__name__)

###########################################################
# Process the command line information
###########################################################

parser = argparse.ArgumentParser(description='Teradata Create User Script')
parser.add_argument('-l','--logonfile', nargs=1,
                   help='logon file for the user creation')
parser.add_argument('-c','--configfile', nargs=1,
                   help='config file for the user creation')

args = parser.parse_args()

###########################################################
# Set Default config and logon info files in case they are not given at programm call
###########################################################
configfile = ''
if args.configfile:
	configfile = args.configfile[0]
else:
	configfile = './appini/demo.ini'

logonfile = ''
if args.logonfile:
	logonfile = args.logonfile[0]
else:
	logonfile = './dwl/demo.dwl'


###########################################################################
# Function Definition
###########################################################################

#######
# create a random password
####### 
def genPWD(length):
	chars1 = string.ascii_letters
	chars2 = string.ascii_letters + string.digits
	random.seed = (os.urandom(1024))
	start = random.choice(chars1)
	rest = ''.join(random.choice(chars2) for i in range(length-1))
	return start + rest

def sendMail(to, subject, text, fromAddress, mailserver):
	msg = MIMEText(text)
	msg['Subject'] = subject
	msg['From'] = fromAddress
	msg['To'] = to
	s = smtplib.SMTP(mailserver)
	s.sendmail(fromAddress, [to], msg.as_string())
	s.quit()

############################################################
# Main
###########################################################

############# 
#init udaExec
############# 

udaExec = teradata.UdaExec (userConfigFile=[configfile,logonfile])

session = udaExec.connect(
	method		='rest', 
	system		='${system}',
	username	='${user}', 
	password	='${password}',
	host		='${host}',
	port		='${port}'
	)
	
pwd = genPWD(int(udaExec.config['passwordLength']))

with session: 

	############# 
	#create User Template
	#############
	cu = '''
CREATE USER ${TDUserName}
FROM ${FromObject} AS
PERMANENT = ${PERMANENT},
PASSWORD = ''' + pwd + ''',
SPOOL = ${SPOOL},
${PROTECTIONTYPE},
DEFAULT DATABASE = ${DEFAULTDATABASE},
STARTUP = ${STARTUP},
TIME ZONE = ${TIMEZONE},
DATEFORM = ${DATEFORM},
DEFAULT CHARACTER SET  ${DEFAULTCHARACTERSET},
DEFAULT ROLE = ${DEFAULTROLE},
PROFILE = ${PROFILE},
ACCOUNT = ${ACCOUNT}
;'''

	session.execute(cu)
	txt = 'The Password for the new Teradata User user ' + udaExec.config['TDUserName'] + ' is: ' + pwd
	sendMail(udaExec.config['userEmailAddress'], 'DBA Message: Password for the new Teradata User', txt,udaExec.config['from'],udaExec.config['mailServer'])
	
	print('Email send')

exit(0)