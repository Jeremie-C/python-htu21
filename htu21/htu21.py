#!/usr/bin/env python
# -*- coding: utf-8 -*-
import smbus
import time
import math
# HTU21D default
DEVICE  = 0x40

H14T14  = 0x00
H08T12  = 0x01
H10T13  = 0x80
H11T11  = 0x81

HOLD    = 0x00
NOHOLD  = 0x10

# Classe
class HTU21:
    def __init__(self, i2cbus=0, addr=DEVICE, mode=NOHOLD):
        if mode not in [HOLD, NOHOLD]:
            raise ValueError('Unexpected mode value {0}. Set mode to one of HTU21.HOLD, HTU21.NOHOLD'.format(mode))
        self.bus = smbus.SMBus(i2cbus)
        self.adr = addr
        self.mode = mode

    def reset(self):
        self.bus.write_byte(self.adr, 0xFE)
        time.sleep(0.15)

    def read_user_reg(self):
        self.bus.write_byte(self.adr, 0xE7)
        return self.bus.read_byte(self.adr)

    def enable_heater(self):
        reg = self.read_user_reg()
        ureg = reg & 0xFB
        new = ureg | 0x04
        self.bus.write_byte_data(self.adr, 0xE6, new)

    def disable_heater(self):
        reg = self.read_user_reg()
        ureg = reg & 0xFB
        new = ureg | 0x00
        self.bus.write_byte_data(self.adr, 0xE6, new)

    def enable_otp(self):
        reg = self.read_user_reg()
        ureg = reg & 0xFD
        new = ureg | 0x00
        self.bus.write_byte_data(self.adr, 0xE6, new)

    def disable_otp(self):
        reg = self.read_user_reg()
        ureg = reg & 0xFD
        new = ureg | 0x02
        self.bus.write_byte_data(self.adr, 0xE6, new)

    def set_resolution(self, res):
        if res not in [H14T14, H08T12, H10T13, H11T11]:
            raise ValueError('Unexpected res value {0}. Set res to one of HTU21.H08T12, HTU21.H10T13, HTU21.H11T11, HTU21.H14T14'.format(res))
        reg = self.read_user_reg()
        ureg = reg & 0x7E
        new = ureg | res
        self.bus.write_byte_data(self.adr, 0xE6, new)

    def get_batt_empty(self):
        reg = self.read_user_reg()
        bat = reg & 0x40
        return bat

    def get_temperature(self):
        raw = self._get_raw_temp()
        temp = float(raw)/65536 * 175.72
        temp -= 46.85
        return temp

    def get_temp_f(self):
        temp_c = self.get_temperature()
        temp_f = (temp_c * 1.8) + 32
        return temp_f

    def get_humidity(self):
        temp = self.get_temperature()
        rawh = self.get_humidity_nc()
        if temp < 0.0 or temp > 80.0:
            hum = rawh + (25.0 - temp) * (-0.15)
        else:
            hum = rawh
        return hum

    def get_humidity_nc(self):
        raw = self._get_raw_hum()
        hum = float(raw)/65536 * 125
        hum -= 6
        return hum

    def get_dewpoint(self):
        ppress = self._get_press_mmhg()
        hum = self.get_humidity()
        den = math.log10(hum * ppress / 100) - 8.1332
        dew = -(1762.39 / den + 235.66)
        return dew

    def get_dewpoint_f(self):
        dewp_c = self.get_dewpoint()
        dewp_f = (dewp_c * 1.8) + 32
        return dewp_f

    def _get_press_mmhg(self):
        temp = self.get_temperature()
        ppress = math.pow(10, 8.1332 - (1762.39 / (temp + 235.66)))
        return ppress

    def _get_raw_temp(self):
        self.bus.write_byte(self.adr, (0xE3 | self.mode))
        time.sleep(0.3)
        msb = self.bus.read_byte(self.adr)
        lsb = self.bus.read_byte(self.adr)
        crc = self.bus.read_byte(self.adr)
        #if self._crc_check(msb, lsb, crc) is False:
        #    raise ValueError('CRC Exception')
        raw = (msb << 8) + lsb
        raw &= 0xFFFC
        return raw

    def _get_raw_hum(self):
        self.bus.write_byte(self.adr, (0xE5 | self.mode))
        time.sleep(0.3)
        msb = self.bus.read_byte(self.adr)
        lsb = self.bus.read_byte(self.adr)
        crc = self.bus.read_byte(self.adr)
        #if self._crc_check(msb, lsb, crc) is False:
        #    raise ValueError('CRC Exception')
        raw = (msb << 8) + lsb
        raw &= 0xFFFC
        return raw

    def _crc_check(self, msb, lsb, crc):
        rem = ((msb << 8) | lsb) << 8
        rem |= crc
        div = 0x988000

        for i in range(0, 16):
            if rem & 1 << (23 - i):
                rem ^= div
            div >>= 1

        if rem == 0:
            return True
        else:
            return False

    def print_user_reg(self):
        reg = self.read_user_reg()
        res = reg & 0x81
        otp = reg & 0x02
        hot = reg & 0x04
        bat = reg & 0x40
        print("User_reg: {}, User_reg: {}, Resolution_temp: {}, Resolution_humidity: {}, otp_disable: {}, heater_enable: {}, end_of_batt_status: {}".format(hex(reg), bin(reg), hex(res), bin(res), hex(otp), hex(hot), hex(bat)))
