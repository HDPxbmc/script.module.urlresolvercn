#!/usr/bin/python
# -*- coding: utf-8 -*-
from t0mm0.common.net import Net
import urlresolvercn
from urlresolvercn.plugnplay.interfaces import UrlResolver
from urlresolvercn.plugnplay.interfaces import PluginSettings
from urlresolvercn.plugnplay.interfaces import EpisodeResolver
from lib.IyoukuResolver import IyoukuResolver
from lib.ItudouResolver import ItudouResolver
from urlresolvercn.plugnplay import Plugin
import re,json,urllib


class TudouResolver(ItudouResolver,Plugin, UrlResolver, EpisodeResolver, PluginSettings):
    implements = [UrlResolver, PluginSettings, EpisodeResolver]
    name = "土豆"

    def __init__(self):
        p = self.get_setting('priority') or 100
        self.priority = int(p)
        self.net = Net()

    def get_media_url(self, host, media_id):
        url = media_id
        html = self.net.http_GET(url).content
        res = urlresolvercn.get_res_setting()
        r = re.search(r",vcode: '(.+?)'", url)
        if r:  #youku
            return  IyoukuResolver.resolve(r.group(1),res)
        else:
            r = re.search(r",iid: (\d+)", url) #iid
            return self.resolve(r.group(1),res)
        
    def get_episode_urls(self, url):
        html = self.net.http_GET(url).content
        r = re.search(r",vcode: '(.+?)'", url)
        if r:  #youku
            list_id = IyoukuResolver.get_list_id(url)
            result = IyoukuResolver.get_episode(list_id)
            return  result
        else:
            r = re.search(r",iid: (\d+)", url) #iid
            return self.resolve(r.group(1))
        return result           
        
    def valid_ep_url(self, url):
        return self.valid_url(url,"")
        
    def get_url(self, host, media_id):
        return media_id

    def get_host_and_id(self, url):
        return "tudou.com",url

    def valid_url(self, url, host):
        if self.get_setting('enabled') == 'false':
            return False
        return (re.match(r'http://tudou/.+?shtml', url) or 'tudou' in url)
