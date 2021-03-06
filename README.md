pygf
====

GrowthForecast API client written in python

Install:
----

```
pip install https://github.com/ReSTARTR/pygf/archive/master.zip
```

or

```
git clone git://github.com/ReSTARTR/pygf.git
cd pygf
python setup.py install
```

Usage:
----

pygf has same methods of [rb-growthforecast](https://github.com/tagomoris/rb-growthforecast)

### instantiate

```python
import pygf
gf = pygf.GrowthForecast('hostname', 5125)
```

### post

```python
spec = gf.post('service_name', 'section_name', 'graph_name', 30)
spec  #=> instance of pygf.Graph
```

### get

```python
glist = gf.graphs()
glist[0]['id']
glist[0]['service_name']
glist[0]['section_name']
glist[0]['graph_name']
glist[0].is_complex  #=> False

graph = gf.graph(glist[0]['id'])  #=> instance of pygf.Graph
graph['id']
graph['service_name']
graph['section_name']
graph['graph_name']
graph.is_complex  #=> False

clist = gf.complexes()

clist[0]['id']
clist[0]['service_name']
clist[0]['section_name']
clist[0]['graph_name']
clist[0].is_complex  #=> True

complex = gf.complex(clist[0]['id'])  #=> instance of pygf.Complex

complex['id']
complex['service_name']
complex['section_name']
complex['graph_name']
complex.is_complex  #=> True

for item in complex.data:
    graph = gf.graph(item['graph_id']).

l = gf.all()  #=> list of specs

tree = gf.tree()
tree['service_name']['section_name']['graph_name']  #=> instance of pygf.Graph

one = gf.by_name('service_name', 'section_name', 'graph_name')
```

### edit

```
TODO
```


### add graph

```python
gf.add_graph('example', 'test', 'graph1')

spec = pygf.Graph({'service_name': 'example', 'section_name': 'test', 'graph_name': 'graph2'})
g.add(spec)
```

### add complex

```python
gf.add_complex('example', 'test', 'summary1', 'testing...', True, 0, 'AREA', 'gauge', True, [graph1['id'], graph2['id']])

# or

spec = pygf.Complex({'service_name': 'example', 'section_name': 'test', 'graph_name': 'summary2',
                   'description': 'testing...', 'sumup': True,
                   'data': map(lambda id: {'graph_name': id, 'type': 'AREA', 'gmode': 'gauge', 'stack': True}, graph_id_list)})

gf.add(spec)
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
