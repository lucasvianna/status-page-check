"""
GCP status page
"""

import csv
import feedparser
import xml.etree.ElementTree as ET
  
def loadRSS(url):
    feed = feedparser.parse(url)
    entry = feed.entries[0]
    print(entry)

def status(url):
    loadRSS(url)
    # print(services)
