# Sistema de rutas con grafo, reglas y búsqueda

Proyecto en Python que modela un sistema de transporte como **grafo** (estaciones = nodos, conexiones = aristas ponderadas), aplica una **base de conocimiento con reglas lógicas** y calcula la mejor ruta entre un punto A y un punto B usando **BFS** y, de forma opcional/avanzada, **A**.

## Requisitos

- Python 3.9 o superior (recomendado 3.10+).
- No se instalan dependencias externas; solo biblioteca estándar.

## Estructura del proyecto


| Archivo              | Descripción                                                                              |
| -------------------- | ---------------------------------------------------------------------------------------- |
| `main.py`            | Construye el grafo de ejemplo, ejecuta casos de prueba y muestra resultados por consola. |
| `graph_model.py`     | Clase `TransportGraph`: nodos, aristas y pesos.                                          |
| `knowledge_rules.py` | Reglas declarativas (avance válido, límite de longitud, coste de una ruta).              |
| `search.py`          | `bfs_shortest_hops` y `astar_shortest_cost`.                                             |


## Cómo ejecutar

Desde la carpeta del proyecto:

```bash
python main.py
```

En Windows (PowerShell o CMD), si `python` no está en el PATH:

```bash
py main.py
```

Si los acentos se ven mal en la consola, ejecuta antes (PowerShell):

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"
python main.py
```

## Qué hace cada parte

1. **Grafo**: se añaden estaciones y conexiones con un peso (en el ejemplo, minutos de viaje).
2. **Reglas** (`knowledge_rules.py`): por ejemplo, solo se puede avanzar entre estaciones conectadas; se puede limitar el número máximo de estaciones en la ruta; el coste total de una ruta es la suma de los pesos.
3. **BFS**: encuentra una ruta con el **mínimo número de saltos** (aristas), respetando las reglas y el límite opcional de estaciones.
4. **A**: encuentra la ruta de **menor tiempo total** (suma de pesos) usando una heurística admisible definida en `main.py` para el ejemplo.

## Nota

En grafos **ponderados**, “mejor ruta” puede significar distintas cosas: menos transbordos (BFS con aristas uniformes) o menor tiempo/distancia (A / Dijkstra). El programa muestra ambos criterios para comparar.