#!/usr/bin/env python
"""
Each row becomes a Rider , maybe the naming is wrong.
"""
import re
import time


TIME_FORMAT="%H:%M:%S"

class Rider:

    def __init__(self, args):
        "docstring"
        self.table = args[Gc_row.TABLE]
        self.frhc = args[Gc_row.FRHC]
        self.gender = args[Gc_row.GENDER]
        self.name = args[Gc_row.NAME]
        self.team = args[Gc_row.TEAM]
        self.stage = args[Gc_row.STAGE]
        self.effort = args[Gc_row.EFFORT]
        self.time = time.strptime(args[Gc_row.TIME],"%H:%M:%S.%f")
        self.parse_effort(self.effort)


    def parse_effort(self, effort_str):
        """Parse the effort into watts and w/kg."""
        watt,wkg = re.split("\s",effort_str)
        self.watt = int(watt.replace("w",""))
        self.wkg = float(wkg.replace("@","").replace("wkg",""))



    def __str__(self):
        return "{} {} {} {} {} {} {} {}".format(self.table, self.frhc,
                                                self.gender, self.name,
                                                self.team, self.stage,
                                                self.effort,
                                                time.strftime(TIME_FORMAT, self.time))

    def tabulate(self):
        """
        Tabulated Rider
        """
        table = [self.table, self.frhc, self.gender, self.name, self.team,
                 self.stage, self.effort, time.strftime(TIME_FORMAT, self.time),
                 self.watt, self.wkg]
        return table






class Gc_row:
    """General classification"""
    TABLE = 0
    FRHC = 1
    GENDER = 2
    NAME = 3
    TEAM = 4
    STAGE = 5
    EFFORT = 6
    TIME = 7
    #Extra fields, Parsed from effort
    WATT = 8
    WKG = 9

    Column_names = {
        TABLE: "TABLE",
        FRHC: "FRHC",
        GENDER: "GENDER",
        NAME: "NAME",
        TEAM: "TEAM",
        STAGE: "STAGE",
        EFFORT: "EFFORT",
        TIME: "TIME",
        WATT: "WATT",
        WKG: "WKG"

    }

    @staticmethod
    def parse_row_riders(table_row):
        """Parse Riders."""
        dic = {Gc_row.TABLE: table_row[Gc_row.TABLE],
               Gc_row.FRHC:   table_row[Gc_row.FRHC],
               Gc_row.GENDER: table_row[Gc_row.GENDER],
               Gc_row.NAME:   table_row[Gc_row.NAME],
               Gc_row.TEAM:   table_row[Gc_row.TEAM],
               Gc_row.STAGE:  table_row[Gc_row.STAGE],
               Gc_row.EFFORT: table_row[Gc_row.EFFORT],
               Gc_row.TIME: table_row[Gc_row.TIME],
               }
        return Rider(dic)




    @staticmethod
    def row_parser(table_row):
        return Gc_row.parse_row_riders(table_row)


    @staticmethod
    def get_index_by_name(index):
        return Gc_row.Column_names[index]

    @staticmethod
    def get_tabulate():
        """Get the tabulate header."""
        return [name for (key, name) in Gc_row.Column_names.items()]



class TableType:
    GC = 0

    @staticmethod
    def get_parser(row_type):
        "Return a parser function for a specific Row."
        if row_type == TableType.GC:
            return Gc_row.row_parser


def table_parser(row, row_type):
    """Parse a row."""
    #ipdb.set_trace()
    parser = TableType.get_parser(row_type)
    return parser(row)



def parse_table(table,filter_func=None):
    """Parse a complete table.
    This returns a list of Riders.
    If we want to filter on that we apply the filter directly
    """
    # TODO: I can get the type from the first column. For now we use GC
    if filter is None:
        return [table_parser(row,TableType.GC) for row in table]
    else:
        return filter(filter_func,[table_parser(row,TableType.GC) for row in table])



def main():
    import printer
    tbl=[
        ["GC", "GC-GHT", "-M", "Ian Coveny", "CRCAF - FoundationNation", 1, "410w @4.10wkg", "00:45:04.294"],
        ["GC", "GC-GHT", "-M", "Patrick Caisse", "LWATT - MWoFosCC", 1, "314w @4.10wkg", "00:45:14.044"],
        ["GC", "GC-GHT", "-M", "Jason Bridges", "RELENTLESS - RELENTLESS - LETOUR", 1, "336w @4.10wkg", "00:45:15.217"]
    ]

    Riders = [table_parser(row, TableType.GC) for row in tbl]
    formatter = printer.get_printer(printer.PrinterType.TABLE)
    print(formatter(Riders, Gc_row.get_tabulate()))

    # for rider in Riders:
    #     print(formatter(rider))


if __name__ == '__main__':
    main()
