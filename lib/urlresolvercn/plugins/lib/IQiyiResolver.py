#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2
import re
import json

from BeautifulSoup import BeautifulSoup


class IQiyiResolver:
    qualities = [(3, '超清'), (2, '高清'), (1, '流畅'), (96, '极速')]
    video_formats = [('m3u8', 'm3u8'), ('mp4', 'mp4'), ('flv', '分段flv')]

    def fetch_url(self, url):
        return urllib2.urlopen(url).read()

    def parse_web(self, url):
        content = self.fetch_url(url)
        _RE_VIDEOPLAY = re.compile(
            r'<div\s*class="videoPlay medium">\s*<div([^>]+)')
        match = _RE_VIDEOPLAY.search(content)
        if match:
            div_innerHtml = match.group(1)
            videoid = re.search(
                r'data-player-videoid="([^"]+)', div_innerHtml).group(1)
            tvid = re.search(
                r'data-player-tvid="([^"]+)', div_innerHtml).group(1)
        else:
            match = re.search(
                r'<script\s*type="text/javascript">\s*var info\s*=(.*?)</script>')  # noqa
            res = json.loads(match.group(1))
            videoid = res['videoId']
            tvid = res['tvId']

        return (tvid, videoid)

    def parse_m(self, tvid, videoid):
        url = 'http://cache.video.qiyi.com/m/%s/%s/' % (tvid, videoid)
        content = self.fetch_url(url)
        _SIG = 'ipadUrl='
        res = json.loads(content[content.find(_SIG) + len(_SIG):])

        return res['data']

    def parse_v(self, tvid, videoid):
        url = 'http://cache.video.qiyi.com/v/%s/%s' % (tvid, videoid)
        content = self.fetch_url(url)
        root = BeautifulSoup(content)

        return root.find('video')

    def try_prefix(self, url):
        prefixs = ['http://qiyi.soooner.com/videos2/',
                   'http://qiyi.soooner.com/videos/']
        part_url = '/'.join(url.rsplit('/', 3)[1:])

        for prefix in prefixs:
            tmp_url = prefix + part_url
            try:
                r = None
                r = urllib2.urlopen(tmp_url)
            except:
                continue
            finally:
                if r:
                    r.close()

            return prefix

        return prefix

    def adjust_url(self, url, prefix):
        part_url = '/'.join(url.rsplit('/', 3)[1:])

        return prefix + part_url

    def valid_url(self, url):
        return re.match(r'http://www.iqiyi.com/[^/]+/\d+/[0-9a-f]+.html', url)

    def resolve(self, url, media_type='m3u8', quality=None, fallback=True):
        tvid, videoid = self.parse_web(url)
        func = {
            'm3u8': self.resolve_m3u8,
            'mp4': self.resolve_mp4,
            'flv': self.resolve_flv,
        }[media_type]

        return func(tvid, videoid, quality, fallback)

    def resolve_m3u8(self, tvid, videoid, quality, fallback=True):
        res = self.parse_m(tvid, videoid)
        if quality is None:
            return res['url']

        quality_order = self.get_quality_order(quality)
        ordered_items = sorted(
            (self.get_quality_order(m['vd']), m['m3u']) for m in res['mtl'])

        for order, url in ordered_items:
            if quality_order == order:
                return url

            if quality_order < order:
                return url if fallback else None

        return ordered_items[-1][1]

    def resolve_mp4(self, tvid, videoid, quality, fallback=True):
        res = self.parse_m(tvid, videoid)
        url = res['mp4Url']
        prefix = self.try_prefix(url)
        url = self.adjust_url(url, prefix)
        return url

    def resolve_flv(self, tvid, videoid, quality, fallback=True):
        video_node = self.parse_v(tvid, videoid)

        if quality is not None:
            qualites_supported = dict((int(node.get('version')), node.text)
                                      for node in video_node.findAll('data'))

            if quality in qualites_supported:
                selected_videoid = qualites_supported[quality]
                if selected_videoid != videoid:
                    video_node = self.parse_v(tvid, selected_videoid)

            elif not fallback:
                return

            else:
                quality_order = self.get_quality_order(quality)
                ordered_items = sorted((self.get_quality_order(q), v)
                                       for q, v in qualites_supported.items())

                for q, v in ordered_items:
                    if quality_order < q:
                        video_node = self.parse_v(tvid, v)
                        break
        files = [node.text for node in video_node.findAll('file')]
        if not files:
            return

        prefix = self.try_prefix(files[0])

        url = 'stack://' + ' , '.join(
            self.adjust_url(url, prefix) for url in files)

        return url

    def get_quality_order(self, quality):
        for i, item in enumerate(self.qualities):
            if item[0] == quality:
                return i

        return -1

    def get_quality_by_index(self, index):
        index = min(max(0, index), len(self.qualities) - 1)
        return self.qualities[index][0]

    def get_videoformat_by_index(self, index):
        index = min(max(0, index), len(self.video_formats) - 1)
        return self.video_formats[index][0]
