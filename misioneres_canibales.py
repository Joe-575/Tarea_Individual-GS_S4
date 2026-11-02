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
