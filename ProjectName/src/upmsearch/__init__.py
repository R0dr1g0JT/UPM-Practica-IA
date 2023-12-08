import time
from ProjectName.src.upmproblems.rcpsp06 import *
import search_exercises

print("Branch & Bound:")
print(search_exercises.exercise1(get_tasks(),get_resources(),get_task_duration(),get_task_resource(),get_task_dependencies()))

print("A*:")
print(search_exercises.exercise2(get_tasks(),get_resources(),get_task_duration(),get_task_resource(),get_task_dependencies()))