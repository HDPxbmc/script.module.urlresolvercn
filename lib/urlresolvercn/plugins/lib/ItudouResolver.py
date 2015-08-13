#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2
import re
import json

class ItudouResolver:


    def fetch_url(self, url):
        return urllib2.urlopen(url).read()
    
    def resolve(self,iid,res):
        url="http://v2.tudou.com/v2/cdn?id="+ iid
        html = self.fetch_url(url)
        find1 = re.search(r'<f w=.*?brt="4">(.*?)<\/f>', html)
        find2 = re.search(r'<f w=.*?brt="3">(.*?)<\/f>', html)
        find3 = re.search(r'<f w=.*?brt="\d">(.*?)<\/f>', html)
        if find1 and res >=3:  #超清
            return find1.group(1)
        elif find2 and res >=2:  #高清
            return find2.group(1)
        elif find3 and res >=1:
            return find3.group(1)
        
