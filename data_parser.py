#The purpose of this page is to collect and parse dino data

import webbrowser
import urllib.request
from html.parser import HTMLParser
import random

BASE_URL = "https://www.nhm.ac.uk"
AZ_URL = "https://www.nhm.ac.uk/discover/dino-directory/name/name-az-all/gallery.html"

#step 1: collect all the dinosaur urls

class DinoLinksParser(HTMLParser):
    def __init__(self):
       super().__init__()
       self.in_link = False
       self.current_href = ""
       self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            dict_attrs = dict(attrs)
            href = dict_attrs.get("href", "")
            if '/discover/dino-directory/' in href and href.endswith(".html"):
                if "gallery.html" not in href and "index.html" not in href:
                    self.current_href = href
                    self.in_link = True

    def handle_data(self, data):
        if self.in_link:
            name = data.strip()
            if name and self.current_href not in self.links:
                self.links.append(BASE_URL + self.current_href)

    def handle_endtag(self, tag):
        if tag == "a":
            self.in_link = False
            self.current_href = ""
        

def collect_html_page():

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    req = urllib.request.Request(AZ_URL, headers=headers)

    #webbrowser.open(BASE_URL) 

    with urllib.request.urlopen(req, timeout=15) as response:
        page_bytes = response.read()

    page_html = page_bytes.decode("utf-8")
    return page_html

def collect_dino_urls(page_html):
    parser = DinoLinksParser()
    parser.feed(page_html)
    return parser.links

def select_random_urls(urls):
    return random.sample(urls, 20)

if __name__ == "__main__":
    page = collect_html_page()
    collect_dino_urls(page)
    links = select_random_urls(collect_dino_urls(page))

    for link in links:
        print(link)

    print(len(links))

