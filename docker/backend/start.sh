#!/bin/bash

proxy_headers="--proxy-headers"
host="0.0.0.0"


uvicorn main:app $proxy_headers --host $host --port 8000
