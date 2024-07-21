A simple logic to igraph toy lang

Example:

```
python -i logicpy/parser.py <<< 'exist (v): or(and(age_lt(v, 25), gender_eq(v, "f")), name_eq(v, "Frank"))'
Vertices [igraph.Vertex(<igraph.Graph object at 0x7f9e6b760150>, 0, {'name': 'Alice', 'age': 25, 'gender': 'f'}),
 igraph.Vertex(<igraph.Graph object at 0x7f9e6b760150>, 1, {'name': 'Bob', 'age': 31, 'gender': 'm'}),
 igraph.Vertex(<igraph.Graph object at 0x7f9e6b760150>, 2, {'name': 'Claire', 'age': 18, 'gender': 'f'}),
 igraph.Vertex(<igraph.Graph object at 0x7f9e6b760150>, 3, {'name': 'Dennis', 'age': 47, 'gender': 'm'}),
 igraph.Vertex(<igraph.Graph object at 0x7f9e6b760150>, 4, {'name': 'Esther', 'age': 22, 'gender': 'f'}),
 igraph.Vertex(<igraph.Graph object at 0x7f9e6b760150>, 5, {'name': 'Frank', 'age': 23, 'gender': 'm'}),
 igraph.Vertex(<igraph.Graph object at 0x7f9e6b760150>, 6, {'name': 'George', 'age': 50, 'gender': 'm'})]
> query::  exist (v): or(and(age_lt(v, 25), gender_eq(v, "f")), name_eq(v, "Frank"))
{'v': {frozendict.frozendict({'name': 'Claire', 'age': 18, 'gender': 'f'}),
       frozendict.frozendict({'name': 'Frank', 'age': 23, 'gender': 'm'}),
       frozendict.frozendict({'name': 'Esther', 'age': 22, 'gender': 'f'})}}
>>> 
```

To install and run the example above: `poetry install && poetry shell`

* `exists` and `forall` are ignored for now
