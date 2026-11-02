# Misioneros y Caníbales: BFS vs DFS

Búsqueda no informada (BFS con cola, DFS con pila) sobre el problema de los misioneros y caníbales.
Estados como tuplas `(misioneros_izq, canibales_izq, bote_izq)`. Sin dependencias externas (Python 3.10+).

```bash
python misioneros_canibales.py     # benchmark, planes y casos límite
```

Métricas: nodos expandidos/generados, frontera máxima, tiempo (mediana), longitud del plan,
factor de ramificación efectivo b* y memoria pico (`tracemalloc`, en corrida aparte).

Autor: Joel Velez