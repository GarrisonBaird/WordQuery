#-*- coding:utf-8 -*-
import inspect
from functools import wraps
import os
from aqt import mw
from aqt.utils import showInfo
from wquery.utils import MapDict
from wquery.context import config


def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton


class ServiceProfile(object):

    def __init__(self, label, cls, instance=None):
        self.label = label
        self.cls = cls
        self.instance = instance
        self.title = label


class ServiceManager(object):

    def __init__(self):
        self.services = self.get_available_services()

    def register(self, service):
        pass

    def start_all(self):
        for service in self.services:
            service.instance = service.cls()

    def get_service(self, label):
        # webservice manager 使用combobox的文本值选择服务
        # mdxservice manager 使用combox的itemData即字典路径选择服务
        for each in self.services:
            if each.label == label:
                return each

    def get_service_action(self, service, label):
        for each in service.fields:
            if each.label == label:
                return each

    def get_available_services(self):
        '''reimplement'''


class Service(object):
    '''service base class'''

    def __init__(self):
        self._exporters = self.get_exporters()
        self._fields, self._actions = zip(
            *self._exporters) if self._exporters else (None, None)
        self.default_result = QueryResult(result="")

    @property
    def fields(self):
        return self._fields

    @property
    def actions(self):
        return self._actions

    @property
    def exporters(self):
        return self._exporters

    def get_exporters(self):
        flds = dict()
        methods = inspect.getmembers(self, predicate=inspect.ismethod)
        for method in methods:
            export_attrs = getattr(method[1], '__export_attrs__', None)
            if export_attrs:
                label, index = export_attrs
                flds.update({int(index): (label, method[1])})
        sorted_flds = sorted(flds)
        # label, function
        return [flds[key] for key in sorted_flds]

    def active(self, action_label, word):
        self.word = word
        # showInfo('service active: %s ##%s##' % (action_label, word))
        for each in self.exporters:
            if action_label == each[0]:
                result = each[1]()
                return result if result else self.default_result  # avoid return None
        return self.default_result


class QueryResult(MapDict):
    """Query Result structure"""
    pass
# define decorators below----------------------------


def register(label):
    """register the dict service with a label, which will be shown in the dicts list."""
    def _deco(cls):
        return _deco
    cls.__register_label__ = label
    return cls


def export(label, index):
    """export dict field function with a label, which will be shown in the fields list."""
    def _with(fld_func):
        @wraps(fld_func)
        def _deco(cls, *args, **kwargs):
            res = fld_func(cls, *args, **kwargs)
            return QueryResult(result=res) if not isinstance(res, QueryResult) else res
        _deco.__export_attrs__ = (label, index)
        return _deco
    return _with


def with_styles(**styles):
    def _with(fld_func):
        def _deco(cls, *args, **kwargs):
            res = fld_func(cls, *args, **kwargs)
            if styles:
                if not isinstance(res, QueryResult):
                    return QueryResult(result=res, **styles)
                else:
                    res.css = css
                    return res
            return res
        return _deco
    return _with

if __name__ == '__main__':
    from youdao import Youdao
    yd = Youdao()
    flds = yd.get_export_flds()
    for each in flds:
        print each.export_fld_label
