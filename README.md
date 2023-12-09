# PicoVision

## PicoVision repository

[Pimoroni/PicoVision](https://github.com/pimoroni/picovision#introduction)

## Install requirements

```shell
# install requirements
$ pip install -r requirements.txt
```

## Prepare PicoVision

> Backup all Pimoroni examples to local project directory and delete them on device.

```shell
# verify device connected
$ ls -la /dev/cu.usb*
crw-rw-rw-  1 root  wheel  0x9000005 Nov 25 10:17 /dev/cu.usbmodem14301

# create backup directory
$ mkdir examples

# list all files and folders on device
$ rshell -p /dev/cu.usbmodem14301 ls /pyboard/

# copy examples from device to local directory
$ rshell -p /dev/cu.usbmodem14301 cp -r /pyboard/* examples/

# remove all files and directories
$ rshell -p /dev/cu.usbmodem14301 rm -r /pyboard/*

# copy main.py back to device
$ rshell -p /dev/cu.usbmodem14301 cp examples/main.py /pyboard/
```

## Upload games

> Upload all local files to device. After successful upload you can press the PicoVision `RESET` button.

```shell
# upload specific file
$ rshell -p /dev/cu.usbmodem14301 cp *.py /pyboard/
```


