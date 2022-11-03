"""
The idea is to parse the fields into a sqlite database, we need 2 inputs.

GC      GC-JLP  -F      Hilary Readhead         EVOLUTION - EVOLUTION - LETOUR  8       121w @1.80wkg   01:31:02.265

"""
import sqlite3
import argparse
import logging
from datetime import datetime
import re
from frr import monad as m


log = logging.getLogger("FrrDbParser")
log.setLevel(logging.DEBUG)
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


RIDER_FIELDS = "{}"

###############################################################################
#                                     Row                                     #
###############################################################################


class GcRow:

    row_splitter = re.compile(r'\s{2,}')
    effort_splitter = re.compile(r'\s')
    TIME_FORMAT = "%H:%M:%S.%f"
    TABLE = 0
    FRHC = 1
    GENDER = 2
    NAME = 3
    TEAM = 4
    STAGE = 5
    EFFORT = 6
    TIME = 7

    def __init__(self, row_str):
        """Parse a row"""
        #self.watt = 0
        #self.wkg = 0.0
        self.row_parser(row_str)

    def row_parser(self, row_str):
        """Parse row string.

        Keyword Arguments:
        row_str -- string according to
        GC      GC-GHT  -M      Calle Olsen     SZ - SZ LOKE    1       221w @3.40wkg   00:52:29.817
        """
        row_items = re.split(self.row_splitter, row_str)
        if len(row_items) < 8:
            log.warning("Invalid row string {}".format(row_str))
        log.debug("GcRow: {}".format(row_str))
        self.table = row_items[self.TABLE]
        self.frhc = row_items[self.FRHC]
        self.gender = row_items[self.GENDER]
        self.name = row_items[self.NAME]
        self.team = row_items[self.TEAM]
        self.stage = int(row_items[self.STAGE])
        self.effort = row_items[self.EFFORT]
        self.time = row_items[self.TIME]

    @property
    def time(self):
        """Return time.
        Keyword Arguments:
        """
        return self._time.strftime(self.TIME_FORMAT)

    @time.setter
    def time(self, time_str):
        """Set time variable."""
        log.debug("timestr: <{}>".format(time_str))
        self._time = datetime.strptime(time_str, self.TIME_FORMAT)


    @property
    def effort(self):
        log.debug("Return effort ")
        return self._effort


    @effort.setter
    def effort(self, effort_str):
        """Setting watt and wkg."""
        log.debug("set effort: {}".format(effort_str))
        watt, wkg = re.split(r"\s", effort_str)
        self.watt = int(watt.replace("w", ""))
        self.wkg = float(wkg.replace("@", "").replace("wkg", ""))
        self._effort = effort_str

    def tabulate(self):
        """Tabulate into fields."""
        return [stringify(self.table), stringify(self.frhc), stringify(self.gender),
                stringify(self.name), stringify(self.team), stringify(self.stage),
                self.watt, self.wkg, stringify(self.time)]

    @staticmethod
    def tabulate_columns():
        """Return a list of columns corresponding to tabulate fields."""
        return ["origin", "frhc", "gender", "name", "team", "stage", "watt", "wkg", "time"]




def stringify(value):
    """Convert into a string."""
    return f"\"{value}\""
###############################################################################
#                            Database functionality                           #
###############################################################################
def create_db_file(new_db_file):
    """
    Keyword Arguments:
    new_db_file -- sqlite database file
    """
    con = sqlite3.connect("frr.db")
    return con

def create_table_fn(db_conn_cursor):
    """Retrun function to create a table.
    Keyword Arguments:
    db_conn -- db connection
    """
    def create_table(*column_names,table_name,):
        column_str = ",".join(column_names)
        str = "create table {}({})".format( table_name, column_str)
        log.debug("Create Table str: \"" +str + "\"")
        try:
            db_conn_cursor.execute(str)
        except Exception:
            log.critical("could not create table")

    return create_table


def insert_into_table(*row_obj, table, db):
    """Insert iteratable to the database
    Keyword Arguments:
    *row_obj -- iterable objects to be inserted
    table    -- name of the table
    db       -- connection to database
    """
    cmd="INSERT INTO {} VALUES {} ".format(table)
    [db.execute(cmd.format(obj.db_line())) for obj in row_obj]

###############################################################################
#                                 Parsing file                                #
###############################################################################

def open_txt_file(filename):
    """
    Keyword Arguments:
    filename --
    """
    with open(filename) as f:
        return [GcRow(row.rstrip()) for row in f]



###############################################################################
#                            Pipline add row to db                            #
# The idea is to transform the raw material to object and insert the object
# into the database.
# raw -> Obj -> inser_db
###############################################################################

def raw_to_tab(raw_str):
    return GcRow(raw_str).tabulate()



def pipe_line_insert_row_db(*,rows, formatter ,db_insert_fn):
    """overview pipline """
    objs = [raw_to_tab(rider_row) for rider_row in rows]
    format_exec_str=formatter(objs)
    log.debug("insert {}".format(format_exec_str))
    db_insert_fn(format_exec_str)
