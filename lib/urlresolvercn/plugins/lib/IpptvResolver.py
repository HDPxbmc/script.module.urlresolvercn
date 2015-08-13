#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2
import re
import urllib
import json
import time

class IpptvResolver:

    
    def fetch_url(self, url):
        return urllib2.urlopen(url).read()
    
    def resolve(self,id,res):
        url = "http://client-play.pplive.cn/chplay3-0-{0}.xml&type=web.fpp&version=4",format(id)
        html = self.fetch_url(url)

        r_rid = re.compile(r'<file cur="\d">(.+?)</file>', re.DOTALL).search(html)
        if r_rid:
            files = r_rid.group(1)            
            match = re.findall(r'<item rid="(.+?)" bitrate="(\d+)" vip="\d" ft="\d*" width="\d*" height="\d*"/>',files)
            name =""
            for file in match:
                bitrate = int(file[1])
                if bitrate >1000 and res >= 4:  #1080P
                    ft = "3"
                    name = file[0]
                elif bitrate >500  and res >= 3:  #720P
                    ft = "2"
                    name = file[0]
                elif bitrate >250  and res >= 2:  #高清
                    ft = "1"
                    name = file[0]
                else:
                    ft = "0"
                    name = file[0]
            r_key = re.compile('<dt ft="'+ ft +r'">.*?<sh>(.+?)</sh>.+?<key expire=".*?">(.*?)</key>.+?</dt>', re.DOTALL).search(html)
            
            if r_key:
                sh = r_key.group(1)
                key = r_key.group(2)
                r_sgms = re.compile('<drag ft="' + ft + r'">(.+?)</drag>', re.DOTALL).search(html)
                
                if r_sgms:
                    result =[]
                    match = re.findall(r'<sgm no="(\d+)" hl=".*?" dur=".*?" fs=".*?" of=".*?" rid="(.*?)"/>',r_sgms.group(1))
                    for i in match:
                        result.append("http://"+ sh + "/" + i[0] +"/" + name + "?k=" + key)
                    return "stack://" + " , ".join(result)
            return False
        
    def get_episode(self,url):
        html = self.fetch_url(url)
        r = re.search(r'"bk_info_id":(.+?),"p_title":".+?","channel_id":(.+?),', html)

        if r:
            if r.group(2) != "null": 
                result  = self.Inner_pptv_list(r.group(2))
            else:
                result  = self.Outer_pptv_list(r.group(1))
        return result    

    def Outer_pptv_list(self,bk_info_id):
        urlc = "http://api2.v.pptv.com/api/page/virtual_list.js?bk_info_id={0}&page=".format(bk_info_id)
        result =[]
        for page in range(20):
            url = urlc + str(page+1) 

            html = self.fetch_url(url)
            data = json.loads(html[1:-2])
            
            htmldata = data["data"]["html"]
            
            match = re.findall(r'<a target="_blank" href="(.+?)">(.+?)</a>',htmldata)
            if not match:
                break;
            for item in match:
                result.append({"title":item[1],
                                "img":"",
                                "url":item[0]})
        return result
        
    def Inner_pptv_list(self,channel_id):
        print channel_id
        urlc =  "http://api2.v.pptv.com/api/page/episodes.js?channel_id={0}&page=".format(channel_id)
        result =[]
        for page in range(20):
            url = urlc + str(page+1) 
            html = self.fetch_url(url)
            jsondata = json.loads(html[1:-2])
            htmldata = jsondata["html"]            
            match = re.findall(r"<a start_time='' href='(.+?)' title='(.+?)'  target='_play' ><img src='(.+?)'",htmldata)
            if not match:
                break;
            for item in match:
                result.append({"title":item[1],
                                "img":item[2],
                                "url":item[0]})
        print len(result)
        return result
             
#aa = IpptvResolver("http://data.movie.kankan.com/movie/38534?id=731018")
