class ExecutionStream(object):
    def __init__(self, ps_handle, stream):
        self._ps_handle = ps_handle
        self._stream = stream
        self._output_buffer = ""
        self._error_buffer = ""
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
            elif "error" in line:
                self._error_buffer += line["error"]
        self._finished = True

    def results(self):
        if self._ps_handle.is_alive():
            return {"finished": False}
        #Consume generator so we can get the results
        [x for x in self.output()]
        return {
            "finished": True,
            "results": self._results_buffer,
            "error": self._error_buffer,
        }
