# -*- coding: utf-8 -*-
"""
Algoritmos de búsqueda sobre el grafo, consultando reglas de knowledge_rules.

BFS (Breadth-First Search):
- Explora por capas (nivel 0, 1, 2, ...) desde el origen.
- En grafos sin peso (o tratando cada arista como coste uniforme 1), la
  primera vez que se alcanza un nodo ya es por el camino con **menor número
  de aristas** (menos transbordos).
- Aquí usamos pesos solo como metadata; para BFS el criterio es **mínimo número
  de saltos**. Los vecinos se filtran con `puede_avanzar` / vecinos del grafo.

A* (opcional / avanzado):
- Combina coste real g(n) desde el origen con heurística h(n) hasta el destino.
- Con h admisible (nunca sobrestima), la primera extracción del destino desde
  la cola de prioridad da la ruta de **menor coste total** (suma de pesos).
- Si h(n)=0 para todo n, A* equivale a Dijkstra.

Complejidad típica: O(V + E) para BFS; O(E log V) para A* con montículo binario.
"""

from __future__ import annotations

import heapq
from collections import deque
from typing import Callable, Dict, List, Optional, Set, Tuple

from graph_model import TransportGraph
from knowledge_rules import excede_saltos_maximos, puede_avanzar, vecinos_alcanzables


def bfs_shortest_hops(
    graph: TransportGraph,
    start: str,
    goal: str,
    max_estaciones: Optional[int] = None,
) -> Optional[List[str]]:
    """
    Encuentra una ruta con el **mínimo número de aristas** entre start y goal.

    max_estaciones: límite opcional de nodos en la ruta (regla de rutas largas).
    """
    if start not in graph.stations() or goal not in graph.stations():
        return None
    if start == goal:
        return [start]

    queue: deque[Tuple[str, List[str]]] = deque()
    queue.append((start, [start]))
    visited: Set[str] = {start}

    while queue:
        current, path = queue.popleft()
        for nxt, _w in vecinos_alcanzables(graph, current):
            if not puede_avanzar(graph, current, nxt):
                continue
            if nxt in visited:
                continue
            new_path = path + [nxt]
            if excede_saltos_maximos(new_path, max_estaciones):
                continue
            if nxt == goal:
                return new_path
            visited.add(nxt)
            queue.append((nxt, new_path))

    return None


def astar_shortest_cost(
    graph: TransportGraph,
    start: str,
    goal: str,
    heuristic: Callable[[str], float],
    max_estaciones: Optional[int] = None,
) -> Optional[List[str]]:
    """
    Ruta de **menor coste sumando pesos** usando A*.

    heuristic(u): estimación no negativa del coste restante de u a goal.
    Debe ser admisible (≤ coste real) para garantizar optimalidad.
    """
    if start not in graph.stations() or goal not in graph.stations():
        return None
    if start == goal:
        return [start]

    # f = g + h; almacenamos (f, g, nodo, path) — path es poco eficiente en
    # grafos grandes; para el curso priorizamos claridad sobre memoria.
    counter = 0
    open_heap: List[Tuple[float, int, str, float, List[str]]] = []
    heapq.heappush(
        open_heap,
        (heuristic(start), counter, start, 0.0, [start]),
    )
    counter += 1

    # Mejor coste g conocido hasta cada nodo (para descartar entradas obsoletas en el montículo).
    best_g: Dict[str, float] = {start: 0.0}

    while open_heap:
        _f, _c, current, g, path = heapq.heappop(open_heap)

        if current == goal:
            return path

        if g > best_g.get(current, float("inf")):
            continue

        for nxt, w in vecinos_alcanzables(graph, current):
            if not puede_avanzar(graph, current, nxt):
                continue
            new_path = path + [nxt]
            if excede_saltos_maximos(new_path, max_estaciones):
                continue
            new_g = g + w
            if new_g < best_g.get(nxt, float("inf")):
                best_g[nxt] = new_g
                h = heuristic(nxt)
                f = new_g + h
                heapq.heappush(open_heap, (f, counter, nxt, new_g, new_path))
                counter += 1

    return None
