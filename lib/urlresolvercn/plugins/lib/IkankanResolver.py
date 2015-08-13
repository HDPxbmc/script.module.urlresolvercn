#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2
import re
import json
import hashlib

class IkankanResolver:

    #def __init__(self,url):
        #return
        #self.get_episode(url)
    
    def fetch_url(self, url):
        return urllib2.urlopen(url).read()
    
    def resolve(self,url,res):
        r = re.search(r'(\d+)/(\d+).shtml\?subid=(\d+)', url)
        if r:
            #http://api.movie.kankan.com/vodjs/subdata/65/65271/325179.js
            url = "http://api.movie.kankan.com/vodjs/subdata/{0}/{1}/{2}.js".format(r.group(1),r.group(2),r.group(3))
        html = self.fetch_url(url)
        r = re.search(r'surls:(\[.+?])', html)
        if r:
            data = json.loads(("{'aa':" + r.group(1)+"}").replace('\'','"'))          
            result =''
            for data_item in data["aa"]:
                print data_item
                if 'pubnet.sandai.net:8080/6/' in data_item:
                    gcid = data_item[32:32+40]
                    print gcid
                    result = self.get_true_url(gcid)
            return result
        else: 
            return False
        
    def get_true_url(self,gcid):
        #http://p2s.cl.kankan.xunlei.com/getCdnresource_flv?gcid=ddd77eb843e0a7d0499212582ad0e190daa2b65a
        url = "http://p2s.cl.kankan.xunlei.com/getCdnresource_flv?gcid=" + gcid
        html = self.fetch_url(url)
        r = re.search(r'ip:"(.+?)",port:(\d+),path:"(.+?)"', html)
        r2 =  re.search(r'\{param1:(\d+?),param2:(\d+?)\}', html)
        if r and r2:
            ip = r.group(1)
            port = r.group(2)
            path = r.group(3)
            param1 = r2.group(1)
            param2 = r2.group(2)
            m = hashlib.md5("xl_mp43651"+param1+param2)
            m.digest()
            key = m.hexdigest()
            addr="http://" + ip + ":80/"+path+"?key="+key +"&key1="+param2
            return addr
        return False
        
    def get_episode(self,url):
        html = self.fetch_url(url)
        divs = re.findall(r'<div id="fenji_\d+_(asc|\d+)"(.*?)<\/div>', html) 
        result = []
        if divs:
            for div in divs:
                #                              链接                                   第N集                 小标题
                r = re.findall(r'<h3><a href="(.*?)" target="_blank" title=".*?">.*?(第\d+集)<\/a></h3><h4>(.+?)</h4>', div[1])

                if r:     #电视剧
                    for ep_data in r:
                        result.append({"title":ep_data[1] + " " + ep_data[2],
                                        "img":"",
                                        "url":ep_data[0]})
                                        
                else: 
                    
                    #                             链接                          标题   小标题            期数(日期)
                    r = re.findall(r'<h3><a href="(.*?)" target="_blank" title="(.*?)">(.*?)<\/a></h3><h4>(.+?)期</h4>', div[1])
                    if r:  #综艺
                        for ep_data in r:
                            dateA = ep_data[3].split("-")
                            date = ""
                            if len(dateA) == 3:  #2012-08-12
                                date = "%s.%s.%s" % (dateA[2],dateA[1],dateA[0])
                            result.append({"title":ep_data[1] + " " + ep_data[2],
                                        "img":"",
                                        "url":ep_data[0],
                                        "date":date})
        return result           
             
#aa = IkankanResolver("http://data.movie.kankan.com/movie/38534?id=731018")