#!/usr/bin/env python3

try:
    from app import cli
    from config import token
    cli.run(token)
except:
    print("Failed to run the app. Try ton install discord module.\n You should add your token in config file.")
