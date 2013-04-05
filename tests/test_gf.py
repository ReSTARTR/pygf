# -*- coding: utf-8 -*-
from pygf import *
import unittest


class TestGrowthForecast(unittest.TestCase):

    def setUp(self):
        self.gf = GrowthForecast('192.168.1.22')
        for graph in self.gf.all():
            self.gf.delete(graph)
        self.assertEqual(len(self.gf), 0)

    def test_post(self):
        graph = self.gf.post('foo', 'bar', 'baz', 1)
        self.assertIsInstance(graph, Graph)
        self.assertEqual(len(self.gf), 1)

        self.gf.delete(graph)
        self.assertEqual(len(self.gf), 0)

    def test_iter(self):
        graph1 = self.gf.post('foo', 'bar', 'baz1', 1)
        graph2 = self.gf.post('foo', 'bar', 'baz2', 1)

        self.assertEqual(len(self.gf), 2)
        self.assertIsInstance(self.gf.all(), list)
        for graph in self.gf.all():
            self.assertIsInstance(graph, Graph)

        self.assertEqual(self.gf.tree().keys(), ['foo'])
        self.assertEqual(self.gf.tree()['foo'].keys(), ['bar'])
        self.assertEqual(self.gf.tree()['foo']['bar'].keys(), ['baz1', 'baz2'])

        graph = self.gf.by_name('foo', 'bar', 'baz1')
        self.assertIsInstance(graph, Graph)
        self.assertEqual(graph['graph_name'], 'baz1')

    def test_add_graph(self):
        graph = self.gf.add_graph('foo', 'bar', 'graph1', initial_value=0, color='#223344', mode='gauge')
        self.assertIsInstance(graph, Graph)
        self.assertEqual(graph['graph_name'], 'graph1')

        graph = self.gf.add_graph('foo', 'bar', 'graph2', initial_value=0, color='#223344', mode='gauge')
        self.assertIsInstance(graph, Graph)
        self.assertEqual(graph['graph_name'], 'graph2')

    def test_complex(self):
        loc = self.gf.add_complex('foo', 'bar', 'complex1', 'tests', False, 19, 'AREA', 'gauge', False, [1, 2])
        self.assertIsInstance(loc, basestring)
        self.assertTrue('/list/foo/bar' in loc)
