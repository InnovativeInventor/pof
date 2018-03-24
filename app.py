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

from flask import Flask, render_template
import feedparser
import requests
from flask_caching import Cache
from xml.etree.ElementTree import fromstring, ElementTree
import time
import git
from pathlib import Path
import platform
import secrets

app = Flask(__name__)

# Configurable variable
pof_frequency = 60 # seconds


random_secret_key = secrets.token_urlsafe(128)
app.config.update(
    DEBUG=False,
    SECRET_KEY=random_secret_key
)

cache = Cache(app, config={
    'CACHE_TYPE': 'simple'
})

# Test if random_secret_key has been changed from the default value
if random_secret_key == 'ib6uYkCK3aTNp3qu7LKd5GcQZehmvWXW5n173wg2ibqDWBe23FZELZDHsN4dSzN1SynnFVe0LxzLQZq5OGSd2hf3tXs1VV8g':
    print("Warning: If you are running this in production, don't forget to change the random_secret_key. This message will automatically disappear if random_secret_key is changed.")
print("This server is configured to update every 60 seconds. Edit pof.py to change your server settings.")
Dockerfile = Path("Dockerfile")
if Dockerfile.is_file():
    system = str(platform.dist()[0])
else:
    system = "docker"

nist_beacon = requests.get('https://beacon.nist.gov/rest/record/last.xml', headers={'Cache-Control': 'no-cache'})
nyt_news = feedparser.parse('https://rss.nytimes.com/services/xml/rss/nyt/World.xml')
bbc_news = feedparser.parse('http://feeds.bbci.co.uk/news/world/rss.xml')
wsj_news = feedparser.parse('http://www.wsj.com/xml/rss/3_7085.xml')
congress_votes = requests.get('https://www.govtrack.us/data/congress/')
bitcoin_blockchain = requests.get('https://blockchain.info/blocks/?format=json')

@app.route('/')
@cache.cached(timeout=720)
def index():
    global pof_frequency
    repo = git.Repo(search_parent_directories=True)
    commit = repo.head.object.hexsha
    return render_template('homepage.html', commit=commit, system=system, pof_frequency=pof_frequency)

@app.route('/pof')
def pof():
    global pof_frequency
    global news_last_checked
    global nist_last_checked
    epoch = int(time.time())
    epoch_time = str(epoch)
    news_titles = all_news()
    nist_beacon = nist()
    next_news_update = str(pof_frequency-(epoch-news_last_checked))
    next_nist_update = pof_frequency-(epoch-nist_last_checked)

    if next_nist_update < 0:
        next_nist_update = str(0)
    else:
        next_nist_update = str(next_nist_update)

    return render_template(
        'layouts.html',
        epoch_time=epoch_time,
        nyt_news_titles=news_titles[0],
        bbc_news_titles=news_titles[1],
        wsj_news_titles=news_titles[2],
        unix_time=nist_beacon[0],
        seed=nist_beacon[1],
        output=nist_beacon[2],
        pof_frequency=pof_frequency,
        next_news_update=next_news_update,
        next_nist_update=next_nist_update
        )

@cache.cached(timeout=pof_frequency, key_prefix='news_feeds')
def all_news():
    global news_last_checked
    news_last_checked = int(time.time())
    nyt_news_titles = news_feeds(nyt_news)
    bbc_news_titles = news_feeds(bbc_news)
    wsj_news_titles = news_feeds(wsj_news)

    return [nyt_news_titles, bbc_news_titles, wsj_news_titles]

def news_feeds(feed):
    title = []
    for count in range(0,3):
        if feed.entries[count].title:
            title.append(feed.entries[count].title)
    return title

@cache.cached(timeout=pof_frequency, key_prefix='nist_beacon')
def nist():
    global nist_last_checked
    tree = ElementTree(fromstring(nist_beacon.content))
    root = tree.getroot()

    nist_last_checked = int(root[2].text)

    unix_time = root[2].text
    seed = root[3].text
    output = root[6].text
    return [unix_time, seed, output]

def undo_list(input_list):
    undo_list = '<br>'.join(input_list)
    return undo_list
