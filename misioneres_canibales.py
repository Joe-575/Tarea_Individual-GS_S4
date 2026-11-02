"""
El Problema de los Misioneros y Canibales
    Tres misioneros y tres canibales deben cruzar un río en un bote que
    solo puede llevar a dos personas. Si en algún momento hay más canibales
    que misiones en cualquiera de las dos orillas, los canibales se comerán
    a los misioneros.

Estado: (misioneros_izq, canibales_izq, bote_izq)
        cantidad de misioneros y canibales en la orilla izquierda,
        bote_izq = 1 si el bote está en la izquierda, 0 si está en la derecha.
Acción: (misioneros_cruzan, canibales_cruzan) = quiénes viajaan en el bote


Autor: Joel Velez
"""

import time
import tracemalloc
from collections import deque
from dataclasses import dataclass
from statistics import median

# Representación de estado (misioneros_izq, canibales_izq, bote_izq)
Estado = tuple[int, int, int]
Accion = tuple[int, int]


class Problema:
    """
    Formulación del problema: personas_por_tipo misioneros, igual número
    de canibales y un bote
    """

    def __init__(self, personas_por_tipo: int = 3, capacidad_bote: int = 2):
        self.personas_por_tipo = personas_por_tipo
        self.capacidad_bote = capacidad_bote
        self.estado_inicial: Estado = (
            personas_por_tipo,
            personas_por_tipo,
            1,
        )  # todos a la izquierda
        self.estado_meta: Estado = (0, 0, 0)  # todos a la derecha

        capacidad = capacidad_bote
        self.acciones_posibles: list[Accion] = (
            [(misioneros, 0) for misioneros in range(1, capacidad + 1)]
            + [(0, canibales) for canibales in range(1, capacidad + 1)]
            + [
                (misioneros, canibales)
                for misioneros in range(1, capacidad + 1)
                for canibales in range(1, capacidad + 1)
                if misioneros + canibales <= capacidad
            ]
        )

    def es_estado_valido(self, misioneros_izq: int, canibales_izq: int) -> bool:
        """
        Válido si hay
        """
        total = self.personas_por_tipo
        misioneros_der = total - misioneros_izq
        canibales_der = total - canibales_izq

        if not (0 <= misioneros_izq <= total and 0 <= canibales_izq <= total):
            return False

        izquierda_segura = misioneros_izq == 0 or misioneros_izq >= canibales_izq
        derecha_segura = misioneros_der == 0 or misioneros_der >= canibales_der
        return izquierda_segura and derecha_segura

    def modelo_transicion(self, estado: Estado, accion: Accion) -> Estado | None:
        """
        Estado que resulta de aplicar la acción, o None si ese estado no es válido
        """
        misioneros_izq, canibales_izq, bote_izq = estado
        misioneros_en_bote, canibales_en_bote = accion
        # Bote a la izquierda: las personas salen de la izquierda (restan).
        # Si no, regresan (suman)
        signo = -1 if bote_izq == 1 else 1
        nuevos_misioneros_izq = misioneros_izq + signo * misioneros_en_bote
        nuevos_canibales_izq = canibales_izq + signo * canibales_en_bote
        if not self.es_estado_valido(nuevos_misioneros_izq, nuevos_canibales_izq):
            return None

        return (nuevos_misioneros_izq, nuevos_canibales_izq, 1 - bote_izq)

    def sucesores(self, estado: Estado):
        """Genera pares (acción, estado_siguiente) para cada acción aplicable."""
        for accion in self.acciones_posibles:
            estado_siguiente = self.modelo_transicion(estado, accion)
            if estado_siguiente is not None:
                yield accion, estado_siguiente


@dataclass
class Resultado:
    plan: list[tuple[Accion, Estado]] | None
    nodos_expandidos: int
    nodos_generados: int
    tamanio_max_frontera: int


def buscar(problema: Problema, estrategia: str) -> Resultado:
    """Búsqueda en grafo con conjunto de estados ya explorados.
    'bfs' -> cola FIFO (marca los estados al generarlos).
    'dfs' -> pila LIFO (marca los estados al expandirlos).
    La prueba de meta se hace al expandir en ambas, para que 'nodos expandidos' sea comparable.
    """
    usa_cola = estrategia == "bfs"
    frontera = deque(
        [(problema.estado_inicial, None)]
    )  # elementos: (estado, (estado_padre, acción))
    padres: dict[Estado, tuple[Estado, Accion] | None] = (
        {}
    )  # estados ya expandidos y de dónde vinieron
    estados_vistos = {problema.estado_inicial}
    nodos_expandidos = nodos_generados = tamano_max_frontera = 0

    while frontera:
        tamano_max_frontera = max(tamano_max_frontera, len(frontera))
        estado_actual, origen = frontera.popleft() if usa_cola else frontera.pop()
        if estado_actual in padres:  # DFS: duplicado que se apiló antes de expandirse
            continue
        padres[estado_actual] = origen
        nodos_expandidos += 1

        if estado_actual == problema.estado_meta:
            plan = reconstruir_plan(padres, estado_actual)
            return Resultado(
                plan, nodos_expandidos, nodos_generados, tamano_max_frontera
            )

        for accion, estado_siguiente in problema.sucesores(estado_actual):
            if (
                usa_cola and estado_siguiente in estados_vistos
            ) or estado_siguiente in padres:
                continue
            estados_vistos.add(estado_siguiente)
            frontera.append((estado_siguiente, (estado_actual, accion)))
            nodos_generados += 1

    return Resultado(None, nodos_expandidos, nodos_generados, tamano_max_frontera)


def reconstruir_plan(padres, estado_final: Estado) -> list[tuple[Accion, Estado]]:
    """Recorre los padres desde la meta hasta el inicio y devuelve el plan en orden."""
    plan = []
    estado = estado_final
    while padres[estado] is not None:
        estado_padre, accion = padres[estado]
        plan.append((accion, estado))
        estado = estado_padre
    return plan[::-1]
