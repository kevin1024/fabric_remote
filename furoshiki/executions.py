import uuid

MAX_EXECUTIONS = 50

# This is a crappy in-memory database. Maybe replace this with a real database someday.
# Also, expire old ones (memory leak) - backported python3.3 lru?
# how about pluggable DB backends?  yes.. yes yes.
executions = {}

class ExecutionStream(object):
    def __init__(self, ps_handle, stream):
        self._ps_handle = ps_handle
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
        if self._ps_handle.is_alive():
            return {"finished": False}
        #Consume generator so we can get the results
        [x for x in self.output()]
        return {
            "finished": True,
            "results": self._results_buffer,
        }

def add(tasks, ps_handle, output_stream):
    global executions
    execution_id = uuid.uuid1()
    executions[execution_id] = {
        "tasks": tasks,
        "stream": ExecutionStream(ps_handle, output_stream),
    }
    return execution_id

def get(execution_id):
    return executions[uuid.UUID(execution_id)]
