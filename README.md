# PicoVision

## PicoVision repository

[Pimoroni/PicoVision](https://github.com/pimoroni/picovision#introduction)

## Prepare local environment

```shell
# clone project from GitHub
$ git clone https://github.com/Lupin3000/PicoVision.git

# change directory
$ cd PicoVision

# create virtual environment
$ python3 -m venv ./venv

# activate virtualenv
$ source venv/bin/activate

# install requirements
(venv) $ pip install -r requirements.txt
```

## Prepare PicoVision

> Backup all Pimoroni examples to local project directory `examples` and delete them on PicoVision device.

```shell
# verify device connected
(venv) $ ls -la /dev/cu.usb*
crw-rw-rw-  1 root  wheel  0x9000005 Nov 25 10:17 /dev/cu.usbmodem14301

# create backup directory
(venv) $ mkdir examples

# list all files and folders on device
(venv) $ rshell -p /dev/cu.usbmodem14301 ls /pyboard/

# copy examples from device to local directory
(venv) $ rshell -p /dev/cu.usbmodem14301 cp -r /pyboard/* examples/

# remove all files and directories
(venv) $ rshell -p /dev/cu.usbmodem14301 rm -r /pyboard/*

# copy main.py back to device
(venv) $ rshell -p /dev/cu.usbmodem14301 cp examples/main.py /pyboard/
```

## Upload games

> Upload all local files to PicoVision device. After successful upload you can press the PicoVision `RESET` button.

```shell
# upload specific file
(venv) $ rshell -p /dev/cu.usbmodem14301 cp *.py /pyboard/
```
