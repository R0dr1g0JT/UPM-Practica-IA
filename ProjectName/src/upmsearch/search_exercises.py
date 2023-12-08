import time
import copy
def exercise1(tasks=0, resources=0, task_duration=[], task_resource=[], task_dependencies=[]):
    """
    Returns the best solution found by the branch and bound algorithm of exercise 1
    :param tasks: number of tasks in the task planning problem with resources
    :param resources: number of resources in the task planning problem with resources
    :param task_duration: list of durations of the tasks
    :param task_resource: list of resources required by each task
    :param task_dependencies: list of dependencies (expressed as binary tuples) between tasks
    :return: list with the start time of each task in the best solution found, or empty list if no solution was found
    """
    inicio = time.time()

    def terminado(solucion=[]):
        ok = True
        for i in solucion:
            if i == -1:
                ok = False
                break
        return ok

        # Poda: quitar aquellos caminos donde aún no estén todas las dependencias de esa tarea en la solucion

    def poda(cp=[], organizada_dependencias=[], solucion=[]):
        # Quita aquellos caminos donde aún no estén todas las dependencias de esa tarea en la solucion
        for candidato in cp:
            for i in range(len(organizada_dependencias[candidato[0] - 1])):
                if solucion[organizada_dependencias[candidato[0] - 1][i] - 1] == -1:
                    cp.pop(cp.index(candidato))
                    break

    def ordenar(candidatos=[]):
        ordenado = []
        while len(candidatos) > 1:
            mejor_valor = 0, 99999
            for i in candidatos:
                if i[1] < mejor_valor[1]:
                    mejor_valor = i
            ordenado.append(mejor_valor)
            candidatos.pop(candidatos.index(mejor_valor))
        if len(candidatos) == 1:
            ordenado.append(candidatos[0])
            candidatos.pop()
        return ordenado

    def lista_organizada_dependencias(task_dependencies=[], tasks=0):
        lista_final = []
        for i in range(1, tasks + 1):
            lista_aux = []
            for origen, destino in task_dependencies:
                if destino == i:
                    lista_aux.append(origen)
            lista_final.append(lista_aux)
        return lista_final  # [[],[],[1,2],[2],[3],[4]]

    def solapamiento(tarea=0, recursos_max=0, makespan=0, path=[], task_duration=[], task_resources=[], dependencias=[],
                     solucion=[]):
        for i in range(0, makespan + 1):
            copia_path = copy.deepcopy(path)
            solucion_copia = copy.deepcopy(solucion)
            aniadir_tarea_planificacion(i, tarea, task_duration[tarea - 1], copia_path)
            solucion_copia[tarea - 1] = i
            if (check_dependencies(tarea, dependencias, solucion_copia, task_duration) is True and
                check_resources(recursos_max, i, i + task_duration[tarea - 1], copia_path, task_resources)) is True:
                return i
        return None

    def aniadir_tarea_planificacion(posicion=0, tarea=0, duracion_tarea=0, path=[]):
        if posicion + duracion_tarea < len(path):
            for i in range(posicion, posicion + duracion_tarea):
                path[i].append(tarea)

        else:
            for i in range(posicion, len(path)):
                path[i].append(tarea)
            for i in range(posicion + duracion_tarea - len(path)):
                path.append([tarea])
            path.append([])  # El intervalo de una tarea se considera como [i,f), por tanto la ultima instancia es vacía

    def check_dependencies(tarea=0, organizado_dependencias=[], solucion=[], task_duration=[]):
        for valor in range(len(organizado_dependencias[tarea - 1])):
            dependencia = organizado_dependencias[tarea - 1][valor]
            # 1: miramos si están añadidas las dependencias
            if solucion[dependencia - 1] == -1:
                return False  # No se cumplen las normas de dependencia
            else:
                # 2: miramos si la dependencia se ejecuta despues o a la vez que la tarea elegida
                if solucion[dependencia - 1] >= solucion[tarea - 1]:
                    return False
                else:
                    # 3: miramos si la tarea se ejecuta en medio de la dependencia
                    if solucion[dependencia - 1] + task_duration[dependencia - 1] > solucion[tarea - 1]:
                        return False
        return True  # Si se cumplen las normas de dependencia

    def check_resources(recursos_max=0, inicio_tarea=0, fin_tarea=0, path=[], task_resources=[]):
        for i in range(inicio_tarea, fin_tarea):
            recursos_aux = 0
            for j in path[i]:
                recursos_aux += task_resources[j - 1]
            if recursos_aux > recursos_max:
                return False  # Se sobrepasan los recursos_max
        return True

    def mejor_raiz(raices=[], organizada_dependencias=[], task_duration=[]):
        # Selecciono un array con el número de hijos que tienen las raices
        aux = [-1 for i in range(len(task_duration))]
        for i in raices:
            if aux[i[0] - 1] == -1:
                aux[i[0] - 1] = 0
        for i in raices:
            for j in organizada_dependencias:
                if (i[0]) in j:
                    aux[i[0] - 1] += 1
        pos = aux.index(max(aux))
        return (pos + 1, 0)
        # COMIENZO DEL CODIGO PRINCIPAL

    cp = []
    raices = []
    path = []
    makespan = 0
    solucion = [-1 for i in range(tasks)]
    organizada_dependencias = lista_organizada_dependencias(task_dependencies, tasks)

    for i in range(len(organizada_dependencias)):
        if len(organizada_dependencias[i]) == 0:
            raices.append((i + 1, 0))

    raiz = mejor_raiz(raices, organizada_dependencias, task_duration)
    cp.append(raiz)
    raices.pop(raices.index(raiz))

    while not terminado(solucion):
        if len(cp) == 0:
            if len(raices) > 0:
                raiz = mejor_raiz(raices, organizada_dependencias, task_duration)
                cp.append(raiz)
                raices.pop(raices.index(raiz))
        if len(cp) > 0:

            solapar_posible = solapamiento(cp[0][0], resources, makespan, path, task_duration, task_resource,
                                           organizada_dependencias, solucion)
            if solapar_posible is not None:
                solucion[cp[0][0] - 1] = solapar_posible
                aniadir_tarea_planificacion(solapar_posible, cp[0][0], task_duration[cp[0][0] - 1], path)
            else:
                aniadir_tarea_planificacion(makespan, cp[0][0], task_duration[cp[0][0] - 1], path)
                solucion[cp[0][0] - 1] = makespan

            makespan = len(path) - 1

            # Expansion
            nodo_actual, c = cp[0]
            lista_expansion = []
            for i in range(len(organizada_dependencias)):
                for j in organizada_dependencias[i]:
                    if nodo_actual == j:
                        solapar_posible = solapamiento(i, resources, makespan, path, task_duration, task_resource,
                                                       organizada_dependencias, solucion)
                        if solapar_posible is None:
                            lista_expansion.append((i + 1, makespan))
                        else:
                            lista_expansion.append((i + 1, solapar_posible))

            cp.pop(0)
            for candidato in lista_expansion:
                cp.append(candidato)
            cp = ordenar(cp)
            poda(cp, organizada_dependencias, solucion)

    return solucion, makespan, time.time() - inicio


