# PicoVision

## Requirements

> If you start the first time have a look on this [website](https://learn.pimoroni.com/article/getting-started-with-picovision)! The original firmware and examples are available on [GitHub](https://github.com/pimoroni/picovision#introduction).

- Python 3.x installed
- latest [VCP](https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers?tab=downloads) driver installed
- 1x PicoVision (_[Pimoroni Shop](https://shop.pimoroni.com/products/picovision)_)
- 1x HDMI cable
- 1x Monitor
- 1x USB cable (_USB-A or USB-C to Micro-USB_)
- optional speaker (_3.5mm stereo jack_)

## Prepare local project and MicroPython environment

Download project from GitHub to your local device, create a Python virtual environment and install all needed Python libraries on your local device.

> The described usage of Python virtual environment is recommended but not mandatory!

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

## Prepare the PicoVision device

Backup all Pimoroni examples to local project directory `examples` and delete them on PicoVision device to save some storage.

> The serial device interface example `usbmodem14301` could be named different on you system (_depending to USB port_)!

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

# copy toaster.png back to device
(venv) $ rshell -p /dev/cu.usbmodem14301 cp examples/toaster.png /pyboard/
```

## Upload games to PicoVision

Upload local files and folders to PicoVision device. After successful upload you can press the PicoVision `RESET` button.

> After the upload and first tests, you can delete the games you don't like.

```shell
# upload specific file
(venv) $ rshell -p /dev/cu.usbmodem14301 cp *.py /pyboard/
```
