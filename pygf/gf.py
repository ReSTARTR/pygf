# -*- coding: utf-8 -*-
import requests
import json
from collections import defaultdict
from .spec import Graph, Complex


class GrowthForecast(object):
    def __init__(self, host='localhost', port=5125, prefix=None, timeout=30, debug=False, username=None, password=None):
        self.host = host
        self.port = int(port)
        self.prefix = prefix or '/'
        self.timeout = int(timeout)
        self.debug = debug
        self.username = username
        self.password = password

    def debug(self, mode=None):
        if mode is None:
            return GrowthForecast(host=self.host, port=self.port, prefix=self.prefix, timeout=self.timeout,
                                  debug=True, username=self.username, password=self.password)
        mode = mode or False
        return self

    def url(self, path):
        if path[0] == '/':
            path = path[1:]
        return 'http://{0}:{1}{2}{3}'.format(self.host, self.port, self.prefix, path)

    def post(self, service_name, section_name, graph_name, value, mode=None, color=None):
        form = {'number': value}
        if mode:
            form['mode'] = mode
        if color:
            form['color'] = color
        path = '/api/{0}/{1}/{2}'.format(service_name, section_name, graph_name)
        res = requests.post(self.url(path), data=form)
        if res.status_code != 200:
            raise Exception(res.json()['messages'])
        d = res.json()
        if d['error'] == 0:
            if 'complex' in d['data']:
                return Complex(d['data'])
            return Graph(d['data'])

    def all(self):
        res = requests.get(self.url('/json/list/all'))
        for spec in res.json():
            if spec['complex']:
                yield Complex(spec)
            else:
                yield Graph(spec)

    def __len__(self):
        return len(list(self.all()))

    def tree(self):
        tree = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
        for graph in self.all():
            tree[graph['service_name']][graph['section_name']][graph['graph_name']] = graph
        return tree

    def by_name(self, service, section, name):
        return self.tree()[service][section][name] or {}

    def graphs(self):
        res = requests.get(self.url('/json/list/graph'))
        return res.json()

    def complexes(self):
        res = requests.get(self.url('/json/list/complex'))
        return res.json()

    def graph(self, id):
        res = requests.get(self.url('/json/graph/{0}'.format(id)))
        return res.json()

    def complex(self, id):
        res = requests.get(self.url('/json/complex/{0}'.format(id)))
        return res.json()

    def edit(self, spec):
        if not spec['id']:
            raise ValueError('cannot edit graph without id (get graph data from GrowthForecast at first)')

        if spec.is_complex:
            path = '/json/edit/complex/{0}'.format(spec['id'])
        else:
            path = '/json/edit/graph/{0}'.format(spec['id'])

        res = requests.post(self.url(path), data=spec)
        if res.status_code == 200:
            d = res.json()
            if spec.is_complex:
                return Complex(d['data'])
            else:
                return Graph(d['data'])

    def delete(self, spec):
        '''
        Args:
            spec: <dict> or <Graph> or <Complex>
        '''
        if not spec['id']:
            raise ValueError('cannot delete graph without id (get graph data from GrowthForecast at first)')

        if spec.is_complex:
            path = '/delete_complex/{id}'.format(**spec)
        else:
            path = '/delete/{service_name}/{section_name}/{graph_name}'.format(**spec)
        res = requests.post(self.url(path))
        if res.ok:
            return res.json()
        raise Exception('cannot delete')

    def add(self, spec):
        '''
        Args:
            spec: <Graph> or <Complex>
        '''
        if not isinstance(spec, (Graph, Complex)):
            raise ValueError('parameter of add() must be instance of Graph or Complex')

        if spec.is_complex:
            self.add_complex(**spec)
        self.add_graph(**spec)

    def add_graph(self, service_name='', section_name='', graph_name='', initial_value=0, color=None, mode=None):
        if not (service_name and section_name and graph_name):
            raise ValueError('service_name, section_name and graph_name must be specified')

        # TODO: check color pattern

        return self.post(service_name, section_name, graph_name, initial_value, mode, color)

    def add_complex(self, service, section, graph_name, description, sumup, sort, type, gmode, stack, data_graph_ids):
        data = map(lambda i: {'graph_id': i, 'type': type, 'gmode': gmode, 'stack': stack},
                   data_graph_ids)
        cmpl = {'service_name': service,
                'section_name': section,
                'graph_name': graph_name,
                'description': description,
                'sumup': sumup,
                'sort': sort,
                'data': data
        }
        res = requests.post(self.url('/json/create/complex'),
                            headers={'content-type': 'application/json'},
                            data=json.dumps(cmpl))
        if res.status_code == 200:
            d = res.json()
            if d['error'] == 0:
                return d['location']
            raise Exception(d)
        raise Exception(res)
