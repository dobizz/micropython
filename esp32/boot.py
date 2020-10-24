# This file is executed on every boot (including wake-boot from deepsleep)
import webrepl
import network
import ubinascii
import machine
import ntptime
from time import sleep


def connect_wifi(ssid, password):
    '''Connect to SSID with given PASSWORD'''
    wlan = network.WLAN(network.STA_IF)
    if not wlan.active():
        wlan.active(True)

    networks = wlan.scan()

    ssid_found = False
    for net in networks:
        available_ssid = str(net[0], 'utf-8')
        if ssid == available_ssid:
            ssid_found = True
            print('SSID {} within range'.format(ssid))
            break

    if not ssid_found:
        print('Unable to connect. SSID {} not within range'.format(ssid))
        return ('0.0.0.0', '0.0.0.0', '0.0.0.0', '0.0.0.0')          

    if not wlan.isconnected():
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            sleep(1)

    # get the interface's IP/netmask/gw/DNS addresses/mac
    ipv4_addr, ipv4_mask, *ipv4_dns = wlan.ifconfig()
    mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()

    return (ipv4_addr, ipv4_mask, ipv4_dns, mac)

# device configuration
# uncomment lines below to overclock
# MAX_CPU_FREQ = 240_000_000
# machine.freq(MAX_CPU_FREQ)

# network configuration
ssid = 'INPUT WIFI SSID HERE'
password = 'INPUT WIFI PASSWORD HERE'
ipv4_addr, ipv4_mask, ipv4_dns, mac = connect_wifi(ssid, password)
print('Connected to', ssid, 'with address', ipv4_addr)

# sync clocks
rtc = machine.RTC()
ntptime.host = 'time.google.com'   # default ntp server is pool.ntp.org
if rtc.datetime()[0:3] == (2000, 1, 1):
    print('Clock not synced. Trying to sync with NTP server {}'.format(ntptime.host))
    ntptime.settime()
else:
    print('Time already synced with NTP server.')
print(rtc.datetime())

# remote configuration
webrepl.start()

