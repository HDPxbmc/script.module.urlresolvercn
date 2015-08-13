'''
ovfile urlresolver plugin
Copyright (C) 2011 anilkuj

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''

from t0mm0.common.net import Net
import urlresolvercn
from urlresolvercn.plugnplay.interfaces import UrlResolver
from urlresolvercn.plugnplay.interfaces import PluginSettings
from urlresolvercn.plugnplay.interfaces import EpisodeResolver
from urlresolvercn.plugnplay import Plugin
from lib.IyoukuResolver import IyoukuResolver
import re



class YoukuResolver(IyoukuResolver, Plugin, UrlResolver, EpisodeResolver, PluginSettings):
    implements = [UrlResolver, PluginSettings, EpisodeResolver]
    name = "优酷"

    def __init__(self):
        p = self.get_setting('priority') or 100
        self.priority = int(p)
        self.net = Net()


    def get_media_url(self, host, media_id):
        res = urlresolvercn.get_res_setting()
        return self.resolve(media_id,res)

    def get_url(self, host, media_id):  
        return 'http://v.youku.com/v_show/id_{0}.html'.format(media_id)
        
        
    def get_host_and_id(self, url):
        r = re.search(r'http://(v.youku.com)/v_show/id_([0-9A-Za-z]+)\.html', url)
        if r:
            return r.groups()
        else:
            r = re.search('//(.+?)/([\w]+)', url)
            if r:
                return r.groups()
            else:
                return False
         
    def get_episode_urls(self, url):
        list_id = self.get_list_id(url)
        result = self.get_episode(list_id)
        return result           
        
    def valid_ep_url(self, url):
        return self.valid_url(url,"")
                
    def valid_url(self, url, host):
        print "valid " + url
        if self.get_setting('enabled') == 'false':
            return False
        return (re.match(r'http://v.youku.com/v_show/id_[0-9A-Za-z]+\.html', url) or 'youku' in host)

