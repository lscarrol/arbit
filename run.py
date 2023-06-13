import multiprocessing
import time
from lib import pointsbet, resortsworldbet, betrivers, fanduel

# Define a list of functions to run in separate processes
# tasks = [pointsbet._parse, resortsworldbet._parse, betrivers._parse, fanduel._parse]
tasks = [fanduel._parse]
# Create a queue
queue = multiprocessing.Queue()

# Create a function to run a task
def run_task(task):
    # Each task function should handle its own error handling, 
    # logging, and any setup/teardown for the WebDriver
    return task(queue)

# Create a pool of processes
with multiprocessing.Pool() as pool:
    # Use map to apply the run_task function to each task
    result_objects = pool.map_async(run_task, tasks)

    # Print the queue contents every time it's updated
    while True:
        while not queue.empty():
            print(queue.get())
            print("///////////////////////////////////////////////////////////////\n")
        
        # Check if all tasks have finished
        if result_objects.ready():
            print("break")
            break

        # Wait before checking the queue again
        time.sleep(1)



