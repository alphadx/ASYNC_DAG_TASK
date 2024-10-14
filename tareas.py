import heapq
from typing import Callable, Any, List
from actividades import Actividad

class Tarea:
    """
    Representa una tarea que ejecutará una acción y puede gatillar otras tareas.
    """
    def __init__(self, nombre: str, accion: Callable[[Any], Any], tareas_gatilladas: List['Tarea'] = None):
        """
        Inicializa una tarea.

        :param nombre: Nombre de la tarea.
        :param accion: Callable que representa la acción a ejecutar.
        :param tareas_gatilladas: Lista de tareas que se gatillan al completar esta tarea.
        """
        self.nombre = nombre
        self.accion = accion
        self.tareas_gatilladas = tareas_gatilladas or []

    async def ejecutar(self, objeto: Any, profundidad: int, cola: List[Actividad]) -> Any:
        """
        Ejecuta la acción y añade las tareas gatilladas a la cola.

        :param objeto: Objeto relacionado con la tarea.
        :param profundidad: Profundidad actual de la ejecución.
        :param cola: Cola de actividades.
        :return: Resultado de la acción.
        """
        print(f"Ejecutando tarea: {self.nombre} con profundidad {profundidad}")
        resultado = await self.accion(objeto)

        # Añadir las tareas gatilladas a la cola con profundidad incrementada
        for tarea in self.tareas_gatilladas:
            nueva_actividad = Actividad(profundidad + 1, tarea, resultado)
            heapq.heappush(cola, nueva_actividad)
        return resultado
