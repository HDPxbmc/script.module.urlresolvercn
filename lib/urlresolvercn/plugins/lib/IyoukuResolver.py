#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2
import re
import json

class IyoukuResolver:
    
    def __init__(self,url):
        return None
        #self.get_qiyi_urls(url)
    
    def fetch_url(self, url):
        return urllib2.urlopen(url).read()

    
    def getFileIDMixString(self,seed): 
        source = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ/\\:._-1234567890"
        mixed = []
        index = 0
        for i in range(len(source)):
            seed = (seed * 211 + 30031) % 65536
            
            index =  seed * len(source) / 65536 
            mixed.append(source[index])
            source = source.replace(source[index],"")
        return ''.join(mixed)

    def getReportSID(self,sid,num):
        a = sid[0:8]
        b = sid[10:]
        return "%s%02X%s" % (a,num,b)
        
    def get_list_id(self,url):
        r = re.search(r'http://www.youku.com/show_page/id_(.+?).html', url)
        print "GetListId::" + url
        if r:
            id = r.group(1)
            return id
        htmldata = self.fetch_url(url)
        r = re.search(r'http://www.youku.com/show_page/id_(.+?).html', htmldata)
        if r:
            id = r.group(1)
            return id
            
    def get_episode(self,list_id):
        #http://www.youku.com/show_episode/id_ze5ead5ae982411e296da.html?dt=json&divid=reload_1
        url = "http://www.youku.com/show_episode/id_{0}.html?dt=json&divid=reload_".format(list_id)
        print "GetEP:::" +list_id
        result =[]
        for i in range(20):
            htmldata = self.fetch_url(url+str(i*40+1)) 
            match = re.findall(r'<a href="(.+?)" title="(.+?)"', htmldata)
            if match:
                for ep_data in match:
                    result.append({"title":ep_data[1],
                                "img":"",
                                "url":ep_data[0]})
            else:
                break
        return result
        
    def resolve(self,vid,res):
        url="http://v.youku.com/player/getPlayList/VideoIDS/"+ vid
        html = self.fetch_url(url)
        jsondata = json.loads(html)
        fileType = 'flv'
        if jsondata['data'][0]['streamfileids'].get('hd3') and res >= 4:  #原画
			dataType ="hd3"
        elif jsondata['data'][0]['streamfileids'].get('hd2') and res >= 3:  #超清
			dataType ="hd2"
        elif jsondata['data'][0]['streamfileids'].get('mp4') and res >= 2:  #高清
            dataType ="mp4"
            fileType = "mp4"
        else: 
            dataType ="flv"
        fileId = self.getfileid(jsondata['data'][0]['streamfileids'][dataType],int(jsondata['data'][0]['seed']))
        
        num = 0 
        dataurls =[]
        for data_item in jsondata['data'][0]['segs'][dataType]:
            data_url = "http://f.youku.com/player/getFlvPath/sid/00_00/st/" + fileType + "/fileid/" + self.getReportSID(fileId,num) + '?K=' + data_item['k'];
            #print data_url
            num = num + 1 
            dataurls.append(data_url)
        return "stack://" + " , ".join(dataurls)    

    def getfileid(self, fileid_flv,seed):
        cg_str = self.getFileIDMixString(seed)
        arr = fileid_flv[0:-1].split("*")
        res = ""
        for item in arr:
            res +=  cg_str[int(item)]  
        return res
        
    def get_qiyi_urls(self, url):
        html = self.fetch_url(url).replace("\n","")
        result =[]
        match1 = re.compile(r'data-lazy="(.+?)" title=".+?" alt=".+?" class=" ">\s<span class="s1"></span> <span class="s2">.+?</span> </a>\s<p><a href="(.+?)">(第\d+集)</a></p><p>(.+?)</p>', re.DOTALL).findall(html)
        print len(match1)
        for listitem in match1:    
            print listitem[1],listitem[0]
            result.append({"title":listitem[2] + " " + listitem[3],
                            "img":listitem[0],
                            "url":listitem[1]})
        return result               

aa = IyoukuResolver("http://www.iqiyi.com/common/topicinc/577551_26361/playlist_1.inc")        
