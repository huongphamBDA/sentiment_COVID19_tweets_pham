# Huong Pham, RedID: 824992682, Final Project GEOG-582, Fall 2020

import string
import re


def process_tweet(tweet):
    # Remove HTML special entities (e.g. &amp;)
    tweet = re.sub(r'&\w*;', '', tweet)

    # Remove tickers
    tweet = re.sub(r'\$\w*', '', tweet)

    # To lowercase
    tweet = tweet.lower()

    # Remove hyperlinks
    tweet = re.sub(r'https?://.*/\w*', '', tweet)

    # Remove Punctuation and split 's, 't, 've with a space for filter
    tweet = re.sub(r'[' + string.punctuation.replace('@', '') + ']+', ' ', tweet)

    # Remove words with 2 or fewer letters
    tweet = re.sub(r'\b\w{1,2}\b', '', tweet)

    # Remove whitespace (including new line characters)
    tweet = re.sub(r'\s\s+', ' ', tweet)

    # Remove single space remaining at the front of the tweet
    tweet = tweet.lstrip(' ')

    # remove numbers
    tweet = re.sub('[0-9]+', '', tweet)

    # Remove characters beyond Basic Multilingual Plane (BMP) of Unicode
    tweet = ''.join(c for c in tweet if c <= '\uFFFF')

    # remove special characters, numbers, punctuations (tweet is string)
    tweet = re.sub(r'[\t\n\r\f\v]', '', tweet)  # \t\n\r\f\v: matches Unicode whitespace character
    tweet = re.sub(r'@\w*', '', tweet)  # \w: match [a-zA-Z0-9_]; \: unescaped backslash

    # ^: caret matches the start of the string
    tweet = tweet.replace("[^a-zA-Z#]", " ")

    # \\: backlash
    tweet = tweet.replace("\\", " ")

    return tweet


def main():
    print('this is process_tweet module')


if __name__ == "__main__":
    main()
