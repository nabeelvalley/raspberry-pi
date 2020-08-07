# Raspberry Pi

This is a repo for miscellaneous Pi things/scripts, feel free to look around. Code should be documented

# Installing Dependencies

Depending on the Distro you're using you may or may not have the relevant dependencies installed, to install the dependencies you will first need `pip` which can be installed with:

```sh
sudo apt-get update
sudo apt-get install python3-pip
```

Then install the Python libraries using Pip

```
python3 -m pip install -r requirements.txt
```

# Running Scripts

All scripts are meant to be run from the root of the directory, you can run a script like so:

```sh
python3 path/to/script.py
```