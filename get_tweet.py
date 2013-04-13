import sys
sys.path.insert(0, 'static/twitter/')

import twitter

api = twitter.Api(consumer_key="ElptdK9AGjxOBuORbiuTQ", consumer_secret="iufJBk1qhX84VVeCeeqeOJrVgDkqmtiVobNTpMKUA", 
    access_token_key="370357185-yFfM8KRTOLuQJqfaURThsTN53clQK5oxAyTbvmb0", access_token_secret="1nSEOq2a6STHJm4gIVObMI0bkoL6cG8zH7n0qQ2bKc")

#to use this, type "sudo pip install twitter" first

def get_tweets(keyword="e"):
	if keyword == " ":
		keyword = "e"
	statuses = api.GetSearch(keyword)
	text = []
	for s in statuses:
		text.append(s.GetText())
		#print s.GetText()
	return text

if __name__ == "__main__":
    get_tweets()