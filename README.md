A simple logic to igraph toy lang

Examples:

```
python -i logicpy/parser.py <<< 'exist (v): or(and(age_lt(v, 25), gender_eq(v, "f")), name_eq(v, "Frank"))'
Vertices [igraph.Vertex(<igraph.Graph object at 0x7bb25a9c6950>, 0, {'name': 'Alice', 'age': 25, 'gender': 'f'}),
 igraph.Vertex(<igraph.Graph object at 0x7bb25a9c6950>, 1, {'name': 'Bob', 'age': 31, 'gender': 'm'}),
 igraph.Vertex(<igraph.Graph object at 0x7bb25a9c6950>, 2, {'name': 'Claire', 'age': 18, 'gender': 'f'}),
 igraph.Vertex(<igraph.Graph object at 0x7bb25a9c6950>, 3, {'name': 'Dennis', 'age': 47, 'gender': 'm'}),
 igraph.Vertex(<igraph.Graph object at 0x7bb25a9c6950>, 4, {'name': 'Esther', 'age': 22, 'gender': 'f'}),
 igraph.Vertex(<igraph.Graph object at 0x7bb25a9c6950>, 5, {'name': 'Frank', 'age': 23, 'gender': 'm'}),
 igraph.Vertex(<igraph.Graph object at 0x7bb25a9c6950>, 6, {'name': 'George', 'age': 50, 'gender': 'm'})]
> query::  exist (v): or(and(age_lt(v, 25), gender_eq(v, "f")), name_eq(v, "Frank"))
{'v': {igraph.Vertex(<igraph.Graph object at 0x7bb25a9c6950>, 2, {'name': 'Claire', 'age': 18, 'gender': 'f'}),
       igraph.Vertex(<igraph.Graph object at 0x7bb25a9c6950>, 4, {'name': 'Esther', 'age': 22, 'gender': 'f'}),
       igraph.Vertex(<igraph.Graph object at 0x7bb25a9c6950>, 5, {'name': 'Frank', 'age': 23, 'gender': 'm'})}}
>>> 
```

```
python logicpy/parser.py <<< 'exist (v, e): _between(e, name_eq(a, "Alice"), name_eq(b, "Bob"))'
Vertices [igraph.Vertex(<igraph.Graph object at 0x7cee433fee50>, 0, {'name': 'Alice', 'age': 25, 'gender': 'f'}),
 igraph.Vertex(<igraph.Graph object at 0x7cee433fee50>, 1, {'name': 'Bob', 'age': 31, 'gender': 'm'}),
 igraph.Vertex(<igraph.Graph object at 0x7cee433fee50>, 2, {'name': 'Claire', 'age': 18, 'gender': 'f'}),
 igraph.Vertex(<igraph.Graph object at 0x7cee433fee50>, 3, {'name': 'Dennis', 'age': 47, 'gender': 'm'}),
 igraph.Vertex(<igraph.Graph object at 0x7cee433fee50>, 4, {'name': 'Esther', 'age': 22, 'gender': 'f'}),
 igraph.Vertex(<igraph.Graph object at 0x7cee433fee50>, 5, {'name': 'Frank', 'age': 23, 'gender': 'm'}),
 igraph.Vertex(<igraph.Graph object at 0x7cee433fee50>, 6, {'name': 'George', 'age': 50, 'gender': 'm'})]
> query::  exist (v, e): _between(e, name_eq(a, "Alice"), name_eq(b, "Bob"))
{'a': {igraph.Vertex(<igraph.Graph object at 0x7cee433fee50>, 0, {'name': 'Alice', 'age': 25, 'gender': 'f'})},
 'b': {igraph.Vertex(<igraph.Graph object at 0x7cee433fee50>, 1, {'name': 'Bob', 'age': 31, 'gender': 'm'})},
 'e': {igraph.Edge(<igraph.Graph object at 0x7cee433fee50>, 0, {'is_formal': False})}}
(logicpy-py3.12) ➜  logicpy git:(master) ✗ gs
```

To install and run the example above: `poetry install && poetry shell`

* `exists` and `forall` are ignored for now
