import numpy as np


def exercise3(seed=0, tasks=0, resources=0, task_duration=[], task_resource=[], task_dependencies=[]):
    np.random.seed(seed)
    alphabet=[]
    for i in range(sum(task_duration)):
        alphabet[i]=i
    tam_Poblacion = 100
    poblacion=[generar_individuo_random(alphabet, tasks)for _ in  range(tam_Poblacion)]
    generation = 0

    fitness_values = [funcionFitness_ej3(poblacion[x],task_dependencies, task_duration, task_resource, resources) for x in range(len(poblacion))]

    while not generation == 100:
        padres = roulette_wheel_selection(poblacion,fitness_values,2)
        nueva_gen=[]
        for k in range(len(padres)//2):
            padre1 = padres[2 * k]
            padre2 = padres[2 * k + 1]
            hijo1, hijo2 = one_point_crossover(padre1, padre2, 0.9)
            hijo1 = uniform_mutation(hijo1, 0.1,(sum(task_duration), tasks))
            hijo2 = uniform_mutation(hijo2,0.1,(sum(task_duration), tasks))
            nueva_gen.append([hijo1,hijo2])
        poblacion = nueva_gen
        fitness_values = [funcionFitness_ej3(poblacion[x],task_dependencies, task_duration, task_resource, resources) for x in poblacion]
        generation+=1
    mejor = 10000
    for i in range(1, poblacion):
        if fitness_values[i] != 0 and sum(poblacion[i]) < mejor:
            mejor = sum(poblacion[i])
            mejor_individuo = poblacion[i]
    return mejor_individuo

    """
    Returns the best solution found by the basic genetic algorithm of exercise 3
    :param seed: used to initialize the random number generator
    :param tasks: number of tasks in the task planning problem with resources
    :param resources: number of resources in the task planning problem with resources
    :param task_duration: list of durations of the tasks
    :param task_resource: list of resources required by each task
    :param task_dependencies: list of dependencies (expressed as binary tuples) between tasks
    :return: list with the start time of each task in the best solution found, or empty list if no solution was found
    """



def exercise4(seed, tasks=0, resources=0, task_duration=[], task_resource=[], task_dependencies=[]):
    """
        Returns the best solution found by the advanced genetic algorithm of exercise 4
        :param seed: used to initialize the random number generator
        :param tasks: number of tasks in the task planning problem with resources
        :param resources: number of resources in the task planning problem with resources
        :param task_duration: list of durations of the tasks
        :param task_resource: list of resources required by each task
        :param task_dependencies: list of dependencies (expressed as binary tuples) between tasks
        :return: list with the start time of each task in the best solution found, or empty list if no solution was found
        """
    np.random.seed(seed)
    tam_Poblacion=100
    poblacion = inicializar_poblacion(tam_Poblacion,task_duration,tasks)
    fitness_poblacion = [funcionFitness(poblacion[a], task_dependencies, task_duration, task_resource, resources) for a in range(len(poblacion))]
    mejor_fitness = 1000
    contador=0
    criterio=True
    while(criterio==True):
        padres = funcionSeleccion(poblacion,tam_Poblacion,task_dependencies,task_duration,task_resource,resources)
        for k in range(len(padres) // 2):
            nueva_generacion = []
            padre1 = padres[2*k]
            padre2 = padres[2*k+1]
            hijo1,hijo2 = funcion_Cruzar(padre1, padre2,tasks)
            hijo1 = funcion_Mutar2(hijo1,tasks,task_duration)
            nueva_generacion.append(hijo1)
            if(2*k+1<len(padres)):
                hijo2 = funcion_Mutar2(hijo2,tasks,task_duration)
                nueva_generacion.append(hijo2)
            poblacion= funcion_seleccionAmbiental(nueva_generacion,poblacion,fitness_poblacion)
            fitness_poblacion = [funcionFitness(poblacion[a], task_dependencies, task_duration, task_resource, resources) for a in range(len(poblacion))]
        if (mejor_fitness<=sum(task_duration)):
                contador+=1
                if(contador==30):
                    criterio = False
        else:
            if(min(fitness_poblacion)<mejor_fitness):
                    mejor_fitness = min(fitness_poblacion)
    mejor_individuo=poblacion[fitness_poblacion.index(min(fitness_poblacion))]
    return mejor_individuo


def checkdependencies(dependencias=[],individuo=[],task_duration=[]):
    disponible=True
    for a in range(len(dependencias)):
        dependenciainicial=dependencias[a][0]
        dependenciafinal=dependencias[a][1]
        if(individuo[dependenciafinal-1]-individuo[dependenciainicial-1]<task_duration[dependenciainicial-1]):
            disponible=False
    return disponible


def checkresources(individuo=[],recursos=[],recursoMax=0,task_duration=[]):
    disponible=True
    for a in range(len(individuo)):
        recurso=0
        for b in range(len(individuo)):
            if(individuo[a]<=individuo[b]<individuo[a]+task_duration[a] or individuo[b]<=individuo[a]<individuo[b]+task_duration[b]):
                recurso=recurso+recursos[b]
        if(recurso>recursoMax):
            disponible=False
    return disponible


def inicializar_poblacion(tam_poblacion=0, task_duration=[], tasks=0):
    poblacion=[]
    for a in range(tam_poblacion):
        individuo=[]
        for i in range(tasks):
            individuo.append(np.random.randint(0,sum(task_duration)-task_duration[task_duration.index(min(task_duration))]))
        poblacion.append(individuo)
    return poblacion


def funcionFitness_ej3(individuo=[], task_dependencies=[], task_duration=[], task_resource=[], resources=0):
    fitness = 0
    if (checkdependencies(task_dependencies, individuo) and checkresources(individuo, task_resource, resources)):
        fitness = max(individuo) + task_duration[individuo.index(max(individuo))]
    return fitness

def funcionFitness(individuo=[], task_dependencies=[], task_duration=[], task_resource=[], resources=0):
    fitness = individuo[individuo.index(max(individuo))] + task_duration[individuo.index(max(individuo))]
    if (not checkdependencies(task_dependencies, individuo, task_duration)):
        fitness += 30
    if (not checkresources(individuo, task_resource, resources, task_duration)):
        fitness += 30
    return fitness
def funcionSeleccion(poblacion=[], tam_Poblacion=0, task_dependencies=[], task_duration=[], task_resource=[], resources=0):
    ganadores = []
    for _ in range(tam_Poblacion//2):
        seleccionados=[]
        for i in range(2):
            num= np.random.randint(0,len(poblacion))
            seleccionados.append(poblacion[num])
        fitness_seleccionados = [funcionFitness(seleccionados[a], task_dependencies, task_duration, task_resource, resources) for a in range(2)]
        mejor = seleccionados[fitness_seleccionados.index(min(fitness_seleccionados))]
        ganadores.append(mejor)
    return ganadores


def funcion_Cruzar(padre1=[], padre2=[], tasks=0):
    punto_corte = np.random.randint(1, tasks - 1)
    hijo = padre1[:punto_corte] + padre2[punto_corte:]
    hijo2= padre2[:punto_corte] + padre1[punto_corte:]
    return hijo,hijo2


def funcion_Mutar(hijo=[], tasks=0):
    if (np.random.rand() <= 1 / tasks):
        p1 = np.random.randint(0, tasks)
        p2 = np.random.randint(0, tasks)
        aux = hijo[p1]
        hijo[p1] = hijo[p2]
        hijo[p2] = aux
    return hijo
def funcion_Mutar2(hijo=[], tasks=0,task_duration=[]):
    for i in range(tasks):
        if(np.random.rand()<=2/tasks):
            hijo[i]=np.random.randint(0,sum(task_duration)-min(task_duration))
    return hijo

def generar_individuo_random(alphabet, length):
    indices = np.random.randint(0, len(alphabet), length)
    return np.array(alphabet)[indices]


def roulette_wheel_selection(population, fitness, number_parents):
    population_fitness = sum(fitness)
    chromosome_probabilities = [f / population_fitness for f in fitness]
    indices = np.random.choice(range(len(fitness)), number_parents, chromosome_probabilities)
    return [population[i] for i in indices]


def funcion_seleccionAmbiental(nueva_generacion=[],poblacion=[],fitness_poblacion=[]):
    nueva_poblacion=[]
    for i in range(len(nueva_generacion)):
        nueva_poblacion.append(nueva_generacion[i])
    for i in range(len(poblacion)-len(nueva_poblacion)):
        posicion=fitness_poblacion.index(min(fitness_poblacion))
        nueva_poblacion.append(poblacion[posicion])
        poblacion.pop(posicion)
        fitness_poblacion.pop(posicion)
    return nueva_poblacion

def one_point_crossover(parent1, parent2, p_cross):
    if np.random.random() < p_cross:
        point = np.random.randint(1,len(parent1)-1)
        child1 = np.append(parent1[:point],parent2[point:])
        child2 = np.append(parent2[:point],parent1[point:])
        return child1, child2
    else:
        return parent1, parent2

def uniform_mutation(chromosome, p_mut, alphabet):
    child = np.copy(chromosome)
    random_values = np.random.random(len(chromosome))
    mask = random_values < p_mut
    indices = np.random.randint(0, len(alphabet), size=np.count_nonzero(mask))
    child[mask] = np.array(alphabet)[indices]
    return child