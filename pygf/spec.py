# -*- coding: utf-8 -*-
import json
import time
import datetime

from . import TIME_FORMAT


def gf_str2time(s, fmt=TIME_FORMAT):
    if s and isinstance(s, basestring):
        st = time.strptime(s, fmt)
        return datetime.datetime.fromtimestamp(time.mktime(st))
    return s


class BaseDict(dict):
    _attrs = {}

    def __init__(self, data):
        if isinstance(data, basestring):
            data = json.loads(data)

        for k, v in self._attrs.items():
            if self._has_default(k):
                self.__setitem__(k, self._get_default(k))
            if k in data:
                self.__setitem__(k, data[k])

    def _has_default(self, k):
        return k in self._attrs \
               and 'default' in self._attrs[k]

    def _get_default(self, k):
        return self._attrs.get(k, {}).get('default')

    def _has_type(self, k):
        return k in self._attrs \
                and 'type' in self._attrs[k]

    def _get_type(self, k):
        return self._attrs.get(k, {}).get('type')

    def _to_type(self, k, v):
        if v is None:
            return v
        if self._has_type(k):
            return self._get_type(k)(v)
        return v

    def __setitem__(self, k, v):
        if not k in self._attrs:
            raise KeyError
        return dict.__setitem__(self, k, self._to_type(k, v))

    def __contains__(self, k):
        return k in self._attrs

    def to_json(self):
        for k, v in self._attrs.items():
            if v.get('requires') and not dict.__contains__(self, k):
                raise ValueError('cannnot jsonify')
        return json.dumps(self)


class Graph(BaseDict):
    is_complex = False

    _attrs = {
        'id': {'type': int},
        'service_name': {},
        'section_name': {},
        'graph_name': {},
        'description': {},
        'mode': {'default': 'gauge'},
        'sort': {'type': int, 'default': 19},
        'color': {'requires': True},
        'gmode': {'default': 'gauge'},
        'type': {'default': 'AREA'},
        'ulimit': {'default': 1000000000},
        'llimit': {'default': -1000000000},
        'stype': {'default': 'AREA'},
        'sulimit': {'default': 1000000000},
        'sllimit': {'default': -1000000000},
        'adjustval': {'type': int, 'default': 1},
        'unit': {'default': ''},
        'number': {'type': int, 'default': 0},
        'data': {'type': list, 'default': []},
        'created_at': {'type': gf_str2time},
        'updated_at': {'type': gf_str2time},
    }


class Item(BaseDict):
    _attrs = {
        'graph_id': {'type': int, 'default': None, 'requires': True},
        'gmode': {'default': 'gauge'},
        'stack': {'default': False},
        'type': {'default': 'AREA'},
    }

    @staticmethod
    def load(v):
        if not isinstance(v, Item):
            return Item(v)
        return v


class Complex(BaseDict):
    is_complex = True

    _attrs = {
        'id': {'type': int},
        'service_name': {},
        'section_name': {},
        'graph_name': {},
        'description': {},
        'sort': {'type': int, 'default': 19},
        'sumup': {'default': False},
        'data': {'type': lambda v: map(lambda _v: Item.load(_v), v)},
        'number': {'type': int, 'default': 0},
        'created_at': {'type': gf_str2time},
        'updated_at': {'type': gf_str2time},
    }

    def __init__(self, *args, **kwargs):
        self.options = {}
        self.graph_ids = []
        super(Complex, self).__init__(*args, **kwargs)

    def set_options(self, options):
        self.options = options

    def add_graph_id(self, id):
        self.graph_ids.append(id)

    def __getitem__(self, k):
        if k != 'data':
            return super(Complex, self).__getitem__(k)
        ds = []
        for id in self.graph_ids:
            d = {'graph_id': id}
            d.update(self.options)
            ds.append(Item(d))
        return ds


def Spec(object):

    def __init__(self, dic, spec_yaml, complex=False):
        self.dic = dic
        self.spec = spec_yaml
        self.name = self.spec['name']
        self.path = self.spec['name']
        self.complex = self.spec['complex'] or complex
        (self.service_name, section_name, graph_name) = self.path.split('/')
        if not (self.service_name and section_name and graph_name):
            raise Exception('\'path\' must be as service/section/graph')

    @property
    def is_complex(self):
        return self.complex

    def replace_keywords(self, s):
        for (i, k) in enumerate(self.dic):
            key = '${%d}' % i
            if key in s:
                s.replace(key, self.dic[k])
        return s

    def check(self, cahce):
        target = cache.get(self.service_name, self.section_name, self.graph_name)
        if not target:
            return (False, ['target path does not exists'])
        elif self.is_complex and target.is_complex:
            return (False, ['complex type is not match'])

        if self.is_complex:
            return self.check_complex(cache, target)
        return self.check_graph(cache, target)

    def merge(self, cache, target):
        if self.is_complex:
            return self.merge_complex(cache, target)
        return self.merge_graph(cache, target)

    def check_graph(self, cache, target):
        errs = []
        for attr in Graph._attrs.keys():
            if not attr in spec:
                target_v = target[attr]
                if attr == 'description' and self.spec[attr]:
                    spec_v = self.replace_keywords(self.spec[attr])
                else:
                    spec_v = self.spec[attr]
                if target_v == spec_v:
                    print 'attribute {0} value mismatch: {1} != {2}'.format(attr, spec_v, target_v)
        return errs


    def merge_graph(self, cache, target):
        if not target:
            target = Graph({'service_name': self.service_name,
                            'section_name': self.section_name,
                            'graph_name': self.graph_name,
                            'description': ''})
        for attr in Graph._attrs.keys():
            if 'attr' in self.spec:
                if attr == 'description':
                    v = self.spec[attr]
                else:
                    v = self.spec[attr]
                target[attr] = v
        return target

    def check_complex(self, cache, target):
        pass

    def merge_complex(self, cache, target):
        pass
