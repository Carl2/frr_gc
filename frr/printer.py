#!/usr/bin/env python
from tabulate import tabulate


class PrinterType:
    TABLE = 0


def get_printer(printer_type):
    """Return a printer type function."""
    if printer_type == PrinterType.TABLE:
        def fun(riders, header=None):
            tab = [rider.tabulate() for rider in riders]
            return tabulate(tab, headers=header,tablefmt='orgtbl')
        return fun
