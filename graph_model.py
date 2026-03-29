# -*- coding: utf-8 -*-
"""
Modelo del sistema de transporte como grafo no dirigido ponderado.

- Nodos: estaciones (identificadores únicos, normalmente str).
- Aristas: conexiones bidireccionales con un coste (p. ej. minutos o km).

Este módulo solo describe la topología y los costes; las reglas de decisión
viven en knowledge_rules.py y la búsqueda en search.py.
"""

from __future__ import annotations

from collections import defaultdict
from typing import DefaultDict, Dict, Iterable, List, Mapping, Optional, Set, Tuple


class TransportGraph:
    """Grafo de estaciones y conexiones con peso positivo en cada arista."""

    def __init__(self) -> None:
        # vecino -> peso (misma arista se guarda en ambos sentidos)
        self._adj: DefaultDict[str, Dict[str, float]] = defaultdict(dict)
        self._stations: Set[str] = set()

    def add_station(self, station: str) -> None:
        """Registra una estación (nodo) en el grafo."""
        self._stations.add(station)

    def add_edge(self, a: str, b: str, weight: float) -> None:
        """
        Añade o actualiza una conexión bidireccional entre a y b.

        weight debe ser > 0 (tiempo, distancia, etc.).
        """
        if weight <= 0:
            raise ValueError("El peso de la arista debe ser positivo.")
        self.add_station(a)
        self.add_station(b)
        self._adj[a][b] = weight
        self._adj[b][a] = weight

    def stations(self) -> Set[str]:
        return set(self._stations)

    def neighbors(self, station: str) -> Mapping[str, float]:
        """Vecinos directos con el coste del tramo station -> vecino."""
        return dict(self._adj.get(station, {}))

    def edge_weight(self, a: str, b: str) -> Optional[float]:
        """Coste de la arista (a, b) o None si no existe."""
        return self._adj.get(a, {}).get(b)

    def has_edge(self, a: str, b: str) -> bool:
        return b in self._adj.get(a, {})
