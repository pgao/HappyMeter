import sys
import math

"""
borrows a lot from Aki Matsukawa's AI workshop for H@B in 2011 (https://github.com/amatsukawa/twitter_sentiment) and 
the AI class I took this semester (https://berkeley.edx.org/courses/BerkeleyX/CS188/fa12/) 
"""

class Vector(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.default = 0

    def __getitem__(self, key):
        if key in self:
            return dict.__getitem__(self, key)
        else:
            return self.default

    def normalize(self):
        total = self.total_value() * 1.0
        normalized = Vector()
        for k in self:
            normalized[k] = self[k]/total
        return normalized

    def total_value(self):
        return sum(self.values())

    def arg_min(self):
        if not self:
            return None
        return sorted(self.items(), key=lambda x: x[1])[0][0]
        
    def arg_max(self):
        if not self:
            return None
        return sorted(self.items(), key=lambda x: -x[1])[0][0]

class NaiveBayes:
    def __init__(self, positive_file="data/train_pos.txt", negative_file="data/train_neg.txt"):
        self.features = set()
        feature_list = open("data/features.txt")
        for line in feature_list:
            self.features.add(line.strip().lower())

        self.stopwords = set()
        stopwords_list = open("data/stopwords.txt")
        for line in stopwords_list:
            self.stopwords.add(line.strip().lower())

        self.cpds = {"+": Vector(),
                     "-": Vector()}
        for vector in self.cpds.values():
            vector.default = 1
        
        self.priors = {"+": 0.6, "-": 0.4}
        self.train(positive_file, negative_file)

    def classify(self, tweet):
        tweet = self.sanitize_tweet(tweet)
        positive_prob = self.priors["+"]
        negative_prob = self.priors["-"]
        for feature in self.features:
            if feature in tweet:
                positive_prob += math.log(self.cpds["+"][feature])
                negative_prob += math.log(self.cpds["-"][feature])
            else:
                positive_prob += math.log(1 - self.cpds["+"][feature])
                negative_prob += math.log(1 - self.cpds["-"][feature])
        if positive_prob > negative_prob + math.log(2):
            return "positive"
        elif negative_prob > positive_prob + math.log(3):
            return "negative"
        else:
            return "neutral"

    def train(self, positive_file, negative_file):
        positive = open(positive_file, "r")
        vector = self.cpds["+"]
        total = 0.0
        for tweet in positive:
            total += 1.0
            tweet = self.sanitize_tweet(tweet)
            for word in tweet.split():
                if word in self.features:
                    if word not in vector:
                        vector[word] = 0.0
                    vector[word] += 1.0
        
        for word in vector:
            vector[word] /= total

        vector.default = 1.0/total

        negative = open(negative_file, "r")
        vector = self.cpds["-"]
        total = 0.0
        for tweet in negative:
            total += 1.0
            tweet = self.sanitize_tweet(tweet)
            for word in tweet.split():
                if word in self.features:
                    if word not in vector:
                        vector[word] = 0.0
                    vector[word] += 1.0

        for word in vector:
            vector[word] /= total

        vector.default = 1.0/total

    def sanitize_tweet(self, tweet):
        tweet = tweet.lower().replace("@", "").replace("#", "")
        words = tweet.split()
        for word in words:
            if word in self.stopwords or "http" in word:
                words.remove(word)
        tweet = " ".join(words)
        return tweet

# def main():
#     classifier = NaiveBayes()
#     print classifier.cpds
#     print classifier.classify("i am in love with cake")

# if __name__ == main():
#     main()