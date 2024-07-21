A simple logic to igraph toy lang

Example:

```
python logicpy/parser.py <<< 'exist (v): and(name_ne(v, "Alice"), age_lt(v, 30))'
Vertices [igraph.Vertex(<igraph.Graph object at 0x71ff57b6c050>, 0, {'name': 'Alice', 'age': 25, 'gender': 'f'}),
 igraph.Vertex(<igraph.Graph object at 0x71ff57b6c050>, 1, {'name': 'Bob', 'age': 31, 'gender': 'm'}),
 igraph.Vertex(<igraph.Graph object at 0x71ff57b6c050>, 2, {'name': 'Claire', 'age': 18, 'gender': 'f'}),
 igraph.Vertex(<igraph.Graph object at 0x71ff57b6c050>, 3, {'name': 'Dennis', 'age': 47, 'gender': 'm'}),
 igraph.Vertex(<igraph.Graph object at 0x71ff57b6c050>, 4, {'name': 'Esther', 'age': 22, 'gender': 'f'}),
 igraph.Vertex(<igraph.Graph object at 0x71ff57b6c050>, 5, {'name': 'Frank', 'age': 23, 'gender': 'm'}),
 igraph.Vertex(<igraph.Graph object at 0x71ff57b6c050>, 6, {'name': 'George', 'age': 50, 'gender': 'm'})]
> query exist (v): and(name_ne(v, "Alice"), age_lt(v, 30))
{'v': {igraph.Vertex(<igraph.Graph object at 0x71ff57b6c050>, 2, {'name': 'Claire', 'age': 18, 'gender': 'f'}),
       igraph.Vertex(<igraph.Graph object at 0x71ff57b6c050>, 4, {'name': 'Esther', 'age': 22, 'gender': 'f'}),
       igraph.Vertex(<igraph.Graph object at 0x71ff57b6c050>, 5, {'name': 'Frank', 'age': 23, 'gender': 'm'})}}
(logicpy-py3.12) ➜  logicpy git:(master) ✗ python logicpy/parser.py <<< 'exist (v): and(name_ne(v, "Alice"), age_lt(v, 30))'
```

To install and run the example above: `poetry install && poetry shell`

* `exists` and `forall` are ignored for now
