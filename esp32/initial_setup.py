import os
import requests
from lxml import html

# Example
# Linux: /dev/ttyUSB0   Windows: COM1
PORT = 'COM1'
FIRMWARE = 'esp32-20180511-v1.9.4.bin'


def get_latest_firmware():
    url = 'https://micropython.org/download/esp32/'
    xpath = '/html/body/div[2]/div/div/ul[1]/li[5]/a'
    tree = html.fromstring(requests.get(url).content)
    element = tree.xpath(xpath)[0]
    return element.text


def download_firmware(FIRMWARE):
    url = f'https://micropython.org/resources/firmware/{FIRMWARE}'
    path = f'./bin/{FIRMWARE}'
    if not os.path.exists(path):
        print(f'Downloading firmware from {url}')
        open(path, 'wb').write(requests.get(url).content)
    else:
        print(f'Firmware {FIRMWARE} already in path.')

def erase_flash(PORT):
    cmd = f'esptool.py --port {PORT} erase_flash'
    os.system(cmd)


def write_firmware(PORT, FIRMWARE):
    cmd = f'esptool.py --chip esp32 --port {PORT} write_flash -z 0x1000 ./bin/{FIRMWARE}'
    os.system(cmd)


if __name__ == '__main__':
    FIRMWARE = get_latest_firmware()

    download_firmware(FIRMWARE)

    erase_flash(PORT)

    write_firmware(PORT, FIRMWARE)
