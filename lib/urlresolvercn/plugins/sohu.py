#!/usr/bin/python
# -*- coding: utf-8 -*-
from t0mm0.common.net import Net
import urlresolvercn
from urlresolvercn.plugnplay.interfaces import UrlResolver
from urlresolvercn.plugnplay.interfaces import PluginSettings
from urlresolvercn.plugnplay.interfaces import EpisodeResolver
from urlresolvercn.plugnplay import Plugin
import re,json,urllib


class SohuResolver(Plugin, UrlResolver, EpisodeResolver, PluginSettings):
    implements = [UrlResolver, PluginSettings, EpisodeResolver]
    name = "搜狐视频"

    def __init__(self):
        p = self.get_setting('priority') or 100
        self.priority = int(p)
        self.net = Net()

    def get_media_url(self, host, media_id):
        url = media_id
        html = self.net.http_GET(url).content
        r = re.search(r'vid="(.*?)"', html)
        print r
        if r:
            res = urlresolvercn.get_res_setting()
            vid = r.group(1)
            print "Vid::" + vid
            data = self.get_video_data(vid)
            dataurls =[]
            if data["data"]["oriVid"] != 0 and res >=4:  #原画
                vid = data["data"]["oriVid"]
                data = self.get_video_data(vid)
            elif data["data"]["superVid"] != 0 and res >=3 :  #超清
                vid = data["data"]["superVid"]
                data = self.get_video_data(vid)
            for i in range(len(data["data"]["clipsURL"])):
                playURL  = self.get_true_url(data["data"]["clipsURL"][i].replace("http://data.vod.itc.cn",""),data["data"]["su"][i]) 
                print playURL
                dataurls.append(playURL)
            return "stack://" + " , ".join(dataurls)    
            return "http://hot.vrs.sohu.com/ipad"+ str(vid) +".m3u8"
        return False
        
    def get_true_url(self,oriFile,newFile):
        url = "http://220.181.61.229/?prot=2&file={0}&new={1}".format(oriFile,newFile)
        html = self.net.http_GET(url).content
        
        paras = html.split("|")
        
        target_url = paras[0] + newFile[1:] + "?key=" + paras[3]
        return target_url
        
    def get_video_data(self,vid):
        #http://hot.vrs.sohu.com/vrs_flash.action?vid=1251186
        url ='http://hot.vrs.sohu.com/vrs_flash.action?vid=' + str(vid)
        html = self.net.http_GET(url).content
        data = json.loads(html)
        return data 
        
    def get_episode_urls(self, url):
        html = self.net.http_GET(url).content
        r = re.search(r'(playlistId|PLAYLIST_ID)="(\d*?)"', html)
        result = []
        if r:
            playlistID = r.group(2)
            #http://hot.vrs.sohu.com/vrs_videolist.action?playlist_id=5206418
            url = "http://hot.vrs.sohu.com/vrs_videolist.action?playlist_id=" + playlistID
            html = self.net.http_GET(url).content
            data = json.loads(html[19:])
            if len(data["videolist"]) > 0:
                for videoinfo in data["videolist"]:
                    print videoinfo["videoUrl"]
                    if videoinfo.get("videoShowDate") and len(videoinfo.get("videoShowDate")) == 8:
                        date = "%s.%s.%s" %( videoinfo["videoShowDate"][6:8],videoinfo["videoShowDate"][4:6],videoinfo["videoShowDate"][0:4])
                    else:
                        date = ""
                    result.append({"title":videoinfo["videoName"] ,
                                "img":videoinfo["videoImage"],
                                "url":videoinfo["videoUrl"],
                                "date":date})
        return result           
        
    def valid_ep_url(self, url):
        return self.valid_url(url,"")
        
    def get_url(self, host, media_id):
        return media_id

    def get_host_and_id(self, url):
        return "tv.sohu.com",url
    def valid_url(self, url, host):
        if self.get_setting('enabled') == 'false':
            return False
        return (re.match(r'http://tv.sohu.com/.+?shtml', url) or 'sohu' in url)
