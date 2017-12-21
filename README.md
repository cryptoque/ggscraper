# Google Group Scraper

## Motivation 
I was working on a project that requires collecting data in a private google group we own, quickely I found that Google OAuth2 API does not cover downloading Google Group message contents, and using takeout.google.com on Google Groups only gives you the contact list of the groups you own, rather than the contents... Existing scripts to scrape Google Group contents for a private group were all broken in some way due to changes either by Google or the lack of robustness of the scripts... So I created this one based on existing work with significant modification so that it works. It also segregates each parts of the message into columns of MySQL database table, preserving original group thread structure. 

## Functionality
ggscraper.py enables you to scrape Google Group contents via Selenium and aggregate scraped messages into MySQL.
Note for Public groups the downloaded messages will contain masked emails, I guess it is Google's protection against spammers 
using automated tools to havest email addresses. 

### Private Group 
For Private Groups, the emails will not be masked with correct credentails. Upon running ggscraper.py, selenium will trigger a testbrowser (Chrome or Firefox, depending on whether you have geckodriver or chromedriver installed, you will need to add the installation path of either driver into the script), where you can login to the google account which has access to the Google group you are trying to scrape. 

saveToDB.py will santitise and aggregate the downloaded message file as it is, and import them into a MySQL table with 
thread ID, message ID, time, subject, sender, receriver, message content ... The entire threaded structure of google group is maintained this way. 

## Instructions
All you need to do out of box is to add path to driver and the url of the google group in script ggscraper.py and manually type login credentials when prompted. 


**_last tested December 2017_**



