# -*- coding: utf-8 -*-
"""
Punto de entrada: construye un ejemplo de red de transporte (8 estaciones),
aplica la base de reglas vía knowledge_rules y encuentra rutas con BFS y A*.

Ejecución:
    python main.py
"""

from __future__ import annotations

from graph_model import TransportGraph
from knowledge_rules import path_total_cost
from search import astar_shortest_cost, bfs_shortest_hops


def build_example_graph() -> TransportGraph:
    """
    Red de ejemplo: 8 estaciones, conexiones y tiempos aproximados (minutos).

    Esquema conceptual:

        Centro ---5--- Norte ---4--- Hospital
          |             |
          3             6
          |             |
        Este ---7--- Universidad
          |
          4
          |
        Sur ---5--- Oeste ---8--- Aeropuerto

    (Algunas conexiones adicionales abajo cierran caminos alternativos.)
    """
    g = TransportGraph()

    # Aristas con peso = minutos de viaje
    g.add_edge("Centro", "Norte", 5)
    g.add_edge("Centro", "Este", 3)
    g.add_edge("Centro", "Oeste", 6)
    g.add_edge("Norte", "Hospital", 4)
    g.add_edge("Norte", "Universidad", 6)
    g.add_edge("Este", "Sur", 4)
    g.add_edge("Este", "Universidad", 7)
    g.add_edge("Sur", "Oeste", 5)
    g.add_edge("Oeste", "Aeropuerto", 8)
    # Conexión extra: acortar caminos y crear elección óptima no trivial
    g.add_edge("Hospital", "Universidad", 5)
    g.add_edge("Universidad", "Aeropuerto", 12)

    return g


def make_heuristic(goal: str) -> dict[str, float]:
    """
    Heurística admisible muy simple para el ejemplo: tabla de 'distancias
    estimadas' en línea recta hasta goal. En un caso real vendrían de GPS.

    Valores ≤ coste real real en los caminos modelados (no sobrestiman).
    """
    # Filas: estación origen de la heurística h(u) = estimación u -> goal
    table: dict[tuple[str, str], float] = {
        ("Centro", "Aeropuerto"): 10,
        ("Norte", "Aeropuerto"): 14,
        ("Sur", "Aeropuerto"): 9,
        ("Este", "Aeropuerto"): 11,
        ("Oeste", "Aeropuerto"): 8,
        ("Hospital", "Aeropuerto"): 15,
        ("Universidad", "Aeropuerto"): 12,
        ("Aeropuerto", "Aeropuerto"): 0,
    }
    # Rellenar simétrico aproximado para otros goals: usar 0 para goal y 8 por defecto
    stations = [
        "Centro",
        "Norte",
        "Sur",
        "Este",
        "Oeste",
        "Hospital",
        "Universidad",
        "Aeropuerto",
    ]
    hmap: dict[str, float] = {}
    for s in stations:
        key = (s, goal)
        hmap[s] = table.get(key, 0.0 if s == goal else 8.0)
    return hmap


def main() -> None:
    graph = build_example_graph()

    print("=" * 60)
    print("Sistema inteligente de rutas (grafo + reglas + búsqueda)")
    print("=" * 60)
    print("\nEstaciones:", ", ".join(sorted(graph.stations())))

    casos = [
        ("Centro", "Aeropuerto"),
        ("Hospital", "Sur"),
        ("Este", "Hospital"),
    ]

    for inicio, fin in casos:
        print(f"\n--- Origen: {inicio} -> Destino: {fin} ---")

        ruta_bfs = bfs_shortest_hops(graph, inicio, fin)
        h_est = make_heuristic(fin)

        def h(u: str) -> float:
            return h_est.get(u, 0.0)

        ruta_astar = astar_shortest_cost(graph, inicio, fin, heuristic=h)

        print("  BFS (mínimo número de saltos / transbordos):")
        if ruta_bfs:
            coste_bfs = path_total_cost(graph, ruta_bfs)
            print(f"    Ruta: {' -> '.join(ruta_bfs)}")
            print(f"    Saltos: {len(ruta_bfs) - 1}  |  Tiempo total: {coste_bfs} min")
        else:
            print("    Sin ruta.")

        print("  A* (mínimo tiempo total con heurística admisible):")
        if ruta_astar:
            coste_a = path_total_cost(graph, ruta_astar)
            print(f"    Ruta: {' -> '.join(ruta_astar)}")
            print(f"    Saltos: {len(ruta_astar) - 1}  |  Tiempo total: {coste_a} min")
        else:
            print("    Sin ruta.")

    # Ejemplo REGLA 3: evitar rutas con demasiadas paradas
    print("\n--- Regla opcional: máximo 3 estaciones en la ruta (incl. inicio y fin) ---")
    inicio, fin = "Centro", "Aeropuerto"
    ruta_limitada = bfs_shortest_hops(graph, inicio, fin, max_estaciones=3)
    print(f"  Origen: {inicio} -> Destino: {fin}")
    if ruta_limitada:
        print(f"  Ruta BFS con límite: {' -> '.join(ruta_limitada)}")
        print(f"  Tiempo total: {path_total_cost(graph, ruta_limitada)} min")
    else:
        print("  No hay ruta que respete el límite de estaciones.")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
