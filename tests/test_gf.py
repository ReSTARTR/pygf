# -*- coding: utf-8 -*-
from pygf import *
import pygf


class TestGrowthForecast(object):

    def pytest_funcarg__gf(self):
        gf = GrowthForecast('192.168.1.22')
        for graph in gf.all():
            gf.delete(graph)
        assert len(gf) == 0
        return gf

    def test_post(self, gf):
        graph = gf.post('foo', 'bar', 'baz', 1)
        assert isinstance(graph, Graph)
        assert len(gf) == 1

        gf.delete(graph)
        assert len(gf) == 0

    def test_iter(self, gf):
        graph1 = gf.post('foo', 'bar', 'baz1', 1)
        graph2 = gf.post('foo', 'bar', 'baz2', 1)

        assert len(gf) == 2
        assert isinstance(gf.all(), list)
        for graph in gf.all():
            assert isinstance(graph, Graph)

        assert gf.tree().keys() == ['foo']
        assert gf.tree()['foo'].keys() == ['bar']
        assert gf.tree()['foo']['bar'].keys() == ['baz1', 'baz2']

        graph = gf.by_name('foo', 'bar', 'baz1')
        assert isinstance(graph, Graph)
        assert graph['graph_name'] == 'baz1'

    def test_add_graph(self, gf):
        graph = gf.add_graph('foo', 'bar', 'graph1', initial_value=0, color='#223344', mode='gauge')
        assert isinstance(graph, Graph)
        assert graph['graph_name'] == 'graph1'

        graph = gf.add_graph('foo', 'bar', 'graph2', initial_value=0, color='#223344', mode='gauge')
        assert isinstance(graph, Graph)
        assert graph['graph_name'] == 'graph2'

    def test_complex(self, gf):
        loc = gf.add_complex('foo', 'bar', 'complex1', 'tests', False, 19, 'AREA', 'gauge', False, [1, 2])
        assert isinstance(loc, basestring)
        assert '/list/foo/bar' in loc
