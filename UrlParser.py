import re
import requests
from requests_html import HTMLSession
from urllib.parse import urlparse

class UrlParser:
    def __init__(self, url):
        
        try:
            # get the actual domain incase 'bit.ly' is received
            if(url[:4] != "http"):
                self.url = requests.head("http://"+url).headers['location']
            else:
                self.url = requests.head(url).headers['location']
        except Exception:
            self.url = url # pass in original link
        # initialize dictionary
        self.data = {}

    def execute(self):
        self.protocolEncoder()
        self.domainEncoder()
        self.extractInternalLinks()
        # return a dictionary with 3 labels:
        #       ['protocol', 'domain_type', 'internal_links']
        return self.data
    
    def protocolEncoder(self):
        # Protocols for encryption grade
        # protocol = ["no_protocol", "http", "https"]
        # protocol_encoding = [0, 1, 2]
        link = self.url
        if isinstance(link, float): # nan, therefore return
            self.data['protocol'] = 0
        elif link[:5] == "https":
            self.data['protocol'] = 2
        elif link[:4] == "http":
            self.data['protocol'] = 1
        else:
            self.data['protocol'] = 0

    def domainEncoder(self):
        domain = [".com/", ".org/", ".edu/", ".gov/", ".uk/", ".net/", ".ca/", ".de/", ".jp/", ".fr/", ".au/", ".us/", ".ru/", ".ch/", ".it/", ".nl/", ".se/", ".no/", ".es/", ".mil/", ".ly/", ".tel/", ".kitchen/", ".email/", ".tech/", ".estate/", ".xyz/", ".codes/", ".bargains/", ".bid/", ".expert/", ".co/", ".name/", ".mobi/", ".asia/", ".biz/", ".arpa/", ".cat/", ".jobs/", ".info/", ".int/", ".pro/", ".aero/", ".travel/", ".coop/"]
        # domain_encoding = [index for index in range(len(domain))]

        default = len(domain) # none of the domains encoding, default
        if isinstance(self.url, float): # nan, therefore return
            self.data['domain_type'] = default
        i = 0
        while(domain[i] not in self.url and i < len(domain)):
            i += 1
        self.data['domain_type'] = i # even if not found, it'll be default

    def extractInternalLinks(self):
        # checks the URL correct format: http://www.foufos.us, www.t.co, NOT(foufos.gr)
        regexUrl = re.compile(r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})')
        
        if isinstance(self.url, float):
            # print("no link present")
            self.data['internal_links'] = 0 # link is nan
        else:
            baseUrl = urlparse(self.url).netloc # without the https://
            try:
                session = HTMLSession() # go to webpage
                r = session.get(self.url)
                
                listOfLinks = r.html.xpath('//a/@href') # extract all links
                
                self.data['internal_links'] = 0
                for link in listOfLinks:
                    if baseUrl not in link and regexUrl.match(link):
                        self.data['internal_links'] += 1
                # all internal links have been added!
            except Exception:
                # print("NOT VALID LINK: ", url)
                self.data['internal_links'] = 0 #no valid links
        # now data has been edited for the class