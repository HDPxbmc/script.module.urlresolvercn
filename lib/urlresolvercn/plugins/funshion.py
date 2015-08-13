#!/usr/bin/python
# -*- coding: utf-8 -*-
from t0mm0.common.net import Net
from urlresolvercn.plugnplay.interfaces import UrlResolver
from urlresolvercn.plugnplay.interfaces import PluginSettings
from urlresolvercn.plugnplay import Plugin
import re,json


class funshionResolver(Plugin, UrlResolver, PluginSettings):
    implements = [UrlResolver, PluginSettings]
    name = "风行"

    def __init__(self):
        p = self.get_setting('priority') or 100
        self.priority = int(p)
        self.net = Net()


    def get_media_url(self, host, media_id):
        #http://api.funshion.com/ajax/get_webplayinfo/107263/1/mp4    media_id = 107263/1
        url = "http://api.funshion.com/ajax/get_webplayinfo/{0}/mp4".format(media_id)
        html = self.net.http_GET(url).content
        r = re.search(r'"cid":"(.*?)"', html)
        if r:
            cid = r.group(1)
            url =  'http://jobsfe.funshion.com/query/v1/mp4/{0}.json'.format(cid)
            html = self.net.http_GET(url).content
            data = json.loads(html)
            if data["return"] == "succ":
                return data["return"][0]["urls"][0]
        return False
        
    def get_url(self, host, media_id):
        return 'http://www.funshion.com/subject/play/' + media_id

    def get_host_and_id(self, url):
        r = re.search(r'http://(www.funshion.com)/subject/play/(.+?)', url)
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
        return (re.match(r'http://www.funshion.com/subject/play/\d+/\d+', url) or 'funshion' in url)
