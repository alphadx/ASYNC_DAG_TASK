import asyncio
import heapq
import logging
from typing import Callable, Any, List

# Configuración básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Definir una Actividad con su prioridad (profundidad)
class Actividad:
    def __init__(self, prioridad: int, tarea: Callable[[Any], Any], objeto: Any):
        self.prioridad = prioridad
        self.tarea = tarea
        self.objeto = objeto

    def __lt__(self, other):
        return self.prioridad > other.prioridad  # Mayor prioridad si tiene mayor profundidad

# Definir la Tarea que ejecutará una acción y puede gatillar otras
class Tarea:
    def __init__(self, nombre: str, accion: Callable[[Any], Any], tareas_gatilladas: List['Tarea'] = None):
        self.nombre = nombre
        self.accion = accion
        self.tareas_gatilladas = tareas_gatilladas or []

    async def ejecutar(self, objeto: Any, profundidad: int, cola: List[Actividad], semaforo: asyncio.Semaphore):
        async with semaforo:
            # Ejecutar la acción y obtener el resultado
            logging.info(f"Ejecutando tarea: {self.nombre}, Objeto: {objeto}, Profundidad: {profundidad}")
            resultado = await self.accion(objeto)
            
            # Añadir las tareas gatilladas a la cola con profundidad incrementada
            for tarea in self.tareas_gatilladas:
                nueva_actividad = Actividad(profundidad + 1, tarea, resultado)
                heapq.heappush(cola, nueva_actividad)
                logging.info(f"Añadida a la cola: {tarea.nombre}, Resultado previo: {resultado}, Nueva profundidad: {profundidad + 1}")
            return resultado

# Función de prueba que multiplica el número por 2 y se demora 5/n segundos
async def multiplicar_por_dos(numero):
    if numero == 0:
        numero = 1  # Para evitar división por 0, simulamos un pequeño retardo
    delay = 5 / numero
    logging.info(f"Procesando número: {numero}, Tiempo estimado: {delay:.2f} segundos")
    await asyncio.sleep(delay)
    return numero * 2

# Definir el worker
async def worker(id_worker: int, cola: List[Actividad], semaforo: asyncio.Semaphore):
    while True:
        if cola:
            actividad = heapq.heappop(cola)  # Tomar la actividad con mayor prioridad
            logging.info(f"[Worker {id_worker}] Procesando tarea: {actividad.tarea.nombre}, Profundidad: {actividad.prioridad}")
            await actividad.tarea.ejecutar(actividad.objeto, actividad.prioridad, cola, semaforo)
        else:
            await asyncio.sleep(0.1)

# Sistema de tareas con múltiples workers
async def sistema_de_tareas(tareas_iniciales: List[Tarea], objetos_iniciales: List[Any], num_workers: int = 2):
    cola_actividades = []
    semaforo = asyncio.Semaphore(num_workers)  # Limitar el número de tareas en ejecución simultáneamente
    
    # Añadir las tareas iniciales a la cola
    for tarea, objeto in zip(tareas_iniciales, objetos_iniciales):
        actividad = Actividad(0, tarea, objeto)
        heapq.heappush(cola_actividades, actividad)
        logging.info(f"Tarea inicial añadida a la cola: {tarea.nombre}, Objeto: {objeto}, Profundidad: 0")
    
    # Lanzar los workers
    workers = [asyncio.create_task(worker(i, cola_actividades, semaforo)) for i in range(num_workers)]
    
    # Mantener el sistema corriendo hasta que no haya más tareas
    await asyncio.gather(*workers)

# Crear el grafo de tareas
tarea3a = Tarea(nombre="Tarea 3A", accion=multiplicar_por_dos)
tarea3b = Tarea(nombre="Tarea 3B", accion=multiplicar_por_dos)
tarea2a = Tarea(nombre="Tarea 2A", accion=multiplicar_por_dos, tareas_gatilladas=[tarea3a, tarea3b])

tarea3c = Tarea(nombre="Tarea 3C", accion=multiplicar_por_dos)
tarea3d = Tarea(nombre="Tarea 3D", accion=multiplicar_por_dos)
tarea2b = Tarea(nombre="Tarea 2B", accion=multiplicar_por_dos, tareas_gatilladas=[tarea3c, tarea3d])

tarea1 = Tarea(nombre="Tarea 1", accion=multiplicar_por_dos, tareas_gatilladas=[tarea2a, tarea2b])

# Lanzar el sistema con varias instancias de tarea 1
async def main():
    await sistema_de_tareas([tarea1, tarea1, tarea1, tarea1], [1, 3, 5, 0], num_workers=2)

# Ejecutar
asyncio.run(main())
