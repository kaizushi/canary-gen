#!/usr/bin/python3
import os
import time
from urllib.request import urlopen
import json

from settings import realname, emails, host, path, template, canaries, enable_news, news_apikey, news_numitems, news_country, news_category

class SettingsNotFinishedError(Exception):
    """Configuration file not properly edited"""
    pass

try:
    from settings import ignorant
    print("You need to configure the program first!")
    raise SettingsNotFinishedError
except ImportError:
    pass

global outputFile

class NewsFetchException(Exception):
    """There was an error fetching the news!"""
    pass

class NewsAPIException(Exception):
    """There was an error reported from the API while fetching news!"""
    pass

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

        print("Fetching news sources!")
        try:
            response = urlopen(url)
        except Exception as e:
            print("Oops!", e.__class__, "occurred.")
            raise NewsFetchException

        return response

def parseNews(response):
    global news_numitems

    response = json.loads(response.read())

    if (response['status'] == "error"):
        raise NewsAPIException

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
        try:
            headlines = parseNews(fetchNews())
        except NewsFetchException:
            print("Could not fetch news from the Internet. See above for more info. Aborting!")
            return
        except NewsAPIException:
            print("The newsapi.org web API has reported an error. Aborting!")
            return

        print("News items downloaded...")

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

comment = input("Comment:")
createCanaryPlaintext()
clearsignCanary()
uploadTheCanary()
