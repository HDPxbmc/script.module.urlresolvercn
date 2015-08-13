#!/usr/bin/python
# -*- coding: utf-8 -*-
from t0mm0.common.net import Net
from urlresolvercn.plugnplay.interfaces import UrlResolver
from urlresolvercn.plugnplay.interfaces import PluginSettings
from urlresolvercn.plugnplay import Plugin
from lib.IQiyiResolver import IQiyiResolver
import re


class M1905Resolver(IQiyiResolver, Plugin, UrlResolver, PluginSettings):
    implements = [UrlResolver, PluginSettings]
    name = "m1905"

    def __init__(self):
        p = self.get_setting('priority') or 100
        self.priority = int(p)
        self.net = Net()


    def get_media_url(self, host, media_id):
        url = "http://static.m1905.com/profile/vod/{0}/{1}/{2}_1_0.xml".format(media_id[0],media_id[1],media_id)
        print url
        html = self.net.http_GET(url).content
        r = re.search(r'bkurl="(.*?)"', html)
        if r:
            return r.group(1)
        else: 
            return False
        
    def get_url(self, host, media_id):
        return 'http://www.m1905.com/vod/play/{0}.shtml#flv'.format(media_id)

    def get_host_and_id(self, url):
        r = re.search(r'http://(www.m1905.com)/vod/play/(\d+)\.shtml', url)
        if r:
            return r.groups()
        else:
            r = re.search('//(.+?)/([\w]+)', url)
            if r:
                return r.groups()
            else:
                return False

    def valid_url(self, url, host):
        if self.get_setting('enabled') == 'false':
            return False
        #http://www.m1905.com/vod/play/656339.shtml#flv
        return (re.match(r'http://www.m1905.com/vod/play/\d+\.shtml', url) or 'm1905' in host)
