#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,re
import xbmcgui
from t0mm0.common.net import Net
from urlresolvercn.plugnplay.interfaces import UrlResolver
from urlresolvercn.plugnplay.interfaces import PluginSettings
from urlresolvercn.plugnplay.interfaces import EpisodeResolver
from urlresolvercn.plugnplay import Plugin
from urlresolvercn import common
from lib.IQiyiResolver import IQiyiResolver


class IQiyiResolver_(IQiyiResolver, Plugin, UrlResolver, EpisodeResolver, PluginSettings):
    implements = [UrlResolver, PluginSettings,EpisodeResolver]
    name = "爱奇艺"

    def __init__(self):
        p = self.get_setting('priority') or 100
        self.priority = int(p)
        self.net = Net()

    def fetch_url(self, url):
        return self.net.http_GET(url).content

    def get_media_url(self, host, media_id):
        url = self.get_url(host, media_id)

        videoformat = self.get_videoformat_by_index(
            int(self.get_setting('videoformat')))
        quality_index = int(self.get_setting('quality')) - 1
        if quality_index == -1 and videoformat != 'mp4':
            dialog = xbmcgui.Dialog()
            quality_index = dialog.select(
                '请选择适合的清晰度', [q for _, q in self.qualities])
            if quality_index == -1:
                quality_index = 0
        quality = self.get_quality_by_index(quality_index)

        media_url = self.resolve(url, videoformat, quality)
        common.addon.log_debug(media_url)

        if not media_url:
            error_logo = os.path.join(
                common.addon_path, 'resources', 'images', 'redx.png')
            common.addon.show_small_popup(
                '爱奇艺解析失败', '未找到合适的视频资源', 8000, error_logo)

        return media_url

    def get_url(self, host, media_id):
        return media_id

    def get_host_and_id(self, url):
        return url[7:url.find('/', 7)], url
        
    def get_episode_urls(self, url):
        html = self.net.http_GET(url).content
        
        match = re.compile(r'<div id="j-album-\d" style="display: none;">(/common/topicinc/.+?/playlist_\d.inc)</div>', re.DOTALL).findall(html)
        result =[]
        for playlist in match:
            listUrl = "http://www.iqiyi.com" + playlist
            listHTML = self.net.http_GET(listUrl).content.replace("\n","").replace("\r","")
            match1 = re.compile(r'data-lazy="(.+?)" title=".+?" alt=".+?" class=" "><span class="s1"></span> <span class="s2">.+?</span> </a><p><a href="(.+?)">(第\d+集)</a></p><p>(.*?)</p>', re.DOTALL).findall(listHTML)
            if not match1:
                match1 = re.compile(r'src="(.+?)" title=".+?" alt=".+?" class=" "><span class="s1"></span> <span class="s2">.+?</span> </a><p><a href="(.+?)">(第\d+集)</a></p><p>(.*?)</p>', re.DOTALL).findall(listHTML)
            for listitem in match1:    
                result.append({"title":listitem[2] + " " + listitem[3],
                                "img":listitem[0],
                                "url":listitem[1]})
        return result           
        
    def valid_ep_url(self, url):
        if self.get_setting('enabled') == 'false':
            return False
        return ("qiyi" in url)
        
    def valid_url(self, url, host):
        if self.get_setting('enabled') == 'false':
            return False

        return IQiyiResolver.valid_url(self, url)

    def get_settings_xml(self):
        xml = PluginSettings.get_settings_xml(self)
        xml += '''\
<setting label="视频格式" id="{prefix}_videoformat" type="enum" values="{videoformat}" default="0" />
<setting label="清晰度" id="{prefix}_quality" type="enum" values="{qualities}" default="0"/>
'''.format(prefix=self.__class__.__name__,
            videoformat='|'.join(v[1] for v in self.video_formats),
            qualities='每次询问|' + '|'.join(q[1] for q in self.qualities))

        return xml
