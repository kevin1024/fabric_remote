#This is a crappy in-memory database. Maybe replace this with a real database someday.

current_execution_index = 0
executions = {}

class ExecutionStream(object):
    def __init__(self, stream):
        self._stream = stream
        self._buffer = ""
        self._finished = False

    def read(self):
        if self._finished:
            yield self._buffer
            return
        for line in self._stream:
            self._buffer += line
            yield line
        self._finished = True

def add(tasks, output_stream):
    global executions
    global current_execution_index
    executions[current_execution_index] = {
        "tasks": tasks,
        "output_stream": ExecutionStream(output_stream),
    }
    current_execution_index += 1
    return current_execution_index -1

def get(execution_id):
    return executions[execution_id]