def exercise2(tasks=0, resources=0, task_duration=[], task_resource=[], task_dependencies=[]):
    """
    Returns the best solution found by the A* algorithm of exercise 2
    :param tasks: number of tasks in the task planning problem with resources
    :param resources: number of resources in the task planning problem with resources
    :param task_duration: list of durations of the tasks
    :param task_resource: list of resources required by each task
    :param task_dependencies: list of dependencies (expressed as binary tuples) between tasks
    :return: list with the start time of each task in the best solution found, or empty list if no solution was found
    """
    # METODOS USADOS
    def terminado(solucion=[]):
        ok = True
        for i in solucion:
            if i == -1:
                ok = False
                break
        return ok

    def ordenar(candidatos=[]):
        ordenado = []
        while len(candidatos) > 1:
            mejor_valor = 0, 99999, 99999
            for i in candidatos:
                if (i[1] + i[2]) < (mejor_valor[1] + mejor_valor[2]):
                    mejor_valor = i
            ordenado.append(mejor_valor)
            candidatos.pop(candidatos.index(mejor_valor))
        if len(candidatos) == 1:
            ordenado.append(candidatos[0])
            candidatos.pop()
        return ordenado

    def poda(cp=[], organizada_dependencias=[], solucion=[]):
        for candidato in cp:
            for i in range(len(organizada_dependencias[candidato[0] - 1])):
                if solucion[organizada_dependencias[candidato[0] - 1][i] - 1] == -1:
                    cp.pop(cp.index(candidato))
                    break

    def get_heuristica(valor, task_duration=[], task_resource=[], solucion=[]):
        contador = 0.1
        for i in solucion:
            if(i != -1):
                contador= contador +1
        heuristica = (task_duration[valor - 1] / task_resource[valor - 1])/contador
        return heuristica

    def lista_organizada_dependencias(task_dependencies=[], tasks=0):
        lista_final = []
        for i in range(1, tasks + 1):
            lista_aux = []
            for origen, destino in task_dependencies:
                if destino == i:
                    lista_aux.append(origen)
            lista_final.append(lista_aux)
        return lista_final

    def solapamiento(tarea=0, recursos_max=0, makespan=0, path=[], task_duration=[], task_resources=[], dependencias=[],solucion=[]):
        for i in range(0, makespan + 1):
            copia_path = copy.deepcopy(path)
            solucion_copia = copy.deepcopy(solucion)
            aniadir_tarea_planificacion(i, tarea, task_duration[tarea - 1], copia_path)
            solucion_copia[tarea - 1] = i
            if (check_dependencies(tarea, dependencias, solucion_copia, task_duration) is True and
                check_resources(recursos_max, i, i + task_duration[tarea - 1], copia_path, task_resources)) is True:
                return i
        return None

    def aniadir_tarea_planificacion(posicion=0, tarea=0, duracion_tarea=0, path=[]):
        if posicion + duracion_tarea < len(path):
            for i in range(posicion, posicion + duracion_tarea):
                path[i].append(tarea)

        else:
            for i in range(posicion, len(path)):
                path[i].append(tarea)
            for i in range(posicion + duracion_tarea - len(path)):
                path.append([tarea])
            path.append([])  # El intervalo de una tarea se considera como [i,f), por tanto la ultima instancia es vacía

    def check_dependencies(tarea=0, organizado_dependencias=[], solucion=[], task_duration=[]):
        for valor in range(len(organizado_dependencias[tarea - 1])):
            dependencia = organizado_dependencias[tarea - 1][valor]
            # 1: miramos si están añadidas las dependencias
            if solucion[dependencia - 1] == -1:
                return False  # No se cumplen las normas de dependencia
            else:
                # 2: miramos si la dependencia se ejecuta despues o a la vez que la tarea elegida
                if solucion[dependencia - 1] >= solucion[tarea - 1]:
                    return False
                else:
                    # 3: miramos si la tarea se ejecuta en medio de la dependencia
                    if solucion[dependencia - 1] + task_duration[dependencia - 1] > solucion[tarea - 1]:
                        return False
        return True  # Si se cumplen las normas de dependencia

    def check_resources(recursos_max=0, inicio_tarea=0, fin_tarea=0, path=[], task_resources=[]):
        for i in range(inicio_tarea, fin_tarea):
            recursos_aux = 0
            for j in path[i]:
                recursos_aux += task_resources[j - 1]
            if recursos_aux > recursos_max:
                return False  # Se sobrepasan los recursos_max
        return True

    # COMIENZO DEL CODIGO PRINCIPAL
    cp = []
    raices = []
    path = []
    makespan = 0
    solucion = [-1 for i in range(tasks)]
    organizada_dependencias = lista_organizada_dependencias(task_dependencies, tasks)

    for i in range(len(organizada_dependencias)):
        if len(organizada_dependencias[i]) == 0:
            raices.append((i + 1, 0, get_heuristica(i + 1, task_duration, task_resource)))

    cp = ordenar(raices)
    while not terminado(solucion):

            solapar_posible = solapamiento(cp[0][0], resources, makespan, path, task_duration, task_resource,
                                           organizada_dependencias, solucion)
            if solapar_posible is not None:
                solucion[cp[0][0] - 1] = solapar_posible
                aniadir_tarea_planificacion(solapar_posible, cp[0][0], task_duration[cp[0][0] - 1], path)
            else:
                aniadir_tarea_planificacion(makespan, cp[0][0], task_duration[cp[0][0] - 1], path)
                solucion[cp[0][0] - 1] = makespan
            makespan = len(path) - 1

            # Expansion
            nodo_actual, c, h = cp[0]
            lista_expansion = []
            for i in range(len(organizada_dependencias)):
                for j in organizada_dependencias[i]:
                    if nodo_actual == j:
                        solapar_posible = solapamiento(i, resources, makespan, path, task_duration, task_resource,
                                           organizada_dependencias, solucion)
                        if solapar_posible is None:
                            lista_expansion.append((i + 1, makespan, get_heuristica(i + 1, task_duration, task_resource,solucion)))
                        else:
                            lista_expansion.append((i + 1, solapar_posible, get_heuristica(i + 1, task_duration, task_resource,solucion)))

            cp.pop(0)
            for candidato in lista_expansion:
                cp.append(candidato)
            cp = ordenar(cp)
            poda(cp, organizada_dependencias, solucion)

    return solucion
