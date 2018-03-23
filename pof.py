#!/usr/bin/env python3

# Made by Innovative Inventor at https://github.com/innovativeinventor.
# If you like this code, star it on GitHub!
# Contributions are always welcome.

# MIT License
# Copyright (c) 2017 InnovativeInventor

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from flask import Flask
import feedparser
import requests

app = Flask(__name__)

# Only change this variable
random_secret_key = 'ib6uYkCK3aTNp3qu7LKd5GcQZehmvWXW5n173wg2ibqDWBe23FZELZDHsN4dSzN1SynnFVe0LxzLQZq5OGSd2hf3tXs1VV8g'

app.config.update(
    DEBUG=False,
    SECRET_KEY=random_secret_key
)

# Test if random_secret_key has been changed from the default value
if random_secret_key == 'ib6uYkCK3aTNp3qu7LKd5GcQZehmvWXW5n173wg2ibqDWBe23FZELZDHsN4dSzN1SynnFVe0LxzLQZq5OGSd2hf3tXs1VV8g':
    print("Warning: If you are running this in production, don't forget to change the random_secret_key. This message will automatically disappear if random_secret_key is changed.")


nist_beacon = feedparser.parse('https://beacon.nist.gov/rest/record/last.xml')
nyt_news = feedparser.parse('https://rss.nytimes.com/services/xml/rss/nyt/World.xml')
bbc_news = feedparser.parse('http://feeds.bbci.co.uk/news/world/rss.xml')
wsj_news = feedparser.parse('http://www.wsj.com/xml/rss/3_7085.xml')
congress_votes = requests.get('https://www.govtrack.us/data/congress/')
bitcoin_blockchain = requests.get('https://blockchain.info/blocks/?format=json')

@app.route('/')
def index():
    return 'Welcome to POF (Proof of Freshness)! This website is made using Flask and the code is on GitHub. To see the POF page, visit <a href="/pof">/pof<a>.'

@app.route('/pof')
def pof():
    news_titles = all_news()
    return str(news_titles)

def all_news():
    nyt_news_titles = str(undo_list(news_feeds(nyt_news)))
    bbc_news_titles = str(undo_list(news_feeds(bbc_news)))
    wsj_news_titles = str(undo_list(news_feeds(wsj_news)))

    news_titles = "<br>NYT: <br>" + nyt_news_titles + "<br><br>BBC: <br>" + bbc_news_titles + "<br><br>WSJ: <br>" + wsj_news_titles
    return str(news_titles)

def news_feeds(feed):
    title = []
    for count in range(0,3):
        if feed.entries[count].title:
            title.append(feed.entries[count].title)
    return title

def nist():
    print(nist_beacon.feed.title)

def undo_list(input_list):
    undo_list = '<br>'.join(input_list)
    return undo_list
