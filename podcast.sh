#!/bin/bash

export http_proxy=http://127.0.0.1:7890 && export https_proxy=http://127.0.0.1:7890 && echo 'proxy is on !'

python3 /opt/workspace/podcast/googlePodcast.py $1

