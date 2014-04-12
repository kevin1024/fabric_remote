# Fabric Remote

A HTTP Rest API to Fabric.

## Development Status

This project is still under heavy development and is not production-ready.

## Requirements
Fabric Remote is written in Flask and requires Fabric to be installed.

## Quickstart

```
pip install fabric_remote
```

```
$ fabric-remote-server --fabfile-path PATH/TO/YOUR/FABFILE.py 
  * Running on http://0.0.0.0:1234/
```

now you can make HTTP requests that will run your Fabric tasks!

### Get Task List

`GET /tasks` returns list of tasks

```json
{
    "host_type": {
        "name": "host_type",
        "description": null
    },
    "check_foo": {
        "name": "check_foo",
        "description": null
    }
}
```

### Execute Task

Send a POST request to the server with the task and args you will execute in the body.  Make sure you set the Content-Type header to application/json.  

`POST /executions body -> [{task: "deploy", args: ["foo", "bar"], kwargs: {"arg1":"val1"}}]`

If this works, it will return 202 Accepted with a json response body containing two other endpoints: results and output.  

```json
{
    "output":"/executions/1234-1234-12345/output",
    "results":"/executions/1234-1234-12345/results",
}
```

The output endpoint will stream the output of the fabric task as it runs.  After the task completes, it will contain the full output of the task.

The results task will return a json response:

```json
{
    "error": "",
    "finished": true,
    "results": [ ]
}
```

`error` contains the error message if there was an error executing your task, `finished` returns the current state of the task, and `results` is a list of all the return values of the tasks you ran.

## Installation
1. `pip install fabric-remote`

## Notes
 * Fabric Remote is only compatible with "new-style" Fabfiles (introduced in Fabric 1.1).  It doesn't know how to deal with "old-style" tasks that don't use the @task decorator or aren't subclasses of the Task object.
 * All responses have CORS headers to allow cross-domain requests from any host.  This could cause crossdomain attacks if you were logged into the fabric remote service in your browser.  That could be bad I guess, I should probably make this configurable.
