#-*- coding:utf-8 -*-
import urllib
import urllib2
import re
import json
from collections import defaultdict
import xml.etree.ElementTree
from .base import export, with_styles
from .webservice import WebService
from aqt.utils import showInfo


class Baicizhan(WebService):

    __register_label__ = u'百词斩'

    def __init__(self):
        super(Baicizhan, self).__init__()

    def _get_from_api(self, lang='eng'):
        url = "http://mall.baicizhan.com/ws/search?w={word}".format(
            word=self.word)
        try:
            html = urllib2.urlopen(url, timeout=5).read()
            return self.cache_this(json.loads(html))
        except:
            return defaultdict(str)

    @export(u'发音', 0)
    def fld_phonetic(self):
        url = 'http://baicizhan.qiniucdn.com/word_audios/{word}.mp3'.format(
            word=self.word)
        audio_name = 'bcz_{word}.mp3'.format(word=self.word)
        try:
            urllib.urlretrieve(url, 'bcz_{word}.mp3'.format(word=self.word))
            return '[sound: %s]' % audio_name
        except:
            return url

    @export(u'音标', 1)
    def fld_explains(self):
        return self.cache_result('accent') if self.cached('accent') else self._get_from_api(self.word)['accent']

    @export(u'图片', 2)
    def fld_img(self):
        return self.cache_result('img') if self.cached('img') else self._get_from_api(self.word)['img']

    @export(u'象形', 3)
    def fld_df(self):
        return self.cache_result('df') if self.cached('df') else self._get_from_api(self.word)['df']

    @export(u'中文释义', 6)
    def fld_mean(self):
        return self.cache_result('mean_cn') if self.cached('mean_cn') else self._get_from_api(self.word)['mean_cn']

    @export(u'英文例句', 4)
    def fld_st(self):
        return self.cache_result('st') if self.cached('st') else self._get_from_api(self.word)['st']

    @export(u'例句翻译', 5)
    def fld_sttr(self):
        return self.cache_result('sttr') if self.cached('sttr') else self._get_from_api(self.word)['sttr']

    @export(u'单词tv', 7)
    def fld_tv_url(self):
        return self.cache_result('tv') if self.cached('tv') else self._get_from_api(self.word)['tv']
