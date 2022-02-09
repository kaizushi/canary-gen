#!/usr/bin/python3
import os
import time
from urllib.request import urlopen
import json

# THESE SETTINGS ARE IMPORTANT
#
# If you cannot figure out how to set this up you could buy my hosting services.
# I would be happy to send you the values for below so your canary automatically
# uploads to your site on my hosting.
#
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

global outputFile

def fetchNews():
    global news_country 
    global news_category
    global news_apikey
    if (enable_news):
        url = "https://newsapi.org/"
        url = url + "v2/top-headlines?country="
        url = url + news_country + "&category="
        url = url + news_category + "&apiKey="
        url = url + news_apikey

        response = urlopen(url)

        return response
    

def parseNews(response):
    global news_numitems

    response = json.loads(response.read())

    total_items = response['totalResults']
    articles = response['articles']

    top_articles = []

    i = 0
    for article in articles:
        top_articles.append(article)
        i = i + 1
        if (i == news_numitems + 1):
            break

    output = ""
    for article in top_articles:
        title = article['title']
        output = output + title + '\n'

    return output

def dateString(type):
        if (type == "fn"): #filename
                return time.strftime("%y-%m-%d")
        if (type == "hr"): #human readable
                return time.strftime("%d-%m-%y")
        return dateString("hr")

def timeString(type):
        if (type == "fn"):
                return time.strftime("%H-%M-%S")
        if (type == "hr"):
                return time.strftime("%H:%M:%S")
        return timeString("hr")

def sigLine(name, email, comment):
        string = "Notice by " + name + " <" + email + "> on "     
        string = string + dateString("hr") + " at " + timeString("hr")
        return string

def replaceStrings(inString, name, email, comment):
        string = inString
        string = string.replace("%%NAME%%",name)
        string = string.replace("%%EMAIL%%",email)
        string = string.replace("%%DATE%%",dateString("hr"))
        string = string.replace("%%TIME%%",timeString("hr"))
        string = string.replace("%%COMMENT%%",comment)
        return string

def replaceWithHeadline(inString, name, email, comment, headlines):
        string = replaceStrings(inString, name, email, comment)
        string = string.replace("%%HEADLINES%%",headlines) 
        return string

def clearsignCanary():
        global outputFile
        cmd = "gpg2 --verbose --clearsign "
        for addrs in emails:
            cmd = cmd + "-u " + addrs + " "
        os.system(cmd + outputFile)

def createCanaryPlaintext():
        global outputFile
        global enable_news

        # headlines is called here so it runs first, in case it can't reach the webapi
        headlines = parseNews(fetchNews())

        filename = canaries + dateString("fn") + "-" + timeString("fn") + ".txt"
        outputFile = filename
        tpl = open(template,'r')
        new = open(filename,'a')
        for line in tpl:
            if enable_news: new.write(replaceWithHeadline(line, realname, email, comment, headlines))
            else: new.write(replaceStrings(line, realname, email, comment))
        tpl.close()
        new.close()

def uploadTheCanary():
    global outputFile
    print("Uploading canary...")
    os.system("scp " + outputFile + ".asc " + host + ":" + path)

print (parseNews(fetchNews()))

comment = input("Comment:")
createCanaryPlaintext()
clearsignCanary()
uploadTheCanary()
