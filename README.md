# PicoVision

## PicoVision repository

[Pimoroni/PicoVision](https://github.com/pimoroni/picovision#introduction)

## Install requirements

```shell
# install requirements
$ pip install -r requirements.txt
```

## Serial connection

```shell
# verify device connected
$ ls -la /dev/cu.usb*
crw-rw-rw-  1 root  wheel  0x9000005 Nov 25 10:17 /dev/cu.usbmodem14301

# start rshell connection
$ rshell -p /dev/cu.usbmodem14301
```

## Explore device

```shell
# list all files and folders on device
PicoVision> ls /pyboard/

# start REPL
PicoVision> repl

# list available modules
>>> help('modules')
```

## Upload files

```shell
# upload specific file
$ rshell -p /dev/cu.usbmodem14301 cp pong.py /pyboard/pong.py
```
