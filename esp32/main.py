import esp32
import machine
from time import sleep, sleep_ms, sleep_us

def read_temp():
    F = esp32.raw_temperature()
    C = (F - 32) * 5/9
    return C

def get_rtc_timestamp():
    rtc = machine.RTC()
    Y, m, d, w, H, M, S, f = rtc.datetime()
    return '{}-{}-{} {}:{}:{}'.format(Y,m,d,H,M,S)

def main():
    while True:
        temp = read_temp()
        timestamp = get_rtc_timestamp()
        print('[{}] {} C'.format(timestamp, temp))
        sleep_ms(100)

if __name__ == '__main__':
    main()
