# TDPythonCreateUser
Create a random password, create a user and send the password to the user via email

feel free to donate bitcoin:12kgAUHFUqvG2sQgaRBXFhCwyf9HXdkGud?label=TeradataDev

##Install

clone the repository or download and unzip the zip file

##Configuration

The main configuration is done via three ini files:

* udaexec.ini - contains the main udaexec ini information
* dwl/XXX.dwl - contains the database logon information
* appini/YYY.ini - contains the specific pivot transformation information


###database logon information - dwl/demo.dwl

The database logoninformation requires the following parameter:

* production=True/False
* password=myPassword
* user=myUser
* system=mySystem
* host=myRestServer
* port=myRestServerPort - Standard 1080

### udaexec.ini 

The only parameters likely to be changed are:

* mailServer=yourMailServer
* from=yourFromEmailAddress

### create user config file (like demo.ini)

* userEmailAddress = user email address to which the password will be send
* passwordLength = length of the generated password
* TDUserName = new teradata username
* FromObject = owner of the user
* PERMANENT = perm space in byte
* STARTUP = startup sql's to be executed after logon
* PROTECTIONTYPE = Protection Tpye
* TEMPORARY = temporary space
* SPOOL = spool space
* DEFAULTDATABASE =  default DB for the user
* ACCOUNT = List of account strings
* TIMEZONE = timezone of the user
* DATEFORM = default date form
* DEFAULTCHARACTERSET = default character set
* DEFAULTROLE = default role
* PROFILE = profile for the user

more to add if needed. But the additional parameter need also to be added to the create user template

## program call

example programm calls

python CreateUser.py -h

result:

usage: CreateUser.py [-h] [-l LOGONFILE] [-c CONFIGFILE]

Teradata create user programm

optional arguments: -h, --help show this help message and exit -l LOGONFILE, --logonfile LOGONFILE logon file for the user creation -c CONFIGFILE, --configfile CONFIGFILE config file for the user creation

python CreateUser.py -l dwl/demo.dwl -c appini/demo1.ini
