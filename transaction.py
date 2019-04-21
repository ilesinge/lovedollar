#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=no-member

import decimal
import colorful

class Transaction(object):

    def __init__(self, base, quote, side, price, size, platform):
        self.base = base
        self.quote = quote
        self.side = side
        self.price = float(price)
        self.formatprice = format(decimal.Decimal(self.price), ".8f")
        self.size = float(size)
        self.platform = platform
        self.change = 0
        self.bigchange = 0
        self.formatchange = ''
    
    def set_change(self, change):
        self.change = float(change)
        self.bigchange = int(self.change * 1000)
        self.formatchange = format(decimal.Decimal(self.price), ".8f")

    def display(self):
        if self.side == "SELL":
            colorside = colorful.bold_red(self.side)
        else:
            colorside = colorful.bold_green(self.side)

        if self.change > 0:
            graphic_change = "➚"
        elif self.change < 0:
            graphic_change = "➘"
        else:
            graphic_change = "➙"
        print(graphic_change + " " + colorside + " " + str(self.size) + " " + colorful.bold_black_on_yellow(self.base) + " for " + self.formatprice + " " + colorful.bold_black_on_yellow(self.quote) + " each")  