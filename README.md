pygf
====

GrowthForecast API client written in python

Usage:
----

compatible with [rb-growthforecast](https://github.com/tagomoris/rb-growthforecast)

### post

```python
from pygf import gf
api = gf.GrowthForecast('hostname', 5125)
api.post('service_name', 'section_name', 'graph_name', 30)
```

### get

```python
graphs = api.graphs():
graphs[0]['id']
graphs[0]['service_name']
graphs[0]['section_name']
graphs[0]['graph_name']
graphs[0].is_complex  #=> False

graph = api.graph(graphs[0]['id'])  #=> instance of pygf.gf.Graph
graph['id']
graph['service_name']
graph['section_name']
graph['graph_name']
graph.is_complex  #=> False

clist = api.complexes()

clist[0]['id']
clist[0]['service_name']
clist[0]['section_name']
clist[0]['graph_name']
clist[0].is_complex  #=> True

complex = api.complex(clist[0]['id'])  #=> instance of pygf.gf.Complex

complex['id']
complex['service_name']
complex['section_name']
complex['graph_name']
complex.is_complex  #=> True

for item in complex.data:
    graph = api.graph(item['graph_id']).

l = api.all()

tree = api.tree()
tree['service_name']['section_name']['graph_name']  #=> instance of gf.Graph

one = api.by_name('service_name', 'section_name', 'graph_name')
```

### edit

```
TODO
```


### add graph

```python
api.add_graph('example', 'test', 'graph1')

spec = gf.Graph({'service_name': 'example', 'section_name': 'test', 'graph_name': 'graph2'})
g.add(spec)
```

### add complex

```python
api.add_complex('example', 'test', 'summary1', 'testing...', True, 0, 'AREA', 'gauge', True, [graph1['id'], graph2['id']])

# or

spec = gf.Complex({'service_name': 'example', 'section_name': 'test', 'graph_name': 'summary2',
            'description': 'testing...', 'sumup': True,
            'data': map(lambda id: {'graph_name': id, 'type': 'AREA', 'gmode': 'gauge', 'stack': True}, graph_id_list)})

api.add(spec)
```

Basic Authentication
----

```python
TODO
```

gfclient
----

```python
TODO
```
