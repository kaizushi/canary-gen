#!/usr/bin/python3
import os
import time

from settings import realname, emails, host, path, template, canaries, enable_news, news_apikey, news_numitems, news_country, news_category

cmd_deps = ["gpg2", "scp"]

# below is a bunch of boilerplate stuff

#checks if you have the software you need
class MissingSoftwareError(Exception):
    """You are missing some of the required software to use this program."""
    pass


def commandCheck(command):
    if (os.system("command -v " + command + " &> /dev/null") != 0):
        print("The command '" + command + "' does not exist on your system.")
        raise MissingSoftwareError

#this loop uses the method above which will show each missing command
cmd_fail = False
for cmd in cmd_deps:
    try:
        commandCheck(cmd)
    except MissingSoftwareError:
        cmd_fail = True

if (cmd_fail):
    raise MissingSoftwareError

# check if the gpg and scp commands exist

class MissingDependenciesError(Exception):
    """You are missing dependencies required by the news feature."""
    pass

# if the news feature is enabled in settings, this tries to import its deps
# if the deps are not there it raises the custom exception above to abort
if (enable_news):
    try:
        from urllib.request import urlopen
        import json
    except ImportError:
        print("You are missing dependencies for the news feature.")
        raise MissingDependenciesError

class SettingsNotFinishedError(Exception):
    """Configuration file not properly edited"""
    pass

# the settings.py file has a line called ignorant at the end that must be deleted
# if it isn't then the exception defined above is raised to abort
try:
    from settings import ignorant
    print("You need to configure the program first!")
    raise SettingsNotFinishedError
except ImportError:
    pass

global outputFile

# some exceptions for things going wrong in the news fetch
class NewsFetchException(Exception):
    """There was an error fetching the news!"""
    pass

class NewsAPIException(Exception):
    """There was an error reported from the API while fetching news!"""
    pass

# literally fetches the news as a HTTPRequest object and returns it
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

#parses the JSON in the HTTP response and returns a list of headlines
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

# This gets the date as formats it either for a filename or human readable
def dateString(type):
        if (type == "fn"): #filename
                return time.strftime("%y-%m-%d")
        if (type == "hr"): #human readable
                return time.strftime("%d-%m-%y")
        return dateString("hr") #default

# same as above but with time
def timeString(type):
        if (type == "fn"):
                return time.strftime("%H-%M-%S")
        if (type == "hr"):
                return time.strftime("%H:%M:%S")
        return timeString("hr")

# this takes a string and some values to replace and returns a string
def replaceStrings(inString, name, email, comment):
        string = inString
        string = string.replace("%%NAME%%",name)
        string = string.replace("%%EMAIL%%",email)
        string = string.replace("%%DATE%%",dateString("hr"))
        string = string.replace("%%TIME%%",timeString("hr"))
        string = string.replace("%%COMMENT%%",comment)
        return string

# this is much like above but takes the list of news headlines as well
def replaceWithHeadline(inString, name, email, comment, headlines):
        string = replaceStrings(inString, name, email, comment)
        string = string.replace("%%HEADLINES%%",headlines) 
        return string

# this runs GPG to do the actual signing of the message
def clearsignCanary():
        global outputFile
        cmd = "gpg2 --verbose --clearsign "
        for addrs in emails:
            cmd = cmd + "-u " + addrs + " "
        os.system(cmd + outputFile)

# this creates the canary itself from the template as files
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

# this uploads the canary to the system
def uploadTheCanary():
    global outputFile
    print("Uploading canary...")
    os.system("scp " + outputFile + ".asc " + host + ":" + path)

# this runs everything involved
comment = input("Comment:")
createCanaryPlaintext()
clearsignCanary()
uploadTheCanary()
