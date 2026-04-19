from dataclasses import dataclass, field
# from collections import deque
from threading import Lock
from typing import Any, Dict


@dataclass
class Task:
    # task_type: str
    payload: Any
    status: str = 'open'
    meta: Dict[str, Any] = field(default_factory=dict)


class TaskQueue:
    def __init__(self):
        # self._queue = deque()
        self._queue = []
        self._lock = Lock()

    def add_task(self, payload: Any, **meta):
        task = Task(payload=payload, meta=meta)

        with self._lock:
            self._queue.append(task)

    def get_next_task(self, meta_filter=None):
        """
        Pick and remove the first task matching criteria.

        task_type: e.g. "email"
        meta_filter: function(meta) -> bool
        """

        with self._lock:
            for i, task in enumerate(self._queue):
                if task.status != 'open':
                    continue
                if meta_filter is not None and not meta_filter(task.meta):
                    continue

                # remove and return matched task
                task = self._queue.pop(i)
                task.status = 'in-progress'
                return task

        return None

    def count(self, meta_filter = None):
        results = []
        with self._lock:
            for i, task in enumerate(self._queue):
                if task.status == 'completed':
                    continue
                if meta_filter is not None and not meta_filter(task.meta):
                    continue
                results.append(task)

        return len(results)
