# THIS IS THE SETTINGS FILE
#
# Editing it is important!
#
# If you are finding it hard I can set it up for you if you buy hosting
# from me and put your canary there. https://kloshost.online/

realname = "Roger West" #Simple enough
emails = ["KEY 1", "KEY 2"] #The email or fingerprint of the keys you sign with
email = "kaizushi@infantile.us" #Your primary email address
host = "" #the SSH server used by scp to upload your canary
path = "" #the location for the canary on the remote server

#template location and a folder to archive your canaries
template = "template.tpl"
canaries = "output/"

#these settings are for the news feature
enable_news = False     #set this to True to enable news
news_apikey = ""        #sign up for newsapi.org and paste the key here
news_numitems = 5       #number of news items to include
news_country = "us"     #news country of origin
news_category = "technology" #the news topic to use (check newsapi.org for valid ones)

ignorant = "YES"        #you must delete this line
