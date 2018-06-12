#!/usr/bin/env python
# -*- coding: utf-8 -*-

import htu21
import time

if __name__ == '__main__':
    htu = htu21.HTU21()
    tc = htu.get_temperature()
    tf = htu.get_temp_f()
    h  = htu.get_humidity()
    hc = htu.get_humidity_nc()
    dc = htu.get_dewpoint()
    df = htu.get_dewpoint_f()

    print "Temperature: %f C" % tc
    print "Temperature: %f F" % tf
    print "Humidity: %f %%" % h
    print "Raw Humidity: %f %%" % hc
    print "Dewpoint: %f C" % dc
    print "Dewpoint: %f F" % df
