#The purpose of this page is to collect and parse dino data

import webbrowser
import urllib.request
from html.parser import HTMLParser
import random
import json

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
            content = data.strip()
            if content and self.current_href not in self.links:
                self.links.append(BASE_URL + self.current_href)

    def handle_endtag(self, tag):
        if tag == "a":
            self.in_link = False
            self.current_href = ""

class DinoDataParser(HTMLParser):
    def __init__(self):
           super().__init__()
           self.in_dl = False
           self.in_dt = False
           self.in_dd = False

           self.in_h1 = False

        #save the current dt and dd
           self.current_term = ""
           self.current_data = ""

           self.h1 = ""
        #where we will store the key pair values
           self.dino_data = {}

    def handle_starttag(self, tag, attrs):
        #an else if chain to determine if all the tags are there
        if tag == "dl":
            self.in_dl = True
        elif self.in_dl and tag == "dt":
            self.in_dt = True
            self.current_term = ""
        elif self.in_dl and tag == "dd":
            self.in_dd = True
            self.current_data = ""
        elif tag == "h1":
            self.in_h1 = True
            self.h1 = ""

    def handle_data(self, data):
        content = data.strip()
        if content:
            if self.in_dt:
                self.current_term += content
            elif self.in_dd and self.current_term:
                self.current_data += content
            elif self.in_h1:
                self.h1 += content
                

    def handle_endtag(self, tag):
        if tag == "dl":
            self.in_dl = False
            #unwraps single values in list to just be strings since a dino can have mulitple locations
            for key, val in self.dino_data.items():
                if isinstance(val, list) and len(val) == 1:
                    self.dino_data[key] = val[0]

        elif tag == "dt":
            self.in_dt = False
            self.current_term = self.current_term.rstrip(":")
            if self.current_term:
                self.dino_data[self.current_term] = []  

        elif tag == "dd":
            self.in_dd = False
            if self.current_term:
                cleaned = self.current_data.strip().strip("', ")
                if cleaned:
                    self.dino_data[self.current_term].append(cleaned)  
            self.current_data = ""

        elif tag == "h1":
            self.in_h1 = False
            if self.h1:
                self.dino_data['Name'] = self.h1.strip()



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

def collect_dino_data_html(urls):
    all_html = []
    for url in urls:
        headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
        req = urllib.request.Request(url, headers=headers)
    
        with urllib.request.urlopen(req, timeout=15) as response:
            page_bytes = response.read()

        page_html = page_bytes.decode("utf-8")
        all_html.append(page_html)

    return all_html

def collect_dino_urls(page_html):
    parser = DinoLinksParser()
    parser.feed(page_html)
    return parser.links

def select_random_urls(urls):
    return random.sample(urls, 20)

def collet_dino_json_data(html_pages):
    data = []
    for page in html_pages:
        parser = DinoDataParser()
        parser.feed(page)
        data.append(parser.dino_data)
    return data
    

if __name__ == "__main__":
    page = collect_html_page()
    links = select_random_urls(collect_dino_urls(page))


    dino_pages_html = collect_dino_data_html(links)
    data = collet_dino_json_data(dino_pages_html)

    with open("dinos.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    

    

    
  

