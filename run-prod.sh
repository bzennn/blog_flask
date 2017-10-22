#!/bin/bash

python/bin/gunicorn --bind 0.0.0.0:5000 runp:app
