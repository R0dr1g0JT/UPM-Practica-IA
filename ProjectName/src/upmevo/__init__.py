import time
from ProjectName.src.upmproblems.rcpsp06 import *
import evo_exercises
inicio=time.time()
print(evo_exercises.exercise4(1241231213,get_tasks(),get_resources(),get_task_duration(),get_task_resource(),get_task_dependencies()))
fin=time.time()
print(fin-inicio)
