# Alarm System - Server

## Requirements

In order to work, the application needs
[64-bit Raspberry Pi OS Lite](https://downloads.raspberrypi.org/raspios_lite_arm64/images/) system able to run
Python 3.5 (and newer). This is, because one of dependencies used by FastAPI does not work on 32-bit systems
(which is default for Raspberries).

## Installation
Firstly, you need to change directory to project root
```
cd something/AlarmSystem-Server
```

Then install dependencies (consider using [Python venv](https://docs.python.org/3/tutorial/venv.html))
```
python3 -m pip install -r requirements.txt
```

After that, you should be able to run server with no problems.
```
python3 main.py
```



## Other information
By default, app uses [0.0.0.0 with 5000 port](http://0.0.0.0:5000/) for API distribution
and 0.0.0.0 with 8888 port for 'settings' broadcast.