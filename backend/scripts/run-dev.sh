#!/bin/bash

export FLASK_APP=app
export FLASK_ENV=development
export FLASK_DEBUG=1

flask run --debugger -h 0.0.0.0 -p 3003
