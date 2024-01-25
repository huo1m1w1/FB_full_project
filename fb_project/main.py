# fb_project/main.py
import importlib




def run_task(task, key_words):
    try:
        task_module = importlib.import_module(f'fb_project.tasks.{task}')
        task_module.run(key_words)
    except ImportError as e:
        print(f"Error: {task} task not found.")
        print(e)

if __name__ == "__main__":
    key_words = input("Please enter your key words in a list, for example: fintech company: ")
    while True:
        # Input validation for tasks
        valid_task_types = ['posts', 'videos', 'posts videos', 'videos videos']

        task_input = input("Enter task types (posts, videos, or both - separated by space) for example, posts, or posts videos: ")
        if task_input not in valid_task_types:
            print("Invalid input, please try again")
            continue
        break
    task_input = task_input.lower().split()

    for task in task_input:
        run_task(task, key_words)






# import importlib
# import os

# # Set the current working directory to the project root
# current_dir = os.path.dirname(os.path.abspath(__file__))
# os.chdir(current_dir)

# def run_task(task, key_words):
#     try:
#         task_module = importlib.import_module(f'tasks.{task}')
#         task_module.run(key_words)
#     except ImportError as e:
#         print(f"Error: {task} task not found.")
#         print(e)

# if __name__ == "__main__":
#     key_words = input("Please enter your key words in a list, for example: fintech company: ")
#     while True:
#         # Input validation for tasks
#         valid_task_types = ['posts', 'videos', 'posts videos', 'videos videos']

#         task_input = input("Enter task types (posts, videos, or both - separated by space) for example, posts, or posts videos: ")
#         if task_input not in valid_task_types:
#             print("Invalid input, please try again")
#             continue
#         break
#     task_input = task_input.lower().split()

#     for task in task_input:
#         run_task(task, key_words)









# import importlib
# import os
# import sys

# # Set the current working directory to the project root
# os.chdir(sys.path[0])

# def run_task(task, key_words):
#     try:
#         task_module = importlib.import_module(f'fb_scraping_project.tasks.{task}')
#         task_module.run(key_words)
#     except ImportError as e:
#         print(f"Error: {task.capitalize()} Task not found.")
#         print(e)

# if __name__ == "__main__":
#     sys.path.append('src')  # Add 'src' to sys.path
#     key_words = input("Please enter your key words in a list, for example: fintech company winter storm")
#     while True:
#         # Input validation for tasks
#         valid_task_types = ['posts', 'videos', 'posts videos', 'videos videos']

#         task_input = input("Enter task types (posts, videos, or both - separated by space) for example, posts, or posts videos: ")
#         if task_input not in valid_task_types:
#             print("Invalid input, please try again")
#             continue
#         break
#     task_input = task_input.lower().split()

#     for task in task_input:
#         run_task(task, key_words)




















# import importlib
# import os
# import sys

# # Set the current working directory to the project root
# os.chdir(sys.path[0])

# def run_task(task, key_words):
#     try:
#         task_module = importlib.import_module(f'src.fb_scraping_project.tasks.{task}')
#         task_module.run(key_words)
#     except ImportError as e:
#         print(f"Error: {task.capitalize()} Task not found.")
#         print(e)

# if __name__ == "__main__":
#     sys.path.append('src')  # Add 'src' to sys.path
#     key_words = input("Please enter your key words in a list, for example: fintech company")
#     while True:
#         # Input validation for tasks
#         valid_task_types = ['posts', 'videos', 'posts videos', 'videos videos']

#         task_input = input("Enter task types (posts, videos, or both - separated by space) for example, posts, or posts videos: ")
#         if task_input not in valid_task_types:
#             print("Invalid input, please try again")
#             continue
#         break
#     task_input = task_input.lower().split()

#     for task in task_input:
#         run_task(task, key_words)







# import importlib
# import os
# import sys

# # Set the current working directory to the project root
# os.chdir(sys.path[0])

# def run_task(task, key_words):
#     try:
#         task_module = importlib.import_module(f'fb_scraping_project.tasks.{task}')
#         task_module.run(key_words)
#     except ImportError as e:
#         print(f"Error: {task.capitalize()} Task not found.")
#         print(e)

# if __name__ == "__main__":
#     sys.path.append('src')  # Corrected the sys.path.append
#     key_words = input("Please enter your key words in a list, for example: fintech company")
#     while True:
#         # Input validation for tasks
#         valid_task_types = ['posts', 'videos', 'posts videos', 'videos videos']

#         task_input = input("Enter task types (posts, videos, or both - separated by space) for example, posts, or posts videos: ")
#         if task_input not in valid_task_types:
#             print("Invalid input, please try again")
#             continue
#         break
#     task_input = task_input.lower().split()

#     for task in task_input:
#         run_task(task, key_words)



 


