# -*- coding: utf-8 -*-
from pygf.spec import BaseDict
import pytest


class TestBaseDict():

    def pytest_funcarg__d(self, request):
        class D(BaseDict):
            _attrs = {
                'foo': {'type': int, 'default': 3},
                'bar': {'default': 'barbar'},
                'req1': {'requires': True},
            }
        return D({})

    def test_contains(self, d):
        assert 'foo' in d
        assert 'bar' in d
        assert 'baz' not in d

    def test_getitem(self, d):
        assert d['foo'] == 3
        assert d['bar'] == 'barbar'
        with pytest.raises(KeyError):
            d['baz']

    def test_getitem(self, d):
        d.update({'foo': 4, 'bar': 'barbarbar'})
        assert d['foo'] == 4
        assert d['bar'] == 'barbarbar'
        with pytest.raises(KeyError):
            d['baz'] = 'setval'

    def test_type_conversion(self, d):
        d['foo'] = '4'
        assert d['foo'] == 4

    def test_as_unpack_as_kwargs(self, d):
        def f(**kwargs):
            assert kwargs['foo'] == 3
            assert kwargs['bar'] == 'barbar'
        f(**d)

    def test_to_json(self, d):
        with pytest.raises(Exception):
            d.to_json()  # not set 'req1' yet
        d['req1'] = 999
        assert d.to_json() == '{"foo": 3, "bar": "barbar", "req1": 999}'
