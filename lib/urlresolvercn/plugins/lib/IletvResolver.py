#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2
import re
import json

class IletvResolver:

    def __init__(self,url):
        return 
        #self.get_episode(url)
    
    def fetch_url(self, url):
        return urllib2.urlopen(url).read()
    
    def resolve(self,vid,res):
        url="http://www.letv.com/v_xml/"+ vid+".xml"
        html = self.fetch_url(url)

        find = re.search(r'<playurl><!\[CDATA\[(.*?)\]\]>', html)
        if find:  
            data = json.loads(find.group(1))
            if data['dispatch'].get('1080p') and res >=4:  #1080P
                return data['dispatch'].get('1080p')[0]
            elif data['dispatch'].get('720p') and res >=3:  #720P
                return data['dispatch'].get('720p')[0]
            elif data['dispatch'].get('1000') and res >=2:  #标清
                return data['dispatch'].get('1000')[0]
            elif data['dispatch'].get('350') and res >=1:  #流畅
                return data['dispatch'].get('350')[0]
        return False
        
    def get_id(self,url):
        html = self.fetch_url(url)
        r = re.search(r' vid:(\d+)', html)
        if r:
            return r.group(1)
        else:
            return False
 
    def get_episode(self,url):
        html = self.fetch_url(url)
        result = []
        #                             连接                                                  标题                         图片                                                               
        find = re.compile(r'<a href="(.{30,50})" target="_blank"><img\s+alt=".+?"\s+title="(.+?)" class="loading"\s+src="(.+?)"', re.DOTALL).findall(html)
        if find:
            for ep_data in find:
                result.append({"title":ep_data[1],
                                "img":ep_data[2],
                                "url":ep_data[0]})
                if len(result) *2 == len(find):
                    break
        return result
             
#aa = IletvResolver("http://so.letv.com/tv/76111.html")