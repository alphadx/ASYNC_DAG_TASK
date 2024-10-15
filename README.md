# Descripción del Programa

Este programa está diseñado para ejecutar tareas asíncronas con diferentes niveles de prioridad. Utiliza una cola de prioridad (heap) para gestionar las tareas según su profundidad, y cada tarea puede desencadenar otras tareas adicionales.

## Componentes del Programa

### Clase `Actividad`

Representa una actividad que contiene una tarea y su prioridad. Se utiliza para organizar las tareas en la cola de prioridades.

```python
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
```

### Clase `Tarea`

Define una tarea con un nombre, una acción a ejecutar y una lista de tareas que pueden ser activadas cuando se completa la tarea principal.

```python
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
```
