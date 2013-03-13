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

tweetbuffer = []

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
        quotes = self.get_stock_quotes()
        global tweetbuffer
        if not tweetbuffer:
            sentiments = self.get_tweet_sentiments()
            tweetbuffer = sentiments
        tweet = tweetbuffer[0]
        tweetbuffer = tweetbuffer[1:]
        self.set_header("Content-Type", "application/json")
        return self.write(simplejson.dumps([quotes, tweet]))
    def get_stock_quotes(self):
        f = urllib2.urlopen("http://download.finance.yahoo.com/d/quotes.csv?s=^IXIC+^GDAXI+^HSI&f=l1 ")
        quotes = f.read().split("\r\n")
        return quotes[:-1]
    def get_tweet_sentiments(self):
        tweets = get_tweet.get_tweets()
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
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
