import sys
import os
import pprint
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

class Error(RuntimeError):
    pass

class StumiData:
    def __init__(self, verbose=False):
        self.songs = []
        self.verbose = verbose
        self.url = None

    def open(self, url):
        try:
            if self.verbose:
                print(f"GET HTML {url}", flush=True)
            fp = urllib.request.urlopen(url)
            self.url = url
        except ValueError:
            fp = open(url)
        soup = BeautifulSoup(fp, 'html.parser')
        return soup

    def parse(self, url):
        soup = self.open(url)
        if soup.head.title.text != "StudioMini_WiFiSync":
            raise Error("This does not look like a StudioMini website")
        rows = soup.find_all('tr')
        for row in rows:
            entry = self.parse_row(row)
            self.songs.append(entry)
    
    def parse_row(self, row):
        entry = {}
        title = row.td.div.text
        if not title:
            raise Error("This does not look like a StudioMini website")
        entry["title"] = title
        links = row.find_all('a')
        for link in links:
            name = link.text
            url = link["href"]
            try:
                key = int(name)
            except ValueError:
                if "mix" in name.lower():
                    key = name
                else:
                    # drum track
                    key = 0
            entry[key] = url
        return entry
    
    def scrape(self):
        for song in self.songs:
            self.scrape_song(song)

    def scrape_song(self, entry):
        title = entry['title']
        if self.verbose:
            print(f"MKDIR {title}", flush=True)
        os.makedirs(title, exist_ok=True)
        for key, url in entry.items():
            if key == 'title':
                continue
            _, filename = os.path.split(url)
            if type(key) == type(1):
                filename = f'{key}-{filename}'
            pathname = os.path.join(title, filename)
            entry[key] = filename
            url = urllib.parse.quote(url)
            url = urllib.parse.urljoin(self.url, url)
            
            if self.verbose:
                print(f'GET AUDIO {url} -> {pathname}', flush=True)
            urllib.request.urlretrieve(url, pathname)

    def dump(self):
        pprint.pprint(self.songs)
        