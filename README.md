# PicoVision

## PicoVision repository

If you start the first time have a look on this [website](https://learn.pimoroni.com/article/getting-started-with-picovision)! The original firmware and examples are available on [GitHub](https://github.com/pimoroni/picovision#introduction).

## Requirements

- Python 3.x installed
- latest [VCP](https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers?tab=downloads) driver installed
- 1x PicoVision (_[Pimoroni Shop](https://shop.pimoroni.com/products/picovision)_)
- 1x HDMI cable
- 1x Monitor
- 1x USB cable (_USB-A or USB-C to Micro-USB_)
- optional speaker (_3.5mm stereo jack_)

## Prepare local environment

```shell
# clone project to local from GitHub
$ git clone https://github.com/Lupin3000/PicoVision.git

# change into git directory
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

# create local backup directory
(venv) $ mkdir examples

# list all files and folders on device (optional)
(venv) $ rshell -p /dev/cu.usbmodem14301 ls /pyboard/

# copy examples from device to local backup directory
(venv) $ rshell -p /dev/cu.usbmodem14301 cp -r /pyboard/* examples/

# remove all files and directories on device
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
