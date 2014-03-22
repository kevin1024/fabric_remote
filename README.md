# Fabric Remote

A HTTP Rest API to Fabric.

## Requirements
Fabric Remote is written in Flask and requires Fabric to be installed.

Just set the FABFILE config variable to point to your Fabfile module.  

### Get Task List

`GET /tasks` returns list of tasks

### Execute Task

`POST /task/deploy body -> {args: ['foo', 'bar'], kwargs: {'arg1':'val1'}}`

### Execute Multiple Tasks

`POST /tasks/deploy,restart body -> {deploy: {args: ['foo', 'bar'], kwargs: {'arg1':'val1'}}, restart: {args:['now']}}`

## Installation
1. `pip install fabric-remote`

## Configuration
1. Set the `FABFILE` configuration variable to point to your Fabfile module. It has to be importable by the Fabric Remote process, so make sure it is on your `PYTHONPATH`
2. Fabric Remote is only compatible with "new-style" Fabfiles (introduced in Fabric 1.1).  It doesn't know how to deal with "old-style" tasks that don't use the @task decorator or aren't subclasses of the Task object.
