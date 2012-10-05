# Furoshiki

A HTTP Rest API to Fabric.

## Requirements
Furoshiki is written in Flask and requires Fabric to be installed.

Just set the FABFILE config variable to point to your Fabfile module.  It has to be importable by the Furoshiki process, so make sure it is on your `PYTHONPATH`

### Get Task List

`GET /tasks` returns list of tasks

### Execute Task

`POST /task/deploy body -> {args: ['foo', 'bar'], kwargs: {'arg1':'val1'}}`

### Execute Multiple Tasks

`POST /tasks/deploy,restart body -> {deploy: {args: ['foo', 'bar'], kwargs: {'arg1':'val1'}}, restart: {args:['now']}}`

