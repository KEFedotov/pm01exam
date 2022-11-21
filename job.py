import os
from pyats.easypy import Task


def main():
    test_path = os.path.dirname(os.path.abspath(__file__))
    testscript = os.path.join(test_path, 'check.py')

    # create two tasks. for simplicity's sake, we'll reuse the same script
    task_1 = Task(testscript = testscript)

    # start both tasks together (async execution)
    task_1.start()

    # wait for tasks to finish before terminating
    task_1.wait()