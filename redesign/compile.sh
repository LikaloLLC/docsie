#!/usr/bin/env bash
staticjinja build --srcpath=./src
python generate_site_map.py https://pc-ask.com
firebase deploy
