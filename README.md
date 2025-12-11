# Introduction

> [μgit](https://www.leshenko.net/p/ugit/#) is a small implementation of a Git-like version control system (VCS). It's top goal is simplicity and educational value. ugit is not exactly Git, but it shares the important ideas of Git. ugit is way shorter and doesn't implement irrelevant features.

# Usage

## Create Virtual Env (Linux/WSL)

May need admin priviliges to create a virtual environment, without this it causes issues.

`sudo python3 -m venv/env`

To run the virtual environment:

`source venv/bin/activate`

Install ugit:

`python3 setup.py developer`

> I'm aware that `setup` is deprecated. As a challenge may look into automating everything including creating virtual env for a user that clones/forks this. Keep in mind this follows a tutorial too!