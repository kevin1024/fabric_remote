# Fabric Remote

![vcr.py](https://raw.github.com/kevin1024/fabric_remote/master/logo.png)

A HTTP Rest API to Fabric.

## Project Goals
Fabric Remote is intended to be a simple thin layer around your Fabric tasks.  I'm using it to automate deployments but you can use it to add an API to any sort of remote executions.  I have tried to make Fabric Remote as thin and simple as possible, with almost no configuration.  It directly exposes your Fabric tasks over HTTP.

## Authentication

Right now there's only one option for authentication:  HTTP Basic Auth.  Set the password in an environment variable when you start Fabric Remote, and send it when making requests.

## Quickstart

```bash
$ pip install fabric_remote
```

```bash
$ fabric-remote-server --fabfile-path PATH/TO/YOUR/FABFILE.py 
  * Running on http://0.0.0.0:1234/
```

now you can make HTTP requests that will run your Fabric tasks!

```bash
$ curl http://localhost:1234/executions -X POST --user admin:secret -H Content-Type:application/json -d "[{\"task\": \"host_type\", \"args\": [], \"kwargs\": {}}]"
{
  "output": "/executions/zDUxHCMX5SBR4C4Xu9PDdB/output",
  "results": "/executions/zDUxHCMX5SBR4C4Xu9PDdB/results"
}
```

## Configuration Options

| env variable     | cmdline option  | default          | description                               |
| ---------------  | --------------  | ---------------- | ----------------------------------------- |
| PASSWORD         | --password=     | secret           | HTTP Basic Auth password                  |
| PORT             | --port=         | 1234             | HTTP port to serve                        |
| BIND             | --bind=         | 0.0.0.0          | IP address to bind server                 |
| CORS_HOSTS       | --cors-hosts=   |                  | Hosts to allow CORS requests              |
| FABFILE_PATH     | --fabfile-path= | fabfile          | Path to fabfile (same as Fabric option)   | 
| DEBUG            | --debug         | False            | Activate debug mode (logs to stdout)      | 

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

## CORS Headers

If you want to use [the javascript client](https://github.com/kevin1024/fabric-remote-js) from a browser, and it's operating on a different domain than your current domain, you will need to enable CORS headers.  You can do this either by passing the --cors-hosts command line flag or by setting the CORS_HOSTS env variable.  Make sure you understand the security implications of doing this.

## Installation
1. `pip install fabric-remote`

## Clients

There are some clients I have written to use Fabric Remote, in various stages of development.

 * [Python Command-line client](https://github.com/kevin1024/fabric_remote/blob/master/clients/cmdline.py)
 * [JavaScript Client](https://github.com/kevin1024/fabric-remote-js)
 * [Web Client](https://github.com/kevin1024/fabric_remote_web)

## Notes
 * Fabric Remote is only compatible with "new-style" Fabfiles (introduced in Fabric 1.1).  It doesn't know how to deal with "old-style" tasks that don't use the @task decorator or aren't subclasses of the Task object.
 * All responses have CORS headers to allow cross-domain requests from any host.  This could cause crossdomain attacks if you were logged into the fabric remote service in your browser.  That could be bad I guess, I should probably make this configurable.
 * Python 3.x is not supported, since Fabric itself does not support Python 3.

## License

The MIT License (MIT)

Copyright (c) 2014 Kevin McCarthy

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
