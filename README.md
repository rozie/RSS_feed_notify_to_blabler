# RSS_feed_notify_to_blabler
Python script to sent notifications about new RSS feed (WordPress) items to
blabler.pl service


Descrition
---------
Simple Python script using MechanicalSoup to post notification about new blog
posts to blabler.pl service. Posts one notification at the time, uses plain
text file to keep information about already posted entries. Tested only with
WordPress RSS feed.

Service blabler.pl does not provide API and it's not actively developed, so
decided to use MechanicalSoup and skip configuration file.


Requirements
---------
- Pytnon 3.x (tested with Python 3.5)
- modules listed in requirements.txt


Configuration
---------
Adjust following constants in script
RSS_URL - URL to your WordPress RSS feed
BLABLER_LOGIN - your blabler.pl login
BLABLER_PASSWORD - your blabler.pl password
You may also want to adjust text variable in main function.


Usage
---------
Run the script. Notification about one RSS entry should be posted to blabler.pl


Contribution
---------
Help is always welcome, so clone this repository, send pull requests or create
issues if you find any bugs.


License
---------
See LICENSE file
