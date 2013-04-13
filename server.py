import tornado.ioloop
import tornado.web
import urllib2
import simplejson
import classify
import get_tweet
import os
import random
import sys
sys.path.insert(0, 'flot/')

PATH = sys.path

classifier = classify.NaiveBayes()

tweetbuffer = {}

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class JQueryHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("/flot/jquery.js")

class FlotHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("/flot/jquery.flot.js")

class StyleHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("style.css")

class DataHandler(tornado.web.RequestHandler):
    def get(self):
        name = str(self.get_argument("name", "^IXIC"))
        quotes = self.get_stock_quotes(name)
        if quotes[-1] == "NASDAQComposite":
            quotes[-1] = "NASDAQ"
        elif quotes[-1] == "S&P 500":
            quotes[-1] = "S&P"
        #print quotes
        global tweetbuffer
        if name not in tweetbuffer or not tweetbuffer[name]:
            print name + " not in tweetbuffer"
            sentiments = self.get_tweet_sentiments(quotes[-1].split()[0])
            #sentiments = self.get_tweet_sentiments(name)
            tweetbuffer[name] = []
            tweetbuffer[name] = sentiments
        if tweetbuffer[name]:
            tweet = tweetbuffer[name][0]
            tweetbuffer[name] = tweetbuffer[name][1:]
        else:
            tweet = "No tweets found"
        self.set_header("Content-Type", "application/json")
        print [quotes, tweet]
        return self.write(simplejson.dumps([quotes, tweet]))
    def get_stock_quotes(self, name):
        #f = urllib2.urlopen("http://download.finance.yahoo.com/d/quotes.csv?s=^IXIC&f=l1n ")
        f = urllib2.urlopen("http://download.finance.yahoo.com/d/quotes.csv?s=" + name.upper() + "&f=l1n")
        #quotes = f.read().split("\r\n")
        quotes = f.read()
        quotationMark = False
        for i, char in enumerate(quotes):
            if char == '"':
                quotationMark = not quotationMark
            if char == "," and quotationMark:
                quotes = quotes[:i] + quotes[i + 1:]
        quotes = quotes.replace("\r\n", "").replace('"', '').split(",")
        return quotes
    def get_tweet_sentiments(self, name):
        tweets = get_tweet.get_tweets(name)
        sentiments = []
        for tweet in tweets:
            sentiments.append((tweet, classifier.classify(tweet)))
        return sentiments

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/getData", DataHandler),
    #(r"/jQuery.js", tornado.web.StaticFileHandler, {'path': '/flot/'}),
    #(r"/jQuery.flot.js", tornado.web.StaticFileHandler, {'path': '/flot/jQuery.flot.js'}),
    (r"/style.css", StyleHandler)
], debug=True, static_path=os.path.join(os.path.dirname(__file__) , 'static'))

if __name__ == "__main__":
    application.listen(80)
    tornado.ioloop.IOLoop.instance().start()
