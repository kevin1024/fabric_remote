#This is a crappy in-memory database. Maybe replace this with a real database someday.

current_execution_index = 0
executions = {}

class ExecutionStream(object):
    def __init__(self, stream):
        self._stream = stream
        self._output_buffer = ""
        self._results_buffer = []
        self._finished = False

    def output(self):
        if self._finished:
            yield self._output_buffer
            return
        for line in self._stream:
            if "output" in line:
                self._output_buffer += line["output"]
                yield line["output"]
            elif "results" in line:
                self._results_buffer.append(line["results"])
        self._finished = True

    def results(self):
        return {
            "finished": self._finished,
            "results": self._results_buffer,
        }

def add(tasks, output_stream):
    global executions
    global current_execution_index
    executions[current_execution_index] = {
        "tasks": tasks,
        "stream": ExecutionStream(output_stream),
    }
    current_execution_index += 1
    return current_execution_index -1

def get(execution_id):
    return executions[execution_id]

