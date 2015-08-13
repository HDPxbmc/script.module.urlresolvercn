#!/usr/bin/python
# -*- coding: utf-8 -*-
from t0mm0.common.net import Net
from urlresolvercn.plugnplay.interfaces import UrlResolver
from urlresolvercn.plugnplay.interfaces import PluginSettings
from urlresolvercn.plugnplay.interfaces import EpisodeResolver
import urlresolvercn
from urlresolvercn.plugnplay import Plugin
from lib.IpptvResolver import IpptvResolver
import re

class PPTVResolver(Plugin, IpptvResolver, UrlResolver, PluginSettings, EpisodeResolver):
    implements = [UrlResolver, PluginSettings, EpisodeResolver]
    name = "PPTV"

    def __init__(self):
        p = self.get_setting('priority') or 100
        self.priority = int(p)
        self.net = Net()

    def get_media_url(self, host, media_id):
        url = media_id
        html = self.fetch_url(url)
        r = re.search(r'"id":(\d+)', html)
        if r:
            id = r.group(1)
            res = urlresolvercn.get_res_setting()
            return self.resolve(id,res)
        else:
            return False
    def get_url(self, host, media_id):
        return media_id

    def get_host_and_id(self, url):
        return "pptv.com",url
        
    def get_episode_urls(self, url):
        return self.get_episode(url)
        
    def valid_ep_url(self, url):
        return self.valid_url(url,"")    

    def valid_url(self, url, host):
        if self.get_setting('enabled') == 'false':
            return False
        return (re.match(r'pptv.com', url) or 'pptv' in url)
