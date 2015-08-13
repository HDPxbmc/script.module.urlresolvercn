#!/usr/bin/python
# -*- coding: utf-8 -*-
from t0mm0.common.net import Net
import urlresolvercn
from urlresolvercn.plugnplay.interfaces import UrlResolver
from urlresolvercn.plugnplay.interfaces import PluginSettings
from urlresolvercn.plugnplay.interfaces import EpisodeResolver
from urlresolvercn.plugnplay import Plugin
from lib.IletvResolver import IletvResolver
import re


class LetvResolver(IletvResolver, Plugin, UrlResolver, PluginSettings, EpisodeResolver):
    implements = [UrlResolver, PluginSettings, EpisodeResolver]
    name = "乐视"

    def __init__(self):
        p = self.get_setting('priority') or 100
        self.priority = int(p)
        self.net = Net()


    def get_media_url(self, host, media_id):
        if media_id:
            res = urlresolvercn.get_res_setting()
            print media_id
            return self.resolve(media_id,res)
        else:
            return False
        
    def get_episode_urls(self, url):
        return self.get_episode(url)           
        
    def valid_ep_url(self, url):
        return self.valid_url(url,"")
        
    def get_url(self, host, media_id):
        return 'http://www.letv.com/ptv/vplay/{0}.html'.format(media_id)

    def get_host_and_id(self, url):
        r = re.search(r'http://(www.letv.com)/ptv/vplay/(\d+).html', url)
        if r:
            return r.groups()
        else:
            id = self.get_id(url)
            if id:
                return "www.letv.com",id
            else:
                return False
    def valid_url(self, url, host):
        if self.get_setting('enabled') == 'false':
            return False
        #http://www.m1905.com/vod/play/656339.shtml#flv
        return re.match(r'http://(www.letv.com)/ptv/vplay/(\d+).html', url) or 'letv' in url
