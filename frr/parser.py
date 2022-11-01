"""
The idea is to parse the fields into a sqlite database, we need 2 inputs.

GC      GC-JLP  -F      Hilary Readhead         EVOLUTION - EVOLUTION - LETOUR  8       121w @1.80wkg   01:31:02.265

"""
import sqlite3
import argparse
import logging
import time
from datetime import datetime
import re

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
#                          Parsing arguments and such                         #
###############################################################################

def parse_arguments():
    """Parse arguments."""
    parser = argparse.ArgumentParser(
        description='Create a database from frr text')
    parser.add_argument('--file', dest='frr_text_file',
                        help='Frr text file', required=True)
    parser.add_argument('--db',
                        dest='db_file',
                        help='Frr text file')
    return parser.parse_args()

def main():
    p = parse_arguments()
    db_connection = create_db_file(new_db_file=p.db_file)
    tbl_create_fn = create_table_fn(db_conn_cursor=db_connection.cursor())
    tbl_create_fn("Tbl", "FRHC", "Gender",
                  "Name", "Team", "Stage", "Watt", "Time", table_name="db")


if __name__ == '__main__':
    main()


###############################################################################
#                                    Test
###############################################################################
class TestClass:
    def test_create_GcRow(self):
        gc = GcRow(r"GC      GC-JLP  -F      Hilary Readhead         EVOLUTION - EVOLUTION - LETOUR  8       121w @1.80wkg   01:31:02.265")
        assert gc is not None
        assert gc.effort == "121w @1.80wkg"
        assert gc.time ==  "01:31:02.265000"
        assert gc.watt == 121
        assert gc.wkg == 1.80

        gc = GcRow(r"GC      GC-CRP  -M      Eric Brandhorst         TEAMCLS - Équipe Orange         1       276w @4.00wkg   00:48:08.726")
        assert gc is not None
        assert gc.table == "GC"
        assert gc.frhc == "GC-CRP"
        assert gc.gender == "-M"
        assert gc.name ==  "Eric Brandhorst"
        assert gc.team ==  "TEAMCLS - Équipe Orange"
        assert gc.stage == 1
        assert gc.effort == "276w @4.00wkg"
        assert gc.watt == 276
        assert gc.wkg == 4.00
        assert gc.time ==  "00:48:08.726000"

    def test_read_file(self):
        """

        """
        gcs = open_txt_file("/home/calle/git/frr_gc/season_1.txt")
        assert len(gcs) > 100
        print(gcs[190].name)
