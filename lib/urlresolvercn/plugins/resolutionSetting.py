#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,re
import xbmcgui
from urlresolvercn.plugnplay.interfaces import PluginSettings
from urlresolvercn.plugnplay import Plugin
from urlresolvercn import common


class ResolutionSetting( Plugin, PluginSettings):
    implements = [PluginSettings]
    name = "通用分辨率设置"
    qualities =[[1,"320P(流畅)"],
                [2,"480P(高清)"],
                [3,"720P(超清)"],
                [4,"1080P(蓝光)"]]

    def __init__(self):
        p = self.get_setting('priority') or 100
        self.priority = int(p)

    def get_settings_xml(self):
        xml = PluginSettings.get_settings_xml(self)
        xml += '''\
<setting label="清晰度" id="{prefix}_quality" type="enum" values="{qualities}" default="0"/>
'''.format(prefix=self.__class__.__name__,
            qualities='每次询问|' + '|'.join(q[1] for q in self.qualities))

        return xml
