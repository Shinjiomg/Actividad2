# -*- coding: utf-8 -*-
"""
Base de conocimiento basada en reglas lógicas para el sistema de transporte.

Las reglas aquí NO ejecutan el algoritmo de búsqueda; expresan condiciones
que cualquier planificador puede consultar. Así se separa:

- **Conocimiento declarativo** (qué es válido, qué se prefiere)
- **Procedimiento** (BFS / A* en search.py)

Reglas modeladas (lectura humana ↔ comprobaciones en código):

1. **Avance por conexión**
   - Si la estación B es vecina directa de A en el grafo, entonces se puede
     avanzar de A a B en un paso.
   - Formalmente: PuedeAvanzar(A, B) := ExisteArista(A, B).

2. **Preferencia por rutas más cortas (en sentido de coste total)**
   - Entre dos rutas factibles que llegan al destino, debe priorizarse la de
     menor coste acumulado (suma de pesos de aristas).
   - Esto la materializa el algoritmo A* (o Dijkstra con h=0), no una regla
     evaluada sobre listas de rutas en este módulo.

3. **Evitar rutas demasiado largas (en número de transbordos / saltos)**
   - Opcional: rechazar cualquier prefijo de exploración que supere un máximo
     de estaciones visitadas en la ruta (incluyendo origen y destino).
   - Útil como restricción de usuario: "no más de N paradas".

La función `path_total_cost` apoya la regla (2) al comparar rutas candidatas.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Tuple

if TYPE_CHECKING:
    from graph_model import TransportGraph


def puede_avanzar(graph: "TransportGraph", origen: str, destino: str) -> bool:
    """
    REGLA 1: Solo se puede ir de origen a destino si hay conexión directa.
    """
    return graph.has_edge(origen, destino)


def vecinos_alcanzables(graph: "TransportGraph", estacion: str) -> List[Tuple[str, float]]:
    """
    Lista de (vecino, coste) desde 'estacion' que la regla 1 considera válidos
    para un paso inmediato.
    """
    return list(graph.neighbors(estacion).items())


def excede_saltos_maximos(ruta: List[str], max_estaciones: Optional[int]) -> bool:
    """
    REGLA 3: Si max_estaciones es None, no hay límite.
    En caso contrario, la ruta no debe tener más de max_estaciones nodos.
    """
    if max_estaciones is None:
        return False
    return len(ruta) > max_estaciones


def path_total_cost(graph: "TransportGraph", ruta: List[str]) -> Optional[float]:
    """
    Suma de pesos a lo largo de la ruta. None si algún tramo no existe.

    Sirve para comparar candidatos y aplicar la REGLA 2 (menor coste = mejor).
    """
    if len(ruta) < 2:
        return 0.0
    total = 0.0
    for i in range(len(ruta) - 1):
        w = graph.edge_weight(ruta[i], ruta[i + 1])
        if w is None:
            return None
        total += w
    return total
