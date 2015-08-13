#!/usr/bin/python
# -*- coding: utf-8 -*-
from t0mm0.common.net import Net
import urlresolvercn
from urlresolvercn.plugnplay.interfaces import UrlResolver
from urlresolvercn.plugnplay.interfaces import PluginSettings
from urlresolvercn.plugnplay.interfaces import EpisodeResolver
from urlresolvercn.plugnplay import Plugin
from lib.IkankanResolver import IkankanResolver
import re



class KankanResolver(Plugin, IkankanResolver, UrlResolver, PluginSettings, EpisodeResolver):
    implements = [UrlResolver, PluginSettings, EpisodeResolver]
    name = "迅雷看看"

    def __init__(self):
        p = self.get_setting('priority') or 100
        self.priority = int(p)
        self.net = Net()


    def get_media_url(self, host, media_id):
        res = urlresolvercn.get_res_setting()
        return self.resolve(media_id,res)
    
    def get_url(self, host, media_id):
        return media_id

    def get_host_and_id(self, url):
        return "kankan.com",url
        
    def get_episode_urls(self, url):
        return self.get_episode(url)
        
    def valid_ep_url(self, url):
        return self.valid_url(url,"")    
        
        
    def valid_url(self, url, host):
        if self.get_setting('enabled') == 'false':
            return False
        return (re.match(r'http://(kankan.xunlei.com|vod.kankan.com)/.+?/\d+\.shtml', url) or 'kankan' in url or 'xunlei' in url )
