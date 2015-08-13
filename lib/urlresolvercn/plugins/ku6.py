#!/usr/bin/python
# -*- coding: utf-8 -*-
from t0mm0.common.net import Net
from urlresolvercn.plugnplay.interfaces import UrlResolver
from urlresolvercn.plugnplay.interfaces import PluginSettings
from urlresolvercn.plugnplay import Plugin
import re,json


class Ku6Resolver(Plugin, UrlResolver, PluginSettings):
    implements = [UrlResolver, PluginSettings]
    name = "ku6"

    def __init__(self):
        p = self.get_setting('priority') or 100
        self.priority = int(p)
        self.net = Net()


    def get_media_url(self, host, media_id):
        #http://api.funshion.com/ajax/get_webplayinfo/107263/1/mp4    media_id = 107263/1
        url =  'http://v.ku6.com/fetch.htm?t=getVideo4Player&vid=' + media_id
        html = self.net.http_GET(url).content
        data = json.loads(html)
        if data["data"]:
            return data["data"]["f"]
        return False
        
    def get_url(self, host, media_id):
        return 'http://v.ku6.com/show/{0}.html'.format( media_id)

    def get_host_and_id(self, url):
        r = re.search(r'http://(v.ku6.com)/.+?/(.{24})\.html', url)
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
            #http://v.ku6.com/show/mnFWW4UoYLmmz4ZznoWPvg...html
            #http://v.ku6.com/special/show_4771038/CnHse2JnNMbq8zPDKXn7Nw...html
        return (re.match(r'http://v.ku6.com/.+?/(.{24})\.html', url) or 'ku6' in url)
