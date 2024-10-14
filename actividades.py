from typing import Callable, Any

class Actividad:
    """
    Representa una actividad con una prioridad y una tarea a ejecutar.
    """
    def __init__(self, prioridad: int, tarea: Callable[[Any], Any], objeto: Any):
        """
        Inicializa una actividad.

        :param prioridad: Prioridad de la actividad.
        :param tarea: Callable que representa la tarea a ejecutar.
        :param objeto: Objeto relacionado con la tarea.
        """
        self.prioridad = prioridad
        self.tarea = tarea
        self.objeto = objeto

    def __lt__(self, other: 'Actividad') -> bool:
        """
        Compara actividades para determinar su orden en la cola.

        :param other: Otra instancia de Actividad.
        :return: True si la prioridad es mayor, False en caso contrario.
        """
        return self.prioridad > other.prioridad  # Invertimos el orden para que la mayor profundidad tenga más prioridad
