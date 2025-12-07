"""
Task Manager for coordinating the textbook generation pipeline tasks.
"""
import json
import os
from pathlib import Path
from datetime import datetime

class TaskManager:
    def __init__(self):
        self.tasks = {}
        self.task_log = []

    def register_task(self, task_id, task_func, dependencies=None):
        """Register a task with its function and dependencies"""
        self.tasks[task_id] = {
            'function': task_func,
            'dependencies': dependencies or [],
            'status': 'pending',
            'start_time': None,
            'end_time': None,
            'result': None
        }

    def execute_task(self, task_id):
        """Execute a single task and update its status"""
        if task_id not in self.tasks:
            raise ValueError(f"Task {task_id} not registered")

        task = self.tasks[task_id]

        # Check dependencies
        for dep_id in task['dependencies']:
            if self.tasks[dep_id]['status'] != 'completed':
                raise RuntimeError(f"Dependency {dep_id} not completed for task {task_id}")

        # Execute task
        task['status'] = 'processing'
        task['start_time'] = datetime.now()

        try:
            result = task['function']()
            task['result'] = result
            task['status'] = 'completed'
            task['end_time'] = datetime.now()

            # Log task execution
            self.task_log.append({
                'task_id': task_id,
                'status': 'completed',
                'start_time': task['start_time'].isoformat(),
                'end_time': task['end_time'].isoformat(),
                'duration': (task['end_time'] - task['start_time']).total_seconds()
            })

            return result
        except Exception as e:
            task['status'] = 'failed'
            task['end_time'] = datetime.now()
            task['error'] = str(e)

            # Log task failure
            self.task_log.append({
                'task_id': task_id,
                'status': 'failed',
                'start_time': task['start_time'].isoformat(),
                'end_time': task['end_time'].isoformat(),
                'error': str(e)
            })

            raise e

    def execute_task_batch(self, task_ids):
        """Execute multiple tasks in parallel"""
        from concurrent.futures import ThreadPoolExecutor, as_completed

        results = {}
        failed_tasks = []

        with ThreadPoolExecutor(max_workers=4) as executor:
            # Submit tasks
            future_to_task_id = {
                executor.submit(self.execute_task, task_id): task_id
                for task_id in task_ids
            }

            # Collect results
            for future in as_completed(future_to_task_id):
                task_id = future_to_task_id[future]
                try:
                    result = future.result()
                    results[task_id] = result
                except Exception as e:
                    failed_tasks.append((task_id, str(e)))

        return results, failed_tasks

    def get_task_status(self, task_id):
        """Get the status of a specific task"""
        if task_id not in self.tasks:
            return None
        return self.tasks[task_id]['status']

    def get_all_statuses(self):
        """Get statuses of all tasks"""
        return {task_id: task['status'] for task_id, task in self.tasks.items()}

    def save_task_log(self, path="backend/processing/task_log.json"):
        """Save the task execution log to a file"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            json.dump(self.task_log, f, indent=2)